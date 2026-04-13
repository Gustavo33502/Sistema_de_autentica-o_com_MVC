-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS sistema_auth CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_auth;

-- Tabela de usuários conforme especificação
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    tentativas_login INT DEFAULT 0,
    ultimo_login DATETIME NULL
);

-- Inserir usuário de teste
-- Senha: 123456 (hash gerado com werkzeug)
-- NOTA: Para gerar o hash, execute no Python:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('123456'))

INSERT INTO usuarios (email, senha, ultimo_login) VALUES 
('admin@empresa.com', 
 'scrypt:32768:8:1$...scrypt:32768:8:1$MiSVeRGLmpSTP5Cj$7bbf1e98024099e54fd0dd0840502623715cd3d17cde4e0a3065acf595733d8198d12a2e94d6de01f3c4d8dfae931e03c7e830daec46e63a07645062a75cc847...', 
 NULL);  -- NULL = primeiro acesso, precisa trocar senha

-- Inserir usuário normal (já acessou antes)
INSERT INTO usuarios (email, senha, ultimo_login, ativo) VALUES 
('usuario@empresa.com', 
 'scrypt:32768:8:1$...scrypt:32768:8:1$MiSVeRGLmpSTP5Cj$7bbf1e98024099e54fd0dd0840502623715cd3d17cde4e0a3065acf595733d8198d12a2e94d6de01f3c4d8dfae931e03c7e830daec46e63a07645062a75cc847...', 
 '2026-13-04 15:00:00', 
 TRUE);