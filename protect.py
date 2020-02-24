from argparse import ArgumentParser
from libs import *


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('-p', '--password', required=True)
    args = parser.parse_args()

    with open(args.input) as f:
        code = f.read()

    cipher = AESCipher(args.password)
    encrypted_code = cipher.encrypt(code)

    with open('libs.py') as f:
        libs_py = f.read()

    with open('out_tpl.py') as f:
        out_tpl_py = f.read()

    with open(args.output, "w") as f:
        f.write(out_tpl_py.format(
            encrypted_code=encrypted_code.decode(), libs_py=libs_py
        ))
