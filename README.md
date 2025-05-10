# EcoRide – Demo interactiva 🚲

Aplicación de demostración hecha con **Streamlit** para ilustrar
los beneficios económicos y ambientales de reemplazar el auto por
alternativas sostenibles en Antofagasta.

> 👉 **Solo frontend mock.** No hay backend, login ni base de datos.
>
> Cualquier *stakeholder* puede clonar el repo, instalar dependencias y
> ejecutar `streamlit run app.py`.

---

## Estructura del Proyecto

```
eco_ride/
├─ app.py              # Interfaz Streamlit
├─ logic.py            # Lógica de negocio y cálculos
├─ mock_data.py        # Datos fake (rutas, comercios)
├─ requirements.txt    # Dependencias exactas
└─ README.md           # Este archivo
```

## Instalación rápida

```bash
python -m venv venv
source venv/bin/activate          # Windows: .\\venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Tecnologías clave

| Capa          | Tecnología  | Motivo                                     |
|---------------|-------------|--------------------------------------------|
| Frontend      | Streamlit   | UI rápida en Python, sin HTML ni JS        |
| Mapas         | Folium      | Mapa estático de Antofagasta               |
| Estilos       | TailwindCSS | CDN via `st.markdown` para look & feel     |
| Datos fake    | Faker       | Simulación realista de rutas y comercios   |
| Análisis      | Pandas      | Manipulación tabular de resultados         |

---

## Roadmap sugerido

- [ ] Agregar gráficos de líneas para evolución histórica.
- [ ] Conectar a API real de rutas (e.g., Google Directions).
- [ ] Persistir usuarios y puntos en base de datos.

¡Contribuciones y feedback son bienvenidos! ✉️ 
