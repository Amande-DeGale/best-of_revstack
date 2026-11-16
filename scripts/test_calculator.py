#!/usr/bin/env python3
"""Teste les calculs et actions locales avec un DOM simulé, sans navigateur."""
from pathlib import Path
from html.parser import HTMLParser
import json, subprocess
ROOT=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.ids={}; self.code=[]; self.current=None
    def handle_starttag(self,t,attrs):
        d=dict(attrs)
        if d.get('id'): self.ids[d['id']]=d
        if t=='script' and not d.get('src') and d.get('type','')!='application/ld+json': self.current=''
    def handle_data(self,text):
        if self.current is not None: self.current+=text
    def handle_endtag(self,t):
        if t=='script' and self.current is not None:self.code.append(self.current);self.current=None
p=Parser();p.feed((ROOT/'outils-gratuits/rentabilite-automatisation/index.html').read_text())
js=r'''
const vm=require('vm'),assert=require('assert'),fs=require('fs');
const data=JSON.parse(fs.readFileSync(0,'utf8'));
let checks=0;
function setup(query='') {
 const nodes={};for(const [id,attr] of Object.entries(data.ids)){nodes[id]={value:attr.value||'',min:attr.min??'',max:attr.max??'',textContent:'',listeners:{},addEventListener(k,f){this.listeners[k]=f},focus(){},select(){}};}
 nodes.calcul.reportValidity=()=>true;
 let csvBlob=null,download=null;
 class MockURL extends URL {static createObjectURL(blob){csvBlob=blob;return 'blob:test'}static revokeObjectURL(){}}
 const document={getElementById:id=>nodes[id],createElement:()=>({click(){download=this.download}})};
 const ctx=vm.createContext({document,location:{href:'https://amande-degale.github.io/best-of_revstack/outils-gratuits/rentabilite-automatisation/'+query},URL:MockURL,Intl,Blob,setTimeout:f=>f()});
 for(const code of data.code)vm.runInContext(code,ctx);
 const recalc=()=>nodes.calcul.listeners.submit({preventDefault(){}});
 return {nodes,recalc,blob:()=>csvBlob,download:()=>download};
}
function check(bool){assert(bool);checks++}
(async()=>{
 let s=setup();check(s.nodes.heures.textContent==='4,17 h');check(s.nodes.net.textContent==='96 $');check(s.nodes.annee.textContent.replace(/\s/g,'')==='1002$');check(s.nodes.retour.textContent==='1,56 mois');
 s.nodes.abonnement.value='200';s.recalc();check(s.nodes.net.textContent==='-75 $');check(s.nodes.retour.textContent.includes('Non récupérable'));
 s.nodes.installation.value='0';s.recalc();check(s.nodes.retour.textContent==='0 mois');
 s.nodes.part.value='101';s.recalc();check(s.nodes.erreur.textContent.includes('Vérifiez'));check(s.nodes.net.textContent==='—');s.nodes.part.value='-1';s.recalc();check(s.nodes.erreur.textContent.includes('Vérifiez'));
 s=setup('?volume=240&minutes=5&part=50&horaire=30&abonnement=0&maintenance=1&installation=0');check(s.nodes.heures.textContent==='10 h');check(s.nodes.net.textContent==='270 $');
 s.nodes.partager.listeners.click();let url=new URL(s.nodes.lien.value);check(url.searchParams.get('volume')==='240');check(url.searchParams.get('maintenance')==='1');
 const restored=setup(url.search);check(restored.nodes.net.textContent===s.nodes.net.textContent);
 s.nodes.export.listeners.click();const csv=await s.blob().text();check(csv.includes('gain_net_mensuel;270'));check(csv.includes('premiere_annee;3240'));check(s.download()==='rentabilite-automatisation.csv');
 s=setup('?part=999&volume=NaN');check(s.nodes.part.value==='50');check(s.nodes.volume.value==='100');
 s.nodes.volume.value='';s.recalc();check(s.nodes.erreur.textContent.includes('Vérifiez'));
 console.log(checks+' vérifications du calculateur, export CSV et liens partageables réussies (DOM simulé).');
})().catch(e=>{console.error(e);process.exit(1)});
'''
subprocess.run(['node','-e',js],input=json.dumps({'ids':p.ids,'code':p.code}),text=True,check=True)
