from modules.gui_manager import crear_ventana # Importa la función que crea la interfaz gráfica

if __name__ == "__main__":
    # Solo se ejecuta cuando este archivo es el programa principal
    ventana = crear_ventana() # Crea la ventana principal de la aplicación
    ventana.mainloop() # Inicia el bucle de eventos que mantiene la ventana abierta