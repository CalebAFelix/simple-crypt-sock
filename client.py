import socket
import pickle
import cripto

host = 'localhost'
port = 60000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
print('Conexão realizada com o servidor')
print('Para sair digite 0 (zero)')

server_public_key = cripto.load_public_key()
AES_key, iv = cripto.AES_key_generator()
pack = {"iv": iv, "key": AES_key}
cipher_text = cripto.encryption(pack, server_public_key)
sock.send(cipher_text)
response = sock.recv(1024)
print('Mensagem recebida: ')
print(cripto.AES_decrypt(response, AES_key, iv))

while True:
	mensagem = input('Digite a mensagem: ')
	if mensagem == '0':
		break
	cipher_text = cripto.AES_encrypt(mensagem, AES_key, iv)
	print(cipher_text)
	sock.send(cipher_text)
	response = sock.recv(1024)
	print('Mensagem recebida: ')
	print(cripto.AES_decrypt(response, AES_key, iv))
	
sock.close()
