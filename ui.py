import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import time
import secrets
from cryptography.fernet import Fernet
import embed_fingerprint
import extract_fingerprint

root = tk.Tk()
root.title("Fingerprint Embedder and Extractor")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

embed_frame = ttk.Frame(notebook)
extract_frame = ttk.Frame(notebook)

notebook.add(embed_frame, text="Embed Fingerprint")
notebook.add(extract_frame, text="Extract Fingerprint")

embed_images = []
embed_fingerprint_var = tk.StringVar()
embed_seed_var = tk.StringVar()
embed_status_var = tk.StringVar()
embed_encrypt_key = None

tk.Label(embed_frame, text="Upload Images:").grid(row=0, column=0, padx=5, pady=5)
tk.Button(embed_frame, text="Browse", command=lambda: upload_images()).grid(row=0, column=1, padx=5, pady=5)
tk.Label(embed_frame, text="Selected Images:").grid(row=1, column=0, padx=5, pady=5)
selected_images_label = tk.Label(embed_frame, text="None")
selected_images_label.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

tk.Label(embed_frame, text="Fingerprint:").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(embed_frame, textvariable=embed_fingerprint_var).grid(row=2, column=1, padx=5, pady=5)
tk.Button(embed_frame, text="Generate", command=lambda: generate_fingerprint()).grid(row=2, column=2, padx=5, pady=5)

tk.Label(embed_frame, text="Seed:").grid(row=3, column=0, padx=5, pady=5)
tk.Entry(embed_frame, textvariable=embed_seed_var).grid(row=3, column=1, padx=5, pady=5)
tk.Button(embed_frame, text="Generate", command=lambda: generate_seed()).grid(row=3, column=2, padx=5, pady=5)

tk.Button(embed_frame, text="Embed Fingerprint", command=lambda: embed_process()).grid(row=4, column=0, columnspan=3, pady=10)

progress = ttk.Progressbar(embed_frame, mode='indeterminate')
progress.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

tk.Label(embed_frame, text="Status:").grid(row=6, column=0, padx=5, pady=5)
tk.Label(embed_frame, textvariable=embed_status_var).grid(row=6, column=1, columnspan=2, padx=5, pady=5, sticky="w")

download_button = tk.Button(embed_frame, text="Download Watermarked Images", state='disabled', command=lambda: download_watermarked())
download_button.grid(row=7, column=0, columnspan=3, pady=5)

tk.Label(embed_frame, text="Seed Used:").grid(row=8, column=0, padx=5, pady=5)
seed_used_label = tk.Label(embed_frame, text="None", wraplength=300)
seed_used_label.grid(row=8, column=1, padx=5, pady=5, sticky="w")

tk.Label(embed_frame, text="Encrypt Key:").grid(row=9, column=0, padx=5, pady=5)
encrypt_key_label = tk.Label(embed_frame, text="None", wraplength=300)
encrypt_key_label.grid(row=9, column=1, padx=5, pady=5, sticky="w")
tk.Button(embed_frame, text="Save Seed & Key to File", command=lambda: save_seed_and_key()).grid(row=9, column=2, padx=5, pady=5)

def upload_images():
    global embed_images
    embed_images = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if embed_images:
        selected_images_label.config(text=", ".join([os.path.basename(f) for f in embed_images]))
    else:
        selected_images_label.config(text="None")

def generate_fingerprint():
    fingerprint = "user_" + time.strftime("%Y%m%d_%H%M%S")
    embed_fingerprint_var.set(fingerprint)

def generate_seed():
    seed = secrets.token_hex(16)
    embed_seed_var.set(seed)

def embed_process():
    global embed_encrypt_key
    if not embed_images:
        messagebox.showerror("Error", "Please upload at least one image.")
        return
    fingerprint = embed_fingerprint_var.get()
    if not fingerprint:
        messagebox.showerror("Error", "Please provide a fingerprint.")
        return
    seed = embed_seed_var.get()
    if not seed:
        messagebox.showerror("Error", "Please provide a seed.")
        return
    progress.start()
    embed_status_var.set("Embedding...")
    root.update_idletasks()
    try:
        for img_path in embed_images:
            output_path = os.path.splitext(img_path)[0] + "_watermarked" + os.path.splitext(img_path)[1]
            embed_encrypt_key = embed_fingerprint.embed_fingerprint(img_path, fingerprint, output_path, seed=seed)
        embed_status_var.set("Embedding successful.")
        download_button.config(state='normal')
        seed_used_label.config(text=seed)
        encrypt_key_label.config(text=embed_encrypt_key.decode())
    except Exception as e:
        embed_status_var.set(f"Error: {str(e)}")
        messagebox.showerror("Error", str(e))
    finally:
        progress.stop()

def download_watermarked():
    messagebox.showinfo("Info", "Watermarked images are saved in the same directory with '_watermarked' suffix.")

def save_seed_and_key():
    if embed_encrypt_key and embed_seed_var.get():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(f"Seed: {embed_seed_var.get()}\n")
                f.write(f"Encrypt Key: {embed_encrypt_key.decode()}\n")
            messagebox.showinfo("Success", "Seed and encrypt key saved successfully.")
    else:
        messagebox.showerror("Error", "No seed or encrypt key to save.")

extract_image = None
extract_seed_var = tk.StringVar()
extract_encrypt_key_var = tk.StringVar()
extract_result_var = tk.StringVar()

tk.Label(extract_frame, text="Upload Watermarked Image:").grid(row=0, column=0, padx=5, pady=5)
tk.Button(extract_frame, text="Browse", command=lambda: upload_extract_image()).grid(row=0, column=1, padx=5, pady=5)
tk.Label(extract_frame, text="Selected Image:").grid(row=1, column=0, padx=5, pady=5)
extract_selected_image_label = tk.Label(extract_frame, text="None")
extract_selected_image_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(extract_frame, text="Seed:").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(extract_frame, textvariable=extract_seed_var).grid(row=2, column=1, padx=5, pady=5)

tk.Label(extract_frame, text="Encrypt Key:").grid(row=3, column=0, padx=5, pady=5)
tk.Entry(extract_frame, textvariable=extract_encrypt_key_var).grid(row=3, column=1, padx=5, pady=5)

tk.Button(extract_frame, text="Extract Fingerprint", command=lambda: extract_process()).grid(row=4, column=0, columnspan=2, pady=10)

extract_progress = ttk.Progressbar(extract_frame, mode='indeterminate')
extract_progress.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

tk.Label(extract_frame, text="Extracted Fingerprint:").grid(row=6, column=0, padx=5, pady=5)
tk.Label(extract_frame, textvariable=extract_result_var, wraplength=300).grid(row=6, column=1, padx=5, pady=5, sticky="w")

def upload_extract_image():
    global extract_image
    extract_image = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if extract_image:
        extract_selected_image_label.config(text=os.path.basename(extract_image))
    else:
        extract_selected_image_label.config(text="None")

def extract_process():
    if not extract_image:
        messagebox.showerror("Error", "Please upload an image.")
        return
    seed = extract_seed_var.get()
    if not seed:
        messagebox.showerror("Error", "Please provide the seed.")
        return
    encrypt_key_str = extract_encrypt_key_var.get()
    if not encrypt_key_str:
        messagebox.showerror("Error", "Please provide the encrypt key.")
        return
    encrypt_key = encrypt_key_str.encode()  # Convert string to bytes
    extract_progress.start()
    extract_result_var.set("Extracting...")
    root.update_idletasks()
    try:
        fingerprint = extract_fingerprint.extract_fingerprint(extract_image, seed=seed, encrypt_key=encrypt_key)
        extract_result_var.set(fingerprint)
    except Exception as e:
        extract_result_var.set(f"Error: {str(e)}")
        messagebox.showerror("Error", str(e))
    finally:
        extract_progress.stop()

root.mainloop()