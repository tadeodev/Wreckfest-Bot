import pyautogui
import keyboard
import time
import random
import logging
import json

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Modo de simulación (True para pruebas, False para ejecución real)
SIMULATION_MODE = False

# Cargar configuración desde archivo JSON
with open("config.json", "r") as config_file:
    CONFIG = json.load(config_file)

def press_key(key, hold_time=0.1):
    """Presiona una tecla con duración controlada."""
    if SIMULATION_MODE:
        logging.info(f"[Simulación] Presionando {key} por {hold_time} segundos.")
    else:
        pyautogui.keyDown(key)
        time.sleep(hold_time)
        pyautogui.keyUp(key)

def detect_image(image_path, confidence=0.8, grayscale=True):
    """Detecta una imagen en la pantalla."""
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence, grayscale=grayscale)
        return location is not None
    except Exception as e:
        logging.error(f"Error al detectar la imagen {image_path}: {e}")
        return False

def random_turn():
    """Realiza un giro aleatorio."""
    direction = random.choice(["left", "right", "down"])
    logging.info(f"Girando a la {direction}")
    if direction == "down":
        pyautogui.keyUp("up")
    press_key(direction, hold_time=random.uniform(1.0, 2.5))


def emulate_keys():
    logging.info("Presiona 'y' para empezar y 'u' para detener.")
    keyboard.wait('y')
    logging.info("Iniciando...")

    while True:
        if keyboard.is_pressed('u'):
            logging.info("Programa detenido por el usuario.")
            break

        logging.info("Buscando mapa...")
        while not detect_image(CONFIG['images']['map']):
            press_key("right", hold_time=0.1)
            time.sleep(CONFIG['timing']['map_check_interval'])

        logging.info("Mapa seleccionado. Presionando Enter para continuar.")
        for _ in range(2):
            press_key("enter", hold_time=0.1)
            time.sleep(0.5)

        logging.info("Seleccionando Battle Bus...")
        while not detect_image(CONFIG['images']['bus']):
            logging.info("Bus no encontrado, buscando nuevamente...")
            press_key("left", hold_time=0.1)
            time.sleep(CONFIG['timing']['bus_check_interval'])

        logging.info("Bus seleccionado. Presionando Enter para avanzar.")
        while not detect_image(CONFIG['images']['resumen']):
            press_key("enter", hold_time=0.2)
        time.sleep(1)

        logging.info("Terminando el resumen... Entrando en el mapa.")
        press_key("enter", hold_time=0.1)

        logging.info("Esperando que cargue el mapa...")
        while detect_image(CONFIG['images']['cargando']):
            logging.info("El mapa aún está cargando...")
            time.sleep(0.5)

        logging.info("Preparando para iniciar carrera...")
        while  detect_image(CONFIG['images']['before_race']):
            press_key("enter", hold_time=0.1)
        time.sleep(0.5)

        timeStarter = time.time()

        while True:
            tiempoTranscurrido = time.time() - timeStarter
            if tiempoTranscurrido >= 110:
                logging.info("Se detiene porque han pasado casi 2 minutos.")
                break

            if keyboard.is_pressed('u'):
                logging.info("Programa detenido por el usuario.")
                return

            pyautogui.keyDown("up")
            time.sleep(random.randint(2,4))
            logging.info("Acelerando")

            for _ in range(random.randint(1, 5)):
                random_turn()

            logging.info("Preparando respawn")
            press_key('space', hold_time=random.uniform(3, 5))
            press_key('r', hold_time=0.5)

        logging.info("Reiniciando ciclo.")
        while not detect_image(CONFIG['images']['event_menu']):
            press_key("enter", hold_time=0.1)
            time.sleep(0.5)

if __name__ == "__main__":
    emulate_keys()
