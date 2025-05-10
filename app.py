"""app.py
Demo interactiva EcoRide construida con Streamlit.
El objetivo es mostrar de manera atractiva el beneficio económico y ambiental de
cambiar el auto por transporte sostenible en Antofagasta.
No requiere backend ni login; todos los datos viven en memoria.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from logic import calculate_options, benefits_vs_auto, random_distance, OptionResult, FUEL_PRICE_CLP
from mock_data import COMERCIOS, ROUTES

st.set_page_config(page_title="EcoRide Demo", page_icon="🚲", layout="centered")

st.markdown(
    '<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">',
    unsafe_allow_html=True
)

# -------------------- Ajustes Avanzados -----------------------------
with st.expander("🔧 Ajustes avanzados"):
    st.write(f"Precio combustible actual: {FUEL_PRICE_CLP} CLP/L")
    n_passengers = st.slider("Pasajeros en carpool", 2, 5, 3)

st.title("🚲 EcoRide – Ahorra y cuida el planeta")

# -------------------- Dashboard Resumen -----------------------------------

st.header("📊 Dashboard")

# Inputs simulados acumulados
if "total_ahorro" not in st.session_state:
    st.session_state.total_ahorro = 0.0
    st.session_state.total_co2 = 0.0
    st.session_state.total_puntos = 0
    st.session_state.puntos_history = [] # Para el gráfico de evolución

col1, col2, col3 = st.columns(3)
col1.metric("💰 Ahorro acumulado", f"${st.session_state.total_ahorro:,.0f}")
col2.metric("🌱 CO₂ evitado", f"{st.session_state.total_co2:.1f} kg")
col3.metric("🏅 Ecopoints", f"{st.session_state.total_puntos}")

st.divider()

# -------------------- Comparador de rutas ---------------------------------

st.header("🛣️ Comparador de rutas")

# Selección random de ruta para demo (podría ser selectbox con ROUTES)
ruta = st.selectbox(
    "Elige una ruta simulada", [f"{r['origen']} ➡ {r['destino']} ({r['dist_km']} km)" for r in ROUTES]
)
idx = st.session_state.get("ruta_idx", 0)
idx = [f"{r['origen']} ➡ {r['destino']} ({r['dist_km']} km)" for r in ROUTES].index(ruta)
distance_km = ROUTES[idx]["dist_km"]

options = calculate_options(distance_km, n_passengers=n_passengers)

df = pd.DataFrame([o.as_dict() for o in options])
st.dataframe(df, use_container_width=True, hide_index=True)

# Selección de opción
chosen_mode = st.radio("Elige tu alternativa preferida", df["Modo"].tolist(), index=1)
chosen = next(o for o in options if o.mode == chosen_mode)

ahorro, co2_ev, pts = benefits_vs_auto(
    distance_km,
    chosen,
    n_passengers=n_passengers,
)

if st.button("✅ Simular viaje y sumar puntos"):
    st.session_state.total_ahorro += ahorro
    st.session_state.total_co2 += co2_ev
    st.session_state.total_puntos += pts
    st.session_state.puntos_history.append(st.session_state.total_puntos) # Añadir al historial
    st.success(f"¡Has ganado {pts} puntos! Ahorro: ${ahorro:,.0f}, CO₂ evitado: {co2_ev:.1f} kg")
    st.rerun() # Forzar recarga para ver el gráfico actualizado inmediatamente

# Mapa Folium
with st.expander("Ver mapa de referencia"):
    m = folium.Map(location=[-23.65, -70.4], zoom_start=12)
    folium.Marker([-23.65, -70.4], tooltip="Antofagasta").add_to(m)
    st_folium(m, height=300, width=700)

st.divider()

# -------------------- Catálogo de Ecopoints -------------------------------

st.header("🏬 Catálogo Ecopoints")

cols = st.columns(len(COMERCIOS))
for c, comercio in zip(cols, COMERCIOS):
    with c:
        st.markdown(
            f"""<div class=\"bg-white shadow-lg p-4 rounded-lg text-center\">""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<h3 class=\"text-lg font-semibold\">{comercio['logo']} {comercio['nombre']}</h3>
<p>Requiere <strong>{comercio['puntos_necesarios']} pts</strong></p>""",
            unsafe_allow_html=True,
        )
        if st.button("Canjear", disabled=st.session_state.total_puntos < comercio['puntos_necesarios'], key=comercio['nombre']):
            st.session_state.total_puntos -= comercio['puntos_necesarios']
            if "redeemed" not in st.session_state:
                st.session_state.redeemed = []
            st.session_state.redeemed.append(comercio['nombre'])
            st.success(f"¡Has canjeado {comercio['puntos_necesarios']} pts por {comercio['nombre']}!")
        st.markdown("</div>", unsafe_allow_html=True)

if "redeemed" in st.session_state and st.session_state.redeemed:
    st.write("**Tus canjes:**")
    for item in st.session_state.redeemed:
        st.write(f"- {item}")

st.divider()

# -------------------- Reporte Resumen -------------------------------------

st.header("📑 Reporte resumen")

st.write("**Resultados acumulados:**")
report_df = pd.DataFrame({
    "Indicador": ["Ahorro CLP", "CO₂ evitado (kg)", "Ecopoints"],
    "Valor": [round(st.session_state.total_ahorro, 0), round(st.session_state.total_co2, 1), st.session_state.total_puntos],
})
st.table(report_df)

st.write("**Evolución de Ecopoints:**")
if st.session_state.puntos_history:
    # Crear un DataFrame para el gráfico de líneas con un índice adecuado
    chart_df = pd.DataFrame({
        'Viaje N°': range(1, len(st.session_state.puntos_history) + 1),
        'Ecopoints Acumulados': st.session_state.puntos_history
    })
    st.line_chart(chart_df.set_index('Viaje N°'))
else:
    st.caption("Simula tu primer viaje para ver la evolución de tus puntos.")

st.write("---")

with st.expander("ℹ️ Metodología de cálculo"):
    st.markdown(
        """
        * Los valores de costo de combustible y emisiones son promedios referenciales.
        * El ahorro y CO₂ evitado se calculan comparando la opción elegida con un auto
          particular de rendimiento 12 km/L y emisiones 0,192 kg CO₂/km.
        * Ecopoints = 1 punto por cada $10 de ahorro + 5 puntos por cada kg de CO₂ evitado.
        """
    )
