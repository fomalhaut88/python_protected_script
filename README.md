# python_protected_script

This is a simple way to encrypt your Python script with a password using AES256. 
The main idea of the approach is to apply AES256 algorithm for a code in the Python script you are going to protect,
that can be decrypted and run with `exec` function if you know the password.

## Step-by-step instruction

1. Let's suppose you have this script to protect:

```python
# script_1.py

def is_prime(n):
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            return False
    return True


if 'limit' not in globals():
    limit = 100
limit = int(limit)

s = 0
for n in range(2, limit):
    if is_prime(n):
        s += 1
print(s)
```

2. To encrypt it with the password `123456` you run the command:

```
python3.7 protect.py script_1.py out_1.py -p 123456
```

3. As the result a new file `out_1.py` will appear:

```python
import sys

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode()

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]



ENCRYPTED_CODE = "eN2RwMf4JiYQg9vfR/TCyo/r6N4g8DldSB8R4KFzSi2XTRlRBXpIEoVx4aIBYUVqUK2+kKx3BafVqxd7VmnWgQYo4ViO418pG69qHpXNOcb4jk5JcOQkq7MFkI4rsSoHjjttQDA/HXMdpaS4rgeooR8ATz6ncDwH9gK6O8PCNdRlL+YAzOu7JUxa6BbUOXx4x3Vqq9nyM6mqNkzaNnT0+995V5FaQ+VmQy3MQsWqXqRmWEavtRYE3at0KpL6LoWiQsFbBB1PlfOnDHXIgc/vR0p+e+VsiamUEyF75zNyGXu5z4DhdefcCW9kDarAV56GQMZMj+8D8x8O1VeuPP9GrD/nwfnVhLMUtabmEXZOeQJJs/E5z9XVAmdND+eIvKW7".encode()


if __name__ == "__main__":
    password = sys.argv[1]
    params_dct = dict(zip(sys.argv[2::2], sys.argv[3::2]))

    cipher = AESCipher(password)
    code = cipher.decrypt(ENCRYPTED_CODE)

    exec(code, params_dct)
```

4. The output file is independent itself, it doesn't require any additional files from this Github project.
All it needs is the same Python version and installed Pycrypto: https://pypi.org/project/pycrypto/.
To run it:

```
python3.7 out_1.py 123456 limit 1000
```

Where `limit` is a parameter that is a global constant in your initial scipt.

