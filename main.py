import numpy as np
import matplotlib.pyplot as plt


def gerar_portadora(fc, t):

    portadora = np.cos(2 * np.pi * fc * t) #Gera portadora cossenoidal

    return portadora

def modulacao(portadora, mensagem, t):

    A = 1.0  # Amplitude da portadora (DC Offset)
    m_t = (A * mensagem) * portadora
    
    return m_t

def demodulacao(m_t, t):

    m_t_hat = retificacao(m_t)
    s_t = low-pass-filter(m_t_hat)

    return s_t



def retificacao(r_t):
    return np.abs(r_t)

def low-pass-filter(m_t_hat)
    
    return s_t

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

    
