from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from datetime import datetime
from models import db, User, Tarefa
import os


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'minha_chave_super_secreta_123')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///classfocus.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def inicio():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return redirect(url_for('cadastro'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar = request.form.get('confirmar')

        if senha != confirmar:
            flash('As senhas não coincidem.', 'danger')
            return render_template('cadastro.html')

        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'warning')
            return render_template('cadastro.html')

        novo = User(nome=nome, email=email)
        novo.set_password(senha)
        db.session.add(novo)
        db.session.commit()
        login_user(novo)
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(senha):
            login_user(user)
            return redirect(url_for('index'))
        flash('Credenciais inválidas.', 'danger')
        return render_template('login.html')
    return render_template('login.html')

@app.route('/index')
@login_required
def index():
    tarefas = Tarefa.query.order_by(Tarefa.data_hora).all()
    disciplinas = sorted(list(set(t.disciplina for t in tarefas if t.disciplina)))

    tarefas_template = []
    for t in tarefas:
        tarefas_template.append({
            'id': t.id,
            'nome': t.nome,
            'data_hora': t.data_hora,
            'disciplina': t.disciplina,
            'urgente': t.urgente
        })

    return render_template('index.html', tarefas=tarefas_template, disciplinas=disciplinas)

@app.route('/disciplina/<nome_disciplina>')
@login_required
def disciplina(nome_disciplina):
    tarefas = Tarefa.query.filter(Tarefa.disciplina.ilike(nome_disciplina)).order_by(Tarefa.data_hora).all()
    disciplinas = sorted(list(set(t.disciplina for t in Tarefa.query.all() if t.disciplina)))

    tarefas_template = []
    for t in tarefas:
        tarefas_template.append({
            'id': t.id,
            'nome': t.nome,
            'data_hora': t.data_hora,
            'disciplina': t.disciplina,
            'urgente': t.urgente
        })

    return render_template(
        'disciplina.html', 
        tarefas=tarefas_template, 
        disciplinas=disciplinas, 
        disciplina_selecionada=nome_disciplina
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if request.method == 'POST':
        nome = request.form['nome']
        data_hora_raw = request.form['data_hora']
        disciplina = request.form['disciplina']
        try:
            data_hora = datetime.fromisoformat(data_hora_raw)
        except Exception:
            flash('Formato de data inválido.', 'danger')
            return redirect(url_for('novo'))

        tarefa = Tarefa(nome=nome, data_hora=data_hora, disciplina=disciplina, user_id=current_user.id)
        db.session.add(tarefa)
        db.session.commit()
        return redirect(url_for('index'))

    disciplinas = sorted(list(set(t.disciplina for t in Tarefa.query.all() if t.disciplina)))
    return render_template('novo.html', disciplinas=disciplinas)


@app.route('/editar/<int:tarefa_id>', methods=['GET', 'POST'])
@login_required
def editar(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    if request.method == 'POST':
        tarefa.nome = request.form['nome']
        try:
            tarefa.data_hora = datetime.fromisoformat(request.form['data_hora'])
        except Exception:
            flash('Formato de data inválido.', 'danger')
            return redirect(url_for('editar', tarefa_id=tarefa_id))
        tarefa.disciplina = request.form['disciplina']
        db.session.commit()
        return redirect(url_for('index'))

    disciplinas = sorted(list(set(t.disciplina for t in Tarefa.query.all() if t.disciplina)))
    tarefa_data = {
        'id': tarefa.id,
        'nome': tarefa.nome,
        'data_hora': tarefa.data_hora.strftime('%Y-%m-%dT%H:%M'),
        'disciplina': tarefa.disciplina
    }
    return render_template('novo.html', disciplinas=disciplinas, tarefa=tarefa_data)


@app.route('/deletar/<int:tarefa_id>', methods=['POST'])
@login_required
def deletar(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

