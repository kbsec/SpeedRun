


from os import urandom
import hashlib


def xor_bytes(a,b):
    return bytes([i ^ j for i, j in zip(a, b)])


class rc4:
    # TODO: Add IV.
    def __init__(self, key, drop_N=False):
        self.__key = key
        self.key_scheduel()
        self.drop_N = drop_N
        # Generator for byte stream 
        self.stream_generator = self._generate_stream()
        
    
    def key_scheduel(self):
        S = [i for i in range(256)]
        j = 0
        for i in range(0,256):
            # (bytes_object) & 0xff  is the same thing as x mod 256
            j = (j + S[i] + self.__key[i % len(self.__key)]) & 0xff
            S[i], S[j] = S[j], S[i]
        self.__S = S
    
    def  _generate_stream(self):
        # Discard bytes 
        drop_n = self.drop_N
        S = self.__S.copy()
        i= j = 0
        while True:
            i = (i + 1) & 0xff
            j = (j + S[i]) & 0xff
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j] ) & 0xff]
            if drop_n:
                # drop the firt N bytes
                drop_n -=1
                continue
            yield K
            
    def crypt(self, data):
        # if We haven't alre
        assert(isinstance(data, (bytes, bytearray)))
        # Calls the generator. 
        # Note this leaks the size of the message. 
        return xor_bytes(data, self.stream_generator)
        

class HMAC:
    # Note, hash_f needs to be from hashlib
    # If you use Keccak,the inner + outer hash are not needed. 
    def __init__(self, key, hash_f):
        self.block_size = hash_f().block_size
        self.digest_size = hash_f().digest_size
        self.hash_f = hash_f
        if len(key) > self.block_size:
            # if the key is larger than then the block size, hash it
            self.__key = self.hash_f.update(key).digest()   
            assert len(self.__key) == self.digest_size
        else:
            # pad with zeos
            pad = bytes( self.block_size - len(key) )
            self.__key = key + pad
            assert len(self.__key) == self.block_size
        self.__inner_pad  =  xor_bytes(self.__key , (bytes([0x36]) * self.block_size))
        self.__outter_pad = xor_bytes(self.__key , (bytes([0x5c]) * self.block_size))
        
        
    def hash_bytes(self, data):
        m = self.hash_f()
        m.update(data)
        return m.digest()
    
    def gen_hmac(self, data):
        return  self.hash_bytes( self.__outter_pad + self.hash_bytes(self.__inner_pad + data))
    
    def verify_mac(self, mac, data):
        return self.gen_hmac(data) == mac


def test_rc4():
    key, plaintext, ciphertext = ('Key', 'Plaintext', bytes.fromhex("BBF316E8D940AF0AD3"))
    rc4_0 = rc4(key.encode())
    return rc4_0.crypt(plaintext.encode()) == ciphertext
        
test_rc4()

def test_hmac():
    hmac_sha256 = HMAC("key".encode(), hashlib.sha256 ).gen_hmac("The quick brown fox jumps over the lazy dog".encode()) 
    return hmac_sha256 == bytes.fromhex("f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8")

def test():
    if test_rc4() + test_hmac() == 2:
        print("[+] All tests passed.")
    print("Failed...")



def example():
    # securely generate a secret key for the MAC as well as the cipher
    secret_cipher_key = urandom(16)
    secret_hmac_key = urandom(16)
    # Encrypt then Mac
    message = "Attack at dawn!".encode()
    cipher_0 = rc4(secret_cipher_key)
    ct = cipher_0.crypt(message)
    hmac_0 = HMAC( secret_hmac_key, hashlib.sha3_256)
    # Encrypt then mac!
    mac = hmac_0.gen_hmac(ct)
    # See if it verifies
    verified = HMAC( secret_hmac_key, hashlib.sha3_256).verify_mac(mac, ct)
    if verified:
        print("[+] Verified ")
    
    cipher_1 = rc4(secret_cipher_key)
    pt = cipher_1.crypt(ct)
    print("[+] Plaintedt:", pt.decode())