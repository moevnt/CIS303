from cryptography.fernet import Fernet
message = 'test'
text = bytes(message, 'utf8')
key = Fernet.generate_key()
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(text)
print(cipher_text.decode())
plain_text = cipher_suite.decrypt(cipher_text)
print(plain_text)
