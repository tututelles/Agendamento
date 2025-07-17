from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Modelo de usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Página inicial
@app.route('/')
def index():
    return render_template('login.html')

# Página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = bcrypt.generate_password_hash(request.form['senha']).decode('utf-8')
        novo_usuario = User(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.senha, senha):
        login_user(user)
        return redirect(url_for('dashboard'))
    return 'Credenciais inválidas'

# Dashboard (restrita)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nome=current_user.nome)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)