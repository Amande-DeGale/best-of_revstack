#!/usr/bin/env python3
"""Soumission IndexNow des URLs du sitemap (Bing/Yandex).
Lit les URLs de sitemap.xml a la racine du depot.
La cle vient de la variable d'environnement INDEXNOW_KEY
(le workflow la lit dans le fichier cle public, jamais ecrite en dur).
La cle n'est jamais affichee : seuls le statut HTTP et le nombre d'URLs le sont.
"""
import json, os, sys, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

SITEMAP = Path(__file__).resolve().parent.parent / "sitemap.xml"
ENDPOINT = "https://api.indexnow.org/indexnow"
HOST = "amande-degale.github.io"

def main():
    key = os.environ.get("INDEXNOW_KEY")
    if not key:
        print("INDEXNOW_KEY manquante. Abandon.", file=sys.stderr)
        sys.exit(2)
    tree = ET.parse(SITEMAP)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [e.text for e in tree.getroot().findall("sm:url/sm:loc", ns)]
    print(f"{len(urls)} URLs a soumettre pour {HOST}")
    payload = json.dumps({"host": HOST, "key": key,
        "keyLocation": f"https://{HOST}/best-of_revstack/{key}.txt",
        "urlList": urls}).encode()
    req = urllib.request.Request(ENDPOINT, data=payload,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        print("IndexNow :", resp.status)

if __name__ == "__main__":
    main()
