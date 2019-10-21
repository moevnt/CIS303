from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from cryptography.fernet import Fernet

addresses = {}
clients= {}


HOST = ''
PORT = 21000
BUFFSIZE = 1024
ADDR = (HOST, PORT)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def handle_new_connection():
	"""Handles new clients to the server"""
	# Always listening
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has entered the chat." % client_address)
		client.send(bytes("You have entered the chat. Enter your name and press enter", "utf8"))
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()
#		client.send_key(bytes(cipher_suite))
		

# single client
def handle_client(client):
	"""Handles each individual client connection"""
	name = client.recv(BUFFSIZE).decode('utf8')
	welc_message = "To exit chat enter {EXIT}"
	client.send(bytes(welc_message, "utf8"))
	clients[client] = name
	
	while True:
		msg = client.recv(BUFFSIZE)
		
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
		sock.send(bytes(prefix, 'utf8') + msg)
		
		
if __name__ == "__main__":
	SERVER.listen(5)
	print("CONNECTING...")
	ACCEPT_THREAD = Thread(target=handle_new_connection())
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()
