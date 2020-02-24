import sys

{libs_py}


ENCRYPTED_CODE = "{encrypted_code}".encode()


if __name__ == "__main__":
    password = sys.argv[1]
    params_dct = dict(zip(sys.argv[2::2], sys.argv[3::2]))

    cipher = AESCipher(password)
    code = cipher.decrypt(ENCRYPTED_CODE)

    exec(code, params_dct)
