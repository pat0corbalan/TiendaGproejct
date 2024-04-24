import sqlite3

class BusinessManagement:
    def __init__(self):
        self.conn = sqlite3.connect('tienda.db')
        self.cursor = self.conn.cursor()

    def get_negocio(self, nombre_negocio):
        query = "SELECT * FROM negocios WHERE nombre = ?"
        self.cursor.execute(query, (nombre_negocio,))
        row = self.cursor.fetchone()
        if row:
            negocio_config = {
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'contacto': row[3],
                'imagen': row[4],
                'ubicacion': row[5],
                'horarios': row[6],
                'rubro': row[7],
                'logo': row[8]
            }
            return negocio_config
        else:
            return None

    def add_negocio(self, nombre, descripcion, contacto, imagen, ubicacion, horarios, rubro, logo):
        query = "INSERT INTO negocios (nombre, descripcion, contacto, imagen, ubicacion, horarios, rubro, logo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (nombre, descripcion, contacto, imagen, ubicacion, horarios, rubro, logo))
        self.conn.commit()

    def add_product(self, product_name, negocio_id):
        query = "INSERT INTO Products (ProductName, NegocioID) VALUES (?, ?)"
        self.cursor.execute(query, (product_name, negocio_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_variation(self, product_id, variation_name, variation_price, variation_description, variation_image):
        try:
            query = "INSERT INTO Variations (ProductID, VariationName, VariationPrice, VariationDescription, VariationImg) VALUES (?, ?, ?, ?, ?)"
            self.cursor.execute(query, (product_id, variation_name, variation_price, variation_description, variation_image))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print("Error inserting variation:", e)
            return None

    def get_productos(self, negocio_id):
        query = "SELECT * FROM Products WHERE NegocioID = ?"
        self.cursor.execute(query, (negocio_id,))
        productos = []
        for row in self.cursor.fetchall():
            producto = {
                'id': row[0],
                'nombre': row[1],
                'variedades': self.get_variedades(row[0])  # Obtener las variedades de cada producto
            }
            productos.append(producto)
        return productos
    
    def get_variedades(self, product_id):
        query = "SELECT * FROM Variations WHERE ProductID = ?"
        self.cursor.execute(query, (product_id,))
        variedades = []
        for row in self.cursor.fetchall():
            variedad = {
                'id': row[0],
                'nombre': row[2],
                'precio': row[3],
                'descripcion': row[4],
                'imagen': row[5]
            }
            variedades.append(variedad)
        return variedades
    
    def make_order(self, nombre, metodo_pago, metodo_entrega, aclaraciones):
        query = "INSERT INTO pedidos (nombre, metodo_pago, metodo_entrega, aclaraciones) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (nombre, metodo_pago, metodo_entrega, aclaraciones))
        self.conn.commit()
        return "Pedido creado correctamente"

    def save_pedido(self, nuevo_pedido):
        # Aquí puedes implementar la lógica para guardar el pedido en tu base de datos
        pass
    
    def guardar_producto(self, nombre, descripcion, imagen, precio_base, negocio_id):
        # Insertar el producto en la base de datos y obtener su ID
        query = "INSERT INTO productos (nombre, descripcion, imagen, precio_base, negocio_id) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (nombre, descripcion, imagen, precio_base, negocio_id))
        self.conn.commit()
        producto_id = self.cursor.lastrowid
        return producto_id
        
    def obtener_negocios(self):
        query = "SELECT id, nombre FROM negocios"
        self.cursor.execute(query)
        negocios = []
        for row in self.cursor.fetchall():
            negocio = {
                'id': row[0],
                'nombre': row[1]
            }
            negocios.append(negocio)
        return negocios
        
    def __del__(self):
        self.conn.close()
