from app import app
from flask import flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/crud'
db = SQLAlchemy(app)

class Usuario(db.Model):
	id = db.Column(db.Integer, primary_key= True)
	nome = db.Column(db.String(200))
	email = db.Column(db.String(150))


@app.route('/')
def users():
	try:
		lista_usuarios = Usuario.query.all()
		return render_template('users.html', lista_usuarios=lista_usuarios)
	except Exception as e:
		print(e)
		

@app.route('/add', methods=['POST'])
def add_user():
	try:
		usuario = Usuario(nome = request.form.get("nome"), email = request.form.get('email'))

		db.session.add(usuario)
		db.session.commit()

		return redirect('/')
		
	except Exception as e:
		print('Erro', e)


@app.route('/select/<int:id>')
def select_by_id(id):
	try:
		usuario = Usuario.query.filter_by(id=id).first()
		print("usuario selecionado:", usuario.id)
		return render_template('edit.html', usuario=usuario)
	except Exception as e:
		print(e)


@app.route('/update/<int:id>', methods=["POST"])
def update(id):
	usuario = Usuario.query.filter_by(id=id).first() 

	usuario.nome = request.form.get("nome")
	usuario.email = request.form.get("email")

	db.session.add(usuario)
	db.session.commit()

	return redirect('/')

		
@app.route('/delete/<int:id>')
def delete(id):

	usuario = Usuario.query.filter_by(id=id).first()
	try:
		db.session.delete(usuario)
		db.session.commit()
		return redirect('/')

	except Exception as e:
		print('Erro', e)
		

if __name__ == "__main__":
    app.run(debug=True)