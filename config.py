import os

class Config:
    
    SECRET_KEY = os.environ.get('gugas') or 'main-gugas'
    
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin'  
    MYSQL_DB = 'sistema_mvc'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    MAX_TENTATIVAS = 3