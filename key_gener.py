from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)