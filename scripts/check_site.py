#!/usr/bin/env python3
"""Vérifie les pages statiques avant publication, sans requêtes externes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote
import json, re, subprocess, sys, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
BASE='https://amande-degale.github.io/best-of_revstack/'
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags=[]; self.scripts=[]; self.script=None; self.title=''; self.in_title=False
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append((tag,attrs))
        if tag=='script': self.script={'attrs':attrs,'code':''}
        if tag=='title': self.in_title=True
    def handle_data(self, text):
        if self.script is not None: self.script['code']+=text
        if self.in_title: self.title+=text
    def handle_endtag(self, tag):
        if tag=='script' and self.script is not None: self.scripts.append(self.script); self.script=None
        if tag=='title': self.in_title=False

def main():
    errors=[]; scripts=[]; count=0; refs=0; canonicals=set()
    for f in sorted(ROOT.rglob('*.html')):
        if any(x in f.parts for x in ['node_modules','.git','.cache']): continue
        if f.name.startswith('google') and f.parent==ROOT: continue
        count+=1; rel=f.relative_to(ROOT).as_posix(); src=f.read_text(); parser=Parser(); parser.feed(src)
        pageurl=urljoin(BASE,rel.removesuffix('index.html'))
        if not parser.title: errors.append(f'{rel}: titre absent')
        if not any(t=='h1' for t,a in parser.tags): errors.append(f'{rel}: H1 absent')
        canonical=[a.get('href') for t,a in parser.tags if t=='link' and a.get('rel')=='canonical']
        if canonical!=[pageurl]: errors.append(f'{rel}: canonique inattendue {canonical}')
        if canonical and canonical[0] in canonicals: errors.append(f'{rel}: canonique dupliquée')
        canonicals.update(canonical)
        if 'cdn.tailwindcss.com' in src or 'tailwind.config =' in src: errors.append(f'{rel}: chargeur CSS CDN résiduel')
        for tag,attrs in parser.tags:
            for key in (['href'] if tag in ['a','link'] else ['src'] if tag in ['script','img'] else []):
                value=attrs.get(key,'')
                if not value or value.startswith(('mailto:','tel:','javascript:','#','data:')): continue
                u=urlparse(urljoin(pageurl,value))
                if u.netloc!='amande-degale.github.io': continue
                refs+=1
                if not u.path.startswith('/best-of_revstack/'): errors.append(f'{rel}: lien hors projet {value}'); continue
                dest=ROOT/unquote(u.path[len('/best-of_revstack/'):])
                if dest.is_dir(): dest=dest/'index.html'
                if not dest.is_file(): errors.append(f'{rel}: cible absente {value}')
        for script in parser.scripts:
            if script['attrs'].get('type')=='application/ld+json':
                try: json.loads(script['code'])
                except ValueError as e: errors.append(f'{rel}: JSON-LD {e}')
            elif not script['attrs'].get('src'): scripts.append({'file':rel,'code':script['code']})
    sitemap=ET.parse(ROOT/'sitemap.xml').getroot()
    urls=[e.text for e in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if len(urls)!=len(set(urls)): errors.append('URL dupliquée dans le sitemap')
    if set(urls)!=canonicals: errors.append('Sitemap et pages canoniques divergent')
    ET.parse(ROOT/'feed.xml')
    js="const fs=require('fs'),vm=require('vm');let errors=[];for(const s of JSON.parse(fs.readFileSync(0,'utf8'))){try{new vm.Script(s.code)}catch(e){errors.push(s.file+': '+e.message)}}console.log(JSON.stringify(errors));"
    checked=subprocess.run(['node','-e',js],input=json.dumps(scripts),text=True,capture_output=True,check=True)
    errors.extend(json.loads(checked.stdout))
    css=(ROOT/'assets/site.css').read_text()
    for selector in ['.grid{','.hidden{','.md\\:grid-cols-3{','.bg-indigo-600{','.font-display{']:
        if selector not in css: errors.append('CSS attendue absente : '+selector)
    if errors:
        print('\n'.join(errors)); return 1
    print(f'{count} pages, {refs} liens/ressources internes, {len(urls)} URL sitemap et {len(scripts)} scripts vérifiés.')
    return 0
if __name__=='__main__': sys.exit(main())
