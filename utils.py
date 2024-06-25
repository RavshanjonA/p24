import bcrypt


def make_password(password):
    salt = bcrypt.gensalt()
    encoded_password = password.encode("utf-8")
    return bcrypt.hashpw(encoded_password, salt).decode("utf-8")


def match_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# if __name__ == '__main__':
# print(make_passoword("testpassword"))
# print(match_password("Testpassword", "$2b$12$QZ4siIZhSb/n19APTL6IiulsLdnsOyM9S1qV2brGLGYK4jslxmW6G"))
