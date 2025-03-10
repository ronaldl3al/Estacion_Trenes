# models/estacion.py
class Estacion:
    def __init__(self, operador, contrasena, nombre, horarios, precio):
        self.operador = operador
        self.contrasena = contrasena
        self.nombre = nombre
        self.horarios = horarios
        self.precio = precio
        self.estado = "Activo"
        self.boletos_vendidos = 0
        self.ventas = []

admin_credentials = {
    "operador": "admin",
    "contrasena": "123"
}

estaciones = [
    Estacion("operador1", "123", "Centro", ["09:00", "13:00", "17:00"], 1.0),
    Estacion("operador2", "123", "Barrio Obrero", ["10:00", "14:00", "18:00"], 1.0),
    Estacion("operador3", "123", "Barrio 1", ["10:00", "14:00", "18:00"], 1.0)
]

usuario_actual = None
