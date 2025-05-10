"""logic.py
Funciones de cálculo y simulación de la demo EcoRide.
Todas las magnitudes están en unidades locales (CLP, km, kg CO₂, puntos).
Esta capa mantiene la lógica de negocio separada de la interfaz Streamlit.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

# ------------------------- Configuración global -----------------------------

# Parámetros aproximados para un auto privado en Antofagasta
FUEL_PRICE_CLP = 1300          # $/litro promedio 2025 (demo)
FUEL_EFFICIENCY_KM_PER_L = 12  # km por litro
CAR_CO2_KG_PER_KM = 0.192      # kg CO₂ por km (fuente: IPCC promedio)

# Transporte público
BUS_CO2_KG_PER_KM = 0.089      # kg CO₂ por pasajero-km (fuente: promedio OCDE)
BUS_COST_CLP_PER_KM = 80       # Tarifa estimada prorrateada por km (demo)

# Bicicleta: sin emisiones y prácticamente sin costo

# Conversión de beneficios a puntos
CLP_TO_POINTS = 0.1            # 1 punto por cada $10 ahorrados
CO2_TO_POINTS = 5              # 5 puntos por cada kg CO₂ evitado

# ---------------------------------------------------------------------------

@dataclass
class OptionResult:
    """Resultado del cálculo de una alternativa de transporte."""
    mode: str  # "Auto", "Bus", "Carpool", "Bicicleta"
    cost_clp: float
    co2_kg: float
    time_min: float  # Tiempo de viaje estimado (no crítico para demo)

    def as_dict(self) -> dict:
        return {
            "Modo": self.mode,
            "Costo (CLP)": round(self.cost_clp, 0),
            "CO₂ (kg)": round(self.co2_kg, 2),
            "Tiempo (min)": round(self.time_min, 0),
        }

# ------------------------- Funciones de cálculo ----------------------------


def _car_cost(distance_km: float, fuel_price: float = FUEL_PRICE_CLP) -> float:
    """Costo en CLP para recorrido en auto particular."""
    litres = distance_km / FUEL_EFFICIENCY_KM_PER_L
    return litres * fuel_price


def _car_co2(distance_km: float) -> float:
    """Emisiones de CO₂ en kg para recorrido en auto particular."""
    return distance_km * CAR_CO2_KG_PER_KM


def _bus_cost(distance_km: float) -> float:
    return distance_km * BUS_COST_CLP_PER_KM


def _bus_co2(distance_km: float) -> float:
    return distance_km * BUS_CO2_KG_PER_KM


def _carpool_cost(distance_km: float, n_passengers: int = 3, fuel_price: float = FUEL_PRICE_CLP) -> float:
    """Costo por pasajero al compartir auto entre *n* pasajeros."""
    return _car_cost(distance_km, fuel_price) / n_passengers


def _carpool_co2(distance_km: float, n_passengers: int = 3) -> float:
    """Emisiones por pasajero al compartir auto."""
    return _car_co2(distance_km) / n_passengers


def calculate_options(distance_km: float, n_passengers: int = 3, fuel_price: float = FUEL_PRICE_CLP) -> list[OptionResult]:
    """Calcula las cuatro alternativas para un trayecto dado.

    Permite ajustar el número de pasajeros en Carpool para reflejar
    escenarios más o menos compartidos.
    """
    travel_time_base = distance_km / 35 * 60  # min, 35 km/h promedio urbano

    return [
        OptionResult("Auto", _car_cost(distance_km, fuel_price), _car_co2(distance_km), travel_time_base),
        OptionResult("Bus", _bus_cost(distance_km), _bus_co2(distance_km), travel_time_base * 1.2),
        OptionResult(
            "Carpool",
            _carpool_cost(distance_km, n_passengers, fuel_price),
            _carpool_co2(distance_km, n_passengers),
            travel_time_base,
        ),
        OptionResult("Bicicleta", 0, 0, travel_time_base * 2),
    ]


# -------------------- Conversión de beneficios a puntos --------------------

def benefits_vs_auto(
    distance_km: float,
    chosen: OptionResult,
    n_passengers: int = 3,
    fuel_price: float = FUEL_PRICE_CLP,
) -> tuple[float, float, int]:
    """Diferencia de costos y CO₂ respecto al automóvil.

    Devuelve (ahorro_clp, co2_evitatado_kg, puntos_generados)
    """
    auto = calculate_options(distance_km, n_passengers, fuel_price)[0]  # index 0 es "Auto"
    ahorro = auto.cost_clp - chosen.cost_clp
    co2_ev = auto.co2_kg - chosen.co2_kg

    puntos = int(ahorro * CLP_TO_POINTS + co2_ev * CO2_TO_POINTS)
    return ahorro, co2_ev, max(puntos, 0)


# -------------------- Utilidades de simulación -----------------------------

def random_distance() -> float:
    """Distancia aleatoria 2-15 km para demo."""
    return round(random.uniform(2, 15), 1)
