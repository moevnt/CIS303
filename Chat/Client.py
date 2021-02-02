import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def receive():
	"""Receives messages from SERVER"""
	while True:
		try:
			msg = client_socket.recv(BUFFSIZE).decode('utf8')
			msg = private_key.decrypt(msg)
			msg = foreign_key.decode().decrypt(msg)
			msg_list.insert(tkinter.END, msg)
		except OSError:
			break


def send(event=None):
	"""Sends messages"""
	msg = my_msg.get()
	my_msg.set("")
	
	msg = msg.encode('utf8')
	msg = public_key.encrypt(msg, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(), label= None))

	client_socket.send(msg)
	if msg =="{EXIT}":
		client_socket.close()
		tk.quit()


def on_closing(event=None):
	"""called when window is closed"""
	my_msg.set('{EXIT}')
	send()
	
	
tk = tkinter.Tk()
tk.title("Chat Room")

frame = tkinter.Frame(tk)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(frame)

msg_list = tkinter.Listbox(frame, height=20, width=50)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
frame.pack()

entry_field = tkinter.Entry(tk, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(tk, text='SEND', command=send)
send_button.pack()

tk.protocol("WM_DELETE_WINDOW", on_closing)


HOST = input('Enter Host address: ')
PORT = input('Enter Port: ')
if not PORT:
	PORT = 21000
else:
	PORT = int(PORT)

BUFFSIZE = 1024
ADDRRESS = (HOST, PORT)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048,backend=default_backend())
public_key = private_key.public_key()

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDRRESS)
client_socket.send(private_key.public_key())
foreign_key = client_socket.recv(BUFFSIZE)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
