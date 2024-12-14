'''
    This files only purpose is to generate keys. It does not implement or change anything by itself.
'''

import secrets

key = secrets.token_hex(32)
print(key)