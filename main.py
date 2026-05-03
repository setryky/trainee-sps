import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
# from filtro.py import filtro_fase_linear


def extrair_mensagem(arquivo, fs_simulacao):
    fs, audio = wavfile.read(arquivo)  # abre o arquivo e o salva em formato uint16
    # para simplificar, vamos usar o audio MONO
    if (
        audio.ndim > 1
    ):  # se for stereo, converte para mono calculando a média entre os canais
        audio = audio.mean(axis=1).astype(audio.dtype)
    # é necessário que a mensagem e a portadora estejam na mesma frequência de amostragem
    # entretanto, os 44.1 kHz são inssuficientes para uma portadora com alta frequência
    # Assim, usamos o resample para que a mensagem tenha amostras suficientes para a portadora que iremos usar.
    mensagem, n_amostras = resample_audio(audio, fs, fs_simulacao)
    return n_amostras, fs, mensagem


def resample_audio(data, freq_original, nova_freq):
    n_amostras = int(
        len(data) * (nova_freq / freq_original)
    )  # recalculando o número de amostras para fazer o resample
    data_resampled = signal.resample(data, n_amostras)
    return data_resampled, n_amostras


def gerar_portadora(fc, fs_simulacao, n_amostras):
    n = np.arange(n_amostras)
    portadora = 1 * np.cos(
        2 * np.pi * fc * (n / fs_simulacao)
    )  # Gera portadora cossenoidal.

    return portadora


def modulacao(portadora, mensagem):
    # A mensagem varia de -32768 a 32767, então precisamos de uma portadora na mesma escala.
    A = 33000  # Amplitude da portadora (DC Offset) com valor inteiro (porque a mensagem está em int16).
    mu = 0.8  # usando um coeficiente de submodulação (mu < 1)
    # mu = 1.0  # usando um coeficiente de submodulação (mu < 1)
    m_t = (
        A + mu * mensagem
    ) * portadora  # Mixing da mensagem com a portadora, gerando o sinal modulado.
    return m_t


def demodulacao(m_t, fs, f_corte=15000):
    s_t = retificacao(m_t)
    s_t = filtro_fase_linear(s_t, fs, f_corte, 301)
    s_t = removedor_DC(s_t)

    return s_t


def retificacao(r_t):
    # Retificação de onda completa, obtendo o valor absoluto do sinal modulado. É como se fosse uma ponte retificadora, ao invés de apenas um diodo.
    return np.abs(r_t)


def filtro_fase_linear(signal, fs, fc, numtaps=101):
    M = (numtaps - 1) / 2
    n = np.arange(numtaps) - M

    f_n = fc / fs
    h_sinc = 2 * f_n * np.sinc(2 * f_n * n)

    window = np.hamming(numtaps)

    h_final = h_sinc * window
    h_final /= np.sum(h_final)  # Garante que o ganho em 0Hz seja 1 (0dB)

    y = np.convolve(signal, h_final, mode="same")

    return y


def removedor_DC(s_t):
    s_final = (
        s_t - np.mean(s_t)
    )  # Remoção do componente DC do sinal filtrado, centralizando o sinal em torno de zero.
    s_final = s_final * (np.pi / 2)  # Compensação teórica da retificação onda completa.
    return s_final


def calcular_espectro(sinal, fs):
    n = len(sinal)
    sinal_fft = np.fft.fftshift(np.fft.fft(sinal))
    # sinal_fft = np.abs(sinal_fft)
    # sinal_fft = sinal_fft / np.max(sinal_fft)
    mag_linear = (np.abs(sinal_fft) / n) * 2

    # Gera o vetor de frequências de -fs/2 até fs/2
    f = np.fft.fftshift(np.fft.fftfreq(n, d=1 / fs))

    mag_db = 20 * np.log10(mag_linear + 1e-5)
    return f, mag_db


def gerar_graficos(mensagem, m_t, s_t, fs):
    # --- Plotando os gráficos do sinal no tempo ---
    fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)
    plt.subplots_adjust(hspace=0.4)

    n = np.arange(len(mensagem))

    # 1. Audio Original
    axs[0].plot(n, mensagem, color="blue")
    axs[0].set_title("Audio Original")
    axs[0].set_ylim(-40000, 40000)
    axs[0].grid(True)

    # 2. Sinal modulado
    axs[1].plot(n, m_t, color="orange")
    axs[1].set_title("Sinal modulado")
    axs[1].grid(True)

    # 3. Sinal demodulado
    axs[2].plot(n, s_t, color="green")
    axs[2].set_title("Sinal demodulado")
    axs[2].set_ylim(-40000, 40000)
    axs[2].grid(True)

    # 4. Diferença entre o sinal original, e o demodulado
    axs[3].plot(n, mensagem - s_t, color="orange")
    axs[3].set_title("Diferença entre o sinal original, e o demodulado")
    axs[3].set_ylim(-40000, 40000)
    axs[3].grid(True)

    plt.xlabel("Tempo (s)")
    plt.show()

    # --- Plotando os espectros dos sinais ---

    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    plt.subplots_adjust(hspace=0.4)

    # 1. Espectro do Audio Original
    f, mensagem_dfft = calcular_espectro(mensagem, fs)
    axs[0].plot(f, mensagem_dfft, color="blue")
    axs[0].set_title("Espectro do Audio Original")
    axs[0].set_xlim(-200000, 200000)
    axs[0].grid(True)

    # 2. Espectro do Sinal modulado
    f, m_t_dfft = calcular_espectro(m_t, fs)
    axs[1].plot(f, m_t_dfft, color="orange")
    axs[1].set_title("Espectro do Sinal modulado")
    axs[1].set_xlim(-200000, 200000)
    axs[1].grid(True)

    # 3. Espectro do Sinal demodulado
    f, s_t_dfft = calcular_espectro(s_t, fs)
    axs[2].plot(f, s_t_dfft, color="green")
    axs[2].set_title("Espectro do Sinal demodulado")
    axs[2].set_xlim(-200000, 200000)
    axs[2].grid(True)

    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.show()

    return


def salvar_audio(audio, fs_simulacao, fs):
    # primeiro, precisamos fazer um downsample para o audio tocar em 44.1kHz
    audio_downsampled, _ = resample_audio(audio, fs_simulacao, fs)
    audio_processado = np.clip(audio_downsampled, -32768, 32767)

    audio = audio_processado.astype(np.int16)
    wavfile.write("audio_recebido.wav", fs, audio)
    return


if __name__ == "__main__":
    fc = 150000  # 150 kHz
    f_corte = 15000  # 15 kHz
    fs_simulacao = 1000000  # 1 MHz
    # queremos uma frequência de simulação alta o suficiente para "ver" a portadora.
    arquivo = "audio.wav"

    # Passo 1: extrair o arquivo de audio
    n_amostras, fs_audio, mensagem = extrair_mensagem(arquivo, fs_simulacao)

    # Passo 2: gerar uma portadora com o mesmo tamanho (n de amostras) do audio
    portadora = gerar_portadora(fc, fs_simulacao, n_amostras)

    # Passo 3: modular via AM convencional
    mensagem_modulada = modulacao(portadora, mensagem)

    # Passo 4: demodular o sinal modulado
    mensagem_demodulada = demodulacao(mensagem_modulada, fs_simulacao, f_corte)

    # Passo 5: salvar o arquivo da mensagem demodulada
    salvar_audio(mensagem_demodulada, fs_simulacao, fs_audio)

    # Passo 6: gerar os gráficos dos sinais, e os espectros
    gerar_graficos(mensagem, mensagem_modulada, mensagem_demodulada, fs_simulacao)
