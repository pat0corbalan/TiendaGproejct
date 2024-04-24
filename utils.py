from app.models import Producto

def obtener_productos(negocio):
    productos = Producto.query.filter_by(negocio=negocio).all()
    return productos
