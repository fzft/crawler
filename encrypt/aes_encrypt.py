import  base64
from Crypto.Cipher import AES
from pyDes import des, CBC,ECB, PAD_PKCS5,PAD_NORMAL,triple_des
from binascii import b2a_hex, a2b_hex

class AESCipher:
    def __init__(self, key):
        self.key = key[0:16] #只截取16位
        self.iv = "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0" # 16位字符，用来填充缺失内容，可固定值也可随机字符串，具体选择看需求。
    def __pad(self, text):
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt(self, raw):
        """加密"""
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(raw.encode(encoding='utf-8')).hex()

    def decrypt(self, enc):
        """解密"""
        enc = bytes.fromhex(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv )
        return self.__unpad(cipher.decrypt(enc).decode(encoding='utf-8'))

def aesEncrypt(key,iv,raw):
    aes=AESCipher(key)
    aes.iv=iv
    r=aes.encrypt(raw)
    return r

def aesDecrypt(key,iv,raw):
    aes=AESCipher(key)
    aes.iv=iv
    r=aes.decrypt(raw)
    return r