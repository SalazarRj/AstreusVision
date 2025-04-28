from webcam_detection import run_webcam
from file_detection import run_file_detection
from screen_monitor import run_screen_monitor

def main():
    while True:
        print("\n1. Webcam (detecção)")
        print("2. Detectar em arquivo imagem/vídeo")
        print("3. Monitorar tela (detecção)")
        print("0. Sair")
        c = input("Escolha: ")
        if c == '1':
            run_webcam()
        elif c == '2':
            run_file_detection()
        elif c == '3':
            run_screen_monitor()
        elif c == '0':
            break
        else:
            print("Opção inválida")

if __name__ == '__main__':
    main()
