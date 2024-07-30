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
    print("Le bouton 'COMMENCER' a été pressé!")

    cap_url = "http://192.168.1.33/cam-hi.jpg"
    run = True
    while run:
        frame = fetch_frame(cap_url)
        if frame is None:
            print("Failed to fetch frame")
            continue

        print("Frame fetched successfully")
        results = model.track(frame, persist=True)
        print("YOLO results: ", results)
        # Visualize the results on the frame
        if not results or len(results) == 0:
            print("No results found")
            continue

        for result in results:
            detection_count = result.boxes.shape[0]
            for i in range(detection_count):
                cls = int(result.boxes.cls[i].item())
                name = result.names[cls]
                track_id = int(result.boxes.id[i].item())
                confidence = float(result.boxes.conf[i].item())
                bounding_box = result.boxes.xyxy[i].cpu().numpy()
                x = int(bounding_box[0])
                y = int(bounding_box[1])
                width = int(bounding_box[2] - x)
                height = int(bounding_box[3] - y)
                print(f"Tracking ID: {track_id}, Name: {name}, Confidence: {confidence}, Bounding Box: {bounding_box}")

    print("Le bouton 'COMMENCER' a été pressé terminé!")


def on_stop_press():
    global run  # Accéder à la variable globale
    run = False
    print("Le bouton 'ARRÊTER' a été pressé!")


def start_yolo_thread():
   on_commencer_press()


# Example usage, this part should be connected to your button press handlers
start_yolo_thread()
