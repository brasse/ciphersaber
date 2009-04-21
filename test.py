from __future__ import with_statement

import ciphersaber

import hashlib
import os
import StringIO
import sys

TEST_FILES_DIR = 'cstest'
TEST_FILES = [
              ('CSTEST1.CS1', 'asdfg', 1,
               '388714343aa28ff65a7c23d3730bd758'),
              ('CSTEST2.CS1', 'SecretMessageforCongress', 1,
               '2db075352f555e526ec17e176b2d6848'),
              ('CKNIGHT.CS1', 'ThomasJefferson', 1,
               'a18a38c7e1a48b60986e0c5da4279aa2'),
              ('CS2TEST1.CS2', 'asdfg', 10,
               '8aadf3915cb5891b9b130a4c63580983'),
             ]

def main():
    for test_file, key, n, expected_hash in TEST_FILES:
        with open(os.path.join(TEST_FILES_DIR, test_file), 'rb') as f:
            out_stream = StringIO.StringIO()
            ciphersaber.process(False, f, key, n, out_stream)

            hash = hashlib.md5(out_stream.getvalue()).hexdigest()

            if hash == expected_hash:
                print '%s OK' % test_file
            else:
                print 'Failed to decrypt %s' % test_file
                print 'Expected hash:  %s' % expected_hash
                print 'Resulting hash: %s' % hash
                return 1

    print 'All files decrypted correctly!'
    return 0

if __name__ == '__main__':
    sys.exit(main())
