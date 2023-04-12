#! /usr/bin/env python3

import rsa
from optparse import OptionParser

def gen_keys(bits=1024):
  return rsa.newkeys(bits)

def sign_message(message, private_key):
  return rsa.sign(message, private_key, 'SHA-1')

def verify_message(message, signature, public_key):
  return rsa.verify(message, signature, public_key)

def create_parser():
  usage = "usage: %prog {gen-keys,sign,verify} <args> [options]"
  parser = OptionParser(description='RSA command line tool', usage=usage)
  parser.add_option('-b', '--bits', dest='bits', default=1024, type='int',
                    help='number of bits for key generation [default=1024]')
  return parser

if __name__ == '__main__':
  parser = create_parser()
  (options, args) = parser.parse_args()
  if len(args) == 0:
    parser.error('invalid number of arguments')

  command = args[0]
  if command == 'gen-keys':
    if len(args) != 1:
      parser.error('invalid number of arguments')
    bits = int(options.bits)
    (public_key, private_key) = gen_keys(bits)
    with open('key_public.pem', 'w') as f:
      f.write(public_key.save_pkcs1().decode('utf-8'))
    with open('key_private.pem', 'w') as f:
      f.write(private_key.save_pkcs1().decode('utf-8'))

  elif command == 'sign':
    if len(args) != 4:
      parser.error('invalid number of arguments')
    with open(args[1], 'rb') as f:
      message = f.read()
    with open(args[2], 'rb') as f:
      private_key = rsa.PrivateKey.load_pkcs1(f.read())
    signature = sign_message(message, private_key)
    with open(args[3], 'wb') as f:
      f.write(signature)

  elif command == 'verify':
    if len(args) != 4:
      parser.error('invalid number of arguments')
    with open(args[1], 'rb') as f:
      message = f.read()
    with open(args[2], 'rb') as f:
      signature = f.read()
    with open(args[3], 'rb') as f:
      public_key = rsa.PublicKey.load_pkcs1(f.read())
    try:
      verify_message(message, signature, public_key)
      print('VALID')
    except rsa.pkcs1.VerificationError:
      print('INVALID')
    
  else:
    parser.error('invalid command')