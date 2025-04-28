
# Detector de Objetos YOLOv8

## Descrição
Este projeto implementa um sistema de detecção de objetos em tempo real utilizando o modelo YOLOv8. Ele oferece múltiplas fontes de entrada para detecção, incluindo webcam, arquivos de imagem/vídeo e monitoramento contínuo da tela do computador. As detecções são exibidas com caixas delimitadoras (bounding boxes) e rótulos traduzidos para o português.

## Funcionalidades

* **Detecção via Webcam**: Captura e processa o vídeo da webcam em tempo real, exibindo os objetos detectados com suas respectivas classificações.
* **Detecção em Arquivos**: Permite selecionar e processar imagens ou vídeos do sistema de arquivos.
* **Monitoramento de Tela**: Analisa continuamente o conteúdo exibido na tela do computador, identificando objetos em tempo real.
* **Tradução Automática**: Traduz automaticamente os rótulos de detecção do inglês para o português.
* **Contagem de Objetos**: Exibe a contagem de cada tipo de objeto detectado.
* **Otimização de Desempenho**: Implementa técnicas como processamento em threads e redimensionamento de frames para melhorar o desempenho.

## Tecnologias Utilizadas

* **Python**: Linguagem de programação principal do projeto.
* **YOLOv8 (Ultralytics)**: Modelo de detecção de objetos de última geração.
* **OpenCV (cv2)**: Biblioteca para processamento de imagens e vídeos.
* **DeepSort (deep_sort_realtime)**: Algoritmo para rastreamento de objetos (utilizado em `detector.py`, embora não explicitamente chamado nas funções principais, está importado).
* **Google Translator (googletrans)**: Biblioteca para tradução dos rótulos de detecção.
* **MSS**: Biblioteca para captura de tela eficiente.
* **Threading**: Módulo nativo do Python para execução paralela (usado em `webcam_detection.py` e `screen_monitor.py`).
* **Tkinter**: Biblioteca padrão do Python para interfaces gráficas (utilizada para a janela de seleção de arquivos em `file_detection.py`).

## Pré-requisitos

* Python 3.6 ou superior
* Placa de vídeo compatível com CUDA (recomendado para melhor desempenho)
* Webcam (para o modo de detecção via webcam)
* Bibliotecas Python necessárias:
  - ultralytics (YOLOv8)
  - opencv-python
  - numpy
  - googletrans
  - deep-sort-realtime
  - mss (para captura de tela)

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <https://github.com/SalazarRj/AstreusVision.git>
    cd <AstreusVision>
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  
    # ou
    venv\Scripts\activate 
    ```

3.  **Instale as dependências:**
    Crie um arquivo `requirements.txt` com o seguinte conteúdo:
    ```txt
    ultralytics
    opencv-python
    numpy
    googletrans==4.0.0-rc1 # Especifique uma versão compatível se necessário
    deep-sort-realtime
    mss
    ```
    Em seguida, instale as bibliotecas:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Modelo YOLOv8:**
    O modelo especificado em `config.py` (`yolov8m.pt` por padrão) será baixado automaticamente pela biblioteca `ultralytics` na primeira execução, se não for encontrado localmente. Certifique-se de ter uma conexão com a internet.

## Uso

Execute o script principal `main.py` a partir do seu terminal, dentro do ambiente virtual ativado:

```bash
python main.py
```

Será apresentado um menu com as seguintes opções:

1.  **Webcam (detecção)**: Inicia a detecção de objetos utilizando a webcam conectada ao seu computador. Uma janela será aberta exibindo o vídeo da webcam com as detecções em tempo real. Pressione `ESC` para fechar a janela e retornar ao menu principal.

2.  **Detectar em arquivo imagem/vídeo**: Abre uma janela do sistema para que você selecione um arquivo de imagem (JPG, JPEG, PNG) ou vídeo (MP4, AVI, MOV). Após a seleção, o arquivo será processado e uma janela exibirá o resultado com as detecções. Para imagens, a janela permanecerá aberta até que você pressione qualquer tecla. Para vídeos, a reprodução ocorrerá com as detecções, e você pode pressionar `ESC` para interromper e retornar ao menu.

3.  **Monitorar tela (detecção)**: Inicia o monitoramento contínuo de uma região da sua tela (definida em `config.py`). Uma janela exibirá a captura da tela com as detecções atualizadas em intervalos regulares. Pressione `ESC` para parar o monitoramento e retornar ao menu principal.

0.  **Sair**: Encerra a aplicação.

## Configuração

As principais configurações do sistema podem ser ajustadas diretamente no arquivo `config.py`:

*   `BOX_COLOR`: Define a cor (em formato BGR) das caixas delimitadoras desenhadas ao redor dos objetos detectados. Padrão: `(0, 255, 0)` (verde).
*   `TEXT_COLOR`: Define a cor (em formato BGR) do texto exibido para os rótulos e a confiança da detecção. Padrão: `(0, 0, 255)` (vermelho).
*   `COUNT_TEXT_COLOR`: Define a cor (em formato BGR) do texto usado para exibir a contagem de objetos detectados. Padrão: `(255, 255, 255)` (branco).
*   `YOLO_MODEL_PATH`: Especifica o nome ou caminho do arquivo do modelo YOLOv8 a ser utilizado. Padrão: `"yolov8m.pt"`. A biblioteca `ultralytics` tentará baixar este modelo se não for encontrado localmente.
*   `MONITOR_CONFIG`: Dicionário que define a área da tela a ser capturada no modo de monitoramento. Contém as chaves `top`, `left`, `width` e `height`. Padrão: `{"top": 0, "left": 0, "width": 1280, "height": 720}`.
*   `FPS`: Taxa de quadros por segundo alvo para a exibição no modo de monitoramento de tela (não afeta a taxa de captura ou detecção diretamente). Padrão: `60`.

Outras configurações, como o fator de redimensionamento (`resize_factor`) ou o intervalo entre detecções (`DETECT_INTERVAL`), podem ser ajustadas diretamente nos respectivos scripts (`webcam_detection.py`, `file_detection.py`, `screen_monitor.py`).

## Estrutura do Projeto

O projeto está organizado nos seguintes arquivos:

* **`main.py`**: Ponto de entrada da aplicação, contém o menu interativo principal que permite escolher entre os diferentes modos de detecção.

* **`detector.py`**: Implementa a classe `Detector` que encapsula a funcionalidade de detecção de objetos usando o modelo YOLOv8. Inclui métodos para tradução de rótulos e desenho das caixas delimitadoras.

* **`webcam_detection.py`**: Contém a classe `WebcamStream` para captura otimizada de vídeo da webcam usando threads, e a função `run_webcam()` que implementa o modo de detecção via webcam.

* **`file_detection.py`**: Implementa a função `run_file_detection()` que permite selecionar e processar arquivos de imagem ou vídeo com detecção de objetos.

* **`screen_monitor.py`**: Implementa a função `run_screen_monitor()` e o worker thread para monitoramento contínuo da tela com detecção de objetos em tempo real.

* **`utils.py`**: Contém funções utilitárias usadas pelos outros módulos, como a função `show_window()` para criar janelas OpenCV.

* **`config.py`**: Armazena as configurações globais do sistema, como cores, caminhos de modelo e parâmetros de monitoramento.

* **`download.py`**: Script de exemplo que demonstra como baixar e usar o modelo YOLOv8 diretamente.

## Contribuição

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma *issue* no repositório do projeto.

Se desejar contribuir com código:

1.  Faça um *fork* do projeto.
2.  Crie uma nova *branch* para sua funcionalidade (`git checkout -b feature/sua-nova-feature`).
3.  Faça o *commit* de suas alterações (`git commit -am 'Adiciona nova feature'`).
4.  Faça o *push* para a *branch* (`git push origin feature/sua-nova-feature`).
5.  Abra um *Pull Request*.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
