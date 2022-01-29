import socket
import pickle
import threading
import cripto

host = 'localhost'
port = 60000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen()
keys = cripto.key_generator()

def handle(connection, address): 
	data_received = connection.recv(1024)
	pack = cripto.decryption(data_received, keys[0])
	print(pack)
	AES_iv = pack['iv']
	AES_key = pack['key']
	connection.send(cripto.AES_encrypt(b'AES aceita', AES_key, AES_iv))
	while True:
		try:
			received_message = connection.recv(1024)
			print(received_message)
			message = cripto.AES_decrypt(received_message, AES_key, AES_iv)
			print('Mensagem recebida: ' + message)
			connection.send(cripto.AES_encrypt(b'OK', AES_key, AES_iv))
		except:
			print('Falha na comunicação')
			print(f"Fechando conexão do host {address[0]} porta {address[1]}")
			connection.close()
			break

print(f"SERVER STARTED\nAguardando conexões...")
while True:
	connection, address = sock.accept()
	print(f"Conexão estabelecida com o host {address[0]} na porta {address[1]}")
	
	thread = threading.Thread(target=handle, args=(connection, address))
	thread.start()

