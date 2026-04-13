from werkzeug.security import generate_password_hash

senha = input("Digite a senha para gerar o hash: ")
hash_gerado = generate_password_hash(senha)
print(f"\nHash gerado:\n{hash_gerado}")
print("\nCole este hash no arquivo database.sql")