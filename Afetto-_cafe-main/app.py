from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Tabelas
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    discount = db.Column(db.Float, nullable=False)

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

@app.route('/sobre_nos')
def sobre_nos():
    return render_template('sobre_nos.html')

@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')

@app.route('/promocoes')
def promocoes():
    return render_template('promocoes.html')

@app.route('/fale_conosco')
def fale_conosco():
    return render_template('fale_conosco.html')

@app.route('/eventos')
def eventos():
    return render_template('eventos.html')

@app.route('/localizacao')
def localizacao():
    return render_template('localizacao.html')

@app.route('/testemunhos')
def testemunhos():
    return render_template('testemunhos.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')
@app.route('/cardapio/MDC')
def MDC():
    return render_template('MDC.html')
@app.route('/cardapio/MDC/PC')
def PC():
    return render_template('PC.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Processa o envio do formulário
        username = request.form['username']  # Captura o usuário
        password = request.form['password']  # Captura a senha
        user = User.query.filter_by(username=username).first()  # Busca no banco
        
        # Verifica credenciais
        if user and user.password == password:
            login_user(user)  # Autentica o usuário
            return redirect(url_for('home'))  # Redireciona para a página inicial
        else:
            flash('Usuário ou senha inválidos!')  # Exibe mensagem de erro
    return render_template('login.html')  # Renderiza o formulário de login

class User(db.Model, UserMixin):  # Tabela de Usuários
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = (password)  # Armazena a senha criptografada

    def check_password(self, password):
        return check_password_hash(self.password, password)  # Verifica a senha criptografada
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Se o formulário for enviado
        username = request.form['username']
        password = request.form['password']
        
        # Verifica se o usuário já existe no banco
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Nome de usuário já existe!')  # Exibe uma mensagem de erro
            return redirect(url_for('register'))
        
        # Cria o novo usuário
        new_user = User(username=username)
        new_user.set_password(password)  # Cria a senha criptografada

        # Adiciona ao banco de dados
        db.session.add(new_user)
        db.session.commit()

        flash('Conta criada com sucesso! Você pode fazer login agora.')  # Sucesso
        return redirect(url_for('login'))  # Redireciona para a página de login
    
    return render_template('register.html')  # Exibe o formulário de registro




# Inicializar banco de dados
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():  # Garante que o contexto da aplicação seja usado
        # Cria um usuário
        new_user = User.query.filter_by(username='admin').first()
        if not new_user:  # Verifica se o usuário já existe
            new_user = User(username='admin', password='1234')
            db.session.add(new_user)
            db.session.commit()
            print("Usuário 'admin' criado com sucesso!")
        else:
            print("O usuário 'admin' já existe.")
    app.run(debug=True)
