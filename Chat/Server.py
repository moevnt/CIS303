from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

addresses = {}
clients = {}
foreign_keys = {}


HOST = ''
PORT = 21000
BUFFSIZE = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
public_key = private_key.public_key()


def handle_new_connection():
	"""Handles new clients to the server"""
	# Always listening
	while True:
		client, client_address = SERVER.accept()
		foreign_keys[client] = client.recv
		client.send(public_key)
		print("%s:%s has entered the chat." % client_address)
		client.send(bytes("You have entered the chat. Enter your name and press enter", "utf8"))
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()


# single client
def handle_client(client):
	"""Handles each individual client connection"""
	name = client.recv(BUFFSIZE).decode('utf8')
	welc_message = "To exit chat enter {EXIT}"
	client.send(bytes(welc_message, "utf8"))
	clients[client] = name
	
	while True:
		msg = client.recv(BUFFSIZE)
		msg = private_key.decrypt(msg)
		
		if msg != bytes("{EXIT}", "utf8"):
			broadcast(msg, name + ": ")
		else:
			client.send(bytes("{EXIT}", "utf8"))
			client.close()
			del clients[client]
			break
			
	
def broadcast(msg, prefix=""):
	"""Sends messages to the chat"""

	for sock in clients:
		msg = clients[sock].encrypt(msg)
		sock.send(bytes(prefix, 'utf8') + msg)
		
		
if __name__ == "__main__":
	SERVER.listen(5)
	print("CONNECTING...")
	ACCEPT_THREAD = Thread(target=handle_new_connection())
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()
