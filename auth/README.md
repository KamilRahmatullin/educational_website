```shell
# Generate an RSA private key, of size 2048
ssh-keygen -t rsa -b 4096 -m PEM -f private.key
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
ssh-keygen -f private.key -e -m PKCS8 > public.key
```
