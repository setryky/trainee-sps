import numpy as np
import matplotlib.pyplot as plt


def gerar_portadora(fc, t):

    portadora = np.cos(2 * np.pi * fc * t) # Gera portadora cossenoidal.

    return portadora

def modulacao(portadora, mensagem, t):

    A = 1.0  # Amplitude da portadora (DC Offset).
    m_t = (A * mensagem) * portadora # Mixing da mensagem com a portadora, gerando o sinal modulado.
    
    return m_t

def demodulacao(m_t, t):

    m_t_hat = retificacao(m_t)
    s_t = low-pass-filter(m_t_hat)
    s_t = dc_removal_gain(s_t)

    return s_t

def retificacao(r_t):
    return np.abs(r_t) # Retificação de onda completa, obtendo o valor absoluto do sinal modulado. É como se fosse uma ponte retificadora, ao invés de apenas um diodo. 

def low-pass-filter(m_t_hat):

    windows_size = 50 # O tamanho da janela define a "inércia" (como o RC do capacitor) do filtro de média móvel. Quanto maior a janela, mais suave será o sinal filtrado, mas também pode introduzir mais atraso e atenuação. O valor de 50 é um ponto de partida razoável para sinais de áudio, mas pode ser ajustado conforme necessário para obter um equilíbrio entre suavização e resposta rápida.
    kernel = np.ones(windows_size) / windows_size # Cria um kernel de média móvel, onde cada elemento é 1/windows_size. Isso significa que cada ponto do sinal filtrado será a média dos últimos "windows_size" pontos do sinal retificado.
    s_t = np.convolve(m_t_hat, kernel, mode="same") # Filtragem do sinal retificado usando uma média móvel (filtro FIR simples) para recuperar a mensagem original.
    return s_t

def dc_removal_gain(s_t):
    s_final = s_t - np.mean(s_t) # Remoção do componente DC do sinal filtrado, centralizando o sinal em torno de zero.
    s_final = s_final * (np.pi / 2)  # Compensação teórica da retificação onda completa.
    return s_final  

def gerar_graficos(portadora, mensagem, m_t, s_t):

    return





if __name__ == '__main__':
    portadora, mensagem, fc, fs, t = np.zeros()

    portadora = gerar_portadora(fc, t)
    # n_samples = len(mensagem)     #n_samples depende de fs e t 
    #
    # fs = 48000
    # t = np.arange(0, n_samples, 1/fs)
    #
    # mensagem = mensagem.wav       #ver como importar o audio em wav

    m_t = modulacao(portadora, mensagem, t)
    
    play_audio(m_t, fs) #procurar a função

    s_t = demodulacao(m_t, t)
    
    gerar_graficos(portadora, mensagem, m_t, s_t)

    
