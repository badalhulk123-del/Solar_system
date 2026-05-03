import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math
import random
import time

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Solar System",
    page_icon="🌌",
    layout="wide"
)

# ---------------- TITLE ----------------

st.title("🌌Solar System")

st.markdown("### 🪐 Earth completes 1 orbit")

# ---------------- SIDEBAR ----------------

speed_multiplier = st.sidebar.slider(
    "Simulation Speed",
    0.1,
    5.0,
    1.0
)

# ---------------- PLANET DATA ----------------

planets = {
    "Mercury": {"distance": 0.4, "size": 5, "color": "gray", "orbit_days": 88},
    "Venus": {"distance": 0.7, "size": 8, "color": "orange", "orbit_days": 225},
    "Me": {"distance": 1.0, "size": 9, "color": "blue", "orbit_days": 365},
    "Mars": {"distance": 1.5, "size": 7, "color": "red", "orbit_days": 687},
    "Jupiter": {"distance": 2.5, "size": 18, "color": "brown", "orbit_days": 4333},
    "Saturn": {"distance": 3.5, "size": 16, "color": "gold", "orbit_days": 10759},
    "Uranus": {"distance": 4.5, "size": 13, "color": "lightblue", "orbit_days": 30687},
    "Neptune": {"distance": 5.5, "size": 13, "color": "darkblue", "orbit_days": 60190},
}

# ---------------- TIME SETTINGS ----------------

EARTH_ORBIT_SECONDS = 300  # 5 minutes

# ---------------- PLACEHOLDER ----------------

chart = st.empty()

# ---------------- ANIMATION LOOP ----------------

frame = 0

while True:

    fig = go.Figure()

    # ---------------- STARS ----------------

    num_stars = 600

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

    earth_x = 0
    earth_y = 0

    # ---------------- PLANETS ----------------

    for planet, data in planets.items():

        orbit_ratio = 365 / data["orbit_days"]

        angle = (
            frame
            * 0.02
            * orbit_ratio
            * speed_multiplier
        )

        x = data["distance"] * math.cos(angle)
        y = data["distance"] * math.sin(angle)
        z = 0

        # Earth position for moon
        if planet == "Me":
            earth_x = x
            earth_y = y

        # Orbit path
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
                color='rgba(255,255,255,0.2)',
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

        # Saturn rings
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

    moon_angle = frame * 0.25 * speed_multiplier

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

    asteroid_x = []
    asteroid_y = []
    asteroid_z = []

    for _ in range(300):

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
        showlegend=False
    ))

    # ---------------- LAYOUT ----------------

    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black',
        scene=dict(
            bgcolor='black',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(
                eye=dict(x=1.4, y=1.4, z=0.8)
            )
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=850
    )

    # ---------------- DISPLAY ----------------

    chart.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------- FRAME UPDATE ----------------

    frame += 1

    time.sleep(0.03)
