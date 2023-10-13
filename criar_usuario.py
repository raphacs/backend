import bcrypt

def criar_hash_senha(senha):
    # Gerar um salt aleatório
    salt = bcrypt.gensalt()
    
    # Hash da senha com o salt
    hash_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
    
    return hash_senha

def verificar_senha(senha_digitada, hash_senha_armazenado):
    # Verificar a senha inserida usando o hash armazenado
    return bcrypt.checkpw(senha_digitada.encode('utf-8'), hash_senha_armazenado)

# Exemplo de uso:
senha = "senha_secreta"

# Criar o hash da senha
hash_senha = criar_hash_senha(senha)

# Simular uma tentativa de login com uma senha correta
tentativa_senha_correta = "senha_secreta"
if verificar_senha(tentativa_senha_correta, hash_senha):
    print("Senha correta. Acesso permitido.")
else:
    print("Senha incorreta. Acesso negado.")

# Simular uma tentativa de login com uma senha incorreta
tentativa_senha_incorreta = "senha_errada"
if verificar_senha(tentativa_senha_incorreta, hash_senha):
    print("Senha correta. Acesso permitido.")
else:
    print("Senha incorreta. Acesso negado.")
