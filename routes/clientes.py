from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import Cliente, db
from datetime import date, datetime 

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('/')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('listar_clientes.html', clientes=clientes)
    

@clientes_bp.route('/novo', methods=['GET'])
def novo_cliente():
    return render_template('clientes.html')

@clientes_bp.route('/novo', methods=['POST'])
def criar_cliente():
    nome = request.form.get('nome')
    email = request.form.get('email')
    numero_telefone = request.form.get('numero_telefone')
    data = request.form.get('data_nascimento')
    try:
        data_nascimento = datetime.strptime(data, '%Y-%m-%d').date()
    except ValueError:
        flash("Data de nascimento inválida!", "error")
        return redirect(url_for('clientes.novo_cliente'))
    empresa = request.form.get('empresa')
    cliente_existente = Cliente.query.filter_by(email=email).first()
    if cliente_existente:
        flash("Já existe um cliente com esse email!", "error")
        return redirect(url_for('clientes.novo_cliente'))
    novo_cliente = Cliente(nome = nome, email = email, numero_telefone = numero_telefone, data_nascimento = data_nascimento, empresa = empresa)
    db.session.add(novo_cliente)
    db.session.commit()
    flash("Cliente criado com sucesso!", "success")
    
  
    return redirect(url_for('clientes.listar_clientes'))

@clientes_bp.route('/deletar/<int:cliente_id>', methods=['POST'])
def deletar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        flash("Cliente não encontrado!", "error")
        return redirect(url_for('clientes.listar_clientes'))
    if cliente.negocios or cliente.tarefas:
        flash("Não é possível deletar este cliente pois possui negócios ou tarefas vinculados!", "error")
        return redirect(url_for('clientes.listar_clientes'))
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente deletado com sucesso!", "success")
    return redirect(url_for('clientes.listar_clientes'))

@clientes_bp.route('/editar/<int:cliente_id>', methods=['GET'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        flash("Cliente não encontrado!", "error")
        return redirect(url_for('clientes.listar_clientes'))
    return render_template('editar_cliente.html', cliente=cliente)

@clientes_bp.route('/editar/<int:cliente_id>', methods=['POST'])
def atualizar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        flash("Cliente não encontrado!", "error")
        return redirect(url_for('clientes.listar_clientes'))
    cliente.nome = request.form.get('nome')
    cliente.email = request.form.get('email')
    cliente.numero_telefone = request.form.get('numero_telefone')
    data = request.form.get('data_nascimento')
    try:
        cliente.data_nascimento = datetime.strptime(data, '%Y-%m-%d').date()
    except ValueError:
        flash("Data de nascimento inválida!", "error")
        return redirect(url_for('clientes.editar_cliente', cliente_id=cliente_id))
    cliente.empresa = request.form.get('empresa')
    db.session.commit()
    flash("Cliente atualizado com sucesso!", "success")
    return redirect(url_for('clientes.listar_clientes'))
