import cv2
import base64
from io import BytesIO
from PIL import Image

def run():
    try:
        # Open de webcam
        webcam = cv2.VideoCapture(0)

        if not webcam.isOpened():
            return {"error": "Kan geen verbinding maken met de webcam"}

        # Maak een foto
        ret, frame = webcam.read()
        webcam.release()

        if not ret:
            return {"error": "Kon geen foto nemen met de webcam"}

        # Converteer het frame van BGR (OpenCV formaat) naar RGB (PIL formaat)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Sla de afbeelding op in het geheugen als PNG
        image = Image.fromarray(frame_rgb)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        # Base64-encodeer de afbeelding
        encoded_image = base64.b64encode(buffer.read()).decode("utf-8")

        return {"webcam_photo": encoded_image}

    except Exception as e:
        return {"error": f"Fout bij het maken van een webcamfoto: {str(e)}"}
