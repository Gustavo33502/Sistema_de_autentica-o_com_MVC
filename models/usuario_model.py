from flask_mysqldb import MySQL
from datetime import datetime, time

class UsuarioModel:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql
    
    def buscar_por_email(self, email: str) -> dict:
        """Busca usuário pelo email. Retorna dict ou None."""
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
    
    def incrementar_tentativas(self, usuario_id: int):
        """Adiciona 1 tentativa falha"""
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET tentativas_login = tentativas_login + 1 WHERE id = %s",
                (usuario_id,)
            )
            self.mysql.connection.commit()
        finally:
            cursor.close()
    
    def zerar_tentativas(self, usuario_id: int):
        """Reseta tentativas e atualiza último login"""
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(
                """UPDATE usuarios 
                   SET tentativas_login = 0, ultimo_login = NOW() 
                   WHERE id = %s""",
                (usuario_id,)
            )
            self.mysql.connection.commit()
        finally:
            cursor.close()
    
    def bloquear_usuario(self, usuario_id: int):
        """Desativa usuário (ativo = FALSE)"""
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET ativo = FALSE WHERE id = %s",
                (usuario_id,)
            )
            self.mysql.connection.commit()
        finally:
            cursor.close()
    
    def atualizar_senha(self, usuario_id: int, senha_hash: str):
        """Atualiza senha e define ultimo_login"""
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET senha = %s, ultimo_login = NOW() WHERE id = %s",
                (senha_hash, usuario_id)
            )
            self.mysql.connection.commit()
        finally:
            cursor.close()
    
    def verificar_horario_permitido(self) -> bool:
        """Verifica se está entre 08h e 18h"""
        agora = datetime.now().time()
        return time(8, 0) <= agora <= time(18, 0)
    
    def criar_usuario(self, email: str, senha_hash: str) -> bool:
        """
        Insere novo usuário no banco.
        Retorna True se sucesso, False se email já existe.
        """
        cursor = self.mysql.connection.cursor()
        try:
            # Verifica se email já existe
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                return False  # Email já cadastrado
            
            # Insere novo usuário
            # ultimo_login = NULL (força troca de senha no primeiro acesso)
            cursor.execute(
                """INSERT INTO usuarios 
                   (email, senha, ativo, tentativas_login, ultimo_login) 
                   VALUES (%s, %s, TRUE, 0, NULL)""",
                (email, senha_hash)
            )
            self.mysql.connection.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return False
        finally:
            cursor.close()
    
    def listar_usuarios(self):
        """Retorna lista de todos usuários (para admin ver)"""
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(
                "SELECT id, email, ativo, tentativas_login, ultimo_login FROM usuarios"
            )
            return cursor.fetchall()
        finally:
            cursor.close()