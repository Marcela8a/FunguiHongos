

# Estructura básica del historial de compras del usuario sin marshmallow
class HistorialCompraSchema:
    def __init__(self, usuario_id, fecha, total, productos):
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.total = total
        self.productos = productos
