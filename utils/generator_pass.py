import bcrypt

# Nome de usuário e senha originais
username = "bi@mynd8.com.br"
password = "mynd1234"

# Gerar hashes
hashed_username = bcrypt.hashpw(username.encode(), bcrypt.gensalt())
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

print("Hashed Username:", hashed_username)
print("Hashed Password:", hashed_password)
