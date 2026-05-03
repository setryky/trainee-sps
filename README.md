
# Simulação de Modulação e Demodulação AM - Trainee SPS

Repositório para o desenvolvimento do projeto Trainee para o capítulo SPS da IEEE. Este repositório contém ferramentas em Python para a simulação do processo de Modulação em Amplitude (AM) e a sua respetiva demodulação através da deteção de invólucro (envelope). O projeto foca-se na aplicação de filtros digitais para o processamento de sinais de áudio reais.

O projeto é composto por dois scripts principais: `filtro.py` e `main.py`.

---

## Requisitos

Para executar os scripts, você precisará ter o Python 3 instalado, junto com as seguintes bibliotecas de processamento e visualização científica:
* numpy
* matplotlib
* scipy

---

## 1. O script `filtro.py`

Este arquivo é focado na análise, projeto e visualização do comportamento de filtros digitais no domínio do tempo e da frequência.

* **`filtro_fase_linear(fs, fc, numtaps=101)`:**
  Calcula a resposta ao impulso (os coeficientes) de um filtro digital passa-baixa FIR (Finite Impulse Response) com fase linear. A implementação baseia-se na geração de uma função *sinc* truncada e aplica uma janela de Hamming. A janela suaviza o sinal nas extremidades, minimizando oscilações residuais causadas pelo truncamento brusco (fenômeno de Gibbs).

---

## 2. O script `main.py`

Este é o arquivo central responsável por executar o *pipeline* de processamento do sinal de áudio, englobando a leitura, modulação, filtragem, demodulação e a gravação do arquivo final.

### Funções de Manipulação de Arquivo e Reamostragem

* **`extrair_mensagem(arquivo, fs_simulacao)`:**
  Lê o arquivo de áudio de entrada `.wav`. Caso o áudio contenha múltiplos canais (estéreo), ele tira a média geométrica dos canais para convertê-lo para mono. Após isso, executa um *upsampling* da taxa de amostragem original do áudio (ex: 44.1 kHz) para uma taxa de amostragem muito mais alta (a frequência de simulação, ex: 1 MHz), o que é vital para conseguirmos processar a portadora de rádiofrequência no meio digital.
* **`resample_audio(data, freq_original, nova_freq)`:**
  Função auxiliar que interpola o sinal no domínio do tempo para recalcular a quantidade de amostras de acordo com a nova taxa de amostragem desejada, utilizando as funções de resample da biblioteca SciPy.
* **`salvar_audio(audio, fs_simulacao, fs)`:**
  Realiza a etapa final de *downsampling*, trazendo o áudio demodulado da frequência de simulação alta de volta para a taxa original de áudio. Também restringe (*clip*) os picos do áudio aos limites estritos do formato inteiro de 16-bits para evitar ruídos de estouro, salvando o resultado em um arquivo `audio_recebido.wav`.

### Funções de Modulação AM

* **`gerar_portadora(fc, fs_simulacao, n_amostras)`:**
  Sintetiza uma onda cossenoidal matemática contínua baseada na frequência da portadora (`fc`) estabelecida.
* **`modulacao(portadora, mensagem)`:**
  Efetua a modulação AM tradicional. Adiciona um nível de tensão constante (nível DC) à mensagem de áudio e aplica um índice de modulação (`mu`). Em seguida, multiplica o sinal modulante resultante pelo sinal da portadora.

### Funções de Demodulação e Filtragem

* **`demodulacao(m_t, fs, f_corte=15000)`:**
  Função coordenadora do circuito detector de envelope. Ela encadeia os passos clássicos da demodulação AM: retificação do sinal modulado, filtragem das altas frequências (removendo a portadora) e retirada do nível de corrente contínua inserido na modulação.
* **`retificacao(r_t)`:**
  Simula um circuito de ponte retificadora de onda completa calculando e extraindo os valores absolutos do sinal da portadora modulada.
* **`filtro_fase_linear(signal, fs, fc, numtaps=101)`** *(Versão aplicação)*:
  Gera os mesmos coeficientes do filtro FIR descritos no arquivo `filtro.py` e executa a operação matemática de convolução contra o sinal recebido. Ao fazer isso, o envelope do sinal de informação é extraído suavemente de dentro da onda de alta frequência retificada.
* **`lowpass_filter(x, K)`:**
  Implementa um filtro passa-baixa IIR (Infinite Impulse Response) de primeira ordem focado no domínio do tempo utilizando uma equação de diferenças. O código calcula os coeficientes da equação baseado no comportamento de um filtro RC analógico tradicional.
* **`removedor_DC(s_t)`:**
  Subtrai a média geral de amplitude do sinal demodulado para centralizá-lo novamente na marca do zero e aplica um fator de ganho em radianos para compensar pequenas perdas na escala impostas pelo método da retificação.

### Funções Analíticas e Visuais

* **`calcular_espectro(sinal, fs)`:**
  Realiza o cálculo computacional da Transformada Rápida de Fourier (FFT), que mapeia a amplitude dos sinais transferindo-os do domínio do tempo para o domínio das frequências em formato logarítmico de Decibéis (dB).
* **`gerar_graficos(mensagem, m_t, s_t, fs)`:**
  Utiliza a biblioteca Matplotlib para traçar painéis visuais de análise comparativa de cada etapa. Ele separa as telas mostrando a progressão temporal em um painel (Áudio Original, Sinal Modulado, Sinal Demodulado e o Erro/Ruído entre eles), e em uma janela separada plota os espectros em frequência de todas as etapas equivalentes.