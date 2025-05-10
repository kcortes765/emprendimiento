# Plan de desarrollo EcoRide

## Objetivo general
Construir una demo web interactiva (solo frontend) que muestre de forma clara y atractiva los beneficios económicos y ambientales de reemplazar el auto por opciones sostenibles en Antofagasta.

## MVP (alcance actual)
1. **Dashboard** con métricas acumuladas de ahorro, CO₂ y puntos.
2. **Comparador de rutas**: selección de trayectos simulados, tabla de costos y opción favorita.
3. **Catálogo de Ecopoints**: tarjetas de comercios y canje simulado.
4. **Reporte resumen** con tabla final y metodología.
5. **Mapa Folium** dentro de `st.expander`.

## Tareas pendientes
- [ ] Graficar evolución de puntos con `matplotlib` o `altair`.
- [ ] Animar actualización de métrica con efecto confeti.
- [ ] Validar parámetros de emisiones con fuentes locales.
- [ ] Internacionalizar textos (i18n).

## Futuro
- Conexión a APIs reales de rutas y tiempo de viaje.
- Base de datos para persistir usuarios y viajes.
