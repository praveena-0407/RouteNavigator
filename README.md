# AP Smart Route Finder — Gradio Edition

## Live Demo
https://huggingface.co/spaces/SaiPraveena04/RouteNavigator

A clean, single-file route planner for Andhra Pradesh cities with:
- ✅ Dropdown city selector (70+ AP cities)
- ✅ All paths found and listed (sorted shortest to longest)
- ✅ Shortest path highlighted on real OpenStreetMap
- ✅ Click city markers on map for Malls, Restaurants, Petrol Bunks, Landmarks
- ✅ Stats bar (total km, number of paths, hops)
- ✅ Simple Gradio UI — no Streamlit needed

---

## 🚀 Setup (3 steps)

```bash
# 1. Install dependencies
pip install gradio networkx numpy folium

# 2. Run
python app_gradio.py

# 3. Open browser
# → http://localhost:7860
```

---

## How to Use

1. **Select Starting City** from the dropdown (e.g. Vijayawada)
2. **Select Destination City** (e.g. Visakhapatnam)
3. Click **🔍 Find Best Route**

### What you'll see:
| Section | Description |
|---|---|
| **Stats Bar** | Total km, paths found, hops, nearby cities |
| **Map** | Real OSM map — orange line = shortest, blue dashes = alternates |
| **Route Details** | Step-by-step breakdown with distances |
| **All Paths** | Every route found, sorted by distance |
| **POI Panels** | Petrol bunks, malls, restaurants, landmarks for source & destination |

### Map Popups
Click any 📍 marker on the map to see:
- ⛽ Petrol Bunks near that city
- 🏬 Malls & Shopping
- 🍽️ Restaurants  
- 🏛️ Landmarks

---

## File Structure

```
app_gradio.py      ← Single file — everything is here
requirements.txt   ← pip install -r requirements.txt
```

---

## Algorithm
The app uses two complementary algorithms internally and picks the best confirmed result:
- **Dijkstra** — guaranteed optimal, O(E + V log V)
- **Grover Amplitude Amplification** — quantum-inspired search, O(√N)

The result shown is always the shortest confirmed path — no algorithm labels shown to the user.

## Cities Covered
70+ cities including all district HQs, major towns across:
- North Andhra: Visakhapatnam, Srikakulam, Vizianagaram
- Godavari: Rajahmundry, Kakinada, Eluru, Bhimavaram
- Krishna: Vijayawada, Machilipatnam, Gudivada
- Guntur: Guntur, Tenali, Narasaraopet
- South Coastal: Nellore, Ongole, Kavali
- Rayalaseema: Kurnool, Kadapa, Anantapur, Chittoor, Tirupati
