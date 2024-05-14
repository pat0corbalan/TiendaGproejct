from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from models.business import BusinessManagement

app = Flask(__name__)
app.secret_key = 'password'
UPLOAD_FOLDER = os.path.join('static', 'uploads', 'productos')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, subfolder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        subfolder_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        path = os.path.join(subfolder_path, filename)
        file.save(path)
        return path
    return None

@app.route("/")
def index():
    nombre_negocio = request.args.get('negocio') or session.get('negocio_actual', 'negocio1')
    session['negocio_actual'] = nombre_negocio
    print("Negocio actual en sesión:", nombre_negocio)
    return redirect(url_for('mostrar_negocio', nombre_negocio=nombre_negocio))

@app.route("/<nombre_negocio>")
def mostrar_negocio(nombre_negocio):
    business = BusinessManagement()
    negocio_config = session.get('negocio_config', {}).get(nombre_negocio)
    if not negocio_config:
        negocio_config = business.get_negocio(nombre_negocio)
        if negocio_config:
            session.setdefault('negocio_config', {})[nombre_negocio] = negocio_config
        else:
            return "Negocio no encontrado", 404
    productos = business.get_productos(negocio_config['id'])
    return render_template("base.html", negocio=negocio_config, productos=productos)

@app.route("/agregar_negocio", methods=["GET", "POST"])
def agregar_negocio():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        contacto = request.form.get("contacto")
        ubicacion = request.form.get("ubicacion")
        horarios = request.form.get("horarios")
        rubro = request.form.get("rubro")
        
        logo_file = request.files['logo']
        imagen_file = request.files['imagen']
        
        logo_path = save_file(logo_file, 'logo')
        imagen_path = save_file(imagen_file, 'imagen')
        
        business = BusinessManagement()
        business.add_negocio(nombre, descripcion, contacto, imagen_path, ubicacion, horarios, rubro, logo_path)
        
        return redirect(url_for("mostrar_negocio", nombre_negocio=nombre))
    
    return render_template("agregar_negocio.html")

@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_productos():
    if request.method == "POST":
        nombre_producto = request.form.get("nombre_producto")
        negocio_id = request.form.get("negocio_id")
        variation_names = request.form.getlist("variation[name][]")
        variation_prices = request.form.getlist("variation[price][]")
        variation_descriptions = request.form.getlist("variation[description][]")
        variation_images = request.files.getlist("variation[image][]")

        business = BusinessManagement()
        producto_id = business.add_product(nombre_producto, negocio_id)

        for name, price, description, image in zip(variation_names, variation_prices, variation_descriptions, variation_images):
            image_filename = save_file(image, 'variaciones')
            business.add_variation(producto_id, name, price, description, image_filename)
        
        negocio = business.get_negocio(negocio_id)
        if negocio:
            return redirect(url_for('mostrar_negocio', nombre_negocio=negocio['nombre']))
    
    negocios = BusinessManagement().obtener_negocios()
    return render_template("agregar_producto.html", negocios=negocios)

@app.route("/negocio/<nombre_negocio>/producto/<int:product_id>")
def mostrar_producto(nombre_negocio, product_id):
    business = BusinessManagement()
    product = business.get_product(product_id)

    if not product:
        return "Producto no encontrado", 404

    return render_template("mostrar_producto.html", nombre_negocio=nombre_negocio, product=product)

@app.route("/realizar_pedido", methods=["GET", "POST"])
def realizar_pedido():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        metodo_pago = request.form.get("metodo_pago")
        metodo_entrega = request.form.get("metodo_entrega")
        aclaraciones = request.form.get("aclaraciones")

        business = BusinessManagement()
        nuevo_pedido = business.make_order(nombre=nombre, metodo_pago=metodo_pago, metodo_entrega=metodo_entrega, aclaraciones=aclaraciones)
        business.save_pedido(nuevo_pedido)

        return jsonify({"message": "Pedido realizado correctamente"})

    return render_template("realizar_pedido.html")

if __name__ == "__main__":
    app.run(debug=True)
