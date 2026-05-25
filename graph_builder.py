"""
graph_builder.py
Builds an Andhra Pradesh road graph with 80+ cities/towns.
Edge weight = haversine × 1.30 road-winding factor.
"""

import math
import networkx as nx

# ── All AP cities/towns with lat/lon ─────────────────────────────────────────
AP_CITIES = {
    # Major cities
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
    # District HQs and major towns
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
    "Tekkali":        (18.6075, 84.2346),
    "Parvathipuram":  (18.7828, 83.4253),
    "Salur":          (18.5247, 83.2025),
    "Gajapathinagaram":(18.3269, 83.6020),
    "Rajam":          (18.4730, 83.6469),
    "Narasannapeta":  (18.4148, 84.0419),
    "Pundi":          (18.0996, 83.5868),
    "Payakaraopeta":  (17.3603, 82.8651),
    "Narsipatnam":    (17.6658, 82.6117),
    "Anakapalle":     (17.6910, 83.0000),
    "Bheemunipatnam": (17.8900, 83.4500),
    "Yellamanchili":  (17.5543, 82.8555),
    "Chodavaram":     (17.8396, 83.1122),
    "Pendurthi":      (17.8078, 83.2265),
    "Yelamanchili":   (17.5543, 82.8555),
    "Madanapalle":    (13.5545, 78.5011),
    "Hindupur":       (13.8294, 77.4911),
    "Dharmavaram":    (14.4113, 77.7181),
    "Tadipatri":      (14.9101, 78.0094),
    "Guntakal":       (15.1712, 77.3726),
    "Adoni":          (15.6279, 77.2744),
    "Nandyal":        (15.4786, 78.4836),
    "Atmakur":        (15.8760, 78.5869),
    "Proddatur":      (14.7500, 78.5500),
    "Jammalamadugu":  (14.8486, 78.3892),
    "Rajampet":       (14.1931, 79.1621),
    "Badvel":         (14.7455, 79.0643),
    "Pulivendula":    (14.4224, 78.2277),
    "Yerraguntla":    (14.6353, 78.5333),
    "Cuddapah":       (14.4674, 78.8241),
    "Allagadda":      (15.1417, 78.5304),
    "Srisailam":      (16.0833, 78.8833),
    "Markapur":       (15.7407, 79.2682),
    "Kandukur":       (15.2143, 79.9057),
    "Kavali":         (14.9165, 79.9932),
    "Gudur":          (14.1459, 79.8516),
    "Sullurpeta":     (13.7630, 79.8878),
    "Venkatagiri":    (13.9617, 79.5812),
    "Atmakur_NLR":    (14.6213, 79.6357),
    "Kovur":          (14.4916, 80.0184),
    "Rapur":          (13.9589, 79.4819),
    "Srikalahasti":   (13.7500, 79.6983),
    "Puttur":         (13.4408, 79.5493),
    "Pileru":         (13.6583, 79.1167),
    "Palamaneru":     (13.2050, 78.7433),
    "Punganur":       (13.3674, 78.5805),
    "Vayalpadu":      (13.5800, 78.6600),
    "Pakala":         (13.4655, 79.1144),
    "Nagari":         (13.3200, 79.5800),
    "Palamaner":      (13.2050, 78.7433),
    "Kuppam":         (12.7500, 78.3333),
    "Peddapuram":     (17.0786, 82.1360),
    "Samalkot":       (17.0582, 82.1761),
    "Tuni":           (17.3586, 82.5476),
    "Prathipadu":     (17.1900, 82.0730),
    "Amalapuram":     (16.5771, 82.0056),
    "Razole":         (16.4784, 81.8413),
    "Mandapeta":      (16.8667, 81.9333),
    "Kovvur":         (17.0167, 81.7333),
    "Nidadavolu":     (17.0578, 81.6728),
    "Jangareddigudem":(17.0074, 81.3007),
    "Akiveedu":       (16.5800, 81.3850),
    "Tanuku":         (16.8600, 81.6800),
    "Palakollu":      (16.5155, 81.7301),
    "Narsapur":       (16.4344, 81.6958),
    "Kanuru":         (16.4900, 80.7000),
    "Kondapalli":     (16.6169, 80.5460),
    "Ibrahimpatnam":  (16.5380, 80.6440),
    "Penamaluru":     (16.4700, 80.6800),
    "Nuzvid":         (16.7853, 80.8459),
    "Gudivada":       (16.4327, 80.9943),
    "Vuyyuru":        (16.3618, 80.8459),
    "Repalle":        (16.0186, 80.8306),
    "Vinukonda":      (16.0500, 79.7333),
    "Sattenapalle":   (16.3932, 80.1528),
    "Ponnur":         (16.0706, 80.5538),
    "Piduguralla":    (16.4757, 79.8985),
    "Macherla":       (16.4795, 79.4352),
    "Gurazala":       (16.5819, 79.6197),
    "Rentachintala":  (16.5505, 79.5764),
    "Dachepalli":     (16.2985, 79.8498),
    "Phirangipuram":  (16.3059, 80.2167),
    "Chilakaluripet": (16.0875, 80.1689),
    "Mangalagiri":    (16.4307, 80.5525),
    "Tadikonda":      (16.5100, 80.4200),
    "Amaravati":      (16.5730, 80.3564),
}

# ── Nearby POIs (malls, restaurants, landmarks) ───────────────────────────────
CITY_POIS = {
    "Visakhapatnam": {
        "malls": ["CMR Central Mall", "Jagadamba Junction Mall", "Gajuwaka Mall", "Pothys Mall"],
        "restaurants": ["Dwaraka Hotel", "Bamboo Bay", "The Park Vizag", "Sea View Restaurant", "Hotel Meghalaya"],
        "landmarks": ["Kailasagiri", "Rishikonda Beach", "INS Kurusura Submarine Museum", "Araku Valley"],
    },
    "Vijayawada": {
        "malls": ["PVP Square", "One Town Mall", "AMB Mall", "AP State Mall"],
        "restaurants": ["Hotel Swagath", "Minerva Coffee Shop", "Babai Hotel", "Hotel Mamta", "Curry Leaf"],
        "landmarks": ["Kanaka Durga Temple", "Prakasam Barrage", "Undavalli Caves", "Bhavani Island"],
    },
    "Guntur": {
        "malls": ["KLM Fashion Mall", "Big Bazaar Guntur", "Sujatha Mall"],
        "restaurants": ["Nagarjuna Restaurant", "Hotel Dwaraka", "Singareni Canteen", "Udupi Hotel"],
        "landmarks": ["Undavalli Caves", "Amaravati Museum", "Kondaveedu Fort"],
    },
    "Tirupati": {
        "malls": ["Leela Mahal Mall", "Star Mall Tirupati"],
        "restaurants": ["Hotel Bliss", "Annapurna Hotel", "Bhimas Deluxe", "Minerva Grand"],
        "landmarks": ["Tirumala Temple", "Sri Padmavathi Temple", "Chandragiri Fort", "Silathoranam"],
    },
    "Nellore": {
        "malls": ["Leela Mall", "Spencers Nellore", "City Center Mall"],
        "restaurants": ["Hotel Sreyas", "Kamat Hotel", "Hotel Bhimas", "Spice Garden"],
        "landmarks": ["Pulicat Lake", "Mypad Beach", "Sri Ranganathaswamy Temple"],
    },
    "Rajahmundry": {
        "malls": ["Rajahmundry Mall", "City Center", "VKC Mall"],
        "restaurants": ["Hotel Anand", "Haritha Hotel", "Surrendra Hotel", "Bay Leaf"],
        "landmarks": ["Godavari Bridge", "Dowleswaram Barrage", "ISKCON Temple", "Papikondalu"],
    },
    "Kadapa": {
        "malls": ["Urban Square Mall", "City Square Kadapa"],
        "restaurants": ["Hotel Sree Ram", "Haritha Hotel Kadapa", "Navaratna Hotel"],
        "landmarks": ["Gandikota Fort", "Vontimitta Temple", "Sidhout Fort"],
    },
    "Kurnool": {
        "malls": ["Kurnool Central Mall", "Forum Mall"],
        "restaurants": ["Hotel Srinivasa", "Hotel Rajeswari", "Minerva Restaurant"],
        "landmarks": ["Belum Caves", "Tungabhadra Dam", "Srisailam Temple", "Oravakal Rocks"],
    },
    "Anantapur": {
        "malls": ["Anantapur City Center", "BigBazaar Anantapur"],
        "restaurants": ["Hotel Surya", "MTR Anantapur", "Ruchi Restaurant"],
        "landmarks": ["Lepakshi Temple", "Thimmamma Marrimanu", "Penna River"],
    },
    "Chittoor": {
        "malls": ["Chittoor Mall", "Leela Shopping Center"],
        "restaurants": ["Hotel Viswa", "KFC Chittoor", "Hotel Mayuri"],
        "landmarks": ["Horsley Hills", "Kailasakona Waterfall", "Nagari Hills"],
    },
}

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def build_proximity_graph(cities: dict, max_dist_km: float = 150.0) -> nx.Graph:
    G = nx.Graph()
    city_list = list(cities.items())
    for name, (lat, lon) in city_list:
        G.add_node(name, lat=lat, lon=lon)
    for i in range(len(city_list)):
        n1, (la1, lo1) = city_list[i]
        for j in range(i + 1, len(city_list)):
            n2, (la2, lo2) = city_list[j]
            d = haversine_km(la1, lo1, la2, lo2)
            if d <= max_dist_km:
                road_d = round(d * 1.30, 1)
                G.add_edge(n1, n2, weight=road_d, distance_km=road_d)
    return G


def get_graph(cities=None, max_dist_km: float = 150.0) -> nx.Graph:
    if cities is None:
        cities = AP_CITIES
    return build_proximity_graph(cities, max_dist_km)


def get_all_cities():
    return sorted(AP_CITIES.keys())


def get_city_coords(city: str):
    return AP_CITIES.get(city)


def get_city_pois(city: str):
    return CITY_POIS.get(city, {
        "malls": ["Local Shopping Complex", "Govt Market"],
        "restaurants": ["Udupi Hotel", "Local Dhaba", "Annapoorna Restaurant"],
        "landmarks": ["Town Center", "Local Temple"],
    })