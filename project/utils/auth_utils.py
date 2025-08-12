import pbkdf2
from Crypto.Cipher import AES 
from Crypto import Random
import base64
import hashlib
from project.component.loggings import set_up_logging
from project.config.config import ENV
import random, string




logger = set_up_logging()

class AESCipher:
   
    def __init__(self, salt, pin): 
        # key = pbkdf2.PBKDF2(PIN_ENCRYPTION_SECRET, salt).read(32) # 256-bit key
        key = pbkdf2.PBKDF2(str(pin), salt).read(32) # 256-bit key
        self.bs = AES.block_size
        self.key = hashlib.sha256(key).digest() 

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encoded = base64.b64encode(iv + cipher.encrypt(raw.encode()))
        return encoded
        # return base64.b64encode(iv + cipher.encrypt(raw))
        
    def decrypt(self, enc):
        try:
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        except Exception as e:
            logger.critical("Error in decrypting pin: " + str(e))
            return None

    def _pad(self, s):
       
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]



def generate_email_otp():
    s_num_email = ''
    email_otp = s_num_email.join(random.choices(string.digits, k=6))
    if ENV=="dev":
        email_otp = '123456'
    return email_otp
