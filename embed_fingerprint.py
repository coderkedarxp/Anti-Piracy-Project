import cv2
import numpy as np
from cryptography.fernet import Fernet
import random

def embed_fingerprint(image_path, fingerprint, output_path, seed="K3d@r!", encrypt_key=None):
    if encrypt_key is None:
        encrypt_key = Fernet.generate_key()
    cipher = Fernet(encrypt_key)

    encrypted_fingerprint = cipher.encrypt(fingerprint.encode())
    fingerprint_bin = ''.join(format(b, '08b') for b in encrypted_fingerprint)
    length_bin = format(len(fingerprint_bin), '016b')
    combined_bin = length_bin + fingerprint_bin

    img = cv2.imread(image_path)
    h, w, _ = img.shape
    if len(combined_bin) > h * w * 3:
        raise ValueError("Fingerprint too large for image.")

    random.seed(seed)  
    indices = list(range(h * w * 3))
    random.shuffle(indices)

    img_flat = img.flatten()
    for i, bit in enumerate(combined_bin):
        img_flat[indices[i]] = (img_flat[indices[i]] & ~1) | int(bit)

    img_embedded = img_flat.reshape(h, w, 3)
    cv2.imwrite(output_path, img_embedded)
    return encrypt_key