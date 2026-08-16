from siteum import database, app
from siteum.models import Post, Usuario

with app.app_context():
    database.create_all()