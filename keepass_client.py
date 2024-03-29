#!/usr/bin/env python2
from base64 import b64decode, b64encode
import os
import requests
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from oracle import Oracle
from ipdb import set_trace
from time import sleep

# kepass settings
key = "F/zUlQQjdvhVBACpAZD3+g=="
id = "test mit cli tools"


class AESCipher(object):

    def __init__(self, key, iv): 
        self.bs = AES.block_size #16
        self.key = b64decode(key)
        self.iv = iv

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        cipher_text = cipher.encrypt(self._pad(raw))
        return b64encode(cipher_text)

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plain_padded = cipher.decrypt(enc)
        return self._unpad(plain_padded)

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[-1])]

class Keepass(object):

    def __init__(self, key, id):
        self.session = requests.session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.endpoint = "http://localhost:19455"
        self.nonce = os.urandom(16)
        self.crypto = AESCipher(key, self.nonce)
        self.key = key
        self.id = id


    def decrypt_login(self, iv, entries):
    # entries: list of dict with Login, Name, Uid, Password
        decryptor = AESCipher(self.key, b64decode(iv))
        logins = []
        for entry in entries:
            e = {}
            e['Uuid'] = decryptor.decrypt(entry['Uuid'])
            e['Name'] = decryptor.decrypt(entry['Name'])
            e['Username'] = decryptor.decrypt(entry['Login'])
            e['Password'] = decryptor.decrypt(entry['Password'])
            logins.append(e)
        return logins


    def get_login(self, url):
        data = {'RequestType': 'get-logins',
                'Nonce': b64encode(self.nonce),
                'Verifier': self.crypto.encrypt(b64encode(self.nonce)),
                'Url': self.crypto.encrypt(url),
                'Id': self.id,
                'TriggerUnlock': False,

        }
        response = self.session.post(self.endpoint, json=data)
        #print(response.text)
#        if response.status_code == 200:
#            raise ValidPaddingException()
        json = response.json()
        return self.decrypt_login(json['Nonce'], json['Entries'])


def test_encryption():
    # decrypt verifier and compare it with nonce to check the encryption
    nonce = "6oaxpiYfXJNpBxajKuNuOQ=="
    verifier = "sUxfFXgvx2QI5B0U38Ux5IaHskctP8BBdaKkpzy1eOY="
    t = AESCipher("F/zUlQQjdvhVBACpAZD3+g==", b64decode(nonce))
    nonce_b64 = t.decrypt(verifier)
    assert nonce_b64 == nonce
    verifier_b64 = t.encrypt(nonce)
    assert verifier_b64 == verifier


def keepass_client():
    # returns all passwords in keepass for a specific url
    k = Keepass(key, id)
    url = "www.heise.de"
    logins = k.get_login(url)
    print("Passwords for: %s\n%s" % (url, logins))

test_encryption()
if __name__ == '__main__':
    keepass_client()
