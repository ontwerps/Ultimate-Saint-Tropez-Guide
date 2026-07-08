---
title: Kaarten
chapter: 12
status: concept
---

# Kaarten

## Samenvatting

Dit hoofdstuk definieert de kaartlagen voor de gids: dorpen, stranden, restaurants, wandelroutes, fietsroutes, parkeren, uitzichtpunten en praktische stops.

## Kaartlagen

- Plaatsen
- Stranden
- Restaurants
- Wandelroutes
- Fietsroutes
- Parkeren
- Uitzichtpunten
- Praktische stops

## Data

Kaartdata moet uit CSV, SQLite of GPX komen. Handmatige kaartpunten zonder bron of controle worden vermeden.

## Google Maps Atlas

De eerste Google Maps Atlas-export is beschikbaar via:

```bash
python3 scripts/export_google_maps.py
```

De export schrijft `output/google_maps_atlas.csv`. Dit bestand is gegenereerd en blijft buiten Git; de brondata blijft in `database/*.csv`.

## Huidige exportregels

- Plaatsen, stranden en restaurants met latitude en longitude worden als punten geëxporteerd.
- Records zonder coordinaten worden overgeslagen totdat ze betrouwbaar gegeocodeerd zijn.
- GPX-routes blijven voorlopig aparte bestanden onder `assets/gpx/`.
- Elke atlasrij behoudt bronverwijzing, onderzoeksstatus, categorie, gemeente en een stabiele Atlas ID.

## Nog nodig

- Meer coordinaten voor stranden, restaurants en praktische stops.
- Kleur- en icoonafspraken per laag.
- Controle van Google My Maps-import en mobiele leesbaarheid.
- Beslissing of route-GPX later als KML/GeoJSON wordt geconverteerd.
