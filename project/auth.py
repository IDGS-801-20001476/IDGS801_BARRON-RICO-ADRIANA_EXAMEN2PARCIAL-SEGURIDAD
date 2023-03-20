
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from . models import User
from . import db, userDataStore

auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    correo = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(correo=correo).first()    

    if not user or not check_password_hash(user.contrasenia, password):
    
        flash('El usuario y/o la contraseña son incorrectos')
        return redirect(url_for('auth.login')) 
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    #Cerramos la sessión
    logout_user()
    return redirect(url_for('main.index'))



@auth.route('/contacto')
def contacto():    
    return render_template('contacto.html')

