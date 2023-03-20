import os
import uuid
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from project.models import Role, Producto
from werkzeug.utils import secure_filename

from . import db

main = Blueprint('main',__name__)


#Definimos la ruta a la página principal
@main.route('/')
def index():
    return render_template('index.html')


@main.route('/administrador')
@login_required
@roles_required('admin')
def gestion():   
    producto= Producto.query.all()
    return render_template('ABCProductos.html',producto=producto)


@main.route('/insertar', methods=['GET','POST'])
@login_required
@roles_required('admin')
def insertar():
  if request.method == 'POST':
      nombre = request.form.get('nombre') 
      descripcion = request.form.get('descripcion')
      precio = request.form.get('precio')
      img = str(uuid.uuid4()) + '.png'
      imagen = request.files['imagen']
      ruta_imagen = os.path.abspath('project\\static\\img')
      imagen.save(os.path.join(ruta_imagen, img))       
  
      producto_registrar = Producto(nombre=nombre, descripcion=descripcion, precio=precio, imagen=img) 
    
      db.session.add(producto_registrar)
    
      db.session.commit()
      flash('El producto se ha registrado correctamente!')
    
      return redirect(url_for('main.gestion'))
    
  return render_template('insertar.html')


@main.route('/modificar', methods=['GET', 'POST'])
@login_required
def modificar():
    if request.method == 'GET':
        id = request.args.get('id')
        producto = Producto.query.get(id)
        print(producto)
        if producto is None:
            flash("El producto no existe", "error")
            return redirect(url_for('main.gestion'))
        if not producto.imagen:
            producto.imagen = 'default.png'
        return render_template('modificar.html', producto=producto,id=id)
    
    elif request.method == 'POST':
        id = request.args.get('id')
        producto = Producto.query.get(id)
        print(producto)
        if producto is None:
            flash("El producto no existe")
            return redirect(url_for('main.admin'))
        producto.nombre = request.form.get('nombre') 
        producto.descripcion = request.form.get('descripcion')
        producto.precio = request.form.get('precio')
        imagen = request.files['imagen']
        ruta_imagen = os.path.abspath('project\\static\\img')        
        if imagen:           
            os.remove(os.path.join(ruta_imagen, producto.imagen))
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(ruta_imagen, filename))
            producto.imagen = filename
        db.session.commit()
        flash("El registro se ha modificado exitosamente.")
        return redirect(url_for('main.gestion'))


@main.route('/eliminar', methods=['GET','POST'])
@login_required
def eliminar():
     if request.method == 'GET':
        id = request.args.get('id')
        producto = Producto.query.get(id)
        print(producto)
        if producto is None:
            flash("El producto no existe", "error")
            return redirect(url_for('main.gestion'))
        if not producto.imagen:
            producto.imagen = 'default.png'
        return render_template('eliminar.html', producto=producto,id=id)
    
     elif request.method == 'POST':
        id = request.args.get('id')
        producto = Producto.query.get(id)
        print(producto)
        if producto is None:
            flash("El producto no existe")
            return redirect(url_for('main.gestion'))
        producto.nombre = request.form.get('nombre') 
        producto.descripcion = request.form.get('descripcion')
        producto.precio = request.form.get('precio')
        imagen = request.files['imagen']
        ruta_imagen = os.path.abspath('project\\static\\img')        
        if imagen:
            os.remove(os.path.join(ruta_imagen, producto.imagen))
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(ruta_imagen, filename))
            producto.imagen = filename
     db.session.delete(producto)
     db.session.commit()
     flash("El registro se ha eliminado exitosamente.")
     return redirect(url_for('main.gestion')) 

    
   
@main.route('/catalogo')
@login_required
def catalogo():
    productos= Producto.query.all()
    
    if len(productos )==0:
       productos=0
        
    return render_template('catalogo.html',productos=productos)



    







