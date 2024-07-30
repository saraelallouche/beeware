import cv2
from ultralytics import YOLO
from collections import defaultdict
import threading
import requests
import numpy as np
from PIL import Image
import io
import os
# Variable globale pour contrôler l'exécution
run = False

track_history = defaultdict(lambda: [])


def fetch_frame(url):
    try:
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error fetching frame: {e}")
        return None


def on_commencer_press():
    global run  # Accéder à la variable globale
    base_dir = os.path.dirname(__file__)  # Répertoire du script courant
    model_path = os.path.join(base_dir, 'assets', 'yolov8n.pt')
    print(model_path)
    model = YOLO(model_path)
    print("yolo model loaded successfully!")

    cap_url = "http://192.168.1.33/cam-hi.jpg"
    run = True
    while run:
        frame = fetch_frame(cap_url)
        if frame is None:
            print("Failed to fetch frame")
            continue

        print("Frame fetched successfully")
        results = model.track("https://youtu.be/LNwODJXcvt4", show=False, persist=True, save=False)


    print("Le bouton 'COMMENCER' a été pressé terminé!")


def on_stop_press():
    global run  # Accéder à la variable globale
    run = False
    print("Le bouton 'ARRÊTER' a été pressé!")


def start_yolo_thread():
    yolo_thread = threading.Thread(target=on_commencer_press)
    yolo_thread.start()

