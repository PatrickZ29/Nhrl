import requests


API_URL = "http://172.20.10.12:8000/upload"


VIDEO = "fight.mp4"

try:
    
    with open(VIDEO, "rb") as f:
        files = {
            "video": ("fight.mp4", f, "video/mp4")
        }

        print("Enviando video al servidor...")

        response = requests.post(
            API_URL,
            files=files,
            timeout=120
        )

        print("Status:", response.status_code)
        print("Respuesta:", response.text)


except FileNotFoundError:
    print("❌ No se encontró el archivo fight.mp4")


except requests.exceptions.ConnectionError:
    print("❌ No se pudo conectar con el servidor")


except requests.exceptions.Timeout:
    print("❌ La solicitud tardó demasiado")


except Exception as e:
    print("❌ Error:", e)