from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario_model import UsuarioModel

auth_bp = Blueprint('auth', __name__)

def init_controller(mysql):
    model = UsuarioModel(mysql)
    
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            senha = request.form.get('senha', '')
            
            if not email or not senha:
                flash('❌ Preencha todos os campos', 'error')
                return render_template('login.html')
            
            usuario = model.buscar_por_email(email)
            
            if not usuario:
                flash('❌ Usuário ou senha inválidos', 'error')
                return render_template('login.html')
 
            if not usuario['ativo']:
                flash('⚠️ Usuário bloqueado. Contate o administrador.', 'warning')
                return render_template('login.html')

            if not model.verificar_horario_permitido():
                flash('⏰ Acesso permitido apenas entre 08h e 18h', 'warning')
                return render_template('login.html')
 
            if not check_password_hash(usuario['senha'], senha):
                model.incrementar_tentativas(usuario['id'])

                usuario_atualizado = model.buscar_por_email(email)
                if usuario_atualizado['tentativas_login'] >= 3:
                    model.bloquear_usuario(usuario['id'])
                    flash('⚠️ Usuário bloqueado após 3 tentativas', 'warning')
                else:
                    restantes = 3 - usuario_atualizado['tentativas_login']
                    flash(f'❌ Senha incorreta. Tentativas restantes: {restantes}', 'error')
                
                return render_template('login.html')

            model.zerar_tentativas(usuario['id'])
            session['usuario_id'] = usuario['id']
            session['usuario_email'] = usuario['email']
            session['logado'] = True

            if usuario['ultimo_login'] is None:
                flash('🔐 Primeiro acesso! Altere sua senha.', 'info')
                return redirect(url_for('auth.primeiro_acesso'))
            
            flash('✅ Login realizado com sucesso!', 'success')
            return redirect(url_for('auth.dashboard'))
        
        return render_template('login.html')
    
    @auth_bp.route('/primeiro-acesso', methods=['GET', 'POST'])
    def primeiro_acesso():
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            nova = request.form.get('nova_senha')
            confirma = request.form.get('confirmar_senha')
            
            if not nova or not confirma:
                flash('❌ Preencha todos os campos', 'error')
            elif nova != confirma:
                flash('❌ As senhas não conferem', 'error')
            elif len(nova) < 6:
                flash('❌ Senha mínima de 6 caracteres', 'error')
            else:
                senha_hash = generate_password_hash(nova)
                model.atualizar_senha(session['usuario_id'], senha_hash)
                flash('✅ Senha alterada! Bem-vindo.', 'success')
                return redirect(url_for('auth.dashboard'))
        
        return render_template('primeiro_acesso.html')
    
    @auth_bp.route('/dashboard')
    def dashboard():
        if not session.get('logado'):
            flash('❌ Faça login primeiro', 'error')
            return redirect(url_for('auth.login'))
        
        return render_template('dashboard.html', 
                            email=session.get('usuario_email'))
    
    @auth_bp.route('/logout')
    def logout():
        session.clear()
        flash('👋 Logout realizado com sucesso!', 'success')
        return redirect(url_for('auth.login'))
    
    @auth_bp.route('/')
    def index():

        return redirect(url_for('auth.login'))
    
    @auth_bp.route('/cadastrar-usuario', methods=['GET', 'POST'])
    def cadastrar_usuario():

        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            senha = request.form.get('senha', '')
            confirmar = request.form.get('confirmar_senha', '')

            if not email or not senha:
                flash('❌ Preencha todos os campos', 'error')
                return render_template('cadastrar_usuario.html')
            
            if len(senha) < 6:
                flash('❌ Senha deve ter no mínimo 6 caracteres', 'error')
                return render_template('cadastrar_usuario.html')
            
            if senha != confirmar:
                flash('❌ As senhas não conferem', 'error')
                return render_template('cadastrar_usuario.html')
            
            if '@' not in email or '.' not in email:
                flash('❌ Email inválido', 'error')
                return render_template('cadastrar_usuario.html')

            senha_hash = generate_password_hash(senha)

            sucesso = model.criar_usuario(email, senha_hash)
            
            if sucesso:
                flash('✅ Usuário criado com sucesso!', 'success')
                flash('🔐 Faça login com sua nova senha', 'info')
                return redirect(url_for('auth.login'))  
            else:
                flash('❌ Email já cadastrado no sistema', 'error')
        
        return render_template('cadastrar_usuario.html')
    
    @auth_bp.route('/lista-usuarios')
    def lista_usuarios():

        if not session.get('logado'):
            flash('❌ Faça login para acessar', 'error')
            return redirect(url_for('auth.login'))
        
        usuarios = model.listar_usuarios()
        return render_template('lista_usuarios.html', usuarios=usuarios)
    
    return auth_bp