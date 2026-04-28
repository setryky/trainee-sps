import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal


def lowpass_filter(x, K):
    # O filtro é implementado pela equação das diferenças calculado.
    # Usamos os termos b0, b1 e a1, que dependem dos valores de capacitância e resistência.
    # Consideramos que o estado inicial é de repouso, logo x[-1] e y[-1] são zero.

    b0 = 1 / (1 + K)
    b1 = 1 / (1 + K)
    a1 = (1 - K) / (1 + K)

    y = np.zeros(shape=x.shape)
    y[0] = b0 * x[0]
    for n in range(1, len(x)):
        y[n] = b0 * x[n] + b1 * x[n - 1] - a1 * y[n - 1]

    return y


def filtro_fase_linear(fs, fc, numtaps=101):
    M = (numtaps - 1) / 2
    n = np.arange(numtaps) - M

    f_n = fc / fs
    # TODO - demonstrar a implementação do filtro ideal com a SINC
    h_sinc = 2 * f_n * np.sinc(2 * f_n * n)

    # Explicar o janelamento de Hamming
    window = np.hamming(numtaps)

    # Aplicação da janela e normalização
    h_final = h_sinc * window
    h_final /= np.sum(h_final)  # Garante que o ganho em 0Hz seja 1 (0dB)
    print(h_final)
    return h_final


if __name__ == "__main__":
    fs = 1_000_000  # 1 MHz
    fc = 15_000  # 15 kHz

    # T = 1 / fs
    # RC = 1 / (2 * np.pi * fc)
    #
    # K = 2 * RC / T
    # b0 = 1 / (1 + K)
    # b1 = 1 / (1 + K)
    # a1 = (1 - K) / (1 + K)
    # filtro_digital = signal.dlti([b0, b1], [1, a1], dt=T)
    #
    # # --- Calculando a Resposta ---
    # # w: frequências, mag: magnitude em dB, phase: fase em graus
    # w, mag, phase = signal.dbode(filtro_digital, n=10000)
    #
    # print("w= ", w)
    # print("mag= ", mag)
    # print("phase= ", phase)

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

    # fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    # plt.subplots_adjust(hspace=0.4)
    # # Gráfico 1: Audio original
    #
    # axs[0].plot(w, mag, color="blue")
    # axs[0].set_title("1. frequência")
    # axs[0].grid(True)
    #
    # # Gráfico 2: Portadora
    #
    # # Gráfico 3: Sinal Modulado
    #
    # axs[1].plot(w, phase, color="orange")
    # axs[1].set_title("2. fase")
    # axs[1].grid(True)
    #
    # plt.show()
