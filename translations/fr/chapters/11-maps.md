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

## Couches finales

Les lieux doivent montrer villages, points de vue, patrimoine et domaines. Les plages doivent être groupées par confort, nature, combinaison Saint-Tropez, navette et absence de surveillance. Les restaurants doivent indiquer moment et budget. Les randonnées et itinéraires vélo restent séparés jusqu'à géométrie fiable.

## Usage mobile

La carte mobile doit répondre vite: qu'est-ce qui est proche de ma base, qu'est-ce qui convient à ce moment de la journée, et quels lieux demandent réservation, parking ou contrôle de sécurité?

## Ce que disent les locaux

- L'été, ajoutez une couche pour la carte quotidienne d'accès aux massifs du Var (risque incendie) : elle décide si randonnées et sorties gravel sont même autorisées.
- Créez une couche jours de marché : Place des Lices mar+sam, Cogolin mer+sam, La Garde-Freinet toute l'année - les habitants y calent courses et visites de villages.
- Traitez les navettes maritimes du golfe comme des « routes » sur la carte : en saison, elles battent la D559.
- Une couche fontaines et points d'eau par village vaut plus ici, pour cyclistes et marcheurs, qu'une couche restaurants.

Ces points rassemblent le consensus local issu de guides d'habitants, d'offices de tourisme et de clubs locaux (voir `database/sources.csv`) ; la vérification sur le terrain avec des habitants reste au programme.
