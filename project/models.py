from email.policy import default
from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

#Definiendo la tabla relacional entre usuarios roles
users_roles = db.Table('users_roles',
    db.Column('userId', db.Integer, db.ForeignKey('user.id')),
    db.Column('roleId', db.Integer, db.ForeignKey('role.id')))

class User(db.Model, UserMixin): 
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), unique=True)
    contrasenia = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    admin = db.Column(db.Boolean,default=0)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role',
            secondary=users_roles,
            backref= db.backref('usuarios', lazy='dynamic'))

class Role(RoleMixin, db.Model):
   __tablename__ = 'role'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50), nullable=False)
   descrition = db.Column(db.String(255))



class Producto(db.Model): 
   __tablename__ = 'Producto'
   id = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String(50), nullable=False)
   descripcion =  db.Column(db.String(255))
   precio = db.Column(db.Integer, nullable=False)
   imagen = db.Column(db.String(255), nullable=False)
   activo =  db.Column(db.Boolean, default=1)    

   def __init__(self, nombre, descripcion, precio, imagen): 
      self.nombre = nombre
      self.descripcion = descripcion
      self.precio = precio
      self.imagen = imagen   


    
    
    
    
    
    