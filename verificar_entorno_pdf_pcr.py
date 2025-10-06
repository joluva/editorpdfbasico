import importlib
import subprocess
import sys

def verificar_libreria(nombre, extra_test=None):
    print(f"🔹 Verificando {nombre}...", end=" ")
    try:
        modulo = importlib.import_module(nombre)
        print("✅ OK")
        if extra_test:
            extra_test(modulo)
    except ModuleNotFoundError:
        print("❌ No encontrado")
        instalar = input(f"¿Querés instalar {nombre}? (s/n): ").lower()
        if instalar == "s":
            subprocess.run([sys.executable, "-m", "pip", "install", nombre])
            print(f"Reintentando {nombre}...\n")
            verificar_libreria(nombre, extra_test)
    except Exception as e:
        print(f"⚠️ Error: {e}")

def test_tesseract(modulo):
    print("   ↳ Probando conexión con Tesseract OCR...")
    try:
        version = modulo.get_tesseract_version()
        print(f"   ✅ Tesseract OCR detectado: versión {version}")
    except Exception as e:
        print(f"   ❌ No se pudo acceder a Tesseract OCR: {e}")
        print("   🔧 Verificá que esté instalado y agregado al PATH.")
        print("   🔹 Windows: C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        print("   🔹 Linux: sudo apt install tesseract-ocr tesseract-ocr-spa")

def test_tkinter(modulo):
    print("   ↳ Probando ventana de Tkinter...")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("Prueba Tkinter")
        root.geometry("250x100")
        label = tk.Label(root, text="Tkinter funcionando ✅")
        label.pack(expand=True)
        root.after(1500, root.destroy)
        root.mainloop()
    except Exception as e:
        print(f"   ⚠️ Error con Tkinter: {e}")

def main():
    print("🧠 Verificación del entorno OCR + PDF + GUI en Python\n")

    verificar_libreria("fitz")          # PyMuPDF
    verificar_libreria("PIL")           # Pillow
    verificar_libreria("pytesseract", test_tesseract)
    verificar_libreria("tkinter", test_tkinter)

    print("\n✅ Verificación finalizada.")

if __name__ == "__main__":
    main()
