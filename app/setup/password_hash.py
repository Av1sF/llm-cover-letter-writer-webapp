from passlib.context import CryptContext

cryptContext = CryptContext(schemes=['des_crypt'], deprecated='auto')

def getPasswordHash(password): 
    return cryptContext.hash(password)

def verifyPassword(plainPw, hashedPw):
    return cryptContext.verify(plainPw, hashedPw)
