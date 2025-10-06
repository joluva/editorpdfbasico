import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
from PIL import Image, ImageTk
import pytesseract, io

# Configurar Tesseract si usas Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

doc = None
pagina_actual = 0
img_tk = None

def abrir_pdf():
    global doc, archivo_pdf, pagina_actual
    archivo_pdf = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if not archivo_pdf:
        return
    doc = fitz.open(archivo_pdf)
    pagina_actual = 0
    mostrar_pagina(pagina_actual)

def mostrar_pagina(num):
    global pagina_actual, img_tk
    if num < 0 or num >= len(doc):
        return
    pagina_actual = num
    pagina = doc[num]
    pix = pagina.get_pixmap()
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    img_tk = ImageTk.PhotoImage(img)
    canvas.delete("all")
    canvas.create_image(0, 0, image=img_tk, anchor="nw")
    root.title(f"Editor PDF OCR - Página {pagina_actual+1}/{len(doc)}")

def guardar_pdf():
    archivo_salida = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
    if archivo_salida:
        doc.save(archivo_salida)
        messagebox.showinfo("Guardado", f"Se guardó en: {archivo_salida}")

# --- OCR ---
def extraer_texto_ocr():
    pagina = doc[pagina_actual]
    pix = pagina.get_pixmap()
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    texto = pytesseract.image_to_string(img, lang="spa")  # OCR en español
    editor_texto(texto)

def editor_texto(texto):
    editor_ventana = tk.Toplevel(root)
    editor_ventana.title(f"OCR/Editar texto - Página {pagina_actual+1}")

    text_area = scrolledtext.ScrolledText(editor_ventana, wrap=tk.WORD, width=80, height=25)
    text_area.pack(expand=True, fill="both")
    text_area.insert("1.0", texto)

    def guardar_edicion():
        nuevo_texto = text_area.get("1.0", tk.END).strip()
        pagina = doc[pagina_actual]
        pagina.insert_text((72,72), nuevo_texto, fontsize=10, color=(0,0,0))
        mostrar_pagina(pagina_actual)
        editor_ventana.destroy()
        messagebox.showinfo("Edición", "Texto OCR insertado en el PDF.")

    btn_guardar = tk.Button(editor_ventana, text="Guardar en PDF", command=guardar_edicion)
    btn_guardar.pack()

# --- INTERFAZ ---
root = tk.Tk()
root.title("Editor PDF con OCR")

frame = tk.Frame(root)
frame.pack(side="top", fill="x")

btn_abrir = tk.Button(frame, text="Abrir PDF", command=abrir_pdf)
btn_abrir.pack(side="left")

btn_guardar = tk.Button(frame, text="Guardar PDF", command=guardar_pdf)
btn_guardar.pack(side="left")

btn_prev = tk.Button(frame, text="<< Anterior", command=lambda: mostrar_pagina(pagina_actual-1))
btn_prev.pack(side="left")

btn_next = tk.Button(frame, text="Siguiente >>", command=lambda: mostrar_pagina(pagina_actual+1))
btn_next.pack(side="left")

btn_ocr = tk.Button(frame, text="OCR Página", command=extraer_texto_ocr)
btn_ocr.pack(side="left")

canvas = tk.Canvas(root, width=800, height=1000, bg="white")
canvas.pack()

root.mainloop()
