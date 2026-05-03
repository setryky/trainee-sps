#!/usr/bin/bash/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def filtro_fase_linear(fs, fc, numtaps=101):
    atraso = (numtaps - 1) / 2
    n = np.arange(numtaps) - atraso
    f_n = fc / fs
    h_sinc = 2 * f_n * np.sinc(2 * f_n * n)

    # Aplicação da janela de hamming no filtro
    window = np.hamming(numtaps)
    h_final = h_sinc * window

    return h_final


# def low_pass_filter(m_t_hat):
#     windows_size = 50
#     kernel = np.ones(windows_size) / windows_size
#     s_t = np.convolve(m_t_hat, kernel, mode="same")
#     return s_t

if __name__ == "__main__":
    fs = 1_000_000  # 1 MHz
    fc = 15_000  # 15 kHz

    # Plotando o filtro de fase linear

    h_final = filtro_fase_linear(fs, fc, 101)
    n = np.arange(len(h_final))
    plt.plot(n, h_final)
    plt.show()

    w, h = signal.freqz(h_final, worN=8000)
    freq_hz = w * fs / (2 * np.pi)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Gráfico de Magnitude (dB)
    ax1.set_title("Resposta em Frequência")
    ax1.plot(freq_hz, 20 * np.log10(abs(h)), "b", label="Magnitude (dB)")
    ax1.set_ylabel("Magnitude [dB]", color="b")
    ax1.set_xlabel("Frequência [Hz]")
    ax1.set_xlim([0, fc * 4])  # Focar na região de interesse (até 60kHz)
    ax1.set_ylim([-80, 5])
    ax1.grid(True)

    # Criar um segundo eixo para a Fase
    ax2 = ax1.twinx()
    # Calcula a fase em radianos e converte para graus
    fase = np.unwrap(np.angle(h)) * 180 / np.pi
    ax2.plot(freq_hz, fase, "r--", label="Fase (graus)")
    ax2.set_ylabel("Fase [Graus]", color="r")

    plt.tight_layout()
    plt.show()

    # Plot do filtro fase não-linear baseado em RC de 1 ordem

    T = 1 / fs
    RC = 1 / (2 * np.pi * fc)

    K = 2 * RC / T
    b0 = 1 / (1 + K)
    b1 = 1 / (1 + K)
    a1 = (1 - K) / (1 + K)
    filtro_digital = signal.dlti([b0, b1], [1, a1], dt=T)

    w, mag, phase = signal.dbode(filtro_digital, n=10000)

    print("w= ", w)
    print("mag= ", mag)
    print("phase= ", phase)

    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    plt.subplots_adjust(hspace=0.4)
    # Gráfico 1: Audio original

    axs[0].plot(w, mag, color="blue")
    axs[0].set_title("1. frequência")
    axs[0].grid(True)

    # Gráfico 2: Portadora

    # Gráfico 3: Sinal Modulado

    axs[1].plot(w, phase, color="orange")
    axs[1].set_title("2. fase")
    axs[1].grid(True)

    plt.show()
