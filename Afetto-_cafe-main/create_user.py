from app import db, User, app  # Importe o banco de dados, o modelo User e o app

# Cria um usuário
new_user = User(username='admin', password='1234')

# Adiciona ao banco
with app.app_context():  # Garante que o contexto da aplicação seja usado
    db.session.add(new_user)
    db.session.commit()

print("Usuário criado com sucesso!")


