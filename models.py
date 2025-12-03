import json
import os
from datetime import datetime

DATA_FILE = 'tarefas.json'

class Tarefa:
    def __init__(self, nome, data_hora, disciplina):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.nome = nome
        self.data_hora = data_hora
        self.disciplina = disciplina
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_hora': self.data_hora,
            'disciplina': self.disciplina
        }

class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = self.carregar_tarefas()
    
    def carregar_tarefas(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    return dados
            except (json.JSONDecodeError, Exception):
                return []
        return []
    
    def salvar_tarefas(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tarefas, f, ensure_ascii=False, indent=2)
    
    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa.to_dict())
        self.salvar_tarefas()
    
    def obter_tarefas(self):
        # Ordenar por data/hora (mais urgente primeiro)
        try:
            return sorted(self.tarefas, key=lambda x: x['data_hora'])
        except (KeyError, TypeError):
            return self.tarefas
    
    def obter_tarefas_por_disciplina(self, disciplina):
        try:
            tarefas_filtradas = [t for t in self.tarefas if t['disciplina'].lower() == disciplina.lower()]
            return sorted(tarefas_filtradas, key=lambda x: x['data_hora'])
        except (KeyError, TypeError):
            return []
    
    def obter_disciplinas(self):
        try:
            disciplinas = list(set(t['disciplina'] for t in self.tarefas))
            return sorted(disciplinas)
        except (KeyError, TypeError):
            return []