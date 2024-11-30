from app import db, User, app  # Importe o banco de dados, o modelo User e o app

# Especifica o ID do usuário que você quer deletar
user_id_to_delete = 2  # Altere para o ID do usuário que você deseja deletar

with app.app_context():  # Garante que o contexto da aplicação esteja sendo usado
    # Busca o usuário pelo ID
    user_to_delete = User.query.get(user_id_to_delete)

    if user_to_delete:
        db.session.delete(user_to_delete)  # Deleta o usuário
        db.session.commit()  # Confirma a exclusão no banco de dados
        print(f"Usuário com ID {user_id_to_delete} deletado com sucesso!")
    else:
        print(f"Usuário com ID {user_id_to_delete} não encontrado!")
