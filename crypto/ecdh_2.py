# -*- coding: utf-8 -*-
# @Time : 2022/5/22 15:13
# @Author : Hanhaha
import base64
import binascii
from binascii import unhexlify
import codecs
import zlib
from urllib import parse

from ecdsa import ECDH, SECP256k1


# ecdh = ECDH(curve=SECP256k1)

def get_PK(ecdh):
    ecdh.generate_private_key()
    local_public_key = ecdh.get_public_key()
    print(local_public_key.to_string("compressed").hex())
    return [ecdh, local_public_key.to_string("compressed").hex()]


#send `local_public_key` to remote party and receive `remote_public_key` from remote party
def get_secret(ecdh,remote_public_key ):
    # remote_public_key = "021debb5ca31ad676a24ea8580fd42f6fcd10eb46680b78f5474a61791b513dc0e"
    # ecdh.load_received_public_key_pem(remote_public_key)
    ecdh.load_received_public_key_bytes(bytes.fromhex(remote_public_key))
    secret = ecdh.generate_sharedsecret_bytes()
    return [ecdh, secret.hex()]

