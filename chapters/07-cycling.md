---
title: Fietsen
chapter: 8
status: concept
---

# Fietsen

## Samenvatting

Het fietshoofdstuk onderscheidt routes voor trekkingfiets, racefiets, gravelbike en e-bike. Veiligheid, wegdek, verkeer, hoogteverschil en stopplaatsen zijn belangrijker dan alleen afstand.

## Routecategorieen

- Trekking
- Race
- Gravel
- E-bike

## Routecriteria

- Afstand
- Hoogteverschil
- Wegdek
- Verkeersdrukte
- Koffiestops
- Waterpunten
- Technische moeilijkheid
- Persoonlijke score

## Database

Alle routes horen in `database/bike_routes.csv`. GPX-bestanden worden apart opgeslagen en gekoppeld via een bestandsnaam of URL.

## Eerste GPX-import

De eerste GPX-bestanden staan in `assets/gpx/`. Dit zijn seed control-tracks voor onderzoek, niet de definitieve navigatiebestanden voor publicatie.

- `prairies-port-grimaud-sainte-maxime-seed.gpx`
- `port-grimaud-frejus-v65-seed.gpx`
- `gassin-ramatuelle-pampelonne-loop-seed.gpx`

## Bronstatus

- De route Port Grimaud - Sainte-Maxime steunt voorlopig op Grimaud-context voor de kustfietspadvermelding en een recente editorial bron over de Parcours Cyclable du Littoral.
- De route Port Grimaud - Fréjus is gekoppeld aan V65/Parcours Cyclable du Littoral-bronnen, maar de exacte geometrie en eventuele onderbrekingen moeten nog tegen officiële routebestanden worden gecontroleerd.
- De Gassin - Ramatuelle - Pampelonne-loop is een gidsconcept voor racefietsers en moet nog lokaal op verkeersdrukte, hellingen, stopplaatsen en veiligheid worden beoordeeld.

## Importregels

- Lokale GPX-bestanden horen onder `assets/gpx/`.
- `database/bike_routes.csv` mag alleen lokale GPX-bestandsnamen bevatten als het bestand bestaat.
- Externe GPX-URL's mogen later worden gebruikt als de bron dat licentietechnisch toestaat.

## Persoonlijke aanbeveling

Nog niet beoordeeld.
