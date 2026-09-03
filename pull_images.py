# -*- coding: utf-8 -*-
"""
vncrypt - PULL
Pour chaque PNG chiffre des dossiers listes dans crypt_targets.txt,
dechiffre l'original embarque et remplace la silhouette par l'image
reelle. Idempotent.
"""

import os
import sys
import base64
from PIL import Image
from Crypto.Cipher import AES

KEY_FILE = "vncrypt_key.bin"
TARGETS_FILE = "crypt_targets.txt"
MARKER_KEY = "vncrypt"
DATA_KEY = "vndata"


def load_key(key_path):
    if not os.path.exists(key_path):
        print(f"[!] Cle introuvable : {key_path}")
        print("    Copie ta cle depuis ta machine de confiance avant de faire un PULL.")
        sys.exit(1)
    with open(key_path, "r", encoding="ascii") as f:
        return base64.b64decode(f.read().strip())


def decrypt_bytes(blob, key):
    nonce, tag, ciphertext = blob[:12], blob[12:28], blob[28:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


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


def process_folder(full_folder, key):
    done, skipped, failed = 0, 0, 0
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

            if img.info.get(MARKER_KEY) != "1":
                skipped += 1
                continue

            b64 = img.info.get(DATA_KEY)
            if not b64:
                print(f"[!] Donnees manquantes, ignore : {fpath}")
                failed += 1
                continue

            try:
                enc = base64.b64decode(b64)
                original = decrypt_bytes(enc, key)
            except Exception as e:
                print(f"[!] Echec dechiffrement {fpath}: {e}")
                failed += 1
                continue

            with open(fpath, "wb") as f:
                f.write(original)
            print(f"[OK] Dechiffre : {os.path.relpath(fpath, full_folder)}")
            done += 1
    return done, skipped, failed


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    key = load_key(os.path.join(root, KEY_FILE))
    folders = get_target_folders(root)

    total_done, total_skipped, total_failed = 0, 0, 0
    for folder in folders:
        full_folder = os.path.join(root, folder)
        if not os.path.isdir(full_folder):
            print(f"[!] Dossier introuvable, ignore : {full_folder}")
            continue
        done, skipped, failed = process_folder(full_folder, key)
        total_done += done
        total_skipped += skipped
        total_failed += failed

    print(f"Dechiffrement termine : {total_done} image(s), {total_skipped} deja en clair, {total_failed} echec(s).")


if __name__ == "__main__":
    main()
