import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import sounddevice as sd

def gerar_portadora(fc, fs_simulacao, n_amostras):
    n = np.arange(n_amostras)
    portadora = np.cos(2 * np.pi * fc * (n/fs_simulacao)) # Gera portadora cossenoidal.

    return portadora

def modulacao(portadora, mensagem):

    A = 33000  # Amplitude da portadora (DC Offset) com valor inteiro (porque a mensagem está em int32).
    mu = 0.8
    m_t = (A + mu * mensagem) * portadora # Mixing da mensagem com a portadora, gerando o sinal modulado.
    
    return m_t

def demodulacao(m_t, K):

    s_t = retificacao(m_t)
    s_t = lowpass_filter(s_t, K)
    s_t = removedor_DC(s_t)

    return s_t

def retificacao(r_t):
    return np.abs(r_t) # Retificação de onda completa, obtendo o valor absoluto do sinal modulado. É como se fosse uma ponte retificadora, ao invés de apenas um diodo. 

# def low-pass-filter(m_t_hat):
#
#     windows_size = 50 # O tamanho da janela define a "inércia" (como o RC do capacitor) do filtro de média móvel. Quanto maior a janela, mais suave será o sinal filtrado, mas também pode introduzir mais atraso e atenuação. O valor de 50 é um ponto de partida razoável para sinais de áudio, mas pode ser ajustado conforme necessário para obter um equilíbrio entre suavização e resposta rápida.
#     kernel = np.ones(windows_size) / windows_size # Cria um kernel de média móvel, onde cada elemento é 1/windows_size. Isso significa que cada ponto do sinal filtrado será a média dos últimos "windows_size" pontos do sinal retificado.
#     s_t = np.convolve(m_t_hat, kernel, mode="same") # Filtragem do sinal retificado usando uma média móvel (filtro FIR simples) para recuperar a mensagem original.
#     return s_t
#

def lowpass_filter(x, K):
    # O filtro é implementado pela equação das diferenças calculado.
    # Usamos os termos b0, b1 e a1, que dependem dos valores de capacitância e resistência.
    # Consideramos que o estado inicial é de repouso, logo x[-1] e y[-1] são zero.
    
    b0 = 1/(1+K)
    b1 = 1/(1+K)
    a1 = (1-K)/(1+K)

    y=np.zeros(shape=x.shape)
    y[0] = b0*x[0]
    for n in range(1, len(x)):
        y[n] = b0*x[n] + b1*x[n-1] - a1*y[n-1]

    return y


def  removedor_DC(s_t):
    s_final = s_t - np.mean(s_t) # Remoção do componente DC do sinal filtrado, centralizando o sinal em torno de zero.
    s_final = s_final * (np.pi / 2)  # Compensação teórica da retificação onda completa.
    return s_final  

def gerar_graficos(portadora, mensagem, m_t, s_t):
    # --- Plotagem ---
    fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)
    plt.subplots_adjust(hspace=0.4)
    n = np.arange(len(mensagem))
# Gráfico 1: Audio original

    axs[0].plot(n, mensagem, color="blue")
    axs[0].set_title("1. Audio Original")
    axs[0].grid(True)

# Gráfico 2: Portadora

    axs[1].plot(n, portadora, color="orange")
    axs[1].set_title("2. Portadora")
    axs[1].grid(True)

# Gráfico 3: Sinal Modulado

    axs[2].plot(n, m_t, color="orange")
    axs[2].set_title("3. Sinal modulado")
    axs[2].grid(True)

# Gráfico 3: 
    axs[3].plot(n, s_t, color="green")
    axs[3].set_title("4. Sinal demodulado")
    axs[3].grid(True)

    # plt.xlabel("Tempo (s)")
    plt.show()
    # implementar função do gráfico

    return

def resample_audio(data, freq_original, nova_freq):
    n_amostras = int(len(data)*(nova_freq/freq_original))        # recalculando o número de amostras para fazer o resample
    data_resampled = signal.resample(data, n_amostras)
    return data_resampled, n_amostras


def extrair_mensagem(arquivo, fs_simulacao):
    fs, audio = wavfile.read(arquivo)   # abre o arquivo e o salva em formato uint16 

    # para simplificar, vamos usar o audio MONO
    if audio.ndim > 1:      #se for stereo, converte para mono calculando a média entre os canais
        audio = audio.mean(axis=1).astype(audio.dtype)

    # é necessário que a mensagem e a portadora estejam na mesma frequência de amostragem
    # entretanto, os 44.1 kHz são inssuficientes para uma portadora com alta frequência
    # Assim, usamos o resample para que a mensagem tenha amostras suficientes para a portadora que iremos usar.
    mensagem, n_amostras = resample_audio(audio, fs, fs_simulacao)
    return n_amostras, fs, mensagem


def salvar_audio(audio, fs_simulacao, fs):
    # primeiro, precisamos fazer um downsample para o audio tocar em 44.1kHz
    audio_downsampled, _ = resample_audio(audio, fs_simulacao, fs)
    audio_processado = np.clip(audio_downsampled, -32768, 32767)

    # 2. Converte explicitamente o tipo da matriz para int16
    audio = audio_processado.astype(np.int16)
    wavfile.write('audio_recebido.wav', fs, audio)
    return



if __name__ == '__main__':
    fc = 150000     # 150 kHz
    fs_simulacao = 1000000  # 1 MHz
    # queremos uma frequência de simulação alta o suficiente para "ver" a portadora.
    arquivo =  'audio.wav'
    n_amostras, fs, mensagem = extrair_mensagem(arquivo, fs_simulacao)
    portadora = gerar_portadora(fc, fs_simulacao, n_amostras)

    T = 1/fs_simulacao
    C = 4.7e-9      # 4.7nF
    R = 2.26e3      # 2.26 kOhms
    K = R*C/T

    # Esses valores de capacitância, resistência resultam em um filtro
    # com frequência de corte de aproximadamente 15 kHz
    
    m_t = modulacao(portadora, mensagem)

    s_t = demodulacao(m_t, K)
    
    salvar_audio(s_t, fs_simulacao, fs) 

    gerar_graficos(portadora, mensagem, m_t, s_t)

    
