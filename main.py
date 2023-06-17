# Credits: Joaking

import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

# Variable global para almacenar los cambios
cambios = []


def abrir_archivo():
    global cambios
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
    if ruta_archivo:
        try:
            with open(ruta_archivo, 'r') as archivo:
                contenido = json.load(archivo)
                goles_jugadores = obtener_estadisticas_jugadores(contenido, 'goals', 'name', 'goals')
                asistencias_jugadores = obtener_estadisticas_jugadores(contenido, 'assists', 'name', 'assists')
                tarjetas_jugadores = obtener_tarjetas_jugadores(contenido)
                cambios = obtener_cambios()
                mvp = obtener_mvp(contenido)
                mostrar_estadisticas(goles_jugadores, asistencias_jugadores, tarjetas_jugadores, cambios, mvp)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")


def obtener_estadisticas_jugadores(contenido, estadistica, nombre_key, estadistica_key):
    estadisticas_jugadores = []
    if 'players' in contenido:
        jugadores = contenido['players']
        for jugador in jugadores:
            if estadistica in jugador and jugador[estadistica] > 0:
                estadisticas_jugadores.append((jugador[nombre_key], jugador[estadistica_key]))
    return estadisticas_jugadores


def obtener_tarjetas_jugadores(contenido):
    tarjetas_jugadores = []
    if 'players' in contenido:
        jugadores = contenido['players']
        for jugador in jugadores:
            if 'yellowCards' in jugador and jugador['yellowCards'] > 0:
                tarjetas_jugadores.append((jugador['name'], ':yellow_square:'))
            if 'redCards' in jugador and jugador['redCards'] > 0:
                tarjetas_jugadores.append((jugador['name'], ':red_square:'))
    return tarjetas_jugadores


def obtener_cambios():
    return cambios


def obtener_mvp(contenido):
    mvp = None
    if 'players' in contenido:
        jugadores = contenido['players']
        max_puntaje = 0
        for jugador in jugadores:
            if 'score' in jugador and jugador['score'] > max_puntaje:
                max_puntaje = jugador['score']
                mvp = jugador['name']
    return mvp


def agregar_cambio():
    global cambios
    jugador_sale = jugador_sale_entry.get()
    jugador_entra = jugador_entra_entry.get()
    if jugador_sale and jugador_entra:
        cambio = (jugador_sale, jugador_entra)
        cambios.append(cambio)
        texto_box.insert(tk.END, f"- Cambio {len(cambios)}: Sale: {jugador_sale} - Entra: {jugador_entra}\n")
        jugador_sale_entry.delete(0, tk.END)
        jugador_entra_entry.delete(0, tk.END)


def borrar_ultimo_cambio():
    global cambios
    if cambios:
        cambios.pop()
        texto_box.delete("end-2l", tk.END)


# Función para guardar los cambios realizados en el archivo

def mostrar_estadisticas(goles_jugadores, asistencias_jugadores, tarjetas_jugadores, cambios, mvp):
    texto_box.delete("1.0", tk.END)

    arbitro = arbitro_entry.get()
    division = division_entry.get()
    equipo_local = equipo_local_entry.get()
    equipo_visitante = equipo_visitante_entry.get()
    resultado = resultado_entry.get()



    if equipo_local and equipo_visitante and resultado:
        texto_box.insert(tk.END, f"\n**{equipo_local} {resultado} {equipo_visitante}**\n\n")

    if division:
        texto_box.insert(tk.END, f"**{division} División**\n")


    if arbitro:
        texto_box.insert(tk.END, f":boy: **Arbitro: {arbitro}**\n \n")
        texto_box.insert(tk.END,f"**-------------------------------------------------------------** \n")
        
    if goles_jugadores:
        texto_box.insert(tk.END, "\n:soccer: **Goles:**\n")
        for jugador, goles in goles_jugadores:
            texto_box.insert(tk.END, f"- **{jugador} x{goles}**\n")

    if asistencias_jugadores:
        texto_box.insert(tk.END, "\n**-------------------------------------------------------------** \n\n :athletic_shoe: **Asistencias:**\n")
        for jugador, asistencias in asistencias_jugadores:
            texto_box.insert(tk.END, f"- **{jugador} x{asistencias}**\n")

    if cambios_var.get() == 1 and cambios:
        texto_box.insert(tk.END, "\n **-------------------------------------------------------------** \n\n :Cambio: **Cambios:**\n\n")
        for i, (jugador_salida, jugador_entrada) in enumerate(cambios, start=1):
            texto_box.insert(tk.END, f"**:Sale: {jugador_salida} :Entra: {jugador_entrada}**\n")
    else:
        texto_box.insert(tk.END, "\n **-------------------------------------------------------------** \n\n :Cambio: **Cambios:**\n - **No se realizaron cambios.**\n")

    if tarjetas_jugadores:
        texto_box.insert(tk.END, "\n**-------------------------------------------------------------** \n\n :warning: **Tarjetas:**\n")
        for jugador, tarjeta in tarjetas_jugadores:
            texto_box.insert(tk.END, f"- **{jugador}: {tarjeta}**\n")
    else:
        texto_box.insert(tk.END, "\n **-------------------------------------------------------------** \n\n :warning: **Tarjetas:** \n - **No hubieron tarjetas.**\n")

    if mvp:
        texto_box.insert(tk.END, f"\n **-------------------------------------------------------------** \n\n :star: **MVP: {mvp}**\n")


def copiar_texto():
    texto = texto_box.get("1.0", tk.END)
    ventana.clipboard_clear()
    ventana.clipboard_append(texto)
    messagebox.showinfo("Copiado", "Las estadisticas han sido copiadas")


def actualizar_estado_agregar_cambio():
    if cambios_var.get() == 1:
        cambios_button_agregar.config(state=tk.NORMAL)
        for cambio in cambios_entries:
            cambio['salida'].config(state=tk.NORMAL)
            cambio['entrada'].config(state=tk.NORMAL)
    else:
        cambios_button_agregar.config(state=tk.DISABLED)
        for cambio in cambios_entries:
            cambio['salida'].config(state=tk.DISABLED)
            cambio['entrada'].config(state=tk.DISABLED)

ventana = tk.Tk()
ventana.title("Analisis de Partido - APA")
ventana.iconbitmap("imagenes\\apa_logo.ico")

# Frame para el archivo y los datos del partido
archivo_frame = tk.LabelFrame(ventana, text="Archivo")
archivo_frame.pack(fill="both", expand="yes", padx=20, pady=20)

abrir_archivo_button = tk.Button(archivo_frame, text="Abrir archivo", command=abrir_archivo)
abrir_archivo_button.grid(row=0, column=0, padx=5, pady=5)

copiar_button = tk.Button(archivo_frame, text="Copiar", command=lambda: ventana.clipboard_append(texto_box.get("1.0", tk.END)))
copiar_button.grid(row=0, column=1, padx=5, pady=5)

salir_button = tk.Button(archivo_frame, text="Salir", command=ventana.quit)
salir_button.grid(row=0, column=2, padx=5, pady=5)

partido_frame = tk.LabelFrame(ventana, text="Datos del Partido")
partido_frame.pack(fill="both", expand="yes", padx=20, pady=20)

arbitro_label = tk.Label(partido_frame, text="Arbitro:")
arbitro_label.grid(row=0, column=0, padx=5, pady=5)
arbitro_entry = tk.Entry(partido_frame)
arbitro_entry.grid(row=0, column=1, padx=5, pady=5)

division_label = tk.Label(partido_frame, text="División:")
division_label.grid(row=1, column=0, padx=5, pady=5)
division_entry = tk.Entry(partido_frame)
division_entry.grid(row=1, column=1, padx=5, pady=5)

equipo_local_label = tk.Label(partido_frame, text="Equipo Local:")
equipo_local_label.grid(row=2, column=0, padx=5, pady=5)
equipo_local_entry = tk.Entry(partido_frame)
equipo_local_entry.grid(row=2, column=1, padx=5, pady=5)

equipo_visitante_label = tk.Label(partido_frame, text="Equipo Visitante:")
equipo_visitante_label.grid(row=3, column=0, padx=5, pady=5)
equipo_visitante_entry = tk.Entry(partido_frame)
equipo_visitante_entry.grid(row=3, column=1, padx=5, pady=5)

resultado_label = tk.Label(partido_frame, text="Resultado:")
resultado_label.grid(row=4, column=0, padx=5, pady=5)
resultado_entry = tk.Entry(partido_frame)
resultado_entry.grid(row=4, column=1, padx=5, pady=5)

# Frame para las estadisticas
estadisticas_frame = tk.LabelFrame(ventana, text="Estadisticas")
estadisticas_frame.pack(fill="both", expand="yes", padx=20, pady=20)

estadisticas_scroll = tk.Scrollbar(estadisticas_frame)
estadisticas_scroll.pack(side=tk.RIGHT, fill=tk.Y)

texto_box = tk.Text(estadisticas_frame, wrap=tk.WORD, yscrollcommand=estadisticas_scroll.set)
texto_box.pack(fill=tk.BOTH, expand=True)

estadisticas_scroll.config(command=texto_box.yview)

# Frame para los cambios
cambios_frame = tk.LabelFrame(ventana, text="Cambios")
cambios_frame.pack(fill="both", expand="yes", padx=20, pady=20)

jugador_sale_label = tk.Label(cambios_frame, text="Jugador que sale:")
jugador_sale_label.grid(row=0, column=0, padx=5, pady=5)
jugador_sale_entry = tk.Entry(cambios_frame)
jugador_sale_entry.grid(row=0, column=1, padx=5, pady=5)

jugador_entra_label = tk.Label(cambios_frame, text="Jugador que entra:")
jugador_entra_label.grid(row=1, column=0, padx=5, pady=5)
jugador_entra_entry = tk.Entry(cambios_frame)
jugador_entra_entry.grid(row=1, column=1, padx=5, pady=5)

cambios_button_agregar = tk.Button(cambios_frame, text="Añadir cambio", command=agregar_cambio)
cambios_button_agregar.grid(row=2, column=0, padx=5, pady=5)

cambios_button_borrar = tk.Button(cambios_frame, text="Borrar último cambio", command=borrar_ultimo_cambio)
cambios_button_borrar.grid(row=2, column=1, padx=5, pady=5)

# Lista para almacenar las entradas de los cambios
cambios_entries = []

# Frame para las opciones
opciones_frame = tk.LabelFrame(ventana, text="Opciones")
opciones_frame.pack(fill="both", expand="yes", padx=20, pady=20)

cambios_var = tk.IntVar()
cambios_check = tk.Checkbutton(opciones_frame, text="Agregar cambios", variable=cambios_var,
                               command=actualizar_estado_agregar_cambio)
cambios_check.pack()

# Frame para los botones
botones_frame = tk.Frame(ventana)
botones_frame.pack(pady=20)

ventana.mainloop()