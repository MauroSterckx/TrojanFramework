import base64
import os
from io import BytesIO
from PIL import ImageGrab

def run():
    try:
        # Maak een screenshot
        screenshot = ImageGrab.grab()
        
        buffer = BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)
        encoded_screenshot = base64.b64encode(buffer.read()).decode("utf-8")
        
        # Geef Base64-gecodeerde data terug
        return {"screenshot": encoded_screenshot}
    
    except Exception as e:
        return {"error": f"Fout bij maken van screenshot: {str(e)}"}
