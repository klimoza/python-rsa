# RSA command line tool
## Usage
```bash
➜ ./main.py --help
Usage: main.py {gen-keys,sign,verify} <args> [options]

RSA command line tool

Options:
  -h, --help            show this help message and exit
  -b BITS, --bits=BITS  number of bits for key generation [default=1024]
```
## Example
```bash
➜  cat test_hello_world.txt
Hello World!
➜ ./main.py gen-keys
➜ ./main.py sign test_hello_world.txt key_private.pem signed_hello_world.txt
➜ ./main.py verify test_hello_world.txt signed_hello_world.txt key_public.pem
VALID
```