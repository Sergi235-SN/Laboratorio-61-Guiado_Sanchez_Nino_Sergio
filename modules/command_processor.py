def procesar_comando(text, estado_label, resultado_label, ventana):
    """
    Procesa el comando de voz transcrito y actualiza la interfaz
    según la palabra clave detectada.
    """
    # Normaliza el texto para facilitar la comparación
    text = text.lower().strip()
    # Encender motor
    if "enciende" in text:
        estado_label.config(text="Motor: ON", bg="#00cc00", fg="black")
        resultado_label.config(text="✅ Motor encendido") 
    # Apagar motor
    elif "apaga" in text:
        estado_label.config(text="Motor: OFF", bg="#333", fg="white")
        resultado_label.config(text="🛑 Motor apagado") 
    # Salir de la aplicación
    elif "salir" in text:
        resultado_label.config(text="👋 Cerrando...") 
        ventana.after(1000, ventana.destroy)
    # No detectó voz
    elif text == "":
        resultado_label.config(text="❌ No se detectó voz.") 
    # Comando no reconocido
    else:
        resultado_label.config(text=f" No reconocido: {text}")