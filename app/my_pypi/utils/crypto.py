from passlib.handlers.sha2_crypt import sha256_crypt as crypto
   
def hash_text(text: str) -> str:
    hashed_text = crypto.encrypt(text, rounds=139843)
    return hashed_text

def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)