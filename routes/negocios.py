from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import Negocio, Cliente, db

negocios_bp = Blueprint('negocios', __name__, url_prefix='/negocios')
@negocios_bp.route('/')
def listar_negocios():
    negocios = Negocio.query.all()
    return render_template('listar_negocios.html', negocios=negocios)

@negocios_bp.route('/novo', methods=['GET'])
def novo_negocio():
    clientes = Cliente.query.all()
    return render_template('novo_negocio.html', clientes=clientes)

@negocios_bp.route('/novo', methods=['POST']) 
def criar_negocio():
    titulo = request.form.get('titulo')
    valor = request.form.get('valor')
    status = request.form.get('status')
    cliente_id = request.form.get('cliente_id')
    novo_negocio = Negocio(titulo=titulo, valor=valor, status=status, cliente_id=cliente_id)
    db.session.add(novo_negocio)
    db.session.commit()
    return redirect(url_for('negocios.listar_negocios'))


@negocios_bp.route('/deletar/<int:negocio_id>', methods=['POST'])
def deletar_negocio(negocio_id):
    negocio = Negocio.query.get(negocio_id)
    if not negocio:
        flash("Negócio não encontrado!", "error")
        return redirect(url_for('negocios.listar_negocios'))
    db.session.delete(negocio)
    db.session.commit()
    flash("Negócio deletado com sucesso!", "success")
    return redirect(url_for('negocios.listar_negocios'))

@negocios_bp.route('/editar/<int:negocio_id>', methods=['GET'])
def editar_negocio(negocio_id):
    negocio = Negocio.query.get(negocio_id)
    if not negocio:
        flash("Negócio não encontrado!", "error")
        return redirect(url_for('negocios.listar_negocios'))
    clientes = Cliente.query.all()
    return render_template('editar_negocio.html', negocio=negocio, clientes=clientes)

@negocios_bp.route('/editar/<int:negocio_id>', methods=['POST'])
def atualizar_negocio(negocio_id):
    negocio = Negocio.query.get(negocio_id)
    if not negocio:
        flash("Negócio não encontrado!", "error")
        return redirect(url_for('negocios.listar_negocios'))
    negocio.titulo = request.form.get('titulo')
    negocio.valor = request.form.get('valor')
    negocio.status = request.form.get('status')
    negocio.cliente_id = request.form.get('cliente_id')
    db.session.commit()
    flash("Negócio atualizado com sucesso!", "success")
    return redirect(url_for('negocios.listar_negocios'))
