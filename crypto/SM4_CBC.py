# -*- coding: utf-8 -*-
# @Time : 2022/4/9 11:42
# @Author : Hanhaha

from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT


def sm4_cbc_en(iv,key,msg):# 传入的都是bytes
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    encrypt_value = crypt_sm4.crypt_cbc(iv, msg)  # bytes
    return encrypt_value    # 返回bytes

def sm4_cbc_de(iv,key,de_msg):# 传入的都是bytes
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_DECRYPT)
    decrypt_value = crypt_sm4.crypt_cbc(iv, de_msg)    # bytes
    return decrypt_value.decode("UTF-8")    # 返回的是str

