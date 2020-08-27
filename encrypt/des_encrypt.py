import  binascii
import  base64
from pyDes import des, CBC,ECB, PAD_PKCS5,PAD_NORMAL,triple_des
from Crypto.Cipher import DES3,AES,DES

from hashlib import sha1

def sha1_enc(data):
    try:
        s = sha1()
        s.update(data.encode('utf8'))

        return s.hexdigest()
    except:
        return ''

def des_cbc_bs64(data,key,iv='01234567'):
    try:
        k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(data, padmode=PAD_PKCS5)

        return str(base64.b64encode(en),"utf-8")
    except Exception as e:
        return ''

def des_cbc_hex(data,key,iv='01234567'):
    try:

        k = des(bytes(key,encoding='utf-8'), CBC, bytes(iv,encoding='utf-8'), padmode=PAD_PKCS5)
        en = k.encrypt(bytes(data,encoding='utf-8'))

        return en.hex()
    except Exception as e:
        return ''
    # k = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)

    # return binascii.b2a_hex(en)

def des_cbc_hex_decrypt(data,key,iv='01234567'):
    try:
        data = bytes.fromhex(data)
        k = des(bytes(key,encoding='utf-8'), CBC, bytes(iv,encoding='utf-8'), pad=None, padmode=PAD_PKCS5)
        en = k.decrypt(data)

        return str(en,encoding='utf-8')
    except Exception as e:
        return ''

def des3_cbc_bs64(data,key,iv='01234567'):
    try:
        BS = DES3.block_size
        data = data + (BS - len(data) % BS) * chr(BS - len(data) % BS)
        cryptor = DES3.new(bytes(key, encoding = "utf8"), DES3.MODE_CBC, bytes(iv, encoding = "utf8"))

        x = len(data) % 8
        if x != 0:
            data = data + '\0' * (8 - x)  # 不满16，32，64位补0
        ciphertext = cryptor.encrypt(bytes(data, encoding = "utf8"))
        return base64.standard_b64encode(ciphertext).decode("utf-8")
    except Exception as e:
        return ''


def des3_cbc_hex(data,key,iv='01234567'):
    try:
        BS = DES3.block_size
        bdata = bytes(data, encoding = "utf8")
        data = data + (BS - len(bdata) % BS) * chr(BS - len(bdata) % BS)
        cryptor = DES3.new(bytes(key, encoding = "utf8"), DES3.MODE_CBC, bytes(iv, encoding = "utf8"))

        x = len(data) % 8
        # if x != 0:
        #     data = data + '\0' * (8 - x)  # 不满16，32，64位补0
        ciphertext = cryptor.encrypt(bytes(data, encoding = "utf8"))
        return ciphertext.hex()
    except Exception as e:
        return ''

def des3_cbc_bs64_decrypt(data, key,iv='01234567'):
    try:
        cryptor = DES3.new(bytes(key, encoding = "utf8"), DES3.MODE_CBC,  bytes(iv, encoding = "utf8"))
        de_text = base64.standard_b64decode(data)
        plain_text = cryptor.decrypt(de_text)
        # st = str(plain_text.decode("utf-8")).rstrip('\0')         
        # out = unpad(st)
        # return out
        #上面注释内容解密如果运行报错，就注释掉试试
        return plain_text
    except:
        return ''

def des3_cbc_hex_decrypt(data, key,iv='01234567'):
    try:
        cryptor = DES3.new(bytes(key, encoding = "utf8"), DES3.MODE_CBC,  bytes(iv, encoding = "utf8"))
        de_text = bytes.fromhex(data)
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')         
        out = st[0:-ord(st[-1])]
        return out
        #上面注释内容解密如果运行报错，就注释掉试试
        # return str(plain_text,'utf-8').rstrip('\0')
    except:
        return ''

def des_ecb_bs64(data,key,iv='01234567'):
    try:
        k = des(key, ECB, iv, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(data, padmode=PAD_PKCS5)

        return str(base64.b64encode(en),"utf-8")
    except Exception as e:
        return ''

def aes_cbc_hex(data, key,iv='0000000000000000'):
    try:
        cryptor = AES.new(bytes(key, encoding = "utf8"), AES.MODE_CBC, bytes(iv, encoding = "utf8"))  
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用  
        BS = 16  
        bdata = bytes(data, encoding = "utf8")
        # count = len(bdata)  
        # if(count % length != 0) :  
        #     add = length - (count % length)  
        # else:  
        #     add = 0  
        # data = data + ('\0' * add)  
        data = data + (BS - len(bdata) % BS) * chr(BS - len(bdata) % BS)
        ciphertext = cryptor.encrypt(bytes(data, encoding = "utf8"))  

        return ciphertext.hex()
    except:
        return ''

def aes_cbc_bs64(data, key,iv='0000000000000000'):
    try:
        cryptor = AES.new(bytes(key, encoding = "utf8"), AES.MODE_CBC, bytes(iv, encoding = "utf8"))  
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用  
        BS = 16  
        bdata = bytes(data, encoding = "utf8")
        # count = len(bdata)  
        # if(count % length != 0) :  
        #     add = length - (count % length)  
        # else:  
        #     add = 0  
        # data = data + ('\0' * add)  
        data = data + (BS - len(bdata) % BS) * '\0'
        # data = data + (BS - len(bdata) % BS) * chr(BS - len(bdata) % BS)
        ciphertext = cryptor.encrypt(bytes(data, encoding = "utf8"))  

        return base64.standard_b64encode(ciphertext).decode("utf-8")
    except:
        return ''

def aes_cbc_bs64_dec(data, key,iv='0000000000000000'):
    try:
        cryptor = AES.new(bytes(key, encoding = "utf8"), AES.MODE_CBC, bytes(iv, encoding = "utf8"))  
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用  
        # BS = 16  
        # bdata = bytes(data, encoding = "utf8")
        # count = len(bdata)  
        # if(count % length != 0) :  
        #     add = length - (count % length)  
        # else:  
        #     add = 0  
        # data = data + ('\0' * add)  
        # data = data + (BS - len(bdata) % BS) * '\0'
        # data = data + (BS - len(bdata) % BS) * chr(BS - len(bdata) % BS)
        data = base64.standard_b64decode(data)
        ciphertext = cryptor.decrypt(data)  

        return  str(ciphertext,encoding='utf-8').replace('\x00',"")
    except Exception as e:
        return ''

def aes_ecb_hex(data,keystr):
    try:
        BS = AES.block_size
        data = data + (BS - len(data) % BS) * chr(BS - len(data) % BS)
        
        # key = bytes.fromhex("050F21034F0B681D300FBCB02430ED96")
        if type(keystr) is str:
            key = bytes(keystr,encoding='utf-8')
        else:
            key = keystr
        # the length can be (16, 24, 32)
        #key='xxxxx'#32位或者0-f的数值，对应16字节
        text = bytes(data, encoding = "utf8")
        
        cipher = AES.new(key, AES.MODE_ECB)#ECB模式 
        
        encrypted = cipher.encrypt(text)
        # print (encrypted.hex())  # will be something like 'f456a6b0e54e35f2711a9fa078a76d16'

        return encrypted.hex()
        

    except Exception as e:
        # print(e)
        return ''

def aes_ecb_hex_dec(data,keystr):
    try:
        BS = AES.block_size
     
        # key = bytes.fromhex("050F21034F0B681D300FBCB02430ED96")
        if type(keystr) is str:
            key = bytes(keystr,encoding='utf-8')
        else:
            key = keystr
        # key = bytes(keystr,encoding='utf-8')
        # the length can be (16, 24, 32)
        #key='xxxxx'#32位或者0-f的数值，对应16字节
        text = bytes.fromhex('F006777365DAC9FC2C8A8FCFBC8D877C21A89D33FA298215341F834379CE0701AE37E02D3BDA7F68CDD416FC10D81E442200354F4020D3AA2F3EDFBD92CC736C512384DFF814CC140BE821DD1E6A9F9D4D5F35B9776868733D7CF8703F9DF062')
        
        cipher = AES.new(key, AES.MODE_ECB)#ECB模式 
        
        encrypted = cipher.decrypt(text)
        # print (encrypted.hex())  # will be something like 'f456a6b0e54e35f2711a9fa078a76d16'

        return base64.standard_b64encode(encrypted).decode("utf-8")
        

    except Exception as e:
        # print(e)
        return ''


def aes_ecb_base64(data,keystr):
    try:
        BS = AES.block_size
        bdata = bytes(data, encoding = "utf8")
        data = data + (BS - len(bdata) % BS) * chr(BS - len(bdata) % BS)
        
        # key = bytes.fromhex("050F21034F0B681D300FBCB02430ED96")
        if type(keystr) is str:
            key = bytes(keystr,encoding='utf-8')
        else:
            key = keystr
        # the length can be (16, 24, 32)
        #key='xxxxx'#32位或者0-f的数值，对应16字节
        text = bytes(data, encoding = "utf8")
        
        cipher = AES.new(key, AES.MODE_ECB)#ECB模式 
        
        encrypted = cipher.encrypt(text)
        # print (encrypted.hex())  # will be something like 'f456a6b0e54e35f2711a9fa078a76d16'

        return base64.standard_b64encode(encrypted).decode("utf-8")
        

    except Exception as e:
        # print(e)
        return ''

def aes_ecb_base64_dec(data,keystr):
    try:
        BS = AES.block_size
     
        # key = bytes.fromhex("050F21034F0B681D300FBCB02430ED96")
        if type(keystr) is str:
            key = bytes(keystr,encoding='utf-8')
        else:
            key = keystr
        # key = bytes(keystr,encoding='utf-8')
        # the length can be (16, 24, 32)
        #key='xxxxx'#32位或者0-f的数值，对应16字节
        text = base64.standard_b64decode(data)
        
        cipher = AES.new(key, AES.MODE_ECB)#ECB模式 
        
        encrypted = cipher.decrypt(text)
        # print (encrypted.hex())  # will be something like 'f456a6b0e54e35f2711a9fa078a76d16'
        desstr = str(encrypted,encoding='utf-8').replace('\x00',"")
        if desstr:
            k = ord(desstr[-1])
            if ord(desstr[-k]) == k:
                return desstr[:-k]
        return  str(encrypted,encoding='utf-8').replace('\x00',"")
        

    except Exception as e:
        # print(e)
        return ''
# import os
# import sys
# o_path = os.getcwd() # 返回当前工作目录

# sys.path.append(o_path) # 添加自己指定的搜索路径
# import utils.helper.convert as convert
# print(convert.get_md5("123654") )   
    
# import hashlib
# md5key = hashlib.md5('IMgzwYRjA3sZgiXl'.encode(encoding='UTF-8')).digest()
# dd=aes_ecb_hex_dec('',md5key)
# print(dd)
# from hashlib import sha1
# import re
# data=data.replace("+","_").replace("=","#").replace("/","|")
# print(aes_cbc_bs64_dec('_mCULV9DNoFPX4s|Av6aKQ##'.replace("_","+").replace("#","=").replace("|","/"),'ln20171026aesenc','ln20171026aesenc'))
# s = sha1()

# #或者s = sha.sha()

# s.update('7Gn60f9aum5eTGJY0XPPRjzile8MKzNenAIz1582435753014.2.0'.encode('utf8'))

# print(s.hexdigest())
# print(aes_ecb_hex('324165','918JCtUES8cOgs6P'))

# print(aes_cbc_bs64('101986','9100674b5bfbe8f3','9100674b5bfbe8f3'))
# text='b5720f816f50db5eb94116fd795b9f770f4af1f252692aa8c138f0e8150856db0b52b7c8000a7be699aabc4ab106f380f9e488a10e8269792beb5b46a667cdf32e20cf7649e74841dcfc49d871e100bda5b005efdca1abf6d8f95b802b6db01dc0bc44d9f75be7b899fcac6bf3674bff51429cb76f9ea21868de805bd328d64047cd9fc780fe7012269a75ff945c90b04cf9087901582657841e249032868f29f86c46b739aaee1ff7915368cf22eb4924d0e9cc0c4e120f3b632911d5496b3466ae615028b475ece984c1d2bb08e3e477f7c1c598f15b85'
# print(des3_cbc_hex_decrypt(text,'1234567`90koiuyhgtfrdews',"\0\0\0\0\0\0\0\0"))
# civ='12345678'

# text = des3_cbc_hex_decrypt('b5720f816f50db5eb94116fd795b9f770f4af1f252692aa888d7e3042ec0492bb72f9139df266d958710a43de3a564d4ddbf95c0171a471f5633040275059dab372e12f2d7fd7169252cfc3d140baa1ca225306b7979f3b16c8ab9ba291b069b27787b6853140b2b014cb74b44fd2c953e3e3c9fc65a859be848ae08a59f6dea84ad0a31236b3c45ed2c4c751d5e596fa00b27554e9f6379d596bba9f589f7980927da2ffb2fd0e3ed1f3e195dd3b030c3ff964b15fabf5d6beeb704586a69c0d841442f96ea23518664d97eb03c8c95245463f36d35bd8f','1234567`90koiuyhgtfrdews',"\0\0\0\0\0\0\0\0")
# print(text)
# aiv=''
# for i in civ:
#     aiv += chr(int(i))
# print(aiv)
# print(des_cbc_hex_decrypt('4B6972239B1AF9964D6622B5F5AAEFC3BED2030ED31E81A797B31D0A052837D407002A009FEA20CBE892F8EBBA174F02C96657FE53A46F35FC624E26CC15DAAAA6A65C7644E375DC9968A807AA27DD1C8A91D89BD40F5567DE82E09E085A39FC4ACF352CF189487D9A0D730F6A100CD7B5B6DA9E575B6C5A45AD0EB8F6DE86208B291D007CF8E91FA8FC9CF7889B4ACA692416F5C23F6282F544B51406E5F7F8A4F8DED2EA6EAA9B4224B5D2B9A6B6DBB90F6479804B26DD7681E7F025E3FD70F55ECE3796306FB6E310CA2F412FDD45A2A5438FE52C7DAF','xwtec$lg',aiv))
# print(des_cbc_hex('[{"dynamicURI":"/login","dynamicParameter":{"method":"lnNew","m":"13913757539","p":"6B61716F657536","deviceCode":"4401816558824292451_297551919283393876","verifyCode":"","openPush":"1","smsCode":"","smsCheck":""},"dynamicDataNodeName":"ln_node"}]','xwtec$lg','12345678').upper())


# a=des_cbc_hex_decrypt('4B6972239B1AF9964D6622B5F5AAEFC3BED2030ED31E81A797B31D0A052837D407002A009FEA20CBE892F8EBBA174F02C96657FE53A46F35FC624E26CC15DAAAA6A65C7644E375DC9968A807AA27DD1C8A91D89BD40F5567DE82E09E085A39FC4ACF352CF189487D9A0D730F6A100CD7B5B6DA9E575B6C5A45AD0EB8F6DE86208B291D007CF8E91FA8FC9CF7889B4ACA692416F5C23F6282F544B51406E5F7F8A4F8DED2EA6EAA9B4224B5D2B9A6B6DB261764B0F7B6FA2399232DA3641EEA5E2B6CA375B2EB770EBB59E4612FB4B9ED3BFFFCF55322748B',"xwtec$lg",'\x01\x02\x03\x04\x05\x06\x07\x08')
# print(a)

# a= aes_ecb_base64('{"companyName":"上海勃池信息技术有限公司","isFromDetail":"1"}','x89j30k23k5s2lln')

# f = open('d:\\aa.txt', 'r', encoding='utf-8') # 打开JS文件
# line = f.readline()
# htmlstr = ''
# while line:
#     htmlstr = htmlstr+line
#     line = f.readline()
# f.close()
# k = aes_ecb_base64_dec(htmlstr,'x89j30k23k5s2lln')
# print(k)