"""Build exodata.js for cosmos3d.html.   Run:  python3 exoplanets.py

1. Tries the NASA Exoplanet Archive (full list, always up to date).
2. If NASA can't be reached, falls back to the Open Exoplanet Catalogue on GitHub.

Only Python's standard library is used. Each output row is:
[name, host star, distance (light-years), year found, method,
 radius (Earths), mass (Earths), orbit (days), RA (deg), Dec (deg), star brightness (vmag)]
"""
import csv, io, json, urllib.parse, urllib.request

NASA = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?" + urllib.parse.urlencode({
    "query": "select pl_name,hostname,sy_dist,disc_year,discoverymethod,pl_rade,"
             "pl_bmasse,pl_orbper,ra,dec,sy_vmag from pscomppars",
    "format": "csv"})
OEC = ("https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/"
       "master/comma_separated/open_exoplanet_catalogue.txt")
PC_TO_LY = 3.26156          # parsec -> light-year
JUPITER_RADIUS_IN_EARTHS = 11.209
JUPITER_MASS_IN_EARTHS = 317.83
METHODS = {"transit": "Transit", "RV": "Radial Velocity", "imaging": "Imaging",
           "microlensing": "Microlensing", "timing": "Timing"}


def download(url):
    return urllib.request.urlopen(url, timeout=60).read().decode("utf-8", "ignore")


def num(text, factor=1.0, digits=3):
    """'12.5' -> 12.5 * factor, rounded. Empty or bad text -> None."""
    try:
        return round(float(text) * factor, digits)
    except (TypeError, ValueError):
        return None


def sexagesimal(text, is_ra):
    """'19 19 43.4' -> degrees. RA is in hours, so it is multiplied by 15."""
    negative = text.strip().startswith("-")
    h, m, s = [abs(float(part)) for part in text.replace("+", "").split()]
    value = h + m / 60 + s / 3600
    return round((-value if negative else value) * (15 if is_ra else 1), 4)


def from_nasa():
    rows = []
    for r in csv.DictReader(io.StringIO(download(NASA))):
        rows.append([r["pl_name"], r["hostname"], num(r["sy_dist"], PC_TO_LY, 1),
                     int(r["disc_year"]) if r["disc_year"] else None, r["discoverymethod"],
                     num(r["pl_rade"], 1, 2), num(r["pl_bmasse"], 1, 1), num(r["pl_orbper"], 1, 2),
                     num(r["ra"], 1, 4), num(r["dec"], 1, 4), num(r["sy_vmag"], 1, 2)])
    return rows, "NASA Exoplanet Archive"


def from_oec():
    rows = []
    for r in csv.DictReader(io.StringIO(download(OEC))):
        if r["list"] != "Confirmed planets":
            continue
        name = r["name"]
        try:
            ra = sexagesimal(r["system_rightascension"], True)
            dec = sexagesimal(r["system_declination"], False)
        except ValueError:
            ra = dec = None
        rows.append([name, name.rsplit(" ", 1)[0], num(r["system_distance"], PC_TO_LY, 1),
                     int(r["discoveryyear"]) if r["discoveryyear"] else None,
                     METHODS.get(r["discoverymethod"], "Other"),
                     num(r["radius"], JUPITER_RADIUS_IN_EARTHS, 2),
                     num(r["mass"], JUPITER_MASS_IN_EARTHS, 1),
                     num(r["period"], 1, 2), ra, dec, None])   # this catalogue has no vmag
    return rows, "Open Exoplanet Catalogue snapshot"


def main():
    try:
        rows, source = from_nasa()
    except Exception as err:                                    # no internet to NASA, blocked, etc.
        print("NASA not reachable (%s). Using the Open Exoplanet Catalogue instead." % err)
        rows, source = from_oec()
    with open("exodata.js", "w", encoding="utf-8") as f:
        f.write("window.EXSRC=%s;window.EXO=%s;" % (
            json.dumps(source), json.dumps(rows, separators=(",", ":"), ensure_ascii=False)))
    print("%d planets from %s written to exodata.js" % (len(rows), source))


if __name__ == "__main__":
    main()