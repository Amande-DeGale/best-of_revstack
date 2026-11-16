#!/usr/bin/env python3
"""Soumission IndexNow (Bing/Yandex).
Par defaut : toutes les URLs de sitemap.xml a la racine du depot.
Avec --urls-file <fichier> : seulement les URLs liste dans le fichier
(une par ligne) — utilise par le workflow pour les nouvelles pages.
La cle vient de la variable d'environnement INDEXNOW_KEY
(le workflow la lit dans le fichier cle public, jamais ecrite en dur).
La cle n'est jamais affichee : seuls le statut HTTP et le nombre d'URLs le sont.
"""
import argparse, json, os, sys, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

SITEMAP = Path(__file__).resolve().parent.parent / "sitemap.xml"
ENDPOINT = "https://api.indexnow.org/indexnow"
HOST = "amande-degale.github.io"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls-file", default=None,
        help="Fichier avec une URL par ligne (sinon : tout le sitemap)")
    args = ap.parse_args()
    key = os.environ.get("INDEXNOW_KEY")
    if not key:
        print("INDEXNOW_KEY manquante. Abandon.", file=sys.stderr)
        sys.exit(2)
    if args.urls_file:
        urls = [l.strip() for l in Path(args.urls_file).read_text().splitlines()
                if l.strip()]
    else:
        tree = ET.parse(SITEMAP)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [e.text for e in tree.getroot().findall("sm:url/sm:loc", ns)]
    if not urls:
        print("Aucune URL a soumettre.")
        return
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
