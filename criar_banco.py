from siteum import app, database
from siteum.models import Post, Usuario

with app.app_context():
    database.create_all()