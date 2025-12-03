from flask import Flask, render_template, request, redirect, url_for
from models import Tarefa, GerenciadorTarefas

app = Flask(__name__)
gerenciador = GerenciadorTarefas()

@app.route('/')
def index():
    tarefas = gerenciador.obter_tarefas()
    disciplinas = gerenciador.obter_disciplinas()
    return render_template('index.html', tarefas=tarefas, disciplinas=disciplinas)

@app.route('/disciplina/<nome_disciplina>')
def disciplina(nome_disciplina):
    tarefas = gerenciador.obter_tarefas_por_disciplina(nome_disciplina)
    disciplinas = gerenciador.obter_disciplinas()
    return render_template('disciplina.html', 
                         tarefas=tarefas, 
                         disciplinas=disciplinas, 
                         disciplina_selecionada=nome_disciplina)

@app.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        nome = request.form['nome']
        data_hora = request.form['data_hora']
        disciplina = request.form['disciplina']
        
        nova_tarefa = Tarefa(nome, data_hora, disciplina)
        gerenciador.adicionar_tarefa(nova_tarefa)
        
        return redirect(url_for('index'))
    
    disciplinas = gerenciador.obter_disciplinas()
    return render_template('novo.html', disciplinas=disciplinas)

if __name__ == '__main__':
    app.run(debug=True)