🔐 Sistema de Autenticação MVC - Guia Completo

📋 O que você precisa ter antes de começar:
Python 3.8 ou superior instalado no computador
MySQL Server (pode ser XAMPP, WAMP, Laragon ou MySQL Workbench)
Um navegador web (Chrome, Firefox, Edge)

🗂️ Estrutura das pastas do projeto:

/project
├── app.py                          # Ponto de entrada da aplicação
├── config.py                       # Configurações do sistema
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── models/
│   └── usuario_model.py           # Model: Acesso ao banco de dados
├── controllers/
│   └── auth_controller.py         # Controller: Regras de negócio e rotas
├── views/
│   └── templates/
│       ├── login.html              # Tela de login
│       ├── dashboard.html          # Área protegida
│       ├── primeiro_acesso.html    # Troca de senha obrigatória
│       ├── cadastrar_usuario.html  # Criação de novos usuários
│       └── lista_usuarios.html     # Lista de usuários cadastrados
└── static/                         # Pasta para CSS/JS/imagens (vazia)

⚙️ Passo 1 - Instalar as dependências:
Abra o terminal na pasta do projeto e digite:
pip install flask flask-mysqldb werkzeug
Se der erro no Windows com mysql, tente:
pip install mysqlclient
ou
pip install pymysql

🗄️ Passo 2 - Configurar o banco de dados:
Abra o MySQL Workbench e execute este código SQL:

CREATE DATABASE sistema_mvc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_mvc;
CREATE TABLE usuarios (
id INT AUTO_INCREMENT PRIMARY KEY,
email VARCHAR(100) UNIQUE NOT NULL,
senha VARCHAR(255) NOT NULL,
ativo BOOLEAN DEFAULT TRUE,
tentativas_login INT DEFAULT 0,
ultimo_login DATETIME NULL
);

✅ Pronto, o banco está criado!
🔧 Passo 3 - Configurar a conexão:

Edite o arquivo config.py e ajuste seus dados:
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  (coloque sua senha aqui se tiver)
MYSQL_DB = 'sistema_mvc'

💡 Dica: No XAMPP/Laragon a senha geralmente fica vazia. No Workbench, use a senha que você definiu na instalação.

🚀 Passo 4 - Rodar o sistema:

No terminal digite:

python app.py

Você verá uma mensagem dizendo que está rodando em http://127.0.0.1:5000

🌐 Passo 6 - Acessar no navegador:

Abra o Chrome ou Firefox e digite:

http://localhost:5000
ou
http://127.0.0.1:5000

🎯 Como usar o sistema:

🆕 Cadastrar novos usuários:

Na tela de login clique em "Criar Novo Usuário"

Preencha email e senha

O novo usuário será salvo e já pode fazer login (mas vai ter que trocar a senha na primeira vez)

📋 Ver usuários cadastrados:

Dentro do Dashboard clique em "Ver Usuários"

Lá mostra quem está ativo, bloqueado, quantas tentativas de login e último acesso

🚪 Sair do sistema:

Clique em "Sair do Sistema" para encerrar a sessão

🔒 Funcionalidades de segurança incluídas:

✓ Senhas sempre criptografadas (nunca salvas em texto puro)
✓ Bloqueio automático após 3 tentativas erradas
✓ Só permite login entre 08h e 18h (horário comercial)
✓ Troca obrigatória de senha no primeiro acesso
✓ Sessões seguras com cookies criptografados

🛠️ Problemas comuns:

❌ "Access denied for user":
A senha do MySQL está errada no config.py. Verifique se deixou vazio ou colocou a senha certa.

❌ "Unknown database":
Você esqueceu de criar o banco de dados. Execute o SQL do Passo 2.

❌ Erro 404:
Verifique se o servidor está rodando (python app.py) e se você digitou o endereço certo.

❌ "Module not found":
Instale as dependências: pip install flask flask-mysqldb

🛠️ Comandos úteis no MySQL:

Para desbloquear um usuário:

UPDATE usuarios SET ativo = TRUE, tentativas_login = 0 WHERE email = 'usuario@email.com';
Para ver todos os usuários:
SELECT * FROM usuarios;
Para apagar um usuário:
DELETE FROM usuarios WHERE email = 'usuario@email.com';

💡 Dicas finais:
O sistema usa MVC (Model-View-Controller) organizado em pastas separadas
As mensagens de erro/sucesso aparecem em cores diferentes na tela
Sempre que modificar o código, reinicie o servidor (Ctrl+C e rode python app.py novamente)
Para desenvolvimento, o modo debug está ligado (mostra erros detalhados)

🎉 Pronto! Seu sistema está completo e funcionando!
