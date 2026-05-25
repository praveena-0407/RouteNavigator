"""
map_utils.py
Builds interactive Folium maps on top of real OpenStreetMap tiles.
"""

import folium
from graph_builder import get_city_coords, AP_CITIES

COL_DIJKSTRA  = "#00e676"
COL_GROVER    = "#ff1744"
COL_BOTH      = "#ffea00"


def _edge_set(path):
    return {frozenset([path[i], path[i+1]]) for i in range(len(path)-1)}


def build_map(G, dijkstra_result, grover_result, source, target, nearby_cities=None):
    src_ll  = get_city_coords(source)
    dst_ll  = get_city_coords(target)

    if src_ll and dst_ll:
        centre = ((src_ll[0]+dst_ll[0])/2, (src_ll[1]+dst_ll[1])/2)
    else:
        centre = (16.0, 80.5)

    m = folium.Map(
        location=centre,
        zoom_start=7,
        tiles="CartoDB dark_matter",
        control_scale=True,
    )

    d_edges = _edge_set(dijkstra_result.get("path", []))
    g_edges = _edge_set(grover_result.get("path", []))

    for u, v, data in G.edges(data=True):
        edge_key = frozenset([u, v])
        ll_u = get_city_coords(u)
        ll_v = get_city_coords(v)
        if not ll_u or not ll_v:
            continue
        in_d = edge_key in d_edges
        in_g = edge_key in g_edges
        if in_d and in_g:
            color, weight, dash, opacity = COL_BOTH, 7, None, 0.95
        elif in_d:
            color, weight, dash, opacity = COL_DIJKSTRA, 6, None, 0.9
        elif in_g:
            color, weight, dash, opacity = COL_GROVER, 5, "10 5", 0.85
        else:
            color, weight, dash, opacity = "#334", 1.2, None, 0.3
        folium.PolyLine(
            locations=[ll_u, ll_v],
            color=color, weight=weight, opacity=opacity, dash_array=dash,
            tooltip=f"{u} \u2194 {v}  ({data.get('weight','')} km)",
        ).add_to(m)

    d_path = dijkstra_result.get("path", [])
    g_path = grover_result.get("path", [])
    path_cities = set(d_path + g_path)

    for city in G.nodes():
        ll = get_city_coords(city)
        if not ll:
            continue
        if city == source:
            icon_color, icon = "orange", "play"
        elif city == target:
            icon_color, icon = "red", "flag"
        elif city in path_cities:
            icon_color, icon = "green", "map-marker"
        else:
            icon_color, icon = "purple", "circle"

        popup_html = f"""
        <div style='font-family:monospace;font-size:13px;min-width:160px'>
          <b style='font-size:15px'>{city}</b><br>
          Lat: {ll[0]:.4f} | Lon: {ll[1]:.4f}<br>
          {'<b style="color:#00e676">On Dijkstra path</b><br>' if city in d_path else ''}
          {'<b style="color:#ff1744">On Grover path</b><br>' if city in g_path else ''}
        </div>"""

        folium.Marker(
            location=ll, tooltip=city,
            popup=folium.Popup(popup_html, max_width=220),
            icon=folium.Icon(color=icon_color, icon=icon, prefix="fa"),
        ).add_to(m)

    if nearby_cities:
        for city in nearby_cities:
            ll = get_city_coords(city)
            if not ll:
                continue
            folium.CircleMarker(
                location=ll, radius=10, color="#ffd740",
                fill=True, fill_color="#ffd740", fill_opacity=0.3,
                tooltip=f"Nearby: {city}",
            ).add_to(m)

    legend_html = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
                background:#0d1117;border:1px solid #30363d;border-radius:8px;
                padding:12px 16px;font-family:monospace;font-size:12px;color:#e6edf3">
      <b style="font-size:13px;color:#58a6ff">LEGEND</b><br><br>
      <span style="color:#00e676">&#9473;&#9473;&#9473;</span>  Dijkstra path<br>
      <span style="color:#ff1744">&#9484;&#9484;&#9484;</span>  Grover path<br>
      <span style="color:#ffea00">&#9473;&#9473;&#9473;</span>  Shared route<br>
      <span style="color:#555">&#9473;&#9473;&#9473;</span>  Road edge<br><br>
      Source (orange) | Target (red)<br>
      On route (green) | Other (purple)
    </div>"""
    m.get_root().html.add_child(folium.Element(legend_html))
    return m._repr_html_()


def get_nearby_cities(city, G, n=5):
    if city not in G:
        return []
    neighbors = [{"city": nbr, "dist_km": G[city][nbr]["weight"]} for nbr in G.neighbors(city)]
    neighbors.sort(key=lambda x: x["dist_km"])
    return neighbors[:n]