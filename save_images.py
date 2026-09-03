# -*- coding: utf-8 -*-
"""
vncrypt - SAVE
Pour chaque PNG des dossiers listes dans crypt_targets.txt qui n'est pas
deja chiffre : remplace l'image visible par une silhouette noire (alpha
conservee) et embarque l'original chiffre (AES-256-GCM) dans un chunk
texte du PNG. Idempotent.
"""

import os
import sys
import base64
from PIL import Image, PngImagePlugin
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY_FILE = "vncrypt_key.bin"
TARGETS_FILE = "crypt_targets.txt"
MARKER_KEY = "vncrypt"
DATA_KEY = "vndata"


def load_or_create_key(key_path):
    if os.path.exists(key_path):
        with open(key_path, "r", encoding="ascii") as f:
            return base64.b64decode(f.read().strip())
    key = get_random_bytes(32)
    with open(key_path, "w", encoding="ascii") as f:
        f.write(base64.b64encode(key).decode("ascii"))
    print(f"[!] Nouvelle cle generee : {key_path}")
    print("    -> Sauvegarde-la precieusement, elle ne doit JAMAIS etre commit.")
    return key


def encrypt_bytes(data, key):
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + tag + ciphertext


def get_target_folders(root):
    targets_path = os.path.join(root, TARGETS_FILE)
    if not os.path.exists(targets_path):
        print(f"[!] Fichier introuvable : {targets_path}")
        sys.exit(1)
    folders = []
    with open(targets_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                folders.append(line)
    return folders


def make_silhouette(img):
    img = img.convert("RGBA")
    _, _, _, a = img.split()
    zero = Image.new("L", img.size, 0)
    return Image.merge("RGBA", (zero, zero, zero, a))


def process_folder(full_folder, key):
    done, skipped = 0, 0
    for dirpath, _, filenames in os.walk(full_folder):
        for fname in filenames:
            if not fname.lower().endswith(".png"):
                continue
            fpath = os.path.join(dirpath, fname)
            try:
                img = Image.open(fpath)
                img.load()
            except Exception as e:
                print(f"[!] Impossible d'ouvrir {fpath}: {e}")
                continue

            if img.info.get(MARKER_KEY) == "1":
                skipped += 1
                continue

            with open(fpath, "rb") as f:
                original_bytes = f.read()

            enc = encrypt_bytes(original_bytes, key)
            b64 = base64.b64encode(enc).decode("ascii")
            silhouette = make_silhouette(img)

            info = PngImagePlugin.PngInfo()
            info.add_text(MARKER_KEY, "1")
            info.add_text(DATA_KEY, b64)
            silhouette.save(fpath, "PNG", pnginfo=info)

            print(f"[OK] Chiffre : {os.path.relpath(fpath, full_folder)}")
            done += 1
    return done, skipped


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    key = load_or_create_key(os.path.join(root, KEY_FILE))
    folders = get_target_folders(root)

    total_done, total_skipped = 0, 0
    for folder in folders:
        full_folder = os.path.join(root, folder)
        if not os.path.isdir(full_folder):
            print(f"[!] Dossier introuvable, ignore : {full_folder}")
            continue
        done, skipped = process_folder(full_folder, key)
        total_done += done
        total_skipped += skipped

    print(f"Chiffrement termine : {total_done} image(s) chiffree(s), {total_skipped} deja a jour.")


if __name__ == "__main__":
    main()
