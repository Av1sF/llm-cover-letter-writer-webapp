from passlib.context import CryptContext

cryptContext = CryptContext(schemes=['des_crypt'], deprecated='auto')

# hash a password string
def getPasswordHash(password): 
    return cryptContext.hash(password)

# verify a given string is the same as it's hashed version from db 
def verifyPassword(plainPw, hashedPw):
    return cryptContext.verify(plainPw, hashedPw)
