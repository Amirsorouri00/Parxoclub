import base64, strgen
from Crypto.Cipher import AES

def Encrypt(prefix, data):
    encryptionAES = AES.new(b"#DN45C&?5Rjhzgar", AES.MODE_CBC, b"a7ePE8w4yN9y=!ZF")
    pkey_data = "{}_{}_".format(prefix, data)
    rnd_len = 16 + (16 - len(pkey_data) % 16)
    strgen_template = "[\l\d]{{{}}}".format(str(rnd_len))
    pkey_data = pkey_data + strgen.StringGenerator(strgen_template).render()
    encripted_key = encryptionAES.encrypt(pkey_data.encode("ascii"))
    return base64.urlsafe_b64encode(encripted_key).decode("utf-8") 

def Decrypt(pkey):
    decryptionAES = AES.new(b"#DN45C&?5Rjhzgar", AES.MODE_CBC, b"a7ePE8w4yN9y=!ZF")
    decode_key = base64.urlsafe_b64decode(pkey)#.encode("ascii")
    return decryptionAES.decrypt(decode_key)

