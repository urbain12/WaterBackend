from django.test import TestCase

from cryptography.fernet import Fernet
from Crypto.Cipher import AES
import  os
import hashlib
import secrets
import string


#Encrypt by pycryptodrome
# ---------------------------------
rootKey="03EE18D9C131304BB39226CCEA86A40E"
bytes_rootKey=bytes.fromhex(rootKey)
payment = '1000.00'
alphabet = string.ascii_letters + string.digits
transactionid = ''.join(secrets.choice(alphabet) for i in range(16))
print('transction id EAX:' , transactionid)
transactionid_ascii = transactionid.encode()
# print(transactionid_ascii)
transactionid_hex = transactionid_ascii.hex()
# print(transactionid_hex)
payment_ascii=payment.encode()
payment_hex=payment_ascii.hex()
mode = AES.MODE_EAX
if len(payment_hex)<32:
    for i in range(32-len(payment_hex)):
        payment_hex+='0'
payment_bytes=bytes.fromhex(payment_hex)
transactionid_bytes = bytes.fromhex(transactionid_hex)

# print(transactionid_bytes)

# print(len(payment_bytes))
# print(payment_bytes)

def encrypt(message,key):
    cipher=AES.new(key,mode)
    nonce=cipher.nonce
    ciphertext,tag=cipher.encrypt_and_digest(message.encode('ascii'))
    return ciphertext

def encrypt2(message,key):
    cipher=AES.new(key,mode)
    nonce=cipher.nonce
    ciphertext,tag=cipher.encrypt_and_digest(message)
    return ciphertext

encrypted_paymetparam=encrypt(transactionid_hex,bytes_rootKey)

encrypted_payment=encrypt2(payment_bytes,encrypted_paymetparam)


print('Encrypted key EAX :' , encrypted_payment.hex())
# ----------------------------------------------------------------------------














#encrypt with cryptography
# -----------------------------

# we will be encryting the below string.
# Rootkey = "03EE18D9C131304BB39226CCEA86A40E"
# transactionid = "57391010bc6e4f2d"
# Purchaseparma = Rootkey + ' ' + transactionid

# key = Fernet.generate_key()

# fernet = Fernet(key)

# encMessage = fernet.encrypt(Purchaseparma.encode('utf-8'))
# print("original string: ", Purchaseparma)
# print("encrypted 1 string: ", len(encMessage.hex()))

# payment = '2000.00'
# amount = fernet.encrypt(payment.encode('utf-8'))

# fullencry = encMessage + amount

# print ("full encryr : ", fullencry.hex())

# decMessage = fernet.decrypt(encMessage).decode()
# print("decrypted string: ", decMessage)







# -----------------------------------------------------------------------------
# convert to hex
#-------------------------
# bytes = 'urbain mutangana'.encode('utf-8') 

# print('Byte variable: ', bytes)
# print('Hexadecimal: ', bytes.hex())
# print('bytes: ', bytes.fromhex())





# encrypt  with hashlib
# -----------------------------

# rootKey="03EE18D9C131304BB39226CCEA86A40E"
# bytes_rootKey=bytes.fromhex(rootKey)
# # key = hashlib.sha256(bytes_rootKey).digest()
# mode = AES.MODE_CBC
# IV = 'This is an IV456'

# transactionsid = "57391010bc6e4f2d"
# amount = "2000.00"
# amountascii = amount.encode()
# print(amountascii)
# amounthex=amountascii.hex()
# print(amounthex)


# def pad_message(amounthex):
#     if len(amounthex)<32:
#         for i in range(32-len(amounthex)):
#             amounthex +='0'
#     return amounthex


# # amountbytes = bytes.fromhex(amounthex)

# cipher = AES.new(bytes_rootKey, mode, IV)

# padded_msg = pad_message(amounthex)

# # fullparam = padded_msg + transactionsid

# encryptytrans = cipher.encrypt(transactionsid,bytes_rootKey)

# encrypted_message = cipher.encrypt(padded_msg)

# final = cipher.encrypt(encryptytrans,encrypted_message)

# print("encrypted key is :", final.hex())










# AES.MODE_ECB
# -------------------

rootKey="03EE18D9C131304BB39226CCEA86A40E"
bytes_rootKey=bytes.fromhex(rootKey)
payment = '1000.00'
alphabet = string.ascii_letters + string.digits
transactionid = ''.join(secrets.choice(alphabet) for i in range(16))
print('transction id ECB:' , transactionid)
transactionid_ascii = transactionid.encode()
# print(transactionid_ascii)
transactionid_hex = transactionid_ascii.hex()
# print(transactionid_hex)
payment_ascii=payment.encode()
payment_hex=payment_ascii.hex()
mode = AES.MODE_ECB
if len(payment_hex)<32:
    for i in range(32-len(payment_hex)):
        payment_hex+='0'
payment_bytes=bytes.fromhex(payment_hex)
transactionid_bytes = bytes.fromhex(transactionid_hex)

# print(transactionid_bytes)

# print(len(payment_bytes))
# print(payment_bytes)

def encrypt(message,key):
    cipher=AES.new(key,mode)
    # nonce=cipher.nonce
    ciphertext=cipher.encrypt(message.encode('ascii'))
    return ciphertext

def encrypt2(message,key):
    cipher=AES.new(key,mode)
    # nonce=cipher.nonce
    ciphertext=cipher.encrypt(message)
    return ciphertext

encrypted_paymetparam=encrypt(transactionid_hex,bytes_rootKey)

encrypted_payment=encrypt2(payment_bytes,encrypted_paymetparam)


print('Encrypted key ECB :' , encrypted_payment.hex())