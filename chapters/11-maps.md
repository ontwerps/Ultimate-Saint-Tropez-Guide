---
title: Kaarten
chapter: 12
status: draft
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

## Volgende kaartverbeteringen

- Meer coordinaten voor stranden, restaurants en praktische stops.
- Kleur- en icoonafspraken per laag.
- Controle van Google My Maps-import en mobiele leesbaarheid.
- Beslissing of route-GPX later als KML/GeoJSON wordt geconverteerd.

## Gidsgebruik

De kaartlaag is nu vooral een atlas voor oriëntatie. Gebruik punten met coordinaten als betrouwbare start voor Google Maps-import, maar gebruik GPX-routes pas als navigatie na officiële of lokale geometriecontrole. Records zonder coordinaten blijven bewust uit de export om schijnprecisie te vermijden.

## Lagen in de uiteindelijke kaart

### Plaatsen

Dorpen, uitzichtpunten, erfgoed en wijnhuizen. Deze laag helpt bij dagplanning: Grimaud/Gassin/Ramatuelle voor hoogte, Port Grimaud/Saint-Tropez voor water en cultuur, Domaine du Rayol/Fort-Freinet voor natuur en erfgoed.

### Stranden

Stranden moeten kleur krijgen per gebruik: comfort, natuur, Saint-Tropez-combinatie, shuttle, niet-bewaakt of gezinsvriendelijk. Niet-bewaakte stranden krijgen een duidelijk waarschuwingstype.

### Restaurants

Restaurantpunten moeten budget en moment tonen: gastronomisch diner, beach lunch, patisserie, havenpodium, palace-brasserie. Zo wordt de kaart geen willekeurige horeca-lijst.

### Wandelroutes

Wandelroutes blijven apart zolang geometrie niet definitief is. Publiceer liever minder routes met goede caveats dan veel onzekere tracks.

### Fietsroutes

Fietsroutes krijgen type: Trekking, E-bike, Race of Gravel. Voeg pas kleur en afstand toe wanneer de route veilig genoeg is om als route te tonen.

## Mobiel gebruik

De kaart moet op telefoon snel antwoord geven op drie vragen:

- Wat is dichtbij mijn basis?
- Wat past bij dit moment van de dag?
- Welke plekken vragen reservering, parking of veiligheidscontrole?

Daarom zijn korte labels beter dan lange beschrijvingen. De hoofdstukken geven context; de kaart geeft keuzes.

## Wat locals zeggen

- Voeg in de zomer een laag toe voor de dagelijkse massiftoegangskaart van de Var (brandgevaar): die bepaalt of wandel- en gravelroutes überhaupt mogen.
- Maak een marktdagenlaag: Place des Lices di+za, Cogolin wo+za, La Garde-Freinet jaarrond - bewoners plannen boodschappen én dorpsbezoek erop.
- Behandel de bootshuttles over de golf als 'wegen' op de kaart: in het seizoen zijn ze sneller dan de D559.
- Een fontein- en waterpuntenlaag per dorp is voor fietsers en wandelaars hier waardevoller dan een restaurantlaag.

Deze punten bundelen lokale consensus uit bewonersgidsen, lokale toerismebureaus en lokale clubs (zie `database/sources.csv`); veldverificatie met bewoners staat op de publicatiechecklist.
