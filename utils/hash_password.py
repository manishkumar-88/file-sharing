import bcrypt
def hash_password(password):
    # Encode the password as bytes
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    return password_hash