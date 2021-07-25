from werkzeug.security import generate_password_hash, check_password_hash

contrasenha = input("Ingrese una contrasenha para el usuario(admin) de hips:")
hash_and_salted_password = generate_password_hash( contrasenha, method='pbkdf2:sha256', salt_length=8)
print(hash_and_salted_password)




