import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import math

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="3D Solar System",
    page_icon="🌌",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at center, #020617, #000000);
    color: white;
}

.title {
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#facc15;
}

.subtitle {
    text-align:center;
    font-size:22px;
    color:white;
    margin-bottom:20px;
}

.timebox {
    text-align:center;
    font-size:24px;
    padding:15px;
    border-radius:15px;
    background:rgba(255,255,255,0.08);
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.markdown('<div class="title">🌌 3D Solar System Simulation</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Real-Time Planetary Motion Simulation</div>',
    unsafe_allow_html=True
)

# ---------------- CURRENT TIME ----------------

now = datetime.now()

st.markdown(
    f'''
    <div class="timebox">
    📅 Date: {now.strftime("%d-%m-%Y")} <br>
    🕒 Time: {now.strftime("%H:%M:%S")}
    </div>
    ''',
    unsafe_allow_html=True
)

# ---------------- PLANET DATA ----------------

planets = {
    "Mercury": {"distance": 0.4, "size": 5, "color": "gray", "speed": 4.8},
    "Venus": {"distance": 0.7, "size": 8, "color": "orange", "speed": 3.5},
    "Earth": {"distance": 1.0, "size": 9, "color": "blue", "speed": 3.0},
    "Mars": {"distance": 1.5, "size": 7, "color": "red", "speed": 2.4},
    "Jupiter": {"distance": 2.5, "size": 18, "color": "brown", "speed": 1.3},
    "Saturn": {"distance": 3.5, "size": 16, "color": "gold", "speed": 1.0},
    "Uranus": {"distance": 4.5, "size": 13, "color": "lightblue", "speed": 0.7},
    "Neptune": {"distance": 5.5, "size": 13, "color": "darkblue", "speed": 0.5},
}

# ---------------- TIME VARIABLE ----------------

t = now.timestamp() / 100000

# ---------------- CREATE FIGURE ----------------

fig = go.Figure()

# ---------------- SUN ----------------

fig.add_trace(go.Scatter3d(
    x=[0],
    y=[0],
    z=[0],
    mode='markers+text',
    marker=dict(size=30, color='yellow'),
    text=["Sun"],
    textposition="top center",
    name="Sun"
))

# ---------------- PLANETS ----------------

for planet, data in planets.items():

    angle = t * data["speed"]

    x = data["distance"] * math.cos(angle)
    y = data["distance"] * math.sin(angle)
    z = 0

    # Planet orbit
    theta = np.linspace(0, 2*np.pi, 200)

    orbit_x = data["distance"] * np.cos(theta)
    orbit_y = data["distance"] * np.sin(theta)
    orbit_z = np.zeros_like(theta)

    fig.add_trace(go.Scatter3d(
        x=orbit_x,
        y=orbit_y,
        z=orbit_z,
        mode='lines',
        line=dict(color='white', width=1),
        showlegend=False
    ))

    # Planet
    fig.add_trace(go.Scatter3d(
        x=[x],
        y=[y],
        z=[z],
        mode='markers+text',
        marker=dict(
            size=data["size"],
            color=data["color"]
        ),
        text=[planet],
        textposition="top center",
        name=planet
    ))

# ---------------- LAYOUT ----------------

fig.update_layout(
    paper_bgcolor='black',
    plot_bgcolor='black',
    scene=dict(
        bgcolor='black',
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        zaxis=dict(
            visible=False
        )
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=800
)

# ---------------- DISPLAY ----------------

st.plotly_chart(fig, use_container_width=True)

# ---------------- FOOTER ----------------

st.markdown(
    """
    <div style='text-align:center; padding:20px;'>
    🚀 Built with Streamlit + Plotly
    </div>
    """,
    unsafe_allow_html=True
)
