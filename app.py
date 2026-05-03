import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math
from datetime import datetime
import random

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Solar System",
    page_icon="🌌",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at center, #000814, #000000);
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
    font-size:24px;
    color:white;
    margin-bottom:20px;
}

.info {
    text-align:center;
    padding:15px;
    background:rgba(255,255,255,0.08);
    border-radius:15px;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.markdown(
    '<div class="title">🌌 My Solar System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Interactive Planetary</div>',
    unsafe_allow_html=True
)

# ---------------- CURRENT TIME ----------------

now = datetime.now()

st.markdown(
    f"""
    <div class="info">
    📅 Date: {now.strftime('%d-%m-%Y')}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR CONTROLS ----------------

st.sidebar.header("🎮 Controls")

speed_multiplier = st.sidebar.slider(
    "Planet Speed",
    0.1,
    10.0,
    1.0
)

show_stars = st.sidebar.checkbox("🌠 Stars Background", True)
show_asteroids = st.sidebar.checkbox("☄️ Asteroid Belt", True)
show_moon = st.sidebar.checkbox("🛰️ Moon Orbit", True)

# ---------------- PLANET DATA ----------------

planets = {
    "Mercury": {"distance": 0.4, "size": 5, "color": "gray", "speed": 4.8},
    "Venus": {"distance": 0.7, "size": 8, "color": "orange", "speed": 3.5},
    "Me": {"distance": 1.0, "size": 9, "color": "blue", "speed": 3.0},
    "Mars": {"distance": 1.5, "size": 7, "color": "red", "speed": 2.4},
    "Jupiter": {"distance": 2.5, "size": 18, "color": "brown", "speed": 1.3},
    "Saturn": {"distance": 3.5, "size": 16, "color": "gold", "speed": 1.0},
    "Uranus": {"distance": 4.5, "size": 13, "color": "lightblue", "speed": 0.7},
    "Neptune": {"distance": 5.5, "size": 13, "color": "darkblue", "speed": 0.5},
}

# ---------------- TIME ----------------

t = now.timestamp() / 100000 * speed_multiplier

# ---------------- FIGURE ----------------

fig = go.Figure()

# ---------------- STARS ----------------

if show_stars:

    num_stars = 800

    star_x = np.random.uniform(-8, 8, num_stars)
    star_y = np.random.uniform(-8, 8, num_stars)
    star_z = np.random.uniform(-8, 8, num_stars)

    fig.add_trace(go.Scatter3d(
        x=star_x,
        y=star_y,
        z=star_z,
        mode='markers',
        marker=dict(
            size=1,
            color='white'
        ),
        showlegend=False
    ))

# ---------------- SUN ----------------

fig.add_trace(go.Scatter3d(
    x=[0],
    y=[0],
    z=[0],
    mode='markers+text',
    marker=dict(
        size=35,
        color='yellow'
    ),
    text=["☀️ Sun"],
    textposition="top center",
    name="Sun"
))

# ---------------- PLANETS ----------------

earth_x = 0
earth_y = 0

for planet, data in planets.items():

    angle = t * data["speed"]

    x = data["distance"] * math.cos(angle)
    y = data["distance"] * math.sin(angle)
    z = 0

    # Store Earth position
    if planet == "Me":
        earth_x = x
        earth_y = y

    # Orbit
    theta = np.linspace(0, 2*np.pi, 300)

    orbit_x = data["distance"] * np.cos(theta)
    orbit_y = data["distance"] * np.sin(theta)
    orbit_z = np.zeros_like(theta)

    fig.add_trace(go.Scatter3d(
        x=orbit_x,
        y=orbit_y,
        z=orbit_z,
        mode='lines',
        line=dict(
            color='white',
            width=1
        ),
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

    # Saturn Rings
    if planet == "Saturn":

        ring_theta = np.linspace(0, 2*np.pi, 200)

        ring_x = x + 0.35 * np.cos(ring_theta)
        ring_y = y + 0.35 * np.sin(ring_theta)
        ring_z = np.zeros_like(ring_theta)

        fig.add_trace(go.Scatter3d(
            x=ring_x,
            y=ring_y,
            z=ring_z,
            mode='lines',
            line=dict(
                color='gold',
                width=3
            ),
            showlegend=False
        ))

# ---------------- MOON ----------------

if show_moon:

    moon_angle = t * 12

    moon_x = earth_x + 0.15 * math.cos(moon_angle)
    moon_y = earth_y + 0.15 * math.sin(moon_angle)

    fig.add_trace(go.Scatter3d(
        x=[moon_x],
        y=[moon_y],
        z=[0],
        mode='markers+text',
        marker=dict(
            size=4,
            color='lightgray'
        ),
        text=["You"],
        textposition="top center",
        name="You"
    ))

# ---------------- ASTEROID BELT ----------------

if show_asteroids:

    asteroid_count = 300

    asteroid_x = []
    asteroid_y = []
    asteroid_z = []

    for _ in range(asteroid_count):

        angle = random.uniform(0, 2*np.pi)
        radius = random.uniform(1.9, 2.3)

        asteroid_x.append(radius * math.cos(angle))
        asteroid_y.append(radius * math.sin(angle))
        asteroid_z.append(random.uniform(-0.05, 0.05))

    fig.add_trace(go.Scatter3d(
        x=asteroid_x,
        y=asteroid_y,
        z=asteroid_z,
        mode='markers',
        marker=dict(
            size=2,
            color='gray'
        ),
        name="Asteroids"
    ))

# ---------------- LAYOUT ----------------

fig.update_layout(
    paper_bgcolor='black',
    plot_bgcolor='black',
    scene=dict(
        bgcolor='black',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False)
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=850
)

# ---------------- DISPLAY ----------------

st.plotly_chart(fig, use_container_width=True)


# ---------------- FOOTER ----------------

st.markdown(
    """
    <div style='text-align:center;padding:20px;'>
    🚀 Let's Go
    </div>
    """,
    unsafe_allow_html=True
)
