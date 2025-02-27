import embed_fingerprint
import extract_fingerprint

# test.py
if __name__ == "__main__":
    secret_key = "K3d@r_xAI_2025!" 
    encrypt_key = embed_fingerprint.embed_fingerprint("images/image1.png", "user123", "images/watermarked.png", seed=secret_key)
    extracted = extract_fingerprint.extract_fingerprint("images/watermarked.png", seed=secret_key, encrypt_key=encrypt_key)
    print(f"Extracted Fingerprint: {extracted}")