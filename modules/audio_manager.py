import os # Para acceder a variables de entorno y otras funciones del sistema
import time # Para funciones de temporización como esperas activas
import requests # Para hacer peticiones HTTP a servicios web
import sounddevice as sd # Para grabar y reproducir audio desde el micrófono
from scipy.io.wavfile import write # Para guardar grabaciones como archivos WAV

# Definimos las constantes necesarias para la API y la grabación de audio
API_KEY = os.getenv("AAI_API_KEY", "TU_API_KEY_AQUI")
UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIBE_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
HEADERS = {"authorization": API_KEY, "content-type": "application/json"}
SAMPLERATE = 16000
DURATION_SECONDS = 5 # Duración de la grabación en segundos
WAV_FILENAME = "temp_audio.wav" # Nombre del archivo de audio guardado

def grabar_audio():
    """
    Graba audio del micrófono durante 5 segundos y guarda el resultado en un archivo WAV.
    """
    print("🎤 Grabando audio...")
    audio = sd.rec(
    int(SAMPLERATE * DURATION_SECONDS),
    samplerate=SAMPLERATE,
    channels=1,
    dtype='int16'
    )
    sd.wait()
    write(WAV_FILENAME, SAMPLERATE, audio)
    print(f"✅ Audio grabado en '{WAV_FILENAME}'")
    return WAV_FILENAME


def subir_audio(filepath):
    """
    Sube el archivo WAV previamente grabado a AssemblyAI y devuelve la URL pública del audio.
    """
    print("📤 Subiendo archivo a AssemblyAI...") 
    with open(filepath, 'rb') as f:
        response = requests.post(UPLOAD_ENDPOINT, headers={"authorization": API_KEY}, data=f)
        if response.status_code == 200:
            upload_url = response.json()["upload_url"]
            print(f"✅ Archivo subido: {upload_url}") 
            return upload_url
        else:
            raise Exception(f"❌ Error: {response.text}")


def solicitar_transcripcion(audio_url):
    """
    Solicita la transcripción asíncrona del audio dado su URL en AssemblyAI, configurada para español.
    """
    print("📝 Solicitando transcripción...") 
    json_data = {
    "audio_url": audio_url,
    "language_code": "es"
    }
    response = requests.post(TRANSCRIBE_ENDPOINT, json=json_data, headers=HEADERS)
    if response.status_code == 200:
        transcript_id = response.json()["id"]
        print(f"✅ ID: {transcript_id}") 
        return transcript_id
    else:
        raise Exception(f"❌ Error: {response.text}")


def obtener_resultado_transcripcion(transcript_id):
    """
    Realiza polling hasta que la transcripción esté completa o haya error.
    """
    print(" Esperando resultados...")

    polling_endpoint = f"{TRANSCRIBE_ENDPOINT}/{transcript_id}"
    while True:
        response = requests.get(polling_endpoint, headers=HEADERS)
        status = response.json()["status"]
        if status == "completed":
            print("✅ Completada.") 
            return response.json().get("text", "")
        elif status == "error":
            raise Exception(f"❌ {response.json()['error']}") 
        else:
            print(f"⏳ Estado: {status}. Reintentando en 2s...") 
            time.sleep(2)


def escuchar():
    """
    Orquesta el proceso completo: grabar, subir, transcribir y obtener texto.
    """
    try:
        archivo = grabar_audio()
        url_audio = subir_audio(archivo)
        id_transcripcion = solicitar_transcripcion(url_audio)
        texto = obtener_resultado_transcripcion(id_transcripcion)
        return texto
    except Exception as e:
        print(f"❌ Error: {e}") 
        return ""
