import numpy as np
import matplotlib.pyplot as plt

fs = 100000  # Taxa de amostragem (100 kHz)
t = np.arange(0, 0.05, 1 / fs)  # 50ms de duração

# 2. Sinais
fm = 100  # Frequência da mensagem (100 Hz)
fc = 1000  # Frequência da portadora (2 kHz)
A = 1.0  # Amplitude da portadora (DC Offset)
m_t = 0.3 * np.sin(2 * np.pi * fm * t)  # Mensagem (Sinal original)

s_t = (A + m_t) * np.cos(2 * np.pi * fc * t)

s_rect = np.abs(s_t)

# 4. Demodulação Estágio 2: Filtragem LP (Filtro FIR de Média Móvel)
# O tamanho da janela define a "inércia" (como o RC do capacitor)
window_size = 50
kernel = np.ones(window_size) / window_size
s_filtered = np.convolve(s_rect, kernel, mode="same")

# 5. Estágio Final: Remoção de DC e Ganho
# Ajustamos para remover o nível A/pi (aproximado) e recuperar a amplitude
s_final = s_filtered - np.mean(s_filtered)
s_final = s_final * (np.pi / 2)  # Compensação teórica da retificação onda completa

# --- Plotagem ---
fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
plt.subplots_adjust(hspace=0.4)

# Gráfico 1: Sinal Recebido
axs[0].plot(t, s_t, color="blue", alpha=0.7)
axs[0].plot(t, A + m_t, "r--", label="Envelope Superior (Mensagem)")
axs[0].set_title("1. Sinal AM Recebido (Portadora + Mensagem)")
axs[0].legend(loc="upper right")
axs[0].grid(True)

# Gráfico 2: Retificação
axs[1].plot(t, s_rect, color="orange")
axs[1].set_title("2. Sinal Retificado (abs(s(t)))")
axs[1].grid(True)

# Gráfico 3: Resultado da Filtragem
axs[2].plot(t, s_final, color="green", label="Sinal Recuperado")
axs[2].set_title("3. Mensagem Recuperada após Filtro LP")
axs[2].grid(True)

plt.xlabel("Tempo (s)")
plt.show()
