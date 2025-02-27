import cv2
import numpy as np
from cryptography.fernet import Fernet
import random


def extract_fingerprint(image_path, seed="K3d@r_xAI_2025!", encrypt_key=None):
    img = cv2.imread(image_path)
    img_flat = img.flatten()

    random.seed(seed)  
    indices = list(range(len(img_flat)))
    random.shuffle(indices)

    length_bin = ''.join(str((img_flat[indices[i]] & 1)) for i in range(16))
    length = int(length_bin, 2)

    fingerprint_bin = ''.join(str((img_flat[indices[i + 16]] & 1)) for i in range(length))
    encrypted_fingerprint = bytes(int(fingerprint_bin[i:i+8], 2) for i in range(0, len(fingerprint_bin), 8))

    cipher = Fernet(encrypt_key)
    fingerprint = cipher.decrypt(encrypted_fingerprint).decode()
    return fingerprint
