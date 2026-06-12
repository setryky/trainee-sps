#!/usr/bin/bash/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import sys

from main import demodulacao, salvar_audio, calcular_espectro


def gerar_graficos(m_t, s_t, fs):
    # --- Plotando os gráficos do sinal no tempo ---
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    plt.subplots_adjust(hspace=0.4)

    n = np.arange(len(m_t))

    # 1. Sinal modulado
    axs[0].plot(n, m_t, color="orange")
    axs[0].set_title("Sinal modulado")
    axs[0].grid(True)

    # 2. Sinal demodulado
    axs[1].plot(n, s_t, color="green")
    axs[1].set_title("Sinal demodulado")
    axs[1].set_ylim(-40000, 40000)
    axs[1].grid(True)

    plt.xlabel("Tempo (s)")
    plt.show()

    # --- Plotando os espectros dos sinais ---

    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    plt.subplots_adjust(hspace=0.4)

    # 1. Espectro do Sinal modulado
    f, m_t_dfft = calcular_espectro(m_t, fs)
    axs[0].plot(f, m_t_dfft, color="orange")
    axs[0].set_title("Espectro do Sinal modulado")
    axs[0].set_xlim(-200000, 200000)
    axs[0].grid(True)

    # 2. Espectro do Sinal demodulado
    f, s_t_dfft = calcular_espectro(s_t, fs)
    axs[1].plot(f, s_t_dfft, color="green")
    axs[1].set_title("Espectro do Sinal demodulado")
    axs[1].set_xlim(-200000, 200000)
    axs[1].grid(True)

    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.show()

    return


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
    # mensagem, n_amostras = resample_audio(audio, fs, fs_simulacao)
    return fs, audio


if __name__ == "__main__":
    # extrair o áudio, modular, e salvar em arquivo
    if len(sys.argv) < 2:
        nome_arquivo = "audio_modulado.wav"
    else:
        nome_arquivo = sys.argv[1]

    fc = 150000  # 150 kHz
    f_corte = 15000  # 15 kHz
    fs_simulacao = 1000000  # 1 MHz
    # queremos uma frequência de simulação alta o suficiente para "ver" a portadora.

    # Passo 1: extrair o arquivo de audio
    fs_audio, mensagem_modulada = extrair_mensagem(nome_arquivo, fs_simulacao)

    # # Passo 2: gerar uma portadora com o mesmo tamanho (n de amostras) do audio
    # portadora = gerar_portadora(fc, fs_simulacao, n_amostras)
    #
    # # Passo 3: modular via AM convencional
    # mensagem_modulada = modulacao(portadora, mensagem)

    # Passo 4: demodular o sinal modulado
    mensagem_demodulada = demodulacao(mensagem_modulada, fs_simulacao, f_corte)

    # Passo 5: salvar o arquivo da mensagem demodulada
    salvar_audio(mensagem_demodulada, fs_simulacao, fs_audio, "audio_demodulado.wav")

    # # Passo 6: gerar os gráficos dos sinais, e os espectros
    gerar_graficos(mensagem_modulada, mensagem_demodulada, fs_simulacao)
