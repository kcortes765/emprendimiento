"""mock_data.py
Genera datos simulados para rutas, comercios y usuarios.
"""
from __future__ import annotations

from faker import Faker
import random

fake = Faker("es_CL")

# ---------------------- Nombres de calles reales (Antofagasta) ---------

AVENIDAS_ANTOFAGASTA = [
    "Avenida Edmundo Pérez Zujovic",
    "Avenida Séptimo de Línea",
    "Avenida Aníbal Pinto",
    "Avenida José Manuel Balmaceda",
    "Avenida Grecia",
    "Avenida República de Croacia",
    "Avenida Ejército",
    "Avenida Jaime Guzmán",
    "Avenida Padre Alberto Hurtado",
    "Avenida Argentina"
]

# ---------------------- Comercios asociados -------------------------------

COMERCIOS = [
    {"nombre": "Líder", "logo": "🛒", "puntos_necesarios": 500},
    {"nombre": "Servipag", "logo": "💳", "puntos_necesarios": 300},
    {"nombre": "Cinemark", "logo": "🎬", "puntos_necesarios": 700},
    {"nombre": "Juan Valdez", "logo": "☕", "puntos_necesarios": 200},
]

# ---------------------- Rutas simuladas -----------------------------------

ROUTES = [] # Será poblado por la nueva función

def generate_routes(n: int = 20):
    """Lista de rutas con origen, destino y distancia aproximada, usando nombres reales."""
    routes = []
    for _ in range(n):
        origen = random.choice(AVENIDAS_ANTOFAGASTA)
        # Asegurarse de que el destino no sea el mismo que el origen para más realismo
        destino_options = [av for av in AVENIDAS_ANTOFAGASTA if av != origen]
        if not destino_options: # En caso de que solo haya una avenida (poco probable aquí)
            destino = origen
        else:
            destino = random.choice(destino_options)
        
        distancia = round(random.uniform(2, 15), 1)
        routes.append({"origen": origen, "destino": destino, "dist_km": distancia})
    return routes

ROUTES = generate_routes()
