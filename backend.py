#!/usr/bin/env python2
from flask import Flask, request, redirect
from binascii import hexlify, unhexlify
from base64 import b64decode, b64encode
import json
from crypto import AESCipher

app = Flask(__name__)

# test if encryption/decryption works. ciphertext will be used as challenge
key = "very strong pw!!"
iv = "thisshouldberndm"
message = "Die ist ein beta Test"
aes = AESCipher(key, iv, 16)
cipher_text = aes.encrypt(message)
assert message == aes.decrypt(cipher_text)


@app.route("/")
def index():
    return r"Please go to /cipher to get the cipher text. The content is IV\nCIPHERTEXT"


@app.route("/cipher")
def cipher():
    # returns the ciphertext/secret you want to decrypt
    # format of IV and ciphertext is hex string seperated with a new line
    return "%s\n%s" % (hexlify(iv), hexlify(cipher_text))


@app.route("/decrypt", methods=['POST'])
def decrypt():
    # decrypts messages from the client
    # cipher_text: ciphertext to decrypt in hex string format
    # return:      plaintext string (or bytes if plaintext were bytes/something goes wrong
    json = request.get_json()
    cipher = json['cipher_text']
    plain = aes.decrypt(unhexlify(cipher))
    return plain


if __name__ == '__main__':
    app.run(debug=True)
