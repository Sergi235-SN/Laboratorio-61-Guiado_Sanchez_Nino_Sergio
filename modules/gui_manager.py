import tkinter as tk # Importamos tkinter para crear la interfaz gráfica
from modules.audio_manager import escuchar # Importa la función para grabar y transcribir voz
from modules.command_processor import procesar_comando # Importa función para procesar comandosde voz

def crear_ventana():
    """
    Crea una ventana gráfica con tkinter para controlar el reconocimiento de voz.
    """
    ventana = tk.Tk()
    ventana.title("Control por voz - AssemblyAI asíncrono")
    ventana.geometry("500x350")
    ventana.config(bg="#1e1e1e")
    # Título principal
    titulo = tk.Label(
    ventana,
    text="CONTROL POR VOZ (AssemblyAI)",
    font=("Arial", 16, "bold"),
    bg="#1e1e1e",
    fg="#00ffcc"
    )
    titulo.pack(pady=10)
    # Instrucciones
    texto_label = tk.Label(
    ventana,
    text="Haz clic en Escuchar y da un comando.",
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="white"
    )
    texto_label.pack(pady=5)
    # Resultado de transcripción
    resultado_label = tk.Label(
    ventana,
    text="...",
    font=("Arial", 14, "bold"),
    bg="#1e1e1e",
    fg="#00ffcc"
    )
    resultado_label.pack(pady=10)
    # Estado del motor
    estado_motor = tk.Label(
    ventana,
    text="Motor: OFF",
    font=("Arial", 16, "bold"),
    bg="#333",
    fg="white",
    width=15,
    height=2
    )
    estado_motor.pack(pady=20)
    def ejecutar_reconocimiento():
        """
        Se ejecuta al pulsar el botón Escuchar:
        Actualiza etiquetas, reconoce voz y procesa el comando resultante.
        """
        texto_label.config(text="🎤 Escuchando... Habla ahora.") 
        ventana.update()
        text = escuchar()
        texto_label.config(text="⏳ Procesando...") 
        ventana.update()
        procesar_comando(text, estado_motor, resultado_label, ventana)
        # Botón principal
    boton = tk.Button(
    ventana,
    text="🎤 Escuchar",
    command=ejecutar_reconocimiento,
    font=("Arial", 14),
    bg="#00ffcc",
    fg="black",
    width=15,
    height=2
    )
    boton.pack(pady=20)
    return ventana
