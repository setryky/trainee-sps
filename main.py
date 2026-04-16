import numpy as np
import matplotlib.pyplot as plt


def gerar_portadora(fc, fs, t):

    return portadora

def modulacao(portadora, mensagem, fs, t):
    
    return m_t

def demodulacao(m_t, fs, t):

    m_t_hat = retificacao(m_t)
    s_t = low-pass-filter(m_t_hat)

    return s_t


def retificacao(r_t):
    return np.abs(r_t)

def low-pass-filter(m_t_hat)
    
    return s_t

if __name__ == '__main__':
    portadora, mensagem, fc, fs, t = np.zeros()

    portadora = gerar_portadora(fc, fs, t)
    # n_samples = len(mensagem)     #n_samples depende de fs e t 
    #
    # fs = 48000
    # t = np.arange(0, n_samples, 1/fs)
    #
    # mensagem = mensagem.wav       #ver como importar o audio em wav

    m_t = modulacao(portadora, mensagem, fs, t)
    
    play_audio(m_t, fs) #procurar a função

    s_t = demodulacao(m_t, fs, t)
    
    gerar_graficos(portadora, mensagem, m_t, s_t)

    
