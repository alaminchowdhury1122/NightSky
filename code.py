"""Download the full NASA Exoplanet Archive and write exodata.js for cosmos3d.html.
Run:  python3 exoplanets.py      (needs internet, no extra packages)
Then keep exodata.js in the same folder as cosmos3d.html and reload the page."""
import csv, io, urllib.parse, urllib.request

QUERY = ("select pl_name,hostname,sy_dist,disc_year,discoverymethod,pl_rade,pl_bmasse,"
         "pl_orbper,ra,dec,sy_vmag from pscomppars")
URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?" + urllib.parse.urlencode(
    {"query": QUERY, "format": "csv"})

def num(v, nd=3, k=1.0):
    try:
        return round(float(v) * k, nd)
    except (TypeError, ValueError):
        return None

raw = urllib.request.urlopen(URL, timeout=60).read().decode("utf-8")
rows = []
for r in csv.DictReader(io.StringIO(raw)):
    rows.append([r["pl_name"], r["hostname"], num(r["sy_dist"], 1, 3.26156),  # parsec -> light-years
                 int(r["disc_year"]) if r["disc_year"] else None, r["discoverymethod"],
                 num(r["pl_rade"]), num(r["pl_bmasse"]), num(r["pl_orbper"]),
                 num(r["ra"], 4), num(r["dec"], 4), num(r["sy_vmag"], 2)])

def js(v):
    if v is None: return "null"
    if isinstance(v, str): return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return str(v)

with open("exodata.js", "w", encoding="utf-8") as f:
    f.write("window.EXO=[" + ",".join("[" + ",".join(js(x) for x in row) + "]" for row in rows) + "];")
print(len(rows), "exoplanets written to exodata.js")
