from Crypto.Cipher import AES

# for debugging
from binascii import hexlify, unhexlify
from ipdb import set_trace

BLOCKSIZE = None

class AESCipher(object):

    def __init__(self, key, iv, block_size):
        global BLOCKSIZE
        self.key = key
        self.iv = iv
        self.bs = block_size
        BLOCKSIZE = block_size


    def encrypt(self, raw):
        # raw:    string or bytes to encrypt
        # return: ciphertext in bytes
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        cipher_text = cipher.encrypt(AESCipher.pad(raw))
        print("Plaintext      %s %s " % (hexlify(raw)[:32], hexlify(raw)[32:]))
        print("Encrypted      %s %s " % (hexlify(cipher_text)[:32], hexlify(cipher_text)[32:]))
        return cipher_text


    def decrypt(self, enc):
        # enc:    ciphertext in bytes
        # return: plaintext as string
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plain_padded = cipher.decrypt(enc)
        print("Encrypted      %s %s " % (hexlify(enc)[:32], hexlify(enc)[32:]))
        print("Decrypted      %s %s " % (hexlify(plain_padded)[:32], hexlify(plain_padded)[32:]))
        plain = AESCipher.unpad(plain_padded)
        return plain

    @staticmethod
    def pad(plaintext):
        return plaintext + (BLOCKSIZE - len(plaintext) % BLOCKSIZE) * \
               chr(BLOCKSIZE - len(plaintext) % BLOCKSIZE)

    @staticmethod
    def unpad(plaintext):
        last_byte = ord(plaintext[-1])
        if last_byte > BLOCKSIZE or last_byte == 0:
            raise Exception("Padding Exception")
        for i in range(last_byte):
            if ord(plaintext[-i-1]) != last_byte:
                raise Exception("Padding Exception")
        return plaintext [:-last_byte]
