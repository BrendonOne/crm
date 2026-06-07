from flask import Flask, render_template
from models import db
from routes.clientes import clientes_bp
from routes.negocios import negocios_bp
from routes.tarefas import tarefas_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cmr@2026brendon!xpto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'


db.init_app(app)
app.register_blueprint(clientes_bp)
app.register_blueprint(negocios_bp)
app.register_blueprint(tarefas_bp)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)