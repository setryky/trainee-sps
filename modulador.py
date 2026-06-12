#!/usr/bin/bash/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import sys

from main import (
    extrair_mensagem,
    gerar_portadora,
    modulacao,
    calcular_espectro,
)


def gerar_graficos(mensagem, m_t, fs):
    # --- Plotando os gráficos do sinal no tempo ---
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
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

    plt.xlabel("Tempo (s)")
    plt.show()

    # --- Plotando os espectros dos sinais ---

    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
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

    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.show()

    return


def salvar_audio(audio, fs_simulacao, fs, nome_arquivo="audio_demodulado.wav"):
    # primeiro, precisamos fazer um downsample para o audio tocar em 44.1kHz
    # audio_downsampled, _ = resample_audio(audio, fs_simulacao, fs)
    # audio_processado = np.clip(audio_downsampled, -32768, 32767)

    # audio = audio_processado.astype(np.int16)
    wavfile.write(nome_arquivo, fs, audio)
    return


if __name__ == "__main__":
    # extrair o áudio, modular, e salvar em arquivo
    if len(sys.argv) < 2:
        nome_arquivo = "audio.wav"
    else:
        nome_arquivo = sys.argv[1]

    fc = 150000  # 150 kHz
    f_corte = 15000  # 15 kHz
    fs_simulacao = 1000000  # 1 MHz
    # queremos uma frequência de simulação alta o suficiente para "ver" a portadora.

    # Passo 1: extrair o arquivo de audio
    n_amostras, fs_audio, mensagem = extrair_mensagem(nome_arquivo, fs_simulacao)

    # Passo 2: gerar uma portadora com o mesmo tamanho (n de amostras) do audio
    portadora = gerar_portadora(fc, fs_simulacao, n_amostras)

    # Passo 3: modular via AM convencional
    mensagem_modulada = modulacao(portadora, mensagem)

    # # Passo 4: demodular o sinal modulado
    # mensagem_demodulada = demodulacao(mensagem_modulada, fs_simulacao, f_corte)
    #
    # Passo 5: salvar o arquivo da mensagem demodulada
    salvar_audio(mensagem_modulada, fs_simulacao, fs_audio, "audio_modulado.wav")

    # Passo 6: gerar os gráficos dos sinais, e os espectros
    gerar_graficos(mensagem, mensagem_modulada, fs_simulacao)
