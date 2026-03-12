from cryptography.fernet import Fernet

# fixed shared key
key = b'YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWE='

cipher = Fernet(key)

def encrypt(data):
    return cipher.encrypt(data.encode())

def decrypt(data):
    return cipher.decrypt(data).decode()