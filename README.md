# 🔐 Image Fingerprint Steganography

A Python-based project that embeds an encrypted fingerprint inside an image using **Least Significant Bit (LSB) Steganography** and extracts it securely using a **seed-based randomized approach**.

## 🚀 Features
- **Secure Fingerprint Embedding**: Encrypts fingerprints before embedding.
- **Randomized Steganography**: Uses a seed value to select pixels in a non-sequential manner.
- **Image Protection**: Minimal distortion using LSB technique.
- **GUI-Based Application**: Simple and interactive Tkinter interface.
- **End-to-End Encryption**: Ensures data confidentiality with **Fernet symmetric encryption**.
- **Custom Seed Generation**: Allows users to generate unique random seeds for added security.

## 📌 How It Works
### 1️⃣ Embedding Process
1. Select an image.
2. Enter or generate a fingerprint.
3. Generate a **random seed** (or use a custom one).
4. The fingerprint is **encrypted** and **embedded** in the image.
5. Save the **seed** and **encryption key** for future extraction.

### 2️⃣ Extraction Process
1. Upload the watermarked image.
2. Provide the **seed** and **encryption key**.
3. Extract the fingerprint using the same seed-based pixel selection.
4. Decrypt the fingerprint and display the result.

## 📂 Project Structure
```
📁 Image-Fingerprint-Stegano/
├── 📜 README.md
├── 📜 embed_fingerprint.py  # Embeds encrypted fingerprint in an image
├── 📜 extract_fingerprint.py  # Extracts and decrypts fingerprint
├── 📜 gui.py  # Tkinter GUI for user interaction
├── 📜 requirements.txt  # Required dependencies
└── 📂 sample_images/  # Sample images for testing
```

## 🛠 Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/coderkedarxp/Anti-Piracy-Project.git
cd Anti-Piracy-Project
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the GUI
```bash
python ui.py
```

## 🎯 Use Cases
🔹 **Digital Forensics** – Watermarking fingerprints in forensic images.
🔹 **Data Security** – Embedding personal identifiers securely in images.
🔹 **Confidential Document Marking** – Hiding authentication details inside official images.

## 🔐 Security Considerations
✔️ The **encryption key** should be stored securely.
✔️ The **seed value** must be the same for embedding and extraction.
✔️ Lossy image formats (JPEG) may distort the fingerprint – PNG is recommended.

## 🤝 Contributing
Contributions are welcome! If you’d like to improve this project, feel free to **fork** the repository, create a branch, and submit a **pull request**.

## 📜 License
This project is licensed under the **MIT License**.

---
🚀 **Secure your images with encrypted fingerprints today!** 🔍

