from datetime import datetime
from flask import Blueprint, redirect, request, render_template, url_for, flash
from models import Tarefa, Cliente, db

tarefas_bp = Blueprint('tarefas', __name__, url_prefix='/tarefas')

@tarefas_bp.route('/')
def listar_tarefas():
    tarefas = Tarefa.query.all()
    return render_template('listar_tarefas.html', tarefas=tarefas)
    
@tarefas_bp.route('/nova',methods=['GET'])
def nova_tarefa():
    clientes = Cliente.query.all()
    return render_template('nova_tarefa.html', clientes=clientes)

@tarefas_bp.route('/nova', methods=['POST'])
def criar_tarefa():
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')

    try:
     data_vencimento = datetime.strptime(request.form.get('data_vencimento'), '%Y-%m-%d').date()
    except ValueError:
     return "Data inválida!", 400
    cliente_id = request.form.get('cliente_id')
    nova_tarefa = Tarefa(titulo=titulo, descricao=descricao, data_vencimento=data_vencimento, cliente_id=cliente_id)
    db.session.add(nova_tarefa)
    db.session.commit()
    return redirect(url_for('tarefas.listar_tarefas'))

@tarefas_bp.route('/deletar/<int:tarefa_id>', methods=['GET'])
def deletar_tarefa_form(tarefa_id):
    tarefa = Tarefa.query.get(tarefa_id)
    if not tarefa:
        flash("Tarefa não encontrada!", "error")
        return redirect(url_for('tarefas.listar_tarefas'))
    return render_template('deletar_tarefa.html', tarefa=tarefa)

@tarefas_bp.route('/deletar/<int:tarefa_id>', methods=['POST'])
def deletar_tarefa(tarefa_id):
    tarefa = Tarefa.query.get(tarefa_id)
    if not tarefa:
        flash("Tarefa não encontrada!", "error")
        return redirect(url_for('tarefas.listar_tarefas'))
    db.session.delete(tarefa)
    db.session.commit()
    flash("Tarefa deletada com sucesso!", "success")
    return redirect(url_for('tarefas.listar_tarefas'))
