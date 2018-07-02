from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from uuid import uuid4
from faker import Faker
from werkzeug.security import generate_password_hash
import random
from random import randint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    '''
    Table user
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password = db.Column(db.String(106), nullable=False, unique=False)
    is_active = db.Column(db.Boolean)
    token = db.Column(db.String(32), nullable=False, unique=False)

    def __init__(self):
        self.is_active = False
        self.token = str(uuid4()).replace('-', '')

    def __repr__(self):
        return '<User %r>' % self.username

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True)
)

class Articulos(db.Model):
    '''
    Tabla Articulos de blog
    '''
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    text = db.Column(db.Text, nullable=False)
    portada = db.Column(db.String(500), nullable=True)

    # Relacion con usuario
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('articles', lazy=True))

    # Relacion con categorias
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'),
        nullable=False)
    categoria = db.relationship('Categorias',
        backref=db.backref('categorias', lazy=True))

    # Relacion de Tags
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('articles', lazy=True))    


    def __repr__(self):
        return '<Article %r>' % self.title


class Categorias(db.Model):
    '''
    Tabla Categorias de los articulos
    '''
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Categoria %r>' % self.name


class Tag(db.Model):
    '''
    Tabla Tags de los articulos
    '''
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Tags %r>' % self.name 

# Comandos

@manager.command
def init_data():
    # Reload tables
    db.drop_all()
    db.create_all()

    # Categorias
    CATEGORIAS_INICIALES = (
        'tiempo',
        'nacional',
        'internacional',
        'deportes',
        'entretenimiento'
        )
    for categoria in CATEGORIAS_INICIALES:
        my_new_category = Categorias(name=categoria)
        db.session.add(my_new_category)
    db.session.commit()
    print('CATEGORIAS creadas')

@manager.command
def fake_data():
    # Reload tables
    db.drop_all()
    db.create_all()

    # Creamos informacion falsa
    fake = Faker('es-ES')

    # Generamos los usuarios
    num_usuarios = 50
    for num in range(num_usuarios):
        temp_fake = fake.simple_profile()
        my_user = User()
        my_user.username=temp_fake['username']
        my_user.email=temp_fake['mail']
        my_user.password=generate_password_hash('123')
        my_user.is_active=True
        db.session.add(my_user)
    db.session.commit()
    print('Usuarios falsos creados')

    # Generamos categorias
    num_categorias = 10
    for num in range(num_categorias):
        my_categoria = Categorias()
        my_categoria.name = fake.word()
        db.session.add(my_categoria)
    db.session.commit()
    print('Categorias falsas generadas')


      # Generamos tags
    num_tags = 10
    for num in range(num_tags):
        my_tag = Tag()
        my_tag.name = fake.word()
        db.session.add(my_tag)
    db.session.commit()
    print('Tags falsos generados')

    # Generamos articulos
    num_articulos = 150
    for num in range(num_articulos):
        my_articulo = Articulos()
        my_articulo.title = fake.sentence()
        my_articulo.text = fake.text(max_nb_chars=10000)
        my_articulo.categoria_id = randint(1, num_categorias)
        my_articulo.user_id = randint(1, num_usuarios)
        # Creamos relaciones aleatorias
        my_range = random.sample(range(1,10), 5)
        for tag_id in my_range:
            my_articulo.tags.append(Tag.query.get(tag_id))
        db.session.add(my_articulo)
    db.session.commit()
    print('Articulos falsos generados')  

    # Generamos relaciones de tags
    num_relaciones_tags = 4   


if __name__ == '__main__':
    manager.run()