from __future__ import with_statement

import operator
import platform
import random
import sys
from optparse import OptionParser

IV_LENGTH = 10

def to_int_list(s):
    return [ord(c) for c in s]

def init_encrypt(out_stream):
    # create IV
    iv = [random.randint(0, 255) for _ in range(IV_LENGTH)]
    for b in iv:
        out_stream.write(chr(b))
    return iv

def init_decrypt(f):
    # get IV
    iv = to_int_list(f.read(IV_LENGTH))
    if not len(iv) == IV_LENGTH:
        raise Exception('malformed IV')
    return iv

def init_s_box(user_key, iv, n):
    key = user_key + iv

    K = []
    while len(K) < 256:
        i = min(len(key), 256 - len(K))
        K.extend(key[0:i])

    S = range(256)

    j = 0
    for k in range(n):
        for i in range(256):
            j = (j + S[i] + K[i]) % 256
            S[i], S[j] = S[j], S[i]

    return S

def next_random_byte(S, i, j):
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    t = (S[i] + S[j]) % 256
    return S[t], i, j

def process(encrypt, in_stream, key_string, n, out_stream=sys.stdout):
    if platform.system() == 'Windows':
        import os, msvcrt
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    key = to_int_list(key_string)
    
    if encrypt:
        iv = init_encrypt(out_stream)
    else:
        iv = init_decrypt(in_stream)

    # initialize
    S = init_s_box(key, iv, n)

    # encrypt/decrypt
    i, j = 0, 0    
    c = in_stream.read(1)
    while len(c) == 1:
        k, i, j = next_random_byte(S, i, j)
        out_stream.write(chr(operator.xor(k, ord(c[0]))))
        c = in_stream.read(1)

def main():
    parser = OptionParser(usage='usage: %prog [options] FILE KEY')
    parser.set_defaults(encrypt=True)
    parser.add_option('-e', action='store_true', dest='encrypt',
                      help='Encrypt FILE (default)')
    parser.add_option('-d', action='store_false', dest='encrypt',
                      help='Decrypt FILE')
    parser.add_option('-n', type='int', dest='n', default=20,
                      help='Mix state array N times. (default: %default)')
                      
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error('wrong number of arguments')

    with open(args[0], 'rb') as f:
        process(options.encrypt, f, args[1], options.n)

if __name__ == '__main__':
    main()
