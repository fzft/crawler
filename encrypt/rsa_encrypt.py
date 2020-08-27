import rsa
import  base64
import binascii
from  Crypto.PublicKey import  RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5,PKCS1_OAEP as nopadding
import Crypto.Cipher.PKCS1_OAEP
#
# class rsa_encrypt():
#     def __init__(self, pk):
#         self.rsa_key = RSA.importKey(pk)



def rsa_pck1padding_hex(data,key):

    key1=base64.b64decode(key)
    rsaKey = RSA.importKey(key1)


    #RSA/ECB/PKCS1Padding
    cipher = Cipher_pkcs1_v1_5.new(rsaKey)
    temp = cipher.encrypt(bytes(data, encoding='utf-8'))

    return  str(binascii.b2a_hex(temp),"utf-8")


def rsa_pck1padding_hexb64(data,key):

    key1=base64.b64decode(key)
    rsaKey = RSA.importKey(key1)


    #RSA/ECB/PKCS1Padding
    cipher = Cipher_pkcs1_v1_5.new(rsaKey)
    temp = cipher.encrypt(bytes(data, encoding='utf-8'))

    return  str(base64.b64encode(binascii.b2a_hex(temp)),"utf-8")

def rsa_pck1padding_bs64(data,key):

    key1=base64.b64decode(key)
    rsaKey = RSA.importKey(key1)


    #RSA/ECB/PKCS1Padding
    cipher = Cipher_pkcs1_v1_5.new(rsaKey)
    temp = cipher.encrypt(bytes(data, encoding='utf-8'))

    return  str(base64.b64encode(temp),"utf-8")

def rsa_base64(data,key):
    try:
        key1=base64.b64decode(key)
    
        rsaKey = RSA.importKey(key1)
        
        cipher = no5_Cipher(rsaKey, b'\0')
        cipher_text = bytes(data, encoding='utf-8')
        cipher_text_rsa = cipher.encrypt(cipher_text)

        return str(base64.b64encode(cipher_text_rsa),"utf-8")
       
    except Exception as e:
        print(e)


def rsa_byte(data,key):
    try:
        key1=base64.b64decode(key)
    
        rsaKey = RSA.importKey(key1)
        
        cipher = no5_Cipher(rsaKey, b'\0')
        cipher_text = bytes(data, encoding='utf-8')
        cipher_text_rsa = cipher.encrypt(cipher_text)

        return cipher_text_rsa
       
    except Exception as e:
        print(e)

def rsa_base64des(data,key):
    try:
        key1=base64.b64decode(key)
    
        rsaKey = RSA.importKey(key1)
        
        cipher = no5_Cipher(rsaKey, b'\0')
        cipher_text = base64.b64decode(data)
        cipher_text_rsa = cipher.decrypt(cipher_text,'error')

        return str(cipher_text_rsa,encoding='utf-8').replace('\x00','')
       
    except Exception as e:
        print(e)


def rsa_hex(data,key,a):
    try:
        from Crypto.Math.Numbers import Integer
        # key1=base64.b64decode(key)
        modulus = int('a5aeb8c636ef1fda5a7a17a2819e51e1ea6e0cceb24b95574ae026536243524f322807df2531a42139389674545f4c596db162f6e6bbb26498baab074c036777', 16)
        exponent = int('10001', 16)
        # rsa_pubkey = rsa.PublicKey(modulus, exponent)
        # rsaKey = RSA.importKey(key1)
        rsaKey = RSA.construct([Integer(modulus),Integer(exponent)])
        # rsaKey.e = exponent
        # rsaKey.n = modulus
        cipher = no5_Cipher(rsaKey,a)
        cipher_text = bytes(data, encoding='utf-8')
        cipher_text_rsa = cipher.encrypt(cipher_text)
        k=cipher_text_rsa.hex()
        if k == "088c7040cb4833238dc99e0c4650e446135484380951f4b4f31a5f9d93f1d330d9f6e3efdb02cbfdc10c0ae19c6706aed1b883522f183fc58830e8b77879417f":
            print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        return cipher_text_rsa.hex()
       
    except Exception as e:
        print(e)
       


# -*- coding: utf-8 -*-
#
#  Cipher/PKCS1-v1_5.py : PKCS#1 v1.5
#
# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# No rights are reserved.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================



from Crypto.Util.number import ceil_div, bytes_to_long, long_to_bytes
from Crypto.Util.py3compat import bord, _copy_bytes
import Crypto.Util.number
from Crypto import Random

class no5_Cipher:
    """This cipher can perform PKCS#1 v1.5 RSA encryption or decryption.
    Do not instantiate directly. Use :func:`Crypto.Cipher.PKCS1_v1_5.new` instead."""

    def __init__(self, key, randfunc):
        """Initialize this PKCS#1 v1.5 cipher object.

        :Parameters:
         key : an RSA key object
          If a private half is given, both encryption and decryption are possible.
          If a public half is given, only encryption is possible.
         randfunc : callable
          Function that returns random bytes.
        """

        self._key = key
        self._randfunc = randfunc

    def can_encrypt(self):
        """Return True if this cipher object can be used for encryption."""
        return self._key.can_encrypt()

    def can_decrypt(self):
        """Return True if this cipher object can be used for decryption."""
        return self._key.can_decrypt()

    def encrypt(self, message):
        """Produce the PKCS#1 v1.5 encryption of a message.

        This function is named ``RSAES-PKCS1-V1_5-ENCRYPT``, and it is specified in
        `section 7.2.1 of RFC8017
        <https://tools.ietf.org/html/rfc8017#page-28>`_.

        :param message:
            The message to encrypt, also known as plaintext. It can be of
            variable length, but not longer than the RSA modulus (in bytes) minus 11.
        :type message: bytes/bytearray/memoryview

        :Returns: A byte string, the ciphertext in which the message is encrypted.
            It is as long as the RSA modulus (in bytes).

        :Raises ValueError:
            If the RSA key length is not sufficiently long to deal with the given
            message.
        """

        # See 7.2.1 in RFC8017
        modBits = Crypto.Util.number.size(self._key.n)
        k = ceil_div(modBits,8) # Convert from bits to bytes
        mLen = len(message)

        # Step 1
        if mLen > k - 11:
            raise ValueError("Plaintext is too long.")
        # Step 2a
        ps = []
        while len(ps) != k - mLen - 3:
            # new_byte=b'\x00'
            new_byte =self._randfunc
            # if bord(new_byte[0]) == 0x00:
            #     continue
            ps.append(new_byte)
        ps = b"".join(ps)
        assert(len(ps) == k - mLen - 3)
        # Step 2b
        em = b'\x00\x00' + ps + b'\x00' + _copy_bytes(None, None, message)
        # Step 3a (OS2IP)
        em_int = bytes_to_long(em)
        # Step 3b (RSAEP)
        m_int = self._key._encrypt(em_int)
        # Step 3c (I2OSP)
        c = long_to_bytes(m_int, k)
        return c

    def decrypt(self, ciphertext, sentinel):
        """Decrypt a PKCS#1 v1.5 ciphertext.

        This function is named ``RSAES-PKCS1-V1_5-DECRYPT``, and is specified in
        `section 7.2.2 of RFC8017
        <https://tools.ietf.org/html/rfc8017#page-29>`_.

        :param ciphertext:
            The ciphertext that contains the message to recover.
        :type ciphertext: bytes/bytearray/memoryview

        :param sentinel:
            The object to return whenever an error is detected.
        :type sentinel: any type

        :Returns: A byte string. It is either the original message or the ``sentinel`` (in case of an error).

        :Raises ValueError:
            If the ciphertext length is incorrect
        :Raises TypeError:
            If the RSA key has no private half (i.e. it cannot be used for
            decyption).

        .. warning::
            You should **never** let the party who submitted the ciphertext know that
            this function returned the ``sentinel`` value.
            Armed with such knowledge (for a fair amount of carefully crafted but invalid ciphertexts),
            an attacker is able to recontruct the plaintext of any other encryption that were carried out
            with the same RSA public key (see `Bleichenbacher's`__ attack).

            In general, it should not be possible for the other party to distinguish
            whether processing at the server side failed because the value returned
            was a ``sentinel`` as opposed to a random, invalid message.

            In fact, the second option is not that unlikely: encryption done according to PKCS#1 v1.5
            embeds no good integrity check. There is roughly one chance
            in 2\ :sup:`16` for a random ciphertext to be returned as a valid message
            (although random looking).

            It is therefore advisabled to:

            1. Select as ``sentinel`` a value that resembles a plausable random, invalid message.
            2. Not report back an error as soon as you detect a ``sentinel`` value.
               Put differently, you should not explicitly check if the returned value is the ``sentinel`` or not.
            3. Cover all possible errors with a single, generic error indicator.
            4. Embed into the definition of ``message`` (at the protocol level) a digest (e.g. ``SHA-1``).
               It is recommended for it to be the rightmost part ``message``.
            5. Where possible, monitor the number of errors due to ciphertexts originating from the same party,
               and slow down the rate of the requests from such party (or even blacklist it altogether).

            **If you are designing a new protocol, consider using the more robust PKCS#1 OAEP.**

            .. __: http://www.bell-labs.com/user/bleichen/papers/pkcs.ps

        """

        # See 7.2.1 in RFC3447
        modBits = Crypto.Util.number.size(self._key.n)
        k = ceil_div(modBits,8) # Convert from bits to bytes

        # Step 1
        if len(ciphertext) != k:
            raise ValueError("Ciphertext with incorrect length.")
        # Step 2a (O2SIP)
        ct_int = bytes_to_long(ciphertext)
        # Step 2b (RSADP)
        m_int = self._key._decrypt(ct_int)
        # Complete step 2c (I2OSP)
        em = long_to_bytes(m_int, k)
        # Step 3
        sep = em.find(b'\x00', 2)
        # if  not em.startswith(b'\x00\x02') or sep < 10:
        #     return sentinel
        # Step 4
        return em[sep + 1:]

# print(1 & 255)
# for i in range(128):
#     a = bytes.fromhex((hex(i)[2:]).rjust(2,'0'))
#     # print(bytes(a,encoding='utf-8'))
#     rsa_hex('147258','MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKWuuMY27x/aWnoXooGeUeHqbgzOskuVV0rgJlNiQ1JPMigH3yUxpCE5OJZ0VF9MWW2xYvbmu7JkmLqrB0wDZ3cCAwEAAQ==',a)
# print("000")
# print(rsa_hex('147258','MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKWuuMY27x/aWnoXooGeUeHqbgzOskuVV0rgJlNiQ1JPMigH3yUxpCE5OJZ0VF9MWW2xYvbmu7JkmLqrB0wDZ3cCAwEAAQ=='))

# a= rsa_base64des('hqHi4g9IHtl/OvxWYq5O/Q4mihKn9tYRyihsAVYsXDnYqF/P0UZTDveIhqpvBugquj7Xl8vAc7ih\n87Z0dbXiiA==','MIIBVgIBADANBgkqhkiG9w0BAQEFAASCAUAwggE8AgEAAkEAsBe3McQahGJmM3a2boYX8Jd5HcjP3ZwawHdrqn05qT05PYup3sWGLMcsr64ipiBLl4Bi5NKZKsBovMSRlo5rWwIDAQABAkEAmIoCrH6GxfUDOUN1pupL5KMiTNW+kub+GYmZX5eYkmu7r+luxv0Qx8xj6onZmZZORq3hAUhhGpK1gayP4UhQmQIhAP6lx/lrPQQ8AFmDWkGAbUJtiM0sZKS4B7w/z7+1uWutAiEAsQchk0GDBChRRs59P2Gu3qnWgXa2jbdpvxHDrvsrlCcCIQCMxA/bbNB5+sEmulm2Q8wiIHKzGIs6ExETmyK4kzhAsQIgdZlXJIuQjWJ7G55wdXpewGvyo25JNztwdA1JASS5fmECIQDR0yiSF5nZY1enMlfcecGutVd+DgdstZaYi6oDrZVXJA==')
# print(a)