from django.test import TestCase

from cryptography.fernet import Fernet



# from Crypto.Cipher import AES
# from secrets import token_bytes
#Encrypt by pycryptodrome
# ---------------------------------
# key = token_bytes(16)
# def encrypt(msg):
#     cipher = AES.new(key, AES.MODE_EAX)
#     nonce = cipher.nonce
#     ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
#     return nonce, ciphertext, tag

# def decrypt(nonce, ciphertext, tag):
#     cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
#     plaintext = cipher.decrypt(ciphertext)
#     try:
#         cipher.verify(tag)
#         return plaintext.decode('ascii')
#     except:
#         return False
# nonce, ciphertext, tag = encrypt(input("enter message: "))
# plaintext = decrypt(nonce, ciphertext, tag)
# print(f'cipher text: {ciphertext}')
# if not plaintext:
#     print('Message is not good')
# else: 
#     print(f'Plain text: {plaintext}')
# ----------------------------------------------------------------------------


#encrypt with cryptography
# -----------------------------

# we will be encryting the below string.
Rootkey = "03EE18D9C131304BB39226CCEA86A40E"
transactionid = "57391010bc6e4f2d"
Purchaseparma = Rootkey + ' ' + transactionid

key = Fernet.generate_key()

fernet = Fernet(key)

encMessage = fernet.encrypt(Purchaseparma.encode('utf-8'))
print("original string: ", Purchaseparma)
byton= encMessage[:16]
print("encrypted 1 string: ", byton.hex())

payment = '2000.00'
amount = fernet.encrypt(payment.encode('utf-8'))

fullencry = encMessage + amount

print ("full encryr : ", fullencry.hex())

# decMessage = fernet.decrypt(encMessage).decode()
# print("decrypted string: ", decMessage)





# -----------------------------------------------------------------------------
# convert to hex
#-------------------------
# bytes = 'urbain mutangana'.encode('utf-8') 

# print('Byte variable: ', bytes)
# print('Hexadecimal: ', bytes.hex())