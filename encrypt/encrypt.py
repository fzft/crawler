import hashlib


def md5(data):
    return hashlib.md5(data.encode()).hexdigest()


import rsa
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode, b64encode


class Encrypt_CBC():
    """
    AES_CBC 加密
    长度:16的倍数
    methods: PKCS5Padding
    """

    def __init__(self, key, iv):
        self.bs = 16
        self.key = key.encode()
        self.iv = iv.encode()

    def pad(self, text):
        # pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs) # 长度不是16的倍数则填充(填充方式：PKCS5Padding)
        add = lambda s: s + (self.bs - len(s) % self.bs) * chr(0)  # zeropadding
        signature = add(text)
        return signature

    def encrypt(self, text):
        # 加密
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        e = base64.b64encode(aes.encrypt(self.pad(text).encode()))
        return base64.b64encode(e).decode()


def md5_encrypt(text):
    """md5 加密"""
    m2 = hashlib.md5()
    m2.update(text.encode('utf-8'))
    return m2.hexdigest()


class Rsa(object):

    def __init__(self, pk):
        self.rsa_key = RSA.importKey(pk)
        # self.cipher = Cipher_PKCS1_v1_5.new(keyPub)

    def encrypt(self, msg):
        x = rsa.encrypt(msg.encode(), self.rsa_key)
        return b64encode(x).decode()


import base64
import binascii
import rsa


class EncryptDate:
    """
    AES_CBC 加密
    这里密钥的长度必须是16的倍数
    methods: PKCS 5/7
    """

    def __init__(self, key):
        self.key = key  # 初始化密钥 todo 目前只有河南省登录需要
        self.length = AES.block_size  # 初始化数据块大小
        self.aes = AES.new(self.key.encode('utf8'), AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        msg = self.aes.decrypt(res).decode("utf8")
        return self.unpad(msg)


class Rsa_bcii(object):
    """
    :param text:要加密的字符串
    :param pk:公钥
    """

    def __init__(self, text, pk):
        self.text = text
        self.pk = pk

    def str2key(self, pk):
        # 对字符串解码
        b_str = base64.b64decode(pk)
        if len(b_str) < 162:
            return False
        hex_str = ''
        # 按位转换成16进制
        for x in b_str:
            h = hex(x)[2:]
            h = h.rjust(2, '0')
            hex_str += h
        # 找到模数和指数的开头结束位置
        m_start = 29 * 2
        e_start = 159 * 2
        m_len = 128 * 2
        e_len = 3 * 2
        modulus = hex_str[m_start:m_start + m_len]
        exponent = hex_str[e_start:e_start + e_len]
        return modulus, exponent

    def rsa_encrypt(self):
        '''
        rsa加密
        :param text:
        :param pk:公钥
        :return:
        '''
        key = self.str2key(self.pk)
        modulus = int(key[0], 16)
        exponent = int(key[1], 16)
        pubkey = rsa.PublicKey(modulus, exponent)
        return binascii.b2a_hex(rsa.encrypt(self.text.encode(), pubkey)).decode()


class USE_RSA(object):
    """
    RSA 非对称加密：利用模数+指数
    """

    def __init__(self, puk, ):
        self.puk = puk

    def str2key(self, s):
        """
        将传过来的puk进行base64处理
        :param s: self.puk
        :return: 模数，指数
        """
        # 对字符串解码
        b_str = base64.b64decode(s)
        # print(b_str)
        # print(len(b_str))
        if len(b_str) < 162:
            return False
        hex_str = ''
        # 按位转换成16进制
        for x in b_str:
            h = hex(x)[2:]
            h = h.rjust(2, '0')
            hex_str += h
        # 找到模数和指数的开头结束位置
        m_start = 29 * 2
        e_start = 159 * 2
        m_len = 128 * 2
        e_len = 3 * 2
        modulus = hex_str[m_start:m_start + m_len]
        exponent = hex_str[e_start:e_start + e_len]
        return modulus, exponent

    def rsaEncrypt(self, message):
        """ 加密函数
        :param message: 加密的字符串
        :return:
        """
        key = self.str2key(self.puk)
        modulus = int(key[0], 16)
        exponent = int(key[1], 16)
        rsa_pubkey = rsa.PublicKey(modulus, exponent)
        crypto = rsa.encrypt(message.encode(), rsa_pubkey)
        return base64.b64encode(crypto)


import urllib

if __name__ == '__main__':
    username = urllib.parse.quote(EncryptDate(key='bf58abc811f38cda').encrypt('13228520322'))
    print(username)
