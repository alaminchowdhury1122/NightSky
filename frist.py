import math
import random
import tkinter as tk

COSMOS_SUMMARY = (
    "Observable Universe: ~hundreds of billions to ~2 trillion galaxies (~93B ly wide) | "
    "Catalogued: Tens of millions (Euclid DR1 ~26M, 1.5B+ planned)"
)

BODIES = [
    {
        "name": "Sun",
        "kind": "G2V Main-Sequence Star",
        "orbit_r": 0.0,
        "orbit_speed": 0.0,
        "radius": 22.0,
        "color": "#fbbf24",
        "dist": "0.00 AU (System Center)",
        "temp": "5,500 °C photosphere / 15M °C core",
        "diam": "1,392,700 km",
        "comp": "73.4% Hydrogen, 25.0% Helium, 1.6% Heavy Elements",
        "features": "Granulation cells, sunspots, coronal loops, solar wind",
        "discovery": "Studied across history; sampled by Parker Solar Probe",
        "info": "99.86% of Solar System mass; fuses ~600M tons of H into He every second.",
    },
    {
        "name": "Mercury",
        "kind": "Terrestrial Planet",
        "orbit_r": 62.0,
        "orbit_speed": 0.022,
        "radius": 5.0,
        "color": "#94a3b8",
        "dist": "0.39 AU (~58M km)",
        "temp": "-180 °C to 430 °C",
        "diam": "4,879 km",
        "comp": "Oversized iron-nickel core (~85% radius), silicate mantle",
        "features": "Caloris Basin (1,550 km), lobate scarps, polar crater ice",
        "discovery": "Mapped by Mariner 10 (1974) & MESSENGER (2011–2015)",
        "info": "Smallest planet with a massive iron core and negligible atmosphere.",
    },
    {
        "name": "Venus",
        "kind": "Terrestrial Planet",
        "orbit_r": 96.0,
        "orbit_speed": 0.015,
        "radius": 8.5,
        "color": "#fcd34d",
        "dist": "0.72 AU (~108M km)",
        "temp": "~465 °C surface",
        "diam": "12,104 km",
        "comp": "96.5% CO2, 3.5% N2 atmosphere with sulfuric acid clouds",
        "features": "Maxwell Montes, volcanic plains, retrograde 243-day spin",
        "discovery": "First reached by Mariner 2 (1962); radar-mapped by Magellan",
        "info": "Runaway CO2 greenhouse, sulfuric acid clouds, slow retrograde rotation.",
    },
    {
        "name": "Earth",
        "kind": "Terrestrial Planet",
        "orbit_r": 140.0,
        "orbit_speed": 0.010,
        "radius": 9.5,
        "color": "#38bdf8",
        "dist": "1.00 AU (~149.6M km)",
        "temp": "~15 °C mean",
        "diam": "12,742 km",
        "comp": "78.1% N2, 20.9% O2 atmosphere; silicate crust & iron core",
        "features": "71% liquid water oceans, plate tectonics, Moon (Luna)",
        "discovery": "Continuously monitored by global Earth observation fleets",
        "info": "Liquid water oceans, plate tectonics, magnetosphere, Moon, and biosphere.",
    },
    {
        "name": "Mars",
        "kind": "Terrestrial Planet",
        "orbit_r": 184.0,
        "orbit_speed": 0.008,
        "radius": 6.8,
        "color": "#f87171",
        "dist": "1.52 AU (~228M km)",
        "temp": "-63 °C mean",
        "diam": "6,779 km",
        "comp": "95.3% CO2 thin atmosphere; iron-oxide regolith & basalt",
        "features": "Olympus Mons (21.9 km), Valles Marineris, Phobos & Deimos",
        "discovery": "Explored by Curiosity, Perseverance rovers & Ingenuity",
        "info": "Iron-oxide dust, Olympus Mons (~21.9 km), Valles Marineris, Phobos & Deimos.",
    },
    {
        "name": "Jupiter",
        "kind": "Gas Giant",
        "orbit_r": 255.0,
        "orbit_speed": 0.0045,
        "radius": 18.5,
        "color": "#fdba74",
        "dist": "5.20 AU (~778M km)",
        "temp": "-110 °C cloud tops",
        "diam": "139,820 km",
        "comp": "~90% Hydrogen, ~10% Helium, ammonia & water cloud decks",
        "features": "Great Red Spot anticyclone, 95 moons (Io, Europa, Ganymede)",
        "discovery": "Galilean moons found in 1610; studied by Voyager, Galileo & Juno",
        "info": "Most massive planet (~2.5x all other planets combined), Great Red Spot, 95 moons.",
    },
    {
        "name": "Saturn",
        "kind": "Gas Giant",
        "orbit_r": 330.0,
        "orbit_speed": 0.0032,
        "radius": 15.5,
        "color": "#fde68a",
        "dist": "9.58 AU (~1.43B km)",
        "temp": "-140 °C cloud tops",
        "diam": "116,460 km",
        "comp": "96.3% Hydrogen, 3.25% Helium; 99.9% water-ice rings",
        "features": "Main rings (A–G), Cassini Division, 146 moons incl. Titan",
        "discovery": "Rings resolved by Huygens (1655); explored by Cassini–Huygens",
        "info": "Water-ice ring system, Cassini Division, low density, 146 moons incl. Titan.",
    },
    {
        "name": "Uranus",
        "kind": "Ice Giant",
        "orbit_r": 395.0,
        "orbit_speed": 0.0022,
        "radius": 11.5,
        "color": "#67e8f9",
        "dist": "19.2 AU (~2.87B km)",
        "temp": "-195 °C cloud tops",
        "diam": "50,724 km",
        "comp": "H2, He, CH4 gas over water-ammonia-methane ice mantle",
        "features": "13 narrow dark rings, 28 moons, extreme ~97.8° axial tilt",
        "discovery": "Discovered by William Herschel (1781); visited by Voyager 2",
        "info": "Water/ammonia/methane ice mantle, ~97.8° axial tilt, 13 narrow rings, 28 moons.",
    },
    {
        "name": "Neptune",
        "kind": "Ice Giant",
        "orbit_r": 455.0,
        "orbit_speed": 0.0016,
        "radius": 11.2,
        "color": "#60a5fa",
        "dist": "30.1 AU (~4.50B km)",
        "temp": "-201 °C cloud tops",
        "diam": "49,244 km",
        "comp": "H2, He, CH4 upper atmosphere over dense icy mantle",
        "features": "Supersonic >2,000 km/h winds, Great Dark Spot, Triton",
        "discovery": "Predicted mathematically in 1846; visited by Voyager 2",
        "info": "Supersonic >2,000 km/h winds, Great Dark Spot storms, retrograde moon Triton.",
    },
]

GALAXIES = [
    {
        "name": "Milky Way",
        "kind": "Barred Spiral Galaxy (SBbc)",
        "pos": (0.0, -40.0, 0.0),
        "color": "#93c5fd",
        "dist": "Home (Sun ~27k ly from core)",
        "temp": "Core gas: ~10K–50K K",
        "diam": "~100,000 ly across",
        "comp": "100–400B stars, molecular H2 clouds, dark matter halo",
        "features": "Sagittarius A* (4.3M M☉ black hole), Orion Arm, 50+ dwarf satellites",
        "discovery": "Resolved into stars by Galileo (1610); mapped in 3D by ESA Gaia",
        "info": "Our home barred-spiral galaxy in the Local Group with Sagittarius A* at its center.",
    },
    {
        "name": "Andromeda (M31)",
        "kind": "Spiral Galaxy (SA(s)b)",
        "pos": (950.0, 180.0, -1250.0),
        "color": "#fcd34d",
        "dist": "~2.5M ly from Earth",
        "temp": "Bulge stars: ~4,500 K",
        "diam": "~152,000 ly across",
        "comp": "~1 trillion stars, double nucleus, ionized gas halo",
        "features": "M32 & M110 satellite galaxies, blueshifted approach (~110 km/s)",
        "discovery": "Recorded by al-Sufi (964 AD); distance proved by Hubble (1923)",
        "info": "Largest major galaxy in the Local Group; visible to the naked eye in dark skies.",
    },
    {
        "name": "Triangulum (M33)",
        "kind": "Unbarred Spiral (SA(s)cd)",
        "pos": (1180.0, -210.0, -920.0),
        "color": "#67e8f9",
        "dist": "~2.7–3.0M ly from Earth",
        "temp": "H II regions: ~10,000 K",
        "diam": "~60,000 ly across",
        "comp": "~40 billion stars, hydrogen gas, young O/B star clusters",
        "features": "NGC 604 giant H II star-forming nursery (~1,500 ly wide)",
        "discovery": "Catalogued by Charles Messier in 1764; 3rd Local Group spiral",
        "info": "Third-largest member of the Local Group and a rich star-forming spiral.",
    },
    {
        "name": "Sombrero (M104)",
        "kind": "Spiral / Lenticular Galaxy",
        "pos": (-1220.0, 260.0, -1050.0),
        "color": "#fdba74",
        "dist": "~29.3M ly from Earth",
        "temp": "Core bulge: ~5,000 K",
        "diam": "~50,000 ly across",
        "comp": "~800 billion stars, dense central bulge, PAH dust lane",
        "features": "1-billion-M☉ central black hole, ~2,000 globular star clusters",
        "discovery": "Discovered by Pierre Méchain (1781); imaged by Hubble & Spitzer",
        "info": "Famous for its brilliant luminous core and broad symmetric dust ring.",
    },
    {
        "name": "Messier 87 (M87)",
        "kind": "Supergiant Elliptical (E0-1)",
        "pos": (-1020.0, -320.0, 1140.0),
        "color": "#fca5a5",
        "dist": "~53.5M ly (Virgo Cluster)",
        "temp": "Jet plasma: millions K",
        "diam": "~120,000 ly across",
        "comp": "Several trillion old stars, hot X-ray intracluster gas",
        "features": "M87* (6.5B M☉ black hole), 5,000-ly relativistic plasma jet",
        "discovery": "M87* shadow imaged by Event Horizon Telescope (2019)",
        "info": "Dominant elliptical galaxy of the Virgo Cluster with supermassive black hole M87*.",
    },
    {
        "name": "Large Magellanic Cloud",
        "kind": "Irregular Dwarf Galaxy",
        "pos": (280.0, -140.0, 340.0),
        "color": "#a5f3fc",
        "dist": "~163,000 ly from Earth",
        "temp": "Tarantula Neb.: ~10,000+ K",
        "diam": "~32,200 ly across",
        "comp": "~30 billion stars, metal-poor gas, young supergiants",
        "features": "30 Doradus (Tarantula Nebula), Supernova 1987A remnant",
        "discovery": "Documented by southern navigators & Magellan's 1519 expedition",
        "info": "Prominent satellite galaxy orbiting the Milky Way in the southern sky.",
    },
]

SKY_STARS = [
    ("Sirius", 155, 28, 4, "#e0f2fe", "8.6 ly", "9,940 K", "2.4M km", "Brightest star in Earth's night sky (Canis Major)."),
    ("Betelgeuse", 115, 42, 4, "#ff9d5c", "548 ly", "3,500 K", "1,234M km", "Massive red supergiant marking Orion's right shoulder."),
    ("Rigel", 132, 24, 4, "#a5d8ff", "860 ly", "12,100 K", "109M km", "Luminous blue supergiant marking Orion's foot."),
    ("Bellatrix", 112, 34, 3, "#bae6fd", "250 ly", "22,000 K", "8.0M km", "Blue giant forming the left shoulder of Orion."),
    ("Alnilam", 122, 33, 3, "#bae6fd", "2,000 ly", "27,000 K", "45M km", "Central blue supergiant jewel of Orion's Belt."),
    ("Polaris", 355, 58, 3, "#fef08a", "433 ly", "6,015 K", "52M km", "The North Star, aligned closely with Earth's rotational axis."),
    ("Vega", 65, 66, 4, "#bae6fd", "25 ly", "9,602 K", "3.3M km", "Bright A0V star in Lyra and vertex of the Summer Triangle."),
    ("Dubhe", 325, 64, 3, "#fde047", "123 ly", "4,660 K", "41M km", "Big Dipper pointer star aiming toward Polaris."),
    ("Merak", 318, 56, 3, "#f8fafc", "79.7 ly", "9,377 K", "4.2M km", "Lower pointer star of the Big Dipper bowl."),
    ("Aldebaran", 92, 46, 3, "#fb923c", "65 ly", "3,910 K", "61M km", "Fiery orange giant eye of Taurus the Bull."),
]


class NightSkyApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("3D Universe & Night Sky Explorer (Python)")
        self.root.geometry("1280x780")

        self.canvas = tk.Canvas(root, bg="#02040a", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        rng = random.Random(42)
        self.stars = [
            (
                f"HD-{10000 + i}",
                rng.uniform(-2600, 2600),
                rng.uniform(-2600, 2600),
                rng.uniform(-2600, 2600),
                rng.choice(["#bae6fd", "#f8fafc", "#fef08a", "#fdba74"]),
            )
            for i in range(900)
        ]
        self.deep_galaxies = [
            (
                f"UDF-{2000 + i}",
                rng.uniform(-2400, 2400),
                rng.uniform(-2400, 2400),
                rng.uniform(-2400, 2400),
                rng.choice(["#fde68a", "#93c5fd", "#fbcfe8"]),
            )
            for i in range(220)
        ]

        self.cam_x, self.cam_y, self.cam_z = 0.0, 190.0, 520.0
        self.yaw = 0.0
        self.pitch = -0.32
        self.fov = 60.0
        self.sky_mode = False
        self.sim_time = 0.0
        self.selected = BODIES[3]  # Default: Earth
        self.fly_target_cam = None
        self.fly_look_target = None

        # Movable HUD Dossier Card coordinates
        self.card_x = None
        self.card_y = 56
        self.card_w = 360
        self.card_h = 330
        self.dragging_card = False
        self.card_drag_offset = (0, 0)

        self.press_pos = None
        self.drag_last = None
        self.hit_targets = []  # List of (sx, sy, radius, payload, world_pos)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<MouseWheel>", self.on_wheel)
        self.canvas.bind("<Button-4>", self.on_wheel_up)
        self.canvas.bind("<Button-5>", self.on_wheel_down)
        root.bind("<KeyPress-v>", lambda _e: self.toggle_sky_mode())
        root.bind("<KeyPress-V>", lambda _e: self.toggle_sky_mode())
        root.bind("<space>", lambda _e: self.reset_view())
        for idx, body in enumerate(BODIES):
            root.bind(str(idx + 1), lambda _e, b=body: self.fly_to_body(b))

        self.loop()

    def toggle_sky_mode(self):
        self.sky_mode = not self.sky_mode
        self.fly_target_cam = None
        self.fov = 55.0 if self.sky_mode else 60.0

    def reset_view(self):
        self.sky_mode = False
        self.fov = 60.0
        self.fly_target_cam = (0.0, 190.0, 520.0)
        self.fly_look_target = (0.0, 0.0, 0.0)

    def aim_camera_at(self, tx, ty, tz):
        dx = tx - self.cam_x
        dy = ty - self.cam_y
        dz = tz - self.cam_z
        horiz = math.hypot(dx, dz)
        if horiz > 1e-4 or abs(dy) > 1e-4:
            self.yaw = math.atan2(dx, dz)
            self.pitch = max(-1.4, min(1.4, -math.atan2(dy, max(1e-4, horiz))))

    def start_flight(self, world_pos, stand_off, payload):
        self.selected = payload
        tx, ty, tz = world_pos
        vx = self.cam_x - tx
        vy = self.cam_y - ty
        vz = self.cam_z - tz
        norm = math.sqrt(vx * vx + vy * vy + vz * vz)
        if norm < 1e-3:
            vx, vy, vz, norm = 0.0, 0.4, 1.0, 1.077
        cx = tx + (vx / norm) * stand_off
        cy = ty + max(stand_off * 0.28, (vy / norm) * stand_off)
        cz = tz + (vz / norm) * stand_off
        self.fly_target_cam = (cx, cy, cz)
        self.fly_look_target = (tx, ty, tz)

    def fly_to_body(self, body):
        self.sky_mode = False
        angle = self.sim_time * body["orbit_speed"]
        bx = math.cos(angle) * body["orbit_r"]
        bz = math.sin(angle) * body["orbit_r"]
        stand_off = max(48.0, body["radius"] * 4.8)
        self.start_flight((bx, 0.0, bz), stand_off, body)

    def on_press(self, event):
        self.press_pos = (event.x, event.y)
        self.drag_last = (event.x, event.y)

        # Check if user grabbed the movable HUD dossier header
        if self.card_x is not None:
            if (
                self.card_x <= event.x <= self.card_x + self.card_w
                and self.card_y <= event.y <= self.card_y + 38
            ):
                self.dragging_card = True
                self.card_drag_offset = (event.x - self.card_x, event.y - self.card_y)
                return

        self.fly_target_cam = None

    def on_drag(self, event):
        if self.dragging_card:
            w = max(400, self.canvas.winfo_width())
            h = max(300, self.canvas.winfo_height())
            self.card_x = max(8, min(w - self.card_w - 8, event.x - self.card_drag_offset[0]))
            self.card_y = max(8, min(h - self.card_h - 8, event.y - self.card_drag_offset[1]))
            return

        if not self.drag_last:
            return
        dx = event.x - self.drag_last[0]
        dy = event.y - self.drag_last[1]
        self.drag_last = (event.x, event.y)
        self.yaw += dx * 0.005
        if self.sky_mode:
            self.pitch = max(0.05, min(1.35, self.pitch + dy * 0.005))
        else:
            self.pitch = max(-1.4, min(1.4, self.pitch - dy * 0.005))

    def on_release(self, event):
        if self.dragging_card:
            self.dragging_card = False
            self.drag_last = None
            return

        if self.press_pos:
            moved = math.hypot(event.x - self.press_pos[0], event.y - self.press_pos[1])
            if moved < 6:
                self.handle_canvas_click(event.x, event.y)

        self.drag_last = None
        self.press_pos = None

    def handle_canvas_click(self, mx, my):
        # 1. Check top toolbar buttons
        w = max(400, self.canvas.winfo_width())
        if w - 175 <= mx <= w - 16 and 12 <= my <= 42:
            self.toggle_sky_mode()
            return

        # 2. Check clicked celestial object (planet, galaxy, or star)
        best_hit = None
        best_dist = 9999.0
        for sx, sy, hit_r, payload, world_pos, stand_off in self.hit_targets:
            d = math.hypot(mx - sx, my - sy)
            if d <= max(14.0, hit_r + 6.0) and d < best_dist:
                best_dist = d
                best_hit = (payload, world_pos, stand_off)

        if best_hit:
            payload, world_pos, stand_off = best_hit
            if self.sky_mode:
                self.selected = payload
            else:
                self.start_flight(world_pos, stand_off, payload)
            return

        # 3. Click anywhere in open 3D space -> fly smoothly into that sector!
        if not self.sky_mode:
            h = max(300, self.canvas.winfo_height())
            focal = (h * 0.5) / math.tan(math.radians(self.fov * 0.5))
            nx = (mx - w * 0.5) / focal
            ny = -(my - h * 0.5) / focal
            nz = 1.0
            inv_len = 1.0 / math.sqrt(nx * nx + ny * ny + nz * nz)
            nx, ny, nz = nx * inv_len, ny * inv_len, nz * inv_len

            cp, sp = math.cos(self.pitch), math.sin(self.pitch)
            cy, sy = math.cos(self.yaw), math.sin(self.yaw)

            y1 = cp * ny + sp * nz
            z1 = -sp * ny + cp * nz
            x1 = nx

            wx = cy * x1 + sy * z1
            wy = y1
            wz = -sy * x1 + cy * z1

            dest = (self.cam_x + wx * 240.0, self.cam_y + wy * 240.0, self.cam_z + wz * 240.0)
            sector_payload = {
                "name": "Deep Space Sector",
                "kind": "Interstellar / Intergalactic Region",
                "color": "#38bdf8",
                "dist": f"Coords ({dest[0]:.0f}, {dest[1]:.0f}, {dest[2]:.0f})",
                "temp": "2.725 K (CMB)",
                "diam": "Open Cosmic Volume",
                "comp": "Cosmic Microwave Background photons & sparse plasma",
                "features": "Direct line-of-sight to surrounding galaxies & star clusters",
                "discovery": "Navigated via free-space coordinate click",
                "info": "Click any nearby galaxy, star, or planet to fly closer and inspect its live surface/telescope view.",
            }
            self.start_flight(dest, 45.0, sector_payload)

    def zoom_step(self, direction):
        self.fly_target_cam = None
        if self.sky_mode:
            if direction < 0 and self.fov >= 82.0:
                self.toggle_sky_mode()
                return
            self.fov = max(24.0, min(85.0, self.fov - direction * 4.0))
            return
        fx = math.sin(self.yaw) * math.cos(self.pitch)
        fy = -math.sin(self.pitch)
        fz = math.cos(self.yaw) * math.cos(self.pitch)
        step = 36.0 * direction
        self.cam_x += fx * step
        self.cam_y += fy * step
        self.cam_z += fz * step

    def on_wheel(self, event):
        self.zoom_step(1 if event.delta > 0 else -1)

    def on_wheel_up(self, _event):
        self.zoom_step(1)

    def on_wheel_down(self, _event):
        self.zoom_step(-1)

    def project(self, wx, wy, wz, w, h):
        rx = wx - self.cam_x
        ry = wy - self.cam_y
        rz = wz - self.cam_z

        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)

        x1 = cy * rx - sy * rz
        z1 = sy * rx + cy * rz
        y1 = ry

        y2 = cp * y1 - sp * z1
        z2 = sp * y1 + cp * z1
        x2 = x1

        if z2 <= 1.0:
            return None
        scale = (h * 0.5) / math.tan(math.radians(self.fov * 0.5)) / z2
        sx = w * 0.5 + x2 * scale
        sy_px = h * 0.5 - y2 * scale
        return sx, sy_px, z2, scale

    def draw_telescope_viewport(self, cx, cy, cw):
        """Renders a live close-up surface / optical telescope preview inside the HUD card."""
        vx, vy, vw, vh = cx + 12, cy + 36, cw - 24, 96
        self.canvas.create_rectangle(vx, vy, vx + vw, vy + vh, fill="#030712", outline="#1e293b", width=1)

        mid_x = vx + vw * 0.5
        mid_y = vy + vh * 0.5
        col = self.selected.get("color", "#38bdf8")
        kind = self.selected.get("kind", "")

        # Micro-stars inside optical frame
        for i in range(16):
            sx = vx + ((i * 53 + 17) % (vw - 8)) + 4
            sy = vy + ((i * 29 + 11) % (vh - 8)) + 4
            self.canvas.create_oval(sx, sy, sx + 1.5, sy + 1.5, fill="#94a3b8", outline="")

        if "Galaxy" in kind:
            # Animated spiral / elliptical galaxy close-up
            rot = self.sim_time * 0.5
            for arm in range(2):
                pts = []
                for step in range(26):
                    ang = arm * math.pi + step * 0.22 + rot
                    rad = step * 1.45
                    px = mid_x + math.cos(ang) * rad * 1.7
                    py = mid_y + math.sin(ang) * rad * 0.65
                    if vx + 4 <= px <= vx + vw - 4 and vy + 4 <= py <= vy + vh - 4:
                        pts.extend([px, py])
                if len(pts) >= 4:
                    self.canvas.create_line(*pts, fill=col, width=2, smooth=True)
            self.canvas.create_oval(mid_x - 10, mid_y - 6, mid_x + 10, mid_y + 6, fill="#fef9c3", outline=col)
        else:
            # Close-up planetary globe / star disk with atmospheric limb & bands
            r = 32
            self.canvas.create_oval(mid_x - r - 4, mid_y - r - 4, mid_x + r + 4, mid_y + r + 4, outline=col, width=1)
            self.canvas.create_oval(mid_x - r, mid_y - r, mid_x + r, mid_y + r, fill=col, outline="")
            if self.selected.get("name") == "Saturn":
                self.canvas.create_oval(mid_x - 66, mid_y - 14, mid_x + 66, mid_y + 14, outline="#fde68a", width=3)
            # Terminator crescent shadow on right side for 3D depth
            self.canvas.create_arc(
                mid_x - r, mid_y - r, mid_x + r, mid_y + r,
                start=-90, extent=180, fill="#060c18", outline=""
            )

        self.canvas.create_text(
            vx + 8, vy + 7,
            text="LIVE OPTICAL / SURFACE FEED",
            fill="#7dd3fc", anchor="nw", font=("Sans", 7, "bold")
        )

    def draw_dossier_card(self, w, h):
        if self.card_x is None:
            self.card_x = w - self.card_w - 16
        cx = max(8, min(w - self.card_w - 8, self.card_x))
        cy = max(8, min(h - self.card_h - 8, self.card_y))
        cw, ch = self.card_w, self.card_h

        self.canvas.create_rectangle(cx, cy, cx + cw, cy + ch, fill="#0b1324", outline="#38bdf8", width=1)
        # Movable header bar
        self.canvas.create_rectangle(cx, cy, cx + cw, cy + 30, fill="#111d36", outline="")
        self.canvas.create_text(
            cx + 12, cy + 15,
            text=f"☰  {self.selected['name']} ({self.selected['kind']})",
            fill="#fde047", anchor="w", font=("Sans", 9, "bold")
        )

        self.draw_telescope_viewport(cx, cy, cw)

        y_cursor = cy + 140
        meta_lines = [
            f"Distance: {self.selected.get('dist', 'N/A')}   |   Diam: {self.selected.get('diam', 'N/A')}",
            f"Temp: {self.selected.get('temp', 'N/A')}",
            f"Composition: {self.selected.get('comp', 'Hydrogen, helium & cosmic dust')}",
            f"Features: {self.selected.get('features', 'Active cosmic structure')}",
            f"Discovery: {self.selected.get('discovery', 'Catalogued via sky surveys')}",
        ]
        for line in meta_lines:
            self.canvas.create_text(
                cx + 12, y_cursor,
                text=line, fill="#e2e8f0", anchor="nw", width=cw - 24, font=("Sans", 8)
            )
            y_cursor += 24 if len(line) > 54 else 18

        self.canvas.create_text(
            cx + 12, y_cursor + 4,
            text=self.selected.get("info", ""),
            fill="#94a3b8", anchor="nw", width=cw - 24, font=("Sans", 8)
        )

    def draw_sky_view(self, w, h):
        horizon_y = h * 0.5 + math.sin(self.pitch) * h * 0.55
        if 0 <= horizon_y <= h:
            self.canvas.create_rectangle(0, horizon_y, w, h, fill="#081220", outline="")
            self.canvas.create_line(0, horizon_y, w, horizon_y, fill="#38bdf8", width=2)

        px_per_deg = w / self.fov
        for name, az, alt, sz, col, dist, temp, diam, info in SKY_STARS:
            d_az = ((az - math.degrees(self.yaw) + 180.0) % 360.0) - 180.0
            d_alt = alt - math.degrees(self.pitch)
            sx = w * 0.5 + d_az * px_per_deg
            sy = h * 0.5 - d_alt * px_per_deg
            if -60 <= sx <= w + 60 and -60 <= sy <= h + 60:
                r = max(2, int(sz * (65.0 / max(25.0, self.fov))))
                self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill=col, outline="")
                self.canvas.create_text(sx + r + 6, sy, text=name, fill="#bae6fd", anchor="w", font=("Sans", 9))
                star_payload = {
                    "name": name,
                    "kind": "Bright Night-Sky Star",
                    "color": col,
                    "dist": dist,
                    "temp": temp,
                    "diam": diam,
                    "comp": "Hydrogen & helium fusion plasma",
                    "features": "Visible to the naked eye from Earth's surface",
                    "discovery": "Catalogued in Hipparcos & Gaia surveys",
                    "info": info,
                }
                self.hit_targets.append((sx, sy, r + 6, star_payload, (0.0, 0.0, 0.0), 40.0))

    def loop(self):
        self.canvas.delete("all")
        self.hit_targets.clear()
        w = max(400, self.canvas.winfo_width())
        h = max(300, self.canvas.winfo_height())
        self.sim_time += 0.016

        # Smooth click-to-travel flight interpolation
        if self.fly_target_cam:
            tx, ty, tz = self.fly_target_cam
            self.cam_x += (tx - self.cam_x) * 0.08
            self.cam_y += (ty - self.cam_y) * 0.08
            self.cam_z += (tz - self.cam_z) * 0.08
            if self.fly_look_target:
                self.aim_camera_at(*self.fly_look_target)
            if math.dist((self.cam_x, self.cam_y, self.cam_z), self.fly_target_cam) < 1.2:
                self.fly_target_cam = None

        if self.sky_mode:
            self.draw_sky_view(w, h)
        else:
            for s_name, sx_w, sy_w, sz_w, col in self.stars:
                p = self.project(sx_w, sy_w, sz_w, w, h)
                if p and 0 <= p[0] <= w and 0 <= p[1] <= h:
                    self.canvas.create_oval(p[0] - 1, p[1] - 1, p[0] + 1, p[1] + 1, fill=col, outline="")
                    star_payload = {
                        "name": f"{s_name} Field Star",
                        "kind": "Main-Sequence / Giant Star",
                        "color": col,
                        "dist": f"{int(math.dist((0, 0, 0), (sx_w, sy_w, sz_w)))} ly (Rel)",
                        "temp": "4,200–11,000 K",
                        "diam": "~1.4M–18M km",
                        "comp": "Hydrogen & helium plasma",
                        "features": "Galactic disk star",
                        "discovery": "Gaia Astrometric Survey",
                        "info": "A distant star in our galaxy radiating light from core nuclear fusion.",
                    }
                    self.hit_targets.append((p[0], p[1], 6.0, star_payload, (sx_w, sy_w, sz_w), 55.0))

            for g_id, gx_w, gy_w, gz_w, col in self.deep_galaxies:
                p = self.project(gx_w, gy_w, gz_w, w, h)
                if p and 0 <= p[0] <= w and 0 <= p[1] <= h:
                    rx = max(2.0, min(8.0, 260.0 / p[2]))
                    self.canvas.create_oval(p[0] - rx, p[1] - rx * 0.5, p[0] + rx, p[1] + rx * 0.5, fill=col, outline="")
                    deep_payload = {
                        "name": f"{g_id} Deep-Field Galaxy",
                        "kind": "Distant Spiral / Elliptical Galaxy",
                        "color": col,
                        "dist": f"~{int(math.dist((0, 0, 0), (gx_w, gy_w, gz_w)) * 18)}M ly",
                        "temp": "Integrated: ~5,200 K",
                        "diam": "~75,000 ly across",
                        "comp": "Billions of stars, interstellar gas & dark matter",
                        "features": "Cosmologically redshifted deep-sky galaxy",
                        "discovery": "Hubble / JWST / Euclid Deep Field Survey",
                        "info": "One of hundreds of billions to ~2 trillion galaxies across the observable universe.",
                    }
                    self.hit_targets.append((p[0], p[1], rx + 6.0, deep_payload, (gx_w, gy_w, gz_w), 65.0))

            for gal in GALAXIES:
                p = self.project(*gal["pos"], w, h)
                if p and -120 <= p[0] <= w + 120 and -120 <= p[1] <= h + 120:
                    rx = max(9.0, min(75.0, 34000.0 / p[2]))
                    ry = max(4.5, rx * 0.42)
                    self.canvas.create_oval(p[0] - rx, p[1] - ry, p[0] + rx, p[1] + ry, outline=gal["color"], width=2)
                    self.canvas.create_text(
                        p[0] + rx + 6, p[1],
                        text=gal["name"],
                        fill="#c7d2fe", anchor="w", font=("Sans", 8, "bold")
                    )
                    self.hit_targets.append((p[0], p[1], rx + 8.0, gal, gal["pos"], 140.0))

            positions = {}
            for body in BODIES:
                angle = self.sim_time * body["orbit_speed"]
                bx = math.cos(angle) * body["orbit_r"]
                bz = math.sin(angle) * body["orbit_r"]
                positions[body["name"]] = (bx, 0.0, bz)

                if body["orbit_r"] > 0:
                    ring = []
                    for step in range(48):
                        a = (2.0 * math.pi * step) / 48.0
                        rp = self.project(math.cos(a) * body["orbit_r"], 0.0, math.sin(a) * body["orbit_r"], w, h)
                        if rp:
                            ring.extend([rp[0], rp[1]])
                    if len(ring) >= 6:
                        self.canvas.create_line(*ring, fill="#1e293b", width=1)

                proj = self.project(bx, 0.0, bz, w, h)
                if proj:
                    sx, sy_px, _z2, scale = proj
                    r = max(3.5, min(140.0, body["radius"] * scale))
                    self.canvas.create_oval(sx - r, sy_px - r, sx + r, sy_px + r, fill=body["color"], outline="")
                    if body["name"] == "Saturn":
                        self.canvas.create_oval(
                            sx - r * 1.9, sy_px - max(2.0, r * 0.35),
                            sx + r * 1.9, sy_px + max(2.0, r * 0.35),
                            outline="#fde68a", width=2
                        )
                    self.canvas.create_text(sx + r + 6, sy_px, text=body["name"], fill="#e2e8f0", anchor="w", font=("Sans", 9, "bold"))
                    self.hit_targets.append((sx, sy_px, r + 6.0, body, (bx, 0.0, bz), max(45.0, body["radius"] * 4.8)))

        # Minimal Top-Right Sky View Button (No top-left text clutter)
        btn_label = "Exit Sky View [V]" if self.sky_mode else "Sky View from Earth [V]"
        self.canvas.create_rectangle(w - 175, 12, w - 16, 42, fill="#0f172a", outline="#38bdf8", width=1)
        self.canvas.create_text(w - 95, 27, text=btn_label, fill="#e0f2fe", font=("Sans", 8, "bold"))

        # Movable Scientific Dossier & Live Surface/Optical Viewport
        self.draw_dossier_card(w, h)

        self.root.after(16, self.loop)


def main():
    try:
        root = tk.Tk()
        NightSkyApp(root)
        root.mainloop()
    except tk.TclError as exc:
        print(f"Display initialization failed: {exc}")


if __name__ == "__main__":
    main()