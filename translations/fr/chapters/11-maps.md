---
title: Cartes
chapter: 12
status: draft
---

# Cartes

## Résumé

Ce chapitre définit les couches cartographiques du guide: villages, plages, restaurants, randonnées, itinéraires vélo, stationnement, points de vue et arrêts pratiques.

## Google Maps Atlas

Générez le premier atlas avec:

```bash
python3 scripts/export_google_maps.py
```

L'export écrit `output/google_maps_atlas.csv`. Le fichier généré reste hors Git; les données sources restent dans `database/*.csv`.

## Règles actuelles

- Les lieux, plages et restaurants avec latitude et longitude sont exportés comme points.
- Les enregistrements sans coordonnées sont ignorés jusqu'à géocodage fiable.
- Les GPX restent des fichiers séparés sous `assets/gpx/`.
- Chaque ligne d'atlas conserve source, statut de recherche, catégorie, commune et identifiant stable.

## Améliorations suivantes

Ajouter des coordonnées, choisir couleurs et icônes par couche, tester l'import Google My Maps et la lisibilité mobile, puis décider plus tard si les GPX deviennent KML ou GeoJSON.

## Usage du guide

La carte est actuellement un atlas d'orientation. Utilisez les coordonnées comme base fiable d'import, mais considérez les GPX comme navigables seulement après contrôle officiel ou local de géométrie.
