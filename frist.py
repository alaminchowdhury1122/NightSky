import math
import sys
import numpy as np
import pygame

# --- ASTRONOMICAL DATA (REAL-WORLD METRICS + ESTIMATED TOTALS) ---
COSMOS_SUMMARY = {
    "observable_estimate": "Few hundred billion to ~2 trillion galaxies",
    "catalogued_note": "Tens of millions catalogued; Euclid alone logged ~26M in DR1 (1.5B+ planned)",
    "observable_diameter": "93 billion light-years",
}

BODIES = [
    {
        "name": "Sun",
        "kind": "Star (G2V Main-Sequence)",
        "orbit_r": 0.0,
        "orbit_speed": 0.0,
        "radius": 24.0,
        "color": (255, 204, 64),
        "glow": (255, 150, 20),
        "distance": "0 AU (Solar System Center)",
        "temp": "5,500 °C (photosphere) / 15M °C (core)",
        "diameter": "1,392,700 km (109x Earth)",
        "details": "Contains 99.86% of the Solar System's mass. Fuses ~600 million tons of hydrogen into helium every second.",
    },
    {
        "name": "Mercury",
        "kind": "Terrestrial Planet",
        "orbit_r": 65.0,
        "orbit_speed": 0.022,
        "radius": 5.5,
        "color": (175, 170, 165),
        "glow": None,
        "distance": "0.39 AU (~58M km from Sun)",
        "temp": "-180 °C to 430 °C",
        "diameter": "4,879 km",
        "details": "Smallest planet with a massive iron core and virtually no atmosphere to hold heat.",
    },
    {
        "name": "Venus",
        "kind": "Terrestrial Planet",
        "orbit_r": 100.0,
        "orbit_speed": 0.015,
        "radius": 9.0,
        "color": (235, 195, 120),
        "glow": (210, 165, 85),
        "distance": "0.72 AU (~108M km from Sun)",
        "temp": "~465 °C (runaway greenhouse)",
        "diameter": "12,104 km",
        "details": "Rotates backward (retrograde) with thick sulfuric acid clouds and ~92x Earth's surface pressure.",
    },
    {
        "name": "Earth",
        "kind": "Terrestrial Planet",
        "orbit_r": 145.0,
        "orbit_speed": 0.010,
        "radius": 10.0,
        "color": (65, 155, 255),
        "glow": (70, 180, 255),
        "distance": "1.00 AU (~149.6M km from Sun)",
        "temp": "~15 °C global average",
        "diameter": "12,742 km",
        "details": "Only known world with liquid surface oceans, plate tectonics, a protective magnetosphere, and life.",
    },
    {
        "name": "Mars",
        "kind": "Terrestrial Planet",
        "orbit_r": 190.0,
        "orbit_speed": 0.008,
        "radius": 7.2,
        "color": (220, 95, 60),
        "glow": (190, 75, 45),
        "distance": "1.52 AU (~228M km from Sun)",
        "temp": "-63 °C average",
        "diameter": "6,779 km",
        "details": "Iron-oxide dust gives its rust hue; home to Olympus Mons and Valles Marineris.",
    },
    {
        "name": "Jupiter",
        "kind": "Gas Giant",
        "orbit_r": 265.0,
        "orbit_speed": 0.0045,
        "radius": 20.0,
        "color": (215, 175, 130),
        "glow": (180, 140, 100),
        "distance": "5.20 AU (~778M km from Sun)",
        "temp": "-110 °C (cloud tops)",
        "diameter": "139,820 km",
        "details": "Most massive planet (~2.5x all other planets combined), famous for zonal bands and the Great Red Spot.",
    },
    {
        "name": "Saturn",
        "kind": "Gas Giant",
        "orbit_r": 345.0,
        "orbit_speed": 0.0032,
        "radius": 16.5,
        "color": (230, 205, 145),
        "glow": None,
        "distance": "9.58 AU (~1.43B km from Sun)",
        "temp": "-140 °C (cloud tops)",
        "diameter": "116,460 km (excluding rings)",
        "details": "Iconic ice-and-rock ring system spanning hundreds of thousands of kilometers with low mean density.",
    },
]

GALAXIES = [
    {
        "name": "Milky Way",
        "gtype": "Barred Spiral (SBbc)",
        "pos": np.array([0.0, 0.0, 0.0]),
        "stars": "100–400 billion stars",
        "size": "~100,000 light-years across",
        "dist": "Home galaxy (Solar System ~27,000 ly from center)",
        "color": (150, 195, 255),
        "details": "Our home galaxy in the Local Group, featuring a central bar, spiral arms, and Sagittarius A* at its core.",
    },
    {
        "name": "Andromeda (M31)",
        "gtype": "Spiral (SA(s)b)",
        "pos": np.array([1400.0, 280.0, -1900.0]),
        "stars": "~1 trillion stars",
        "size": "~152,000 light-years across",
        "dist": "~2.5 million light-years from Earth",
        "color": (255, 210, 155),
        "details": "Largest major galaxy in the Local Group; visible to the naked eye in dark skies and approaching a merger.",
    },
    {
        "name": "Triangulum (M33)",
        "gtype": "Unbarred Spiral (SA(s)cd)",
        "pos": np.array([1750.0, -320.0, -1450.0]),
        "stars": "~40 billion stars",
        "size": "~60,000 light-years across",
        "dist": "~2.7–3.0 million light-years from Earth",
        "color": (140, 215, 255),
        "details": "Third-largest member of the Local Group and a rich star-forming spiral in the constellation Triangulum.",
    },
    {
        "name": "Sombrero (M104)",
        "gtype": "Unbarred Spiral / Lenticular",
        "pos": np.array([-1850.0, 450.0, -1600.0]),
        "stars": "~800 billion stars",
        "size": "~50,000 light-years across",
        "dist": "~29.3 million light-years from Earth",
        "color": (255, 225, 175),
        "details": "Known for its bright central bulge, prominent dust ring, and unusually large globular cluster system.",
    },
    {
        "name": "Messier 87 (M87)",
        "gtype": "Supergiant Elliptical (E0-1pec)",
        "pos": np.array([-1500.0, -520.0, 1750.0]),
        "stars": "Several trillion stars",
        "size": "~120,000 light-years across",
        "dist": "~53.5 million light-years from Earth",
        "color": (255, 190, 125),
        "details": "Anchor of the Virgo Cluster; houses M87*, the supermassive black hole first imaged by the Event Horizon Telescope.",
    },
    {
        "name": "Large Magellanic Cloud",
        "gtype": "Irregular Dwarf (SB(s)m)",
        "pos": np.array([420.0, -240.0, 520.0]),
        "stars": "~30 billion stars",
        "size": "~32,200 light-years across",
        "dist": "~163,000 light-years from Earth",
        "color": (165, 210, 255),
        "details": "Brightest satellite galaxy orbiting the Milky Way, prominent in the southern hemisphere sky.",
    },
]

# Bright night-sky stars & constellations for Human Sky View (azimuth_deg, alt_deg, mag_size, color, label)
SKY_STARS = [
    ("Sirius", 155, 28, 4.2, (195, 225, 255)),
    ("Betelgeuse", 115, 42, 3.8, (255, 155, 105)),
    ("Rigel", 132, 24, 3.9, (180, 215, 255)),
    ("Bellatrix", 112, 34, 2.5, (185, 220, 255)),
    ("Alnilam", 122, 33, 2.4, (195, 220, 255)),
    ("Polaris", 355, 58, 2.8, (255, 245, 215)),
    ("Vega", 65, 66, 3.6, (205, 230, 255)),
    ("Dubhe", 325, 64, 2.6, (255, 210, 160)),
    ("Merak", 318, 56, 2.3, (215, 230, 255)),
    ("Aldebaran", 92, 46, 3.2, (255, 165, 110)),
]

CONSTELLATION_LINES = [
    # Orion rough outline
    ((112, 34), (115, 42)),
    ((115, 42), (122, 33)),
    ((122, 33), (132, 24)),
    ((132, 24), (112, 34)),
    # Big Dipper / Ursa Major pointer
    ((318, 56), (325, 64)),
    ((325, 64), (355, 58)),
]


def generate_starfield(n_stars=2200, radius=4200.0, seed=42):
    rng = np.random.default_rng(seed)
    u = rng.uniform(-1, 1, n_stars)
    theta = rng.uniform(0, 2 * np.pi, n_stars)
    r = radius * (rng.uniform(0.55, 1.0, n_stars) ** (1 / 3))
    sin_phi = np.sqrt(np.maximum(0.0, 1.0 - u * u))
    pts = np.column_stack([r * sin_phi * np.cos(theta), r * u, r * sin_phi * np.sin(theta)])
    palette = np.array([
        [200, 220, 255],
        [255, 250, 240],
        [255, 215, 170],
        [170, 205, 255],
        [255, 180, 140],
    ], dtype=np.float32)
    cols = palette[rng.integers(0, len(palette), n_stars)]
    sizes = rng.choice([1, 1, 1, 2, 2, 3], n_stars)
    return pts, cols, sizes


def generate_deep_galaxies(n_gal=420, min_r=1200.0, max_r=4500.0, seed=108):
    rng = np.random.default_rng(seed)
    u = rng.uniform(-1, 1, n_gal)
    theta = rng.uniform(0, 2 * np.pi, n_gal)
    dist = rng.uniform(min_r, max_r, n_gal)
    sin_phi = np.sqrt(np.maximum(0.0, 1.0 - u * u))
    pts = np.column_stack([dist * sin_phi * np.cos(theta), dist * u, dist * sin_phi * np.sin(theta)])
    palette = np.array([
        [255, 205, 145],
        [165, 205, 255],
        [240, 225, 200],
        [255, 175, 130],
    ], dtype=np.float32)
    cols = palette[rng.integers(0, len(palette), n_gal)]
    radii = rng.uniform(2.0, 5.5, n_gal)
    return pts, cols, radii


def project_point(world_pt, cam_pos, yaw, pitch, fov, w, h):
    rel = world_pt - cam_pos
    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)

    # Yaw around Y axis
    x1 = cy * rel[0] - sy * rel[2]
    z1 = sy * rel[0] + cy * rel[2]
    y1 = rel[1]

    # Pitch around X axis
    y2 = cp * y1 - sp * z1
    z2 = sp * y1 + cp * z1
    x2 = x1

    if z2 <= 1.0:
        return None
    scale = (h * 0.5) / math.tan(math.radians(fov * 0.5)) / z2
    sx = int(w * 0.5 + x2 * scale)
    sy_px = int(h * 0.5 - y2 * scale)
    return sx, sy_px, z2, scale


def draw_sky_view(screen, font, small_font, yaw, pitch, fov, sim_time):
    w, h = screen.get_size()
    screen.fill((5, 9, 20))

    # Subtle horizon band
    horizon_y = int(h * 0.5 + math.sin(pitch) * h * 0.65)
    if 0 <= horizon_y <= h:
        pygame.draw.rect(screen, (14, 24, 38), (0, horizon_y, w, h - horizon_y))
        pygame.draw.line(screen, (65, 115, 155), (0, horizon_y), (w, horizon_y), 2)

    def sky_to_screen(az_deg, alt_deg):
        d_az = ((az_deg - math.degrees(yaw) + 180) % 360) - 180
        d_alt = alt_deg - math.degrees(pitch)
        px_per_deg = (w / fov)
        sx = int(w * 0.5 + d_az * px_per_deg)
        sy = int(h * 0.5 - d_alt * px_per_deg)
        return sx, sy

    # Constellation stick figures
    for p1, p2 in CONSTELLATION_LINES:
        s1 = sky_to_screen(*p1)
        s2 = sky_to_screen(*p2)
        pygame.draw.line(screen, (55, 95, 145), s1, s2, 1)

    # Named bright stars
    for name, az, alt, sz, col in SKY_STARS:
        sx, sy = sky_to_screen(az, alt)
        if -50 <= sx <= w + 50 and -50 <= sy <= h + 50:
            r = max(2, int(sz * (70.0 / max(25.0, fov))))
            pygame.draw.circle(screen, col, (sx, sy), r)
            lbl = small_font.render(name, True, (185, 215, 245))
            screen.blit(lbl, (sx + r + 4, sy - 6))

    # Visible planets in night sky
    for idx, b in enumerate(BODIES[1:], start=1):
        az = (idx * 58 + sim_time * 8) % 360
        alt = 20 + ((idx * 17) % 42)
        sx, sy = sky_to_screen(az, alt)
        if -50 <= sx <= w + 50 and -50 <= sy <= h + 50:
            pygame.draw.circle(screen, b["color"], (sx, sy), 5)
            pygame.draw.circle(screen, (255, 255, 255), (sx, sy), 6, 1)
            lbl = small_font.render(f"{b['name']} (Planet)", True, (255, 235, 175))
            screen.blit(lbl, (sx + 8, sy - 6))

    banner = font.render("HUMAN NIGHT SKY VIEW (Earth Horizon) — Drag to look, Scroll to zoom, [V] for 3D Space", True, (150, 220, 255))
    screen.blit(banner, (20, 18))


def main():
    pygame.init()
    w, h = 1280, 780
    screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    pygame.display.set_caption("Captain's Universe & Night Sky Explorer (Python)")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("DejaVu Sans", 16, bold=True)
    small_font = pygame.font.SysFont("DejaVu Sans", 13)
    tiny_font = pygame.font.SysFont("DejaVu Sans", 12)

    star_pts, star_cols, star_sizes = generate_starfield()
    deep_pts, deep_cols, deep_radii = generate_deep_galaxies()

    cam_pos = np.array([0.0, 220.0, 620.0], dtype=np.float64)
    yaw = 0.0
    pitch = -0.32
    fov = 60.0
    sky_mode = False
    show_galaxies = True
    selected_body = BODIES[3]  # Default focus: Earth
    sim_time = 0.0
    dragging = False
    last_mouse = (0, 0)

    while True:
        w, h = screen.get_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_v:
                    sky_mode = not sky_mode
                    fov = 55.0 if sky_mode else 60.0
                elif event.key == pygame.K_g:
                    show_galaxies = not show_galaxies
                elif event.key == pygame.K_SPACE:
                    sky_mode = False
                    fov = 60.0
                    cam_pos = np.array([0.0, 220.0, 620.0], dtype=np.float64)
                    yaw, pitch = 0.0, -0.32
                elif pygame.K_1 <= event.key <= pygame.K_7:
                    sky_mode = False
                    selected_body = BODIES[event.key - pygame.K_1]
                    angle = sim_time * selected_body["orbit_speed"]
                    bx = math.cos(angle) * selected_body["orbit_r"]
                    bz = math.sin(angle) * selected_body["orbit_r"]
                    cam_pos = np.array([bx, selected_body["radius"] * 3.5 + 18.0, bz + selected_body["radius"] * 5.0])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    last_mouse = event.pos
                elif event.button == 4:  # Scroll up -> zoom in
                    if sky_mode:
                        fov = max(22.0, fov - 4.0)
                    else:
                        forward = np.array([
                            math.sin(yaw) * math.cos(pitch),
                            -math.sin(pitch),
                            math.cos(yaw) * math.cos(pitch),
                        ])
                        cam_pos += forward * 28.0
                elif event.button == 5:  # Scroll down -> zoom out
                    if sky_mode:
                        fov = min(85.0, fov + 4.0)
                    else:
                        forward = np.array([
                            math.sin(yaw) * math.cos(pitch),
                            -math.sin(pitch),
                            math.cos(yaw) * math.cos(pitch),
                        ])
                        cam_pos -= forward * 28.0
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                mx, my = event.pos
                dx = mx - last_mouse[0]
                dy = my - last_mouse[1]
                last_mouse = (mx, my)
                yaw += dx * 0.005
                pitch = max(-1.45, min(1.45, pitch - dy * 0.005))

        keys = pygame.key.get_pressed()
        if not sky_mode:
            speed = 12.0 if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else 5.5
            forward = np.array([math.sin(yaw), 0.0, math.cos(yaw)])
            right = np.array([math.cos(yaw), 0.0, -math.sin(yaw)])
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                cam_pos += forward * speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                cam_pos -= forward * speed
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                cam_pos -= right * speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                cam_pos += right * speed

        sim_time += 0.016

        if sky_mode:
            draw_sky_view(screen, font, small_font, yaw, pitch, fov, sim_time)
        else:
            screen.fill((3, 5, 12))

            # Background stars
            for i in range(len(star_pts)):
                p = project_point(star_pts[i], cam_pos, yaw, pitch, fov, w, h)
                if p:
                    sx, sy, _, _ = p
                    if 0 <= sx < w and 0 <= sy < h:
                        pygame.draw.circle(screen, star_cols[i].astype(int), (sx, sy), int(star_sizes[i]))

            # Distant background galaxies (countless-style deep field)
            if show_galaxies:
                for i in range(len(deep_pts)):
                    p = project_point(deep_pts[i], cam_pos, yaw, pitch, fov, w, h)
                    if p:
                        sx, sy, z2, _ = p
                        if 0 <= sx < w and 0 <= sy < h:
                            r = max(2, min(10, int(deep_radii[i] * 500.0 / z2)))
                            col = deep_cols[i].astype(int)
                            pygame.draw.ellipse(screen, col, (sx - r, sy - r // 2, r * 2, max(2, r)))

                # Named major galaxies
                for g in GALAXIES:
                    p = project_point(g["pos"], cam_pos, yaw, pitch, fov, w, h)
                    if p:
                        sx, sy, z2, _ = p
                        if -100 <= sx <= w + 100 and -100 <= sy <= h + 100:
                            rx = max(6, min(95, int(42000.0 / z2)))
                            ry = max(3, int(rx * 0.42))
                            surf = pygame.Surface((rx * 2 + 4, ry * 2 + 4), pygame.SRCALPHA)
                            pygame.draw.ellipse(surf, (*g["color"], 95), (2, 2, rx * 2, ry * 2))
                            pygame.draw.circle(surf, (*g["color"], 190), (rx + 2, ry + 2), max(3, rx // 5))
                            screen.blit(surf, (sx - rx - 2, sy - ry - 2))
                            lbl = tiny_font.render(f"{g['name']} [{g['gtype']}]", True, (180, 215, 250))
                            screen.blit(lbl, (sx + 8, sy - 8))

            # Solar System bodies & orbits
            body_positions = {}
            for b in BODIES:
                angle = sim_time * b["orbit_speed"]
                bx = math.cos(angle) * b["orbit_r"]
                bz = math.sin(angle) * b["orbit_r"]
                pos = np.array([bx, 0.0, bz], dtype=np.float64)
                body_positions[b["name"]] = pos

                if b["orbit_r"] > 0:
                    ring_pts = []
                    for step in range(48):
                        a = (2 * math.pi * step) / 48
                        rp = project_point(
                            np.array([math.cos(a) * b["orbit_r"], 0.0, math.sin(a) * b["orbit_r"]]),
                            cam_pos, yaw, pitch, fov, w, h,
                        )
                        if rp:
                            ring_pts.append((rp[0], rp[1]))
                    if len(ring_pts) > 2:
                        pygame.draw.lines(screen, (35, 48, 72), True, ring_pts, 1)

                proj = project_point(pos, cam_pos, yaw, pitch, fov, w, h)
                if proj:
                    sx, sy, z2, scale = proj
                    rad = max(3, min(180, int(b["radius"] * scale)))
                    if b["glow"]:
                        glow_surf = pygame.Surface((rad * 4 + 4, rad * 4 + 4), pygame.SRCALPHA)
                        pygame.draw.circle(glow_surf, (*b["glow"], 55), (rad * 2 + 2, rad * 2 + 2), rad * 2)
                        screen.blit(glow_surf, (sx - rad * 2 - 2, sy - rad * 2 - 2))
                    pygame.draw.circle(screen, b["color"], (sx, sy), rad)
                    if b["name"] == "Saturn":
                        pygame.draw.ellipse(screen, (215, 190, 135), (sx - int(rad * 1.9), sy - max(2, rad // 3), int(rad * 3.8), max(4, int(rad * 0.65))), 2)
                    lbl = small_font.render(b["name"], True, (235, 242, 255))
                    screen.blit(lbl, (sx + rad + 5, sy - 7))

            # Distance-triggered focus detection
            closest_b = min(BODIES, key=lambda item: float(np.linalg.norm(cam_pos - body_positions[item["name"]])))
            closest_dist = float(np.linalg.norm(cam_pos - body_positions[closest_b["name"]]))
            if closest_dist < 140.0:
                selected_body = closest_b

            # Top-left controls & galaxy census header
            top_lines = [
                "3D UNIVERSE EXPLORER — Drag: Look | WASD/Arrows: Move | Scroll: Zoom | [1-7]: Focus | [G]: Galaxies | [V]: Sky View",
                f"Observable Universe: {COSMOS_SUMMARY['observable_estimate']} | {COSMOS_SUMMARY['catalogued_note']}",
            ]
            for i, line in enumerate(top_lines):
                surf = tiny_font.render(line, True, (155, 195, 235) if i == 0 else (130, 220, 190))
                screen.blit(surf, (16, 14 + i * 18))

            # Right-side HUD card for selected/zoomed body
            card_w, card_h = 350, 235
            cx, cy = w - card_w - 18, 56
            hud_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            pygame.draw.rect(hud_surf, (12, 20, 36, 215), (0, 0, card_w, card_h), border_radius=10)
            pygame.draw.rect(hud_surf, (70, 130, 195, 180), (0, 0, card_w, card_h), 1, border_radius=10)
            screen.blit(hud_surf, (cx, cy))

            sel_dist = float(np.linalg.norm(cam_pos - body_positions[selected_body["name"]]))
            hud_entries = [
                (font.render(f"{selected_body['name']} ({selected_body['kind']})", True, (255, 230, 150)), 12),
                (tiny_font.render(f"Camera Distance: {sel_dist:.1f}u  |  Scale: {selected_body['distance']}", True, (150, 215, 255)), 36),
                (tiny_font.render(f"Diameter: {selected_body['diameter']}", True, (215, 225, 240)), 56),
                (tiny_font.render(f"Temp: {selected_body['temp']}", True, (215, 225, 240)), 74),
            ]
            for txt_surf, y_off in hud_entries:
                screen.blit(txt_surf, (cx + 14, cy + y_off))

            # Word-wrap details
            words = selected_body["details"].split()
            lines, cur = [], ""
            for word in words:
                test = f"{cur} {word}".strip()
                if tiny_font.size(test)[0] <= card_w - 28:
                    cur = test
                else:
                    lines.append(cur)
                    cur = word
            if cur:
                lines.append(cur)
            for idx_l, l_txt in enumerate(lines[:5]):
                screen.blit(tiny_font.render(l_txt, True, (185, 200, 220)), (cx + 14, cy + 98 + idx_l * 16))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()