"""
AP Smart Route Finder — Gradio Edition
Run:  pip install gradio networkx numpy folium
      python app_gradio.py
"""
from algorithms import run_dijkstra, run_grover
import math, random, time
import numpy as np
import networkx as nx
import gradio as gr

# ══════════════════════════════════════════════════════════════════════════════
# CITY DATA
# ══════════════════════════════════════════════════════════════════════════════
AP_CITIES = {
    "Visakhapatnam":  (17.6868, 83.2185),
    "Vijayawada":     (16.5062, 80.6480),
    "Guntur":         (16.3067, 80.4365),
    "Nellore":        (14.4426, 79.9865),
    "Kurnool":        (15.8281, 78.0373),
    "Rajahmundry":    (16.9891, 81.7837),
    "Tirupati":       (13.6288, 79.4192),
    "Kadapa":         (14.4674, 78.8241),
    "Kakinada":       (16.9891, 82.2475),
    "Anantapur":      (14.6819, 77.6006),
    "Amaravati":      (16.5730, 80.3564),
    "Eluru":          (16.7107, 81.0952),
    "Ongole":         (15.5057, 80.0499),
    "Srikakulam":     (18.2949, 83.8938),
    "Vizianagaram":   (18.1066, 83.3956),
    "Chittoor":       (13.2172, 79.1003),
    "Machilipatnam":  (16.1875, 81.1386),
    "Narasaraopet":   (16.2346, 80.0490),
    "Tenali":         (16.2435, 80.6404),
    "Mangalagiri":    (16.4307, 80.5525),
    "Bhimavaram":     (16.5449, 81.5212),
    "Tadepalligudem": (16.8133, 81.5271),
    "Bapatla":        (15.9049, 80.4671),
    "Chirala":        (15.8264, 80.3538),
    "Narasapuram":    (16.4344, 81.6958),
    "Palasa":         (18.7726, 84.4083),
    "Bobbili":        (18.5744, 83.3588),
    "Parvathipuram":  (18.7828, 83.4253),
    "Rajam":          (18.4730, 83.6469),
    "Anakapalle":     (17.6910, 83.0000),
    "Yellamanchili":  (17.5543, 82.8555),
    "Madanapalle":    (13.5545, 78.5011),
    "Hindupur":       (13.8294, 77.4911),
    "Dharmavaram":    (14.4113, 77.7181),
    "Tadipatri":      (14.9101, 78.0094),
    "Guntakal":       (15.1712, 77.3726),
    "Adoni":          (15.6279, 77.2744),
    "Nandyal":        (15.4786, 78.4836),
    "Proddatur":      (14.7500, 78.5500),
    "Rajampet":       (14.1931, 79.1621),
    "Badvel":         (14.7455, 79.0643),
    "Pulivendula":    (14.4224, 78.2277),
    "Allagadda":      (15.1417, 78.5304),
    "Srisailam":      (16.0833, 78.8833),
    "Markapur":       (15.7407, 79.2682),
    "Kandukur":       (15.2143, 79.9057),
    "Kavali":         (14.9165, 79.9932),
    "Gudur":          (14.1459, 79.8516),
    "Sullurpeta":     (13.7630, 79.8878),
    "Venkatagiri":    (13.9617, 79.5812),
    "Srikalahasti":   (13.7500, 79.6983),
    "Puttur":         (13.4408, 79.5493),
    "Pileru":         (13.6583, 79.1167),
    "Punganur":       (13.3674, 78.5805),
    "Kuppam":         (12.7500, 78.3333),
    "Peddapuram":     (17.0786, 82.1360),
    "Samalkot":       (17.0582, 82.1761),
    "Tuni":           (17.3586, 82.5476),
    "Amalapuram":     (16.5771, 82.0056),
    "Razole":         (16.4784, 81.8413),
    "Mandapeta":      (16.8667, 81.9333),
    "Kovvur":         (17.0167, 81.7333),
    "Nidadavolu":     (17.0578, 81.6728),
    "Tanuku":         (16.8600, 81.6800),
    "Palakollu":      (16.5155, 81.7301),
    "Nuzvid":         (16.7853, 80.8459),
    "Gudivada":       (16.4327, 80.9943),
    "Vuyyuru":        (16.3618, 80.8459),
    "Repalle":        (16.0186, 80.8306),
    "Vinukonda":      (16.0500, 79.7333),
    "Sattenapalle":   (16.3932, 80.1528),
    "Macherla":       (16.4795, 79.4352),
    "Chilakaluripet": (16.0875, 80.1689),
    "Ongole":         (15.5057, 80.0499),
    "Narasannapeta":  (18.4148, 84.0419),
}

CITY_POIS = {
    "Visakhapatnam": {
        "malls": ["CMR Central Mall", "Jagadamba Junction Mall", "Pothys Mall"],
        "restaurants": ["Dwaraka Hotel", "Bamboo Bay", "Sea View Restaurant", "Hotel Meghalaya"],
        "landmarks": ["Kailasagiri", "Rishikonda Beach", "INS Kurusura Museum", "Araku Valley"],
        "petrol_bunks": ["HP Petrol Bunk - MVP Colony", "Indian Oil - Dwaraka Nagar", "BPCL - Gajuwaka", "Shell - Vizag Steel Area"],
    },
    "Vijayawada": {
        "malls": ["PVP Square", "One Town Mall", "AMB Mall"],
        "restaurants": ["Hotel Swagath", "Minerva Coffee Shop", "Babai Hotel", "Curry Leaf"],
        "landmarks": ["Kanaka Durga Temple", "Prakasam Barrage", "Undavalli Caves", "Bhavani Island"],
        "petrol_bunks": ["HP Bunk - Governorpet", "Indian Oil - Benz Circle", "BPCL - Eluru Road", "Shell - Autonagar"],
    },
    "Guntur": {
        "malls": ["KLM Fashion Mall", "Big Bazaar Guntur"],
        "restaurants": ["Nagarjuna Restaurant", "Hotel Dwaraka", "Udupi Hotel"],
        "landmarks": ["Undavalli Caves", "Amaravati Museum", "Kondaveedu Fort"],
        "petrol_bunks": ["HP - Brodipet", "Indian Oil - Arundelpet", "BPCL - Naaz Centre"],
    },
    "Tirupati": {
        "malls": ["Leela Mahal Mall", "Star Mall Tirupati"],
        "restaurants": ["Hotel Bliss", "Annapurna Hotel", "Bhimas Deluxe"],
        "landmarks": ["Tirumala Temple", "Sri Padmavathi Temple", "Chandragiri Fort"],
        "petrol_bunks": ["HP - Alipiri", "Indian Oil - Renigunta Road", "BPCL - Tiruchanur"],
    },
    "Nellore": {
        "malls": ["Leela Mall", "City Center Mall"],
        "restaurants": ["Hotel Sreyas", "Kamat Hotel", "Spice Garden"],
        "landmarks": ["Pulicat Lake", "Mypad Beach", "Sri Ranganathaswamy Temple"],
        "petrol_bunks": ["HP - Grand Trunk Road", "Indian Oil - Pogathota", "BPCL - Dargamitta"],
    },
    "Rajahmundry": {
        "malls": ["Rajahmundry Mall", "City Center"],
        "restaurants": ["Hotel Anand", "Haritha Hotel", "Bay Leaf"],
        "landmarks": ["Godavari Bridge", "Dowleswaram Barrage", "Papikondalu"],
        "petrol_bunks": ["HP - Morampudi", "Indian Oil - Innespeta", "BPCL - Godavari Bund"],
    },
    "Kadapa": {
        "malls": ["Urban Square Mall"],
        "restaurants": ["Hotel Sree Ram", "Haritha Hotel Kadapa"],
        "landmarks": ["Gandikota Fort", "Vontimitta Temple"],
        "petrol_bunks": ["HP - Railway Station Road", "Indian Oil - Beside Bus Stand", "BPCL - Cuddapah Bypass"],
    },
    "Kurnool": {
        "malls": ["Kurnool Central Mall", "Forum Mall"],
        "restaurants": ["Hotel Srinivasa", "Minerva Restaurant"],
        "landmarks": ["Belum Caves", "Tungabhadra Dam", "Srisailam Temple"],
        "petrol_bunks": ["HP - NH-44", "Indian Oil - Dinne Bypass", "BPCL - Budhawarpet"],
    },
    "Anantapur": {
        "malls": ["Anantapur City Center"],
        "restaurants": ["Hotel Surya", "MTR Anantapur"],
        "landmarks": ["Lepakshi Temple", "Thimmamma Marrimanu"],
        "petrol_bunks": ["HP - Bangalore Road", "Indian Oil - Subash Road", "BPCL - Anantapur Bypass"],
    },
    "Chittoor": {
        "malls": ["Chittoor Mall"],
        "restaurants": ["Hotel Viswa", "Hotel Mayuri"],
        "landmarks": ["Horsley Hills", "Kailasakona Waterfall"],
        "petrol_bunks": ["HP - Madanapalle Road", "Indian Oil - Punganur Road"],
    },
}

DEFAULT_POIS = {
    "malls": ["Local Shopping Centre", "Town Market"],
    "restaurants": ["Udupi Hotel", "Local Dhaba", "Annapoorna Restaurant"],
    "landmarks": ["Town Centre", "Local Temple", "Bus Stand"],
    "petrol_bunks": ["HP Petrol Bunk", "Indian Oil Bunk", "Local Petrol Station"],
}

# ══════════════════════════════════════════════════════════════════════════════
# GRAPH
# ══════════════════════════════════════════════════════════════════════════════
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def build_graph(max_dist_km=150.0):
    G = nx.Graph()
    city_list = list(AP_CITIES.items())
    for name, (lat, lon) in city_list:
        G.add_node(name, lat=lat, lon=lon)
    for i in range(len(city_list)):
        n1, (la1, lo1) = city_list[i]
        for j in range(i + 1, len(city_list)):
            n2, (la2, lo2) = city_list[j]
            d = haversine_km(la1, lo1, la2, lo2)
            if d <= max_dist_km:
                road_d = round(d * 1.30, 1)
                G.add_edge(n1, n2, weight=road_d)
    return G

G = build_graph()
ALL_CITIES = sorted(AP_CITIES.keys())

# ══════════════════════════════════════════════════════════════════════════════
# ALGORITHMS
# ══════════════════════════════════════════════════════════════════════════════
def run_dijkstra(G, source, target):
    import time
    t0 = time.perf_counter()
    
    try:
        path = nx.dijkstra_path(G, source, target, weight="weight")
        cost = nx.dijkstra_path_length(G, source, target, weight="weight")
    except Exception as e:
        return {"path": [], "cost": None, "time_ms": 0, "error": str(e)}

    elapsed = (time.perf_counter() - t0) * 1000

    return {
        "path": path,
        "cost": round(cost, 1),
        "time_ms": round(elapsed, 3),   # ✅ FIX
        "error": None
    }

def _collect_paths(G, source, target, max_paths=256):
    try:
        optimal = nx.dijkstra_path(G, source, target, weight="weight")
    except:
        optimal = None
    paths = []
    for p in nx.all_simple_paths(G, source, target, cutoff=7):
        paths.append(p)
        if len(paths) >= max_paths:
            break
    if optimal and optimal not in paths:
        paths.insert(0, optimal)
    return paths

def _path_cost(G, path):
    return sum(G[path[i]][path[i+1]]["weight"] for i in range(len(path)-1))

def run_grover(G, source, target, max_paths=200):
    import time
    t0 = time.perf_counter()

    paths = _collect_paths(G, source, target, max_paths)
    N = len(paths)

    if N == 0:
        return {"path": [], "cost": None, "time_ms": 0, "oracle_calls": 0, "error": "No paths"}

    costs = np.array([_path_cost(G, p) for p in paths], dtype=np.float64)
    optimal_cost = costs.min()

    threshold = optimal_cost * 1.10
    oracle_mask = (costs <= threshold).astype(np.float64)

    amplitudes = np.ones(N, dtype=np.float64) / math.sqrt(N)
    num_iter = max(1, round((math.pi / 4) * math.sqrt(N)))

    oracle_calls = 0   # ✅ NEW

    for _ in range(num_iter):
        oracle_calls += 1

        amplitudes = amplitudes * (1 - 2 * oracle_mask)
        mean_amp = amplitudes.mean()
        amplitudes = 2 * mean_amp - amplitudes

        norm = np.linalg.norm(amplitudes)
        if norm > 1e-12:
            amplitudes /= norm

    probs = amplitudes ** 2
    probs = np.clip(probs, 0, None)
    probs /= probs.sum()

    idx = int(np.random.choice(N, p=probs))

    elapsed = (time.perf_counter() - t0) * 1000

    return {
        "path": paths[idx],
        "cost": round(costs[idx], 1),
        "time_ms": round(elapsed, 3),     # ✅ NEW
        "oracle_calls": oracle_calls,     # ✅ NEW
        "error": None
    }

def get_all_paths(G, source, target, limit=8):
    """Get several simple paths sorted by cost."""
    all_paths = []
    try:
        for p in nx.all_simple_paths(G, source, target, cutoff=6):
            cost = _path_cost(G, p)
            all_paths.append((p, round(cost, 1)))
            if len(all_paths) >= limit:
                break
    except:
        pass
    all_paths.sort(key=lambda x: x[1])
    return all_paths

def combined_shortest_path(G, source, target):
    d = run_dijkstra(G, source, target)
    g = run_grover(G, source, target)

    if d["error"] and g["error"]:
        return None, None, None

    candidates = []
    if not d["error"]:
        candidates.append((d["path"], d["cost"]))
    if not g["error"]:
        candidates.append((g["path"], g["cost"]))

    candidates.sort(key=lambda x: x[1])

    comparison = {
        "dijkstra_time": d.get("time_ms", 0),
        "grover_time": g.get("time_ms", 0),
        "grover_oracle_calls": g.get("oracle_calls", 0)
    }

    return candidates[0][0], candidates[0][1], comparison

# ══════════════════════════════════════════════════════════════════════════════
# MAP BUILDER (Folium)
# ══════════════════════════════════════════════════════════════════════════════
def build_folium_map(source, target, shortest_path, all_paths):
    try:
        import folium
    except ImportError:
        return "<p style='color:red'>Install folium: pip install folium</p>"

    src_ll = AP_CITIES.get(source, (16.0, 80.5))
    tgt_ll = AP_CITIES.get(target, (16.0, 80.5))
    centre = ((src_ll[0]+tgt_ll[0])/2, (src_ll[1]+tgt_ll[1])/2)

    m = folium.Map(location=centre, zoom_start=7,
                   tiles="CartoDB positron", control_scale=True)

    # Draw all paths (faint)
    sp_set = set(zip(shortest_path[:-1], shortest_path[1:])) if shortest_path else set()
    drawn_edges = set()
    for path, cost in all_paths:
        is_shortest = (path == shortest_path)
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            key = frozenset([u, v])
            if key in drawn_edges and not is_shortest:
                continue
            drawn_edges.add(key)
            ll_u = AP_CITIES.get(u)
            ll_v = AP_CITIES.get(v)
            if not ll_u or not ll_v:
                continue
            if is_shortest:
                folium.PolyLine([ll_u, ll_v], color="#FF6B35", weight=6,
                                opacity=0.95, tooltip=f"{u}→{v}").add_to(m)
            else:
                folium.PolyLine([ll_u, ll_v], color="#6B8FD4", weight=2.5,
                                opacity=0.5, dash_array="8 4",
                                tooltip=f"{u}→{v}").add_to(m)

    # All graph edges (very faint background)
    for u, v, data in G.edges(data=True):
        key = frozenset([u, v])
        if key in drawn_edges:
            continue
        ll_u = AP_CITIES.get(u)
        ll_v = AP_CITIES.get(v)
        if not ll_u or not ll_v:
            continue
        folium.PolyLine([ll_u, ll_v], color="#CCCCCC", weight=1,
                        opacity=0.15).add_to(m)

    # Markers for cities on path
    path_cities = set(shortest_path) if shortest_path else set()
    for city in path_cities:
        ll = AP_CITIES.get(city)
        if not ll:
            continue
        pois = CITY_POIS.get(city, DEFAULT_POIS)
        if city == source:
            icon_color, icon_name = "green", "play"
        elif city == target:
            icon_color, icon_name = "red", "flag"
        else:
            icon_color, icon_name = "orange", "map-marker"

        popup_html = f"""
        <div style='font-family:Segoe UI,sans-serif;min-width:200px;max-width:260px'>
          <h3 style='margin:0 0 8px;color:#1a1a2e;font-size:16px'>📍 {city}</h3>
          <div style='background:#f8f9fa;border-radius:6px;padding:8px;margin-bottom:6px'>
            <b style='color:#e63946'>🏬 Malls</b><br>
            {'<br>'.join('• '+m for m in pois.get('malls',['—'])[:3])}
          </div>
          <div style='background:#f8f9fa;border-radius:6px;padding:8px;margin-bottom:6px'>
            <b style='color:#2d6a4f'>🍽️ Restaurants</b><br>
            {'<br>'.join('• '+r for r in pois.get('restaurants',['—'])[:3])}
          </div>
          <div style='background:#f8f9fa;border-radius:6px;padding:8px;margin-bottom:6px'>
            <b style='color:#e9c46a'>⛽ Petrol Bunks</b><br>
            {'<br>'.join('• '+b for b in pois.get('petrol_bunks',['—'])[:3])}
          </div>
          <div style='background:#f8f9fa;border-radius:6px;padding:8px'>
            <b style='color:#457b9d'>🏛️ Landmarks</b><br>
            {'<br>'.join('• '+l for l in pois.get('landmarks',['—'])[:2])}
          </div>
        </div>"""

        folium.Marker(
            location=ll,
            tooltip=f"📍 {city} — click for info",
            popup=folium.Popup(popup_html, max_width=280),
            icon=folium.Icon(color=icon_color, icon=icon_name, prefix="fa"),
        ).add_to(m)

    # Legend
    legend = """
    <div style="position:fixed;bottom:25px;left:25px;z-index:1000;
         background:white;border:1px solid #ddd;border-radius:10px;
         padding:12px 16px;font-family:Segoe UI,sans-serif;font-size:12px;box-shadow:0 2px 8px rgba(0,0,0,.15)">
      <b style="font-size:13px">🗺️ Legend</b><br><br>
      <span style="color:#FF6B35;font-weight:700">━━━</span> Shortest Path<br>
      <span style="color:#6B8FD4">╌╌╌</span> Alternate Paths<br>
      <span style="color:#aaa">━━━</span> Road Network<br><br>
      🟢 Start &nbsp; 🔴 End &nbsp; 🟠 Via
    </div>"""
    m.get_root().html.add_child(folium.Element(legend))
    return m._repr_html_()

# ══════════════════════════════════════════════════════════════════════════════
# RESULT BUILDERS
# ══════════════════════════════════════════════════════════════════════════════
def build_path_display(shortest_path, shortest_cost, all_paths):
    if not shortest_path:
        return "<div style='padding:20px;color:#e63946;font-size:16px'>❌ No route found between selected cities.</div>"

    # Shortest path details
    hops_html = ""
    running = 0
    for i in range(len(shortest_path)-1):
        u, v = shortest_path[i], shortest_path[i+1]
        w = G[u][v]["weight"]
        running += w
        hops_html += f"""
        <div style="display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid #f0f0f0">
          <span style="background:#FF6B35;color:white;border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0">{i+1}</span>
          <span style="font-weight:600;color:#1a1a2e">{u}</span>
          <span style="color:#aaa">→</span>
          <span style="font-weight:600;color:#1a1a2e">{v}</span>
          <span style="margin-left:auto;font-size:12px;color:#666;background:#f5f5f5;padding:2px 8px;border-radius:10px">{w} km</span>
          <span style="font-size:11px;color:#999">({round(running,1)} total)</span>
        </div>"""

    # All paths list
    paths_html = ""
    for idx, (path, cost) in enumerate(all_paths):
        is_best = (path == shortest_path)
        badge = '<span style="background:#FF6B35;color:white;border-radius:8px;padding:1px 8px;font-size:11px;margin-left:8px">★ SHORTEST</span>' if is_best else ""
        row_bg = "#fff8f5" if is_best else "white"
        path_str = " → ".join(path)
        paths_html += f"""
        <div style="background:{row_bg};border:1px solid {'#FF6B35' if is_best else '#e9ecef'};border-radius:8px;
             padding:10px 14px;margin-bottom:8px">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px">
            <span style="font-weight:700;color:#1a1a2e;font-size:13px">Path {idx+1}{badge}</span>
            <span style="font-weight:700;color:#FF6B35;font-size:15px">{cost} km</span>
          </div>
          <div style="font-size:12px;color:#555;line-height:1.6">{path_str}</div>
          <div style="font-size:11px;color:#999;margin-top:4px">{len(path)-1} hops &nbsp;·&nbsp; {len(path)} cities</div>
        </div>"""

    html = f"""
    <div style="font-family:'Segoe UI',sans-serif;max-width:100%">

      <!-- SHORTEST PATH CARD -->
      <div style="background:linear-gradient(135deg,#fff8f5,#fff);border:2px solid #FF6B35;
           border-radius:14px;padding:20px;margin-bottom:20px;box-shadow:0 4px 20px rgba(255,107,53,.12)">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
          <span style="font-size:28px">🏆</span>
          <div>
            <div style="font-size:18px;font-weight:800;color:#1a1a2e">Recommended Route</div>
            <div style="font-size:13px;color:#666">Optimal path from {shortest_path[0]} to {shortest_path[-1]}</div>
          </div>
          <div style="margin-left:auto;text-align:right">
            <div style="font-size:28px;font-weight:900;color:#FF6B35">{shortest_cost} km</div>
            <div style="font-size:12px;color:#999">{len(shortest_path)-1} hops</div>
          </div>
        </div>
        <div style="background:white;border-radius:10px;padding:14px;border:1px solid #ffe5d9">
          {hops_html}
        </div>
        <div style="margin-top:12px;font-size:13px;color:#888;display:flex;gap:6px;align-items:center">
          <span>🛣️</span>
          <span>Route: {' → '.join(shortest_path)}</span>
        </div>
      </div>

      <!-- ALL PATHS -->
      <div style="background:white;border:1px solid #e9ecef;border-radius:14px;padding:20px">
        <div style="font-size:15px;font-weight:700;color:#1a1a2e;margin-bottom:14px;display:flex;align-items:center;gap:8px">
          <span>🛤️</span> All Available Paths ({len(all_paths)} found)
        </div>
        {paths_html}
      </div>
    </div>"""
    return html

def build_poi_panel(city):
    pois = CITY_POIS.get(city, DEFAULT_POIS)

    def section(icon, label, color, items):
        pills = "".join(f'<span style="background:{color}15;color:{color};border:1px solid {color}40;border-radius:20px;padding:4px 12px;font-size:12px;display:inline-block;margin:3px">{item}</span>' for item in items)
        return f"""
        <div style="margin-bottom:16px">
          <div style="font-weight:700;color:#1a1a2e;margin-bottom:8px;font-size:13px">{icon} {label}</div>
          <div>{pills}</div>
        </div>"""

    html = f"""
    <div style="font-family:'Segoe UI',sans-serif;padding:4px">
      <h3 style="color:#1a1a2e;margin:0 0 16px;font-size:16px;border-bottom:2px solid #FF6B35;padding-bottom:8px">
        📍 {city} — Points of Interest
      </h3>
      {section('⛽', 'Petrol Bunks', '#e9c46a', pois.get('petrol_bunks', ['—']))}
      {section('🏬', 'Malls & Shopping', '#e63946', pois.get('malls', ['—']))}
      {section('🍽️', 'Restaurants', '#2d6a4f', pois.get('restaurants', ['—']))}
      {section('🏛️', 'Landmarks', '#457b9d', pois.get('landmarks', ['—']))}
    </div>"""
    return html

def build_stats_bar(source, target, shortest_path, shortest_cost, all_paths):
    nearby_src = sorted(
        [(n, G[source][n]["weight"]) for n in G.neighbors(source)],
        key=lambda x: x[1]
    )[:3]
    nearby_tgt = sorted(
        [(n, G[target][n]["weight"]) for n in G.neighbors(target)],
        key=lambda x: x[1]
    )[:3]

    nearby_src_str = ", ".join(f"{c} ({d}km)" for c,d in nearby_src)
    nearby_tgt_str = ", ".join(f"{c} ({d}km)" for c,d in nearby_tgt)

    html = f"""
    <div style="font-family:'Segoe UI',sans-serif;display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:4px">
      <div style="background:#fff8f5;border:1px solid #ffe5d9;border-radius:10px;padding:14px;text-align:center">
        <div style="font-size:22px;font-weight:900;color:#FF6B35">{shortest_cost}</div>
        <div style="font-size:11px;color:#999;text-transform:uppercase;letter-spacing:.5px">km (shortest)</div>
      </div>
      <div style="background:#f5f8ff;border:1px solid #dce8ff;border-radius:10px;padding:14px;text-align:center">
        <div style="font-size:22px;font-weight:900;color:#4361ee">{len(all_paths)}</div>
        <div style="font-size:11px;color:#999;text-transform:uppercase;letter-spacing:.5px">paths found</div>
      </div>
      <div style="background:#f5fff8;border:1px solid #d4edda;border-radius:10px;padding:14px;text-align:center">
        <div style="font-size:22px;font-weight:900;color:#2d6a4f">{len(shortest_path)-1}</div>
        <div style="font-size:11px;color:#999;text-transform:uppercase;letter-spacing:.5px">hops on route</div>
      </div>
      <div style="background:#fffbf5;border:1px solid #fff3cd;border-radius:10px;padding:14px;text-align:center">
        <div style="font-size:22px;font-weight:900;color:#e9c46a">{G.number_of_nodes()}</div>
        <div style="font-size:11px;color:#999;text-transform:uppercase;letter-spacing:.5px">cities in graph</div>
      </div>
    </div>
    <div style="font-family:'Segoe UI',sans-serif;margin-top:10px;display:grid;grid-template-columns:1fr 1fr;gap:12px">
      <div style="background:#f9f9f9;border-radius:10px;padding:12px;font-size:12px;color:#555">
        <b style="color:#1a1a2e">Near {source}:</b> {nearby_src_str}
      </div>
      <div style="background:#f9f9f9;border-radius:10px;padding:12px;font-size:12px;color:#555">
        <b style="color:#1a1a2e">Near {target}:</b> {nearby_tgt_str}
      </div>
    </div>"""
    return html

# ══════════════════════════════════════════════════════════════════════════════
# MAIN FIND ROUTE FUNCTION
# ══════════════════════════════════════════════════════════════════════════════
def find_route(source, target):
    if not source or not target:
        return (
            "<div style='padding:20px;color:#e63946'>Please select both Source and Destination.</div>",
            "<div style='padding:20px;color:#999'>Select cities and click Find Route.</div>",
            "<div style='padding:20px;color:#999'>POI info will appear here.</div>",
            "<div style='padding:20px;color:#999'>Stats will appear here.</div>",
            "<div style='padding:20px;color:#999'>POI info will appear here.</div>",
        )
    if source == target:
        return (
            "<div style='padding:20px;color:#e63946'>Source and Destination must be different cities.</div>",
            "<div style='padding:20px;color:#999'>—</div>",
            "<div style='padding:20px;color:#999'>—</div>",
            "<div style='padding:20px;color:#999'>—</div>",
            "<div style='padding:20px;color:#999'>—</div>",
        )

    shortest_path, shortest_cost, comparison = combined_shortest_path(G, source, target)
    all_paths = get_all_paths(G, source, target, limit=8)

    if not shortest_path:
        return (
            "<div style='padding:20px;color:#e63946'>No route found. Cities may not be connected.</div>",
            "<div style='padding:20px;color:#999'>—</div>",
            "<div style='padding:20px;color:#999'>—</div>",
            "<div style='padding:20px;color:#999'>—</div>",
            "<div style='padding:20px;color:#999'>—</div>",
        )

    path_html  = build_path_display(shortest_path, shortest_cost, all_paths)
    map_html   = build_folium_map(source, target, shortest_path, all_paths)
    poi_src    = build_poi_panel(source)
    poi_tgt    = build_poi_panel(target)
    stats_html = build_stats_bar(source, target, shortest_path, shortest_cost, all_paths)
    comparison_html = f"""
<div style="background:white;border:2px solid #FF6B35;border-radius:12px;padding:16px;margin-top:12px">

  <h3 style="margin:0 0 12px;color:#1a1a2e !important;font-weight:800">
    ⚖️ Algorithm Comparison
  </h3>

  <div style="display:flex;justify-content:space-between;margin-bottom:10px;font-size:15px">
    <span style="color:#000 !important;font-weight:800">Dijkstra Time</span>
    <span style="color:#FF6B35;font-weight:800">{comparison['dijkstra_time']} ms</span>
  </div>

  <div style="display:flex;justify-content:space-between;margin-bottom:10px;font-size:15px">
    <span style="color:#000 !important;font-weight:800">Grover Time</span>
    <span style="color:#4361ee;font-weight:800">{comparison['grover_time']} ms</span>
  </div>

  <div style="display:flex;justify-content:space-between;font-size:15px">
    <span style="color:#000 !important;font-weight:800">Grover Oracle Calls</span>
    <span style="color:#2d6a4f;font-weight:800">{comparison['grover_oracle_calls']}</span>
  </div>

</div>
"""

    return map_html, path_html, poi_src, stats_html + comparison_html, poi_tgt

# ══════════════════════════════════════════════════════════════════════════════
# GRADIO UI
# ══════════════════════════════════════════════════════════════════════════════
CSS = """
body, .gradio-container {
    font-family: 'Segoe UI', system-ui, sans-serif !important;
    background: #f7f8fc !important;
}
.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
}
.app-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 20px;
    color: white;
    display: flex;
    align-items: center;
    gap: 20px;
}
#find-btn {
    background: linear-gradient(135deg, #FF6B35, #e63946) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 14px !important;
    box-shadow: 0 4px 20px rgba(255,107,53,.4) !important;
    transition: all .2s !important;
}
#find-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px rgba(255,107,53,.55) !important;
}
.section-label {
    font-weight: 700;
    font-size: 13px;
    color: #1a1a2e;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin-bottom: 6px;
}
.gr-dropdown {
    border-radius: 10px !important;
    border: 1.5px solid #dee2e6 !important;
}
footer { display: none !important; }
"""

HEADER_HTML = """
<div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);border-radius:16px;
     padding:24px 32px;margin-bottom:4px;color:white;display:flex;align-items:center;gap:18px">
  <span style="font-size:48px">🗺️</span>
  <div>
    <div style="font-size:26px;font-weight:900;letter-spacing:-0.5px">AP Smart Route Finder</div>
    <div style="font-size:13px;color:#a8c6fa;margin-top:4px">
      Andhra Pradesh · All-Paths Route Planner · Real-time Map · POI Explorer
    </div>
    <div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap">
      <span style="background:#FF6B3530;color:#FF6B35;border:1px solid #FF6B3560;border-radius:6px;padding:2px 10px;font-size:11px">⚡ Smart Routing</span>
      <span style="background:#4361ee30;color:#a8c6fa;border:1px solid #4361ee60;border-radius:6px;padding:2px 10px;font-size:11px">🗺️ Live OSM Map</span>
      <span style="background:#2d6a4f30;color:#95d5b2;border:1px solid #2d6a4f60;border-radius:6px;padding:2px 10px;font-size:11px">⛽ Petrol Bunks</span>
      <span style="background:#e9c46a30;color:#e9c46a;border:1px solid #e9c46a60;border-radius:6px;padding:2px 10px;font-size:11px">🏬 Malls & Restaurants</span>
    </div>
  </div>
</div>
"""

with gr.Blocks(css=CSS, title="AP Route Finder") as demo:

    gr.HTML(HEADER_HTML)

    with gr.Row():
        with gr.Column(scale=1, min_width=220):
            src_dd = gr.Dropdown(
                choices=ALL_CITIES,
                label="🚀 Starting City",
                value="Vijayawada",
                interactive=True,
            )
        with gr.Column(scale=1, min_width=220):
            tgt_dd = gr.Dropdown(
                choices=ALL_CITIES,
                label="🏁 Destination City",
                value="Visakhapatnam",
                interactive=True,
            )
        with gr.Column(scale=1, min_width=180):
            find_btn = gr.Button("🔍 Find Best Route", elem_id="find-btn", size="lg")

    stats_out = gr.HTML(
        value="<div style='padding:14px;color:#999;font-family:Segoe UI,sans-serif;text-align:center'>Select cities above and click Find Best Route</div>",
        label="",
    )

    with gr.Row():
        with gr.Column(scale=3):
            gr.HTML("<div class='section-label'>🗺️ Interactive Map — click city markers for POIs</div>")
            map_out = gr.HTML(
                value="<div style='height:500px;background:#f0f4f8;border-radius:14px;display:flex;align-items:center;justify-content:center;color:#aaa;font-size:16px;font-family:Segoe UI'>Map will load here after searching</div>",
            )

        with gr.Column(scale=2):
            gr.HTML("<div class='section-label'>🛤️ Route Details & All Paths</div>")
            path_out = gr.HTML(
                value="<div style='padding:20px;color:#aaa;font-family:Segoe UI'>Route info will appear here</div>",
            )

    with gr.Row():
        with gr.Column():
            gr.HTML("<div class='section-label'>📍 Source City — Nearby Places</div>")
            poi_src_out = gr.HTML(
                value="<div style='padding:20px;color:#aaa;font-family:Segoe UI'>Select a source city</div>",
            )
        with gr.Column():
            gr.HTML("<div class='section-label'>📍 Destination City — Nearby Places</div>")
            poi_tgt_out = gr.HTML(
                value="<div style='padding:20px;color:#aaa;font-family:Segoe UI'>Select a destination city</div>",
            )

    gr.HTML("""
    <div style='text-align:center;font-family:Segoe UI,sans-serif;font-size:11px;color:#aaa;padding:16px 0 4px'>
      AP Smart Route Finder · 70+ Andhra Pradesh cities · Smart path optimization · OpenStreetMap tiles
    </div>""")

    find_btn.click(
        fn=find_route,
        inputs=[src_dd, tgt_dd],
        outputs=[map_out, path_out, poi_src_out, stats_out, poi_tgt_out],
    )

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)