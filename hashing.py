from passlib.context import CryptContext

pwd_encrypt=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hashingpassword(password):
    return pwd_encrypt.hash(password)

def verifyingpassword(original_password,hashedpassword):
    return pwd_encrypt.verify(original_password,hashedpassword)

