# models/estacion.py

class Tren:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad  # Capacidad total del tren
        self.boletos_vendidos = 0

    def vender_boletos(self, cantidad):
        if self.boletos_vendidos + cantidad > self.capacidad:
            raise Exception("Capacidad insuficiente en el tren")
        self.boletos_vendidos += cantidad  # Se incrementan los boletos vendidos

    def capacidad_disponible(self):
        return self.capacidad - self.boletos_vendidos  # Disminuye a medida que se venden boletos

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

        self.trenes = [
            Tren("Tren 1", 80),
            Tren("Tren 2", 80),
            Tren("Tren 3", 80)
        ]

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
