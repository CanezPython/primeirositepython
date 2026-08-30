from siteum import app, database
from siteum.models import Usuario, Post

with app.app_context():

    # Primeiro apaga todos os posts
    Post.query.delete()

    # Depois apaga todos os usuários
    Usuario.query.delete()

    # Salva as alterações
    database.session.commit()

    print("Banco de dados limpo com sucesso!")