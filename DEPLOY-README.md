# Déploiement GitHub Pages — Best of RevStack

**Préparé le 14 novembre 2026. Marjorie a donné son GO (« Oui, déploie sur GitHub Pages »).**
**Rien n'a été poussé sur GitHub, rien n'a été déployé : ce dossier est le contenu PRÊT à pousser.**

URL finale : **https://amande-degale.github.io/best-of_revstack/**
Dépôt : **Amande-DeGale/best-of_revstack**, branche **main**, dossier **/** (racine).

---

## 1. Contenu exact du dossier (361 fichiers)

| Fichier / dossier | Contenu |
|---|---|
| `index.html` | Page d'accueil corrigée (15 outils, prix et taux vérifiés le 14 nov. 2026). URLs canoniques pointées vers GitHub Pages, favicon en relatif, + liens « Comparatifs » ajoutés dans l'en-tête et le pied de page |
| `outils/` | 50 fiches outils (`/outils/<outil>/`) |
| `comparatifs/` | 305 pages : 244 comparatifs head-to-head, 50 « Alternative à X », 5 guides par métier, 5 pages catégories, 1 index des comparatifs |
| `sitemap.xml` | Sitemap fusionné : accueil + 355 pages pSEO = **356 URLs**, toutes vers amande-degale.github.io/best-of_revstack/ |
| `robots.txt` | `Sitemap: https://amande-degale.github.io/best-of_revstack/sitemap.xml` |
| `favicon.svg` | Logo (corrigé : `href="/favicon.svg"` → `href="favicon.svg"`) |
| `_headers` | En-têtes de sécurité — **ignoré par GitHub Pages** (fonction Netlify), conservé pour un éventuel retour sur Netlify |
| `.nojekyll` | Fichier vide — **désactive Jekyll** sur GitHub Pages (sinon les fichiers commençant par `_` sont ignorés) |
| `DEPLOY-README.md` | Ce fichier — **ne pas pousser ?** Il peut rester dans le dépôt, il est inoffensif (il sera servi en texte à /best-of_revstack/DEPLOY-README.md). Le retirer du push si on ne veut pas l'exposer. |

**Sources :** `revstack-site-corrige/` (index, robots, sitemap, _headers, favicon) + pSEO régénéré avec `--base-url https://amande-degale.github.io/best-of_revstack` (les 4 721 liens internes racine `/...` ont été réécrits en `/best-of_revstack/...`).

## 2. Vérifications passées (14 nov. 2026, serveur local)

- Régénération pSEO : 355 pages, **0 erreur de validation** (aucun terme interdit, titre + H1 + canonique partout).
- Serveur local simulant le sous-chemin `/best-of_revstack/` : **14 URLs testées, toutes en 200** (accueil, favicon, robots, sitemap, index comparatifs, 3 fiches outils, comparatif, alternative, catégorie, guide).
- Audit complet des liens internes : **356 pages, 4 724 liens internes vérifiés, 0 cassé**.
- **0 mention de netlify.app** restante ; **0 canonique incorrecte**.

## 3. Pousser sur GitHub (une fois authentifié)

```bash
git clone https://github.com/Amande-DeGale/best-of_revstack.git
cp -r ~/workspace/your_files/revstack-deploy/. best-of_revstack/
cd best-of_revstack
rm -f _headers.jpg   # ancien fichier mal nommé dans le dépôt, remplacé par _headers
git add -A
git status           # vérifier le contenu avant de commiter
git commit -m "GitHub Pages : site corrigé + 355 pages pSEO"
git push origin main
```

## 4. Activer GitHub Pages (navigateur, compte GitHub Amande-DeGale)

1. Aller sur **https://github.com/Amande-DeGale/best-of_revstack/settings/pages**
2. Sous « Build and deployment », **Source : « Deploy from a branch »**
3. **Branch : main**, dossier **/ (root)** → **Save**
4. Attendre 1 à 2 minutes : le site apparaît à **https://amande-degale.github.io/best-of_revstack/**

**Ordre : pousser d'abord, activer Pages ensuite** (sinon l'ancien contenu du dépôt se déploie).

## 5. À savoir après le déploiement

- **Le site Netlify reste en ligne en parallèle** (best-of-revstack.netlify.app). Les canoniques pointent désormais vers GitHub Pages : Google considérera l'adresse GitHub Pages comme la version principale. Ne pas supprimer Netlify tout de suite.
- **Domaine best-of-revstack.com (~15–20 $/an, non acheté)** : quand il sera acheté, ajouter un fichier `CNAME` contenant le domaine à la racine du dépôt, configurer le DNS chez le registrar (CNAME vers `amande-degale.github.io`), puis remplacer l'URL de base partout (régénérer le pSEO avec `--base-url https://best-of-revstack.com`, corriger `index.html`, `robots.txt`, `sitemap.xml`).
- **Après déploiement :** soumettre le sitemap à Search Console + lancer IndexNow (script `submit_indexnow.py` dans `revstack-gemini-plan/pseo/`, clé dans `INDEXNOW_KEY` — ne pas lancer avant le déploiement) + installer une mesure d'audience gratuite.
- **Ce qui reste non vérifié :** 35 prix affichés comme « indicatifs » sur les pages pSEO, 43 programmes d'affiliation non vérifiés, aucun lien affilié actif (`affiliateUrl` vides). À compléter au fur et à mesure des approbations.
- **Effet de bord de la préparation :** `build-report.json` dans `revstack-gemini-plan/pseo/` a été régénéré avec la nouvelle base URL (c'est le rapport de cette génération, pas un fichier du site).
