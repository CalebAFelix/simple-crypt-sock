from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util import Padding
from Crypto import Random
import pickle
import base64


def key_generator():
	key = RSA.generate(2048)

	f = open('mykey.pem','wb')
	f.write(key.exportKey('PEM'))
	f.close()
	
	private_key = key.exportKey()
	public_key = key.publickey().exportKey()
	
	keys = [private_key, public_key]
	
	return keys

def load_public_key():
	f = open('mykey.pem','r')
	key = RSA.importKey(f.read())
	f.close()
	
	public_key = key.publickey().exportKey()

	return public_key

def encryption(msg, public_key):
	msg = pickle.dumps(msg)
	key = RSA.importKey(public_key)
	cipher_rsa = PKCS1_OAEP.new(key)
	c_msg = cipher_rsa.encrypt(msg)

	return base64.b64encode(c_msg)


def decryption(msg, private_key):
	msg = base64.b64decode(msg)
	key = RSA.importKey(private_key)
	cipher_rsa = PKCS1_OAEP.new(key)
	c_msg = cipher_rsa.decrypt(msg)

	return pickle.loads(c_msg)

def AES_key_generator():
	return Random.get_random_bytes(32), Random.get_random_bytes(16)

def AES_encrypt(message, key, iv):
	cipher = AES.new(key, AES.MODE_CBC, iv=iv)
	cipher_data = cipher.encrypt(Padding.pad(pickle.dumps(message), AES.block_size))
	return cipher_data

def AES_decrypt(cipher_data, key, iv):
	cipher = AES.new(key, AES.MODE_CBC, iv=iv)
	plaintext = Padding.unpad(cipher.decrypt(cipher_data), AES.block_size)
	return pickle.loads(plaintext)

def main():

	msg = 'Essa é a mensagem!'

	keys = key_generator()

	private_key = keys[0]
	public_key = keys[1]

	enc_msg = encryption(msg, public_key)

	print('Essa é a mensagem criptografada: {}.'.format(enc_msg))

	dec_msg = decryption(enc_msg, private_key)

	print('Essa é a mensagem descriptografada: "{}"'.format(dec_msg))

	AES_key, iv = AES_key_generator()
	cipher_data = AES_encrypt('olá AES esse teste', AES_key, iv)
	print(cipher_data)
	plain_text = AES_decrypt(cipher_data, AES_key, iv)
	print(plain_text)


if __name__ == '__main__':
    main()
