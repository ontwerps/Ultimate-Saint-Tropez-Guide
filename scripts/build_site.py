#!/usr/bin/env python3
"""Build a lightweight multilingual static HTML version of the guide."""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_TITLE = "Ultimate Saint-Tropez Guide"

LANGUAGES = {
    "nl": {
        "name": "Nederlands",
        "chapter_dir": "chapters",
        "output_dir": "",
        "home": "Inhoud",
        "back": "Terug naar inhoud",
        "chapters": "Hoofdstukken",
        "chapter_label": "Hoofdstuk",
        "hero": "Een Markdown-first reisgids voor de Golf van Saint-Tropez, rechtstreeks gegenereerd uit de repository.",
        "note": "Deze preview is leesbaar afgerond, maar datumgevoelige aanbevelingen houden hun verificatiestatus tot officiële en lokale controle klaar is.",
        "status_heading": "Publicatiestatus",
        "footer": "Gegenereerd uit de bronbestanden van de repository.",
    },
    "en": {
        "name": "English",
        "chapter_dir": "translations/en/chapters",
        "output_dir": "en",
        "home": "Contents",
        "back": "Back to contents",
        "chapters": "Chapters",
        "chapter_label": "Chapter",
        "hero": "A Markdown-first travel handbook for the Gulf of Saint-Tropez, generated directly from the repository.",
        "note": "This preview is reader-ready, while date-sensitive recommendations keep their verification status until official and local checks are complete.",
        "status_heading": "Publication Status",
        "footer": "Generated from the repository source files.",
    },
    "fr": {
        "name": "Français",
        "chapter_dir": "translations/fr/chapters",
        "output_dir": "fr",
        "home": "Sommaire",
        "back": "Retour au sommaire",
        "chapters": "Chapitres",
        "chapter_label": "Chapitre",
        "hero": "Un guide de voyage Markdown-first pour le golfe de Saint-Tropez, généré directement depuis la repository.",
        "note": "Cette prévisualisation est lisible et structurée, tandis que les recommandations sensibles aux dates gardent leur statut de vérification jusqu'aux contrôles officiels et locaux.",
        "status_heading": "Statut de publication",
        "footer": "Généré depuis les fichiers sources de la repository.",
    },
}

STATUS_LABELS = {
    "nl": {
        "draft": "preview",
        "concept": "preview",
        "verified": "geverifieerd",
        "official_partial_verification": "gedeeltelijk geverifieerd",
        "seed_needs_official_verification": "onderzoeksbasis",
    },
    "en": {
        "draft": "preview",
        "concept": "preview",
        "verified": "verified",
        "official_partial_verification": "partly verified",
        "seed_needs_official_verification": "research lead",
    },
    "fr": {
        "draft": "prévisualisation",
        "concept": "prévisualisation",
        "verified": "vérifié",
        "official_partial_verification": "partiellement vérifié",
        "seed_needs_official_verification": "piste de recherche",
    },
}

EDITORIAL_LABELS = {
    "nl": {
        "winner": "Nr. 1 contender",
        "top10": "Top 10",
        "best_for": "Best voor",
        "avoid_if": "Vermijd als",
        "price": "Prijs",
        "review": "Guide review",
        "rating_note": "Editoriale gidsrating, geen externe reviewscore.",
    },
    "en": {
        "winner": "No. 1 contender",
        "top10": "Top 10",
        "best_for": "Best for",
        "avoid_if": "Avoid if",
        "price": "Price",
        "review": "Guide review",
        "rating_note": "Editorial guide rating, not a third-party review score.",
    },
    "fr": {
        "winner": "Choix n°1",
        "top10": "Top 10",
        "best_for": "Idéal pour",
        "avoid_if": "À éviter si",
        "price": "Prix",
        "review": "Avis du guide",
        "rating_note": "Note éditoriale du guide, pas une note d'avis externe.",
    },
}

TOP_RECOMMENDATIONS = {
    "nl": [
        {
            "title": "Saint-Tropez vroeg + La Ponche + Citadelle",
            "href": "chapters/03-saint-tropez.html",
            "rating": 5,
            "price": "€€",
            "best_for": "eerste echte dag, cultuur, haven en sfeer",
            "avoid_if": "je pas midden op de dag vertrekt zonder parkeerplan",
            "review": "De beste eerste keuze omdat je in één compacte route haven, oude stad, uitzicht en mythe begrijpt zonder meteen een strandclubbudget nodig te hebben.",
        },
        {
            "title": "Pampelonne met reservering",
            "href": "chapters/05-beaches.html",
            "rating": 5,
            "price": "€€€€",
            "best_for": "iconische stranddag en luxe lunch",
            "avoid_if": "je stilte, laag budget of spontane parking zoekt",
            "review": "De klassieker wint alleen wanneer sector, parking en lunch vooraf gekozen zijn.",
        },
        {
            "title": "Port Grimaud ochtendlus",
            "href": "chapters/02-port-grimaud.html",
            "rating": 4,
            "price": "€",
            "best_for": "aankomstdag, gezinnen, foto's en korte wandeling",
            "avoid_if": "je vooral ruige natuur of stilte zoekt",
            "review": "De makkelijkste eerste laag vanuit Prairies de la Mer: vlak, visueel en laag risico.",
        },
        {
            "title": "Grimaud + Gassin late middag",
            "href": "chapters/04-villages.html",
            "rating": 4,
            "price": "€€",
            "best_for": "uitzicht, dorpen en rust na strand",
            "avoid_if": "mobiliteit of hitte een probleem is",
            "review": "Sterk contrast met de kustdrukte, vooral wanneer je de dorpen rond licht plant.",
        },
        {
            "title": "La Nartelle comfortstrand",
            "href": "chapters/05-beaches.html",
            "rating": 4,
            "price": "€€",
            "best_for": "gezinnen, voorzieningen en watersport",
            "avoid_if": "je het Saint-Tropez-icoon zoekt",
            "review": "Minder mythe dan Pampelonne, maar vaak praktischer en relaxter.",
        },
        {
            "title": "Gigaro - Cap Lardier natuurdag",
            "href": "chapters/06-hiking.html",
            "rating": 4,
            "price": "€",
            "best_for": "wandelaars, natuur en kustgevoel",
            "avoid_if": "het heet is of je geen water/schoenen hebt",
            "review": "De beste natuurlijke tegenhanger van strandclubs en havenpodium.",
        },
        {
            "title": "La Tarte Tropézienne stop",
            "href": "chapters/08-restaurants.html",
            "rating": 4,
            "price": "€",
            "best_for": "iconische zoete pauze in Saint-Tropez",
            "avoid_if": "je een rustige lange lunch zoekt",
            "review": "Hoge gidswaarde omdat het klassiek, snel en relatief laagdrempelig is.",
        },
        {
            "title": "Château Minuty caveau",
            "href": "chapters/09-wine.html",
            "rating": 4,
            "price": "€€",
            "best_for": "wijn, Gassin/Ramatuelle-combinatie en aankopen",
            "avoid_if": "je nog moet rijden zonder sober plan",
            "review": "Sterkste wijnanker door de huidige bronbasis voor proeverijen en caveau.",
        },
        {
            "title": "Domaine du Rayol halve dag",
            "href": "chapters/10-hidden-gems.html",
            "rating": 4,
            "price": "€€",
            "best_for": "tuinen, rust en natuur buiten de drukste kern",
            "avoid_if": "je geen extra rit buiten de golf wilt",
            "review": "Niet geheim, wel een rijke premium omweg voor wie meer wil dan strand.",
        },
        {
            "title": "La Vague d'Or als hoofdavond",
            "href": "chapters/08-restaurants.html",
            "rating": 5,
            "price": "€€€€",
            "best_for": "gastronomische reisavond",
            "avoid_if": "je alleen 'even uit eten' wilt",
            "review": "Een topkeuze wanneer de avond zelf het reisdoel is en logistiek klopt.",
        },
    ],
    "en": [
        {
            "title": "Early Saint-Tropez + La Ponche + Citadelle",
            "href": "chapters/03-saint-tropez.html",
            "rating": 5,
            "price": "€€",
            "best_for": "first real day, culture, harbour and atmosphere",
            "avoid_if": "you leave at midday without a parking plan",
            "review": "The best first choice because one compact route explains the harbour, old town, views and myth without beach-club spending.",
        },
        {
            "title": "Booked Pampelonne",
            "href": "chapters/05-beaches.html",
            "rating": 5,
            "price": "€€€€",
            "best_for": "iconic beach day and luxury lunch",
            "avoid_if": "you want quiet, low cost or spontaneous parking",
            "review": "The classic only wins when sector, parking and lunch are chosen in advance.",
        },
        {
            "title": "Port Grimaud morning loop",
            "href": "chapters/02-port-grimaud.html",
            "rating": 4,
            "price": "€",
            "best_for": "arrival day, families, photos and easy walking",
            "avoid_if": "you mainly want wild nature or silence",
            "review": "The easiest first layer from Prairies de la Mer: flat, visual and low-risk.",
        },
        {
            "title": "Grimaud + Gassin late afternoon",
            "href": "chapters/04-villages.html",
            "rating": 4,
            "price": "€€",
            "best_for": "views, villages and calm after beach",
            "avoid_if": "heat or mobility are limiting",
            "review": "A strong contrast to the coast when planned around light.",
        },
        {
            "title": "La Nartelle comfort beach",
            "href": "chapters/05-beaches.html",
            "rating": 4,
            "price": "€€",
            "best_for": "families, services and watersports",
            "avoid_if": "you want the Saint-Tropez icon",
            "review": "Less myth than Pampelonne, often more practical.",
        },
        {
            "title": "Gigaro - Cap Lardier nature day",
            "href": "chapters/06-hiking.html",
            "rating": 4,
            "price": "€",
            "best_for": "walkers, nature and coastal feeling",
            "avoid_if": "it is hot or you lack water and shoes",
            "review": "The best natural counterpoint to beach clubs and harbour theatre.",
        },
        {
            "title": "La Tarte Tropézienne stop",
            "href": "chapters/08-restaurants.html",
            "rating": 4,
            "price": "€",
            "best_for": "iconic sweet pause in Saint-Tropez",
            "avoid_if": "you want a long quiet lunch",
            "review": "High guide value because it is classic, quick and approachable.",
        },
        {
            "title": "Château Minuty cellar",
            "href": "chapters/09-wine.html",
            "rating": 4,
            "price": "€€",
            "best_for": "wine, Gassin/Ramatuelle pairing and buying",
            "avoid_if": "you still need to drive without a sober plan",
            "review": "The strongest wine anchor because current sources document visit formats.",
        },
        {
            "title": "Domaine du Rayol half-day",
            "href": "chapters/10-hidden-gems.html",
            "rating": 4,
            "price": "€€",
            "best_for": "gardens, calm and nature beyond the busiest core",
            "avoid_if": "you do not want an extra drive",
            "review": "Not secret, but a rich premium detour beyond beach rhythm.",
        },
        {
            "title": "La Vague d'Or as the main evening",
            "href": "chapters/08-restaurants.html",
            "rating": 5,
            "price": "€€€€",
            "best_for": "gastronomic travel evening",
            "avoid_if": "you only want a casual dinner",
            "review": "A top choice when the evening itself is the destination.",
        },
    ],
    "fr": [
        {
            "title": "Saint-Tropez tôt + La Ponche + Citadelle",
            "href": "chapters/03-saint-tropez.html",
            "rating": 5,
            "price": "€€",
            "best_for": "première vraie journée, culture, port et ambiance",
            "avoid_if": "vous partez à midi sans plan de parking",
            "review": "Le meilleur premier choix: port, vieille ville, vue et mythe dans une route compacte.",
        },
        {
            "title": "Pampelonne réservée",
            "href": "chapters/05-beaches.html",
            "rating": 5,
            "price": "€€€€",
            "best_for": "plage iconique et déjeuner luxe",
            "avoid_if": "vous cherchez calme, petit budget ou parking spontané",
            "review": "Le classique gagne seulement si secteur, parking et déjeuner sont choisis d'avance.",
        },
        {
            "title": "Boucle matinale Port Grimaud",
            "href": "chapters/02-port-grimaud.html",
            "rating": 4,
            "price": "€",
            "best_for": "arrivée, familles, photos et marche facile",
            "avoid_if": "vous cherchez surtout nature sauvage ou silence",
            "review": "La première couche la plus simple depuis Prairies de la Mer.",
        },
        {
            "title": "Grimaud + Gassin en fin d'après-midi",
            "href": "chapters/04-villages.html",
            "rating": 4,
            "price": "€€",
            "best_for": "vues, villages et calme après plage",
            "avoid_if": "chaleur ou mobilité limitent la journée",
            "review": "Très bon contraste avec la côte quand la lumière devient douce.",
        },
        {
            "title": "La Nartelle confort",
            "href": "chapters/05-beaches.html",
            "rating": 4,
            "price": "€€",
            "best_for": "familles, services et sports nautiques",
            "avoid_if": "vous cherchez l'icône Saint-Tropez",
            "review": "Moins mythique que Pampelonne, souvent plus pratique.",
        },
        {
            "title": "Gigaro - Cap Lardier nature",
            "href": "chapters/06-hiking.html",
            "rating": 4,
            "price": "€",
            "best_for": "marche, nature et littoral",
            "avoid_if": "il fait chaud ou vous manquez d'eau/chaussures",
            "review": "Le meilleur contrepoint naturel aux beach clubs.",
        },
        {
            "title": "Pause La Tarte Tropézienne",
            "href": "chapters/08-restaurants.html",
            "rating": 4,
            "price": "€",
            "best_for": "pause sucrée iconique",
            "avoid_if": "vous cherchez un long déjeuner calme",
            "review": "Classique, rapide et accessible.",
        },
        {
            "title": "Caveau Château Minuty",
            "href": "chapters/09-wine.html",
            "rating": 4,
            "price": "€€",
            "best_for": "vin, Gassin/Ramatuelle et achats",
            "avoid_if": "vous devez conduire sans plan sobre",
            "review": "L'ancrage vin le plus solide dans la base actuelle.",
        },
        {
            "title": "Domaine du Rayol demi-journée",
            "href": "chapters/10-hidden-gems.html",
            "rating": 4,
            "price": "€€",
            "best_for": "jardins, calme et nature",
            "avoid_if": "vous ne voulez pas rouler plus loin",
            "review": "Pas secret, mais riche et plus calme que beaucoup de journées plage.",
        },
        {
            "title": "La Vague d'Or comme soirée principale",
            "href": "chapters/08-restaurants.html",
            "rating": 5,
            "price": "€€€€",
            "best_for": "soirée gastronomique",
            "avoid_if": "vous voulez juste dîner vite",
            "review": "Un choix majeur quand la soirée elle-même est le voyage.",
        },
    ],
}

CHAPTER_IMAGE_ALTS = {
    "nl": "Illustratie bij dit hoofdstuk",
    "en": "Illustration for this chapter",
    "fr": "Illustration de ce chapitre",
}

CHAPTER_RANKING_LABELS = {
    "nl": {
        "eyebrow": "Beste keuzes",
        "heading": "Topkeuzes in dit hoofdstuk",
        "sort": "Sorteer",
        "sort_rating": "Rating hoog-laag",
        "sort_price": "Prijs laag-hoog",
        "sort_name": "Naam A-Z",
        "rank": "Nr",
        "choice": "Keuze",
        "rating": "Rating",
        "price": "Prijs",
        "best_for": "Best voor",
        "review": "Guide review",
        "rating_note": "Editoriale gidsrating en prijsband; geen externe live reviewscore.",
    },
    "en": {
        "eyebrow": "Best choices",
        "heading": "Top choices in this chapter",
        "sort": "Sort",
        "sort_rating": "Rating high-low",
        "sort_price": "Price low-high",
        "sort_name": "Name A-Z",
        "rank": "No.",
        "choice": "Choice",
        "rating": "Rating",
        "price": "Price",
        "best_for": "Best for",
        "review": "Guide review",
        "rating_note": "Editorial guide rating and price band; not a live third-party review score.",
    },
    "fr": {
        "eyebrow": "Meilleurs choix",
        "heading": "Meilleurs choix de ce chapitre",
        "sort": "Trier",
        "sort_rating": "Note décroissante",
        "sort_price": "Prix croissant",
        "sort_name": "Nom A-Z",
        "rank": "N°",
        "choice": "Choix",
        "rating": "Note",
        "price": "Prix",
        "best_for": "Idéal pour",
        "review": "Avis du guide",
        "rating_note": "Note éditoriale du guide et niveau de prix; pas une note d'avis externe en direct.",
    },
}

CHAPTERS_WITHOUT_PRICE = {"07-cycling"}

CHAPTER_RANKINGS = {
    "04-villages": [
        {
            "title": "Saint-Tropez old town",
            "rating": 5,
            "price": "€€",
            "best_for": {
                "nl": "eerste stadsdag, haven, La Ponche en Citadelle",
                "en": "first town day, harbour, La Ponche and Citadelle",
                "fr": "première journée ville, port, La Ponche et Citadelle",
            },
            "review": {
                "nl": "Hoogste gidswaarde wanneer je vroeg gaat en parking vooraf plant.",
                "en": "Highest guide value when you go early and plan parking first.",
                "fr": "Meilleure valeur du guide si vous partez tôt avec parking prévu.",
            },
        },
        {
            "title": "Grimaud village",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "erfgoed en rust", "en": "heritage and calm", "fr": "patrimoine et calme"},
            "review": {
                "nl": "Sterkste rustige dorpslaag, vooral met Pont des Fées.",
                "en": "Best quiet village layer, especially with Pont des Fées.",
                "fr": "La meilleure couche village calme, surtout avec le Pont des Fées.",
            },
        },
        {
            "title": "Port Grimaud",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "vlak wandelen en watergevoel", "en": "flat walking and canals", "fr": "marche facile et canaux"},
            "review": {
                "nl": "Makkelijkste keuze vanuit Prairies de la Mer, maar minder authentiek dan de heuveldorpen.",
                "en": "Easiest choice from Prairies de la Mer, but less authentic than the hill villages.",
                "fr": "Le choix le plus facile depuis Prairies de la Mer, moins authentique que les villages perchés.",
            },
        },
        {
            "title": "Gassin village",
            "rating": 4,
            "price": "€€",
            "best_for": {"nl": "uitzicht en late middag", "en": "views and late afternoon", "fr": "vue et fin d'après-midi"},
            "review": {
                "nl": "Prachtige panorama-keuze als hitte en parkeerlogistiek kloppen.",
                "en": "A strong panorama choice when heat and parking logistics work.",
                "fr": "Très bon choix panorama quand chaleur et parking sont maîtrisés.",
            },
        },
        {
            "title": "Ramatuelle village",
            "rating": 4,
            "price": "€€",
            "best_for": {"nl": "strand, wijn en dorp combineren", "en": "linking beach, wine and village", "fr": "lier plage, vin et village"},
            "review": {
                "nl": "Beste dorpskoppeling met Pampelonne, Minuty en Escalet.",
                "en": "Best village pairing with Pampelonne, Minuty and Escalet.",
                "fr": "Meilleure liaison village avec Pampelonne, Minuty et Escalet.",
            },
        },
    ],
    "05-beaches": [
        {
            "title": "Plage de Pampelonne",
            "rating": 5,
            "price": "€€€€",
            "best_for": {"nl": "iconische stranddag", "en": "iconic beach day", "fr": "journée plage iconique"},
            "review": {
                "nl": "Winnaar voor Saint-Tropez-mythe, mits sector, parking en lunch vooraf gekozen zijn.",
                "en": "Winner for Saint-Tropez myth when sector, parking and lunch are chosen in advance.",
                "fr": "Gagnant pour le mythe Saint-Tropez si secteur, parking et déjeuner sont choisis d'avance.",
            },
        },
        {
            "title": "Plage de la Nartelle",
            "rating": 4,
            "price": "€€",
            "best_for": {"nl": "gezinnen en watersport", "en": "families and watersports", "fr": "familles et sports nautiques"},
            "review": {
                "nl": "Praktischer dan Pampelonne voor voorzieningen en minder zware logistiek.",
                "en": "More practical than Pampelonne for services and easier logistics.",
                "fr": "Plus pratique que Pampelonne pour les services et la logistique.",
            },
        },
        {
            "title": "Plage de l'Escalet",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "snorkelen en natuurgevoel", "en": "snorkelling and nature feel", "fr": "snorkeling et nature"},
            "review": {
                "nl": "Beste Ramatuelle-natuurkeuze buiten het klassieke beach-clubritme.",
                "en": "Best Ramatuelle nature choice outside the beach-club rhythm.",
                "fr": "Meilleur choix nature à Ramatuelle hors rythme beach club.",
            },
        },
        {
            "title": "Plage de Gigaro",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "kustpad en natuurdag", "en": "coastal path and nature day", "fr": "sentier littoral et nature"},
            "review": {
                "nl": "Sterk door shuttle- en wandelcontext; neem water en timing serieus.",
                "en": "Strong because of shuttle and walking context; take water and timing seriously.",
                "fr": "Solide grâce au contexte navette et marche; eau et timing comptent.",
            },
        },
        {
            "title": "Cavalaire Plage du Parc",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "ruimte en toegankelijkheid", "en": "space and accessibility", "fr": "espace et accessibilité"},
            "review": {
                "nl": "Comfortabele familiekeuze wanneer je brede baai boven iconografie kiest.",
                "en": "Comfortable family choice when broad bay beats icon value.",
                "fr": "Choix familial confortable si la grande baie prime sur l'icône.",
            },
        },
        {
            "title": "Plage de la Bouillabaisse",
            "rating": 3,
            "price": "€€",
            "best_for": {"nl": "Saint-Tropez-combinatie", "en": "Saint-Tropez pairing", "fr": "combinaison Saint-Tropez"},
            "review": {
                "nl": "Handig als korte strandlaag, niet als mooiste natuurdestination.",
                "en": "Useful as a short beach layer, not the strongest nature destination.",
                "fr": "Utile comme courte couche plage, pas comme meilleure destination nature.",
            },
        },
    ],
    "06-hiking": [
        {
            "title": "Gigaro - Cap Lardier - Cap Taillat",
            "rating": 5,
            "price": "€",
            "best_for": {"nl": "mooiste natuurwandeling", "en": "best nature walk", "fr": "meilleure marche nature"},
            "review": {
                "nl": "Topkeuze voor kustgevoel, mits hitte, water en terugweg serieus gepland zijn.",
                "en": "Top choice for coastal feeling if heat, water and return are planned seriously.",
                "fr": "Premier choix littoral si chaleur, eau et retour sont vraiment planifiés.",
            },
        },
        {
            "title": "Fort-Freinet",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "erfgoed en uitzicht", "en": "heritage and views", "fr": "patrimoine et vue"},
            "review": {
                "nl": "Beste binnenland-contrast met de kust, maar niet op hete middagen.",
                "en": "Best inland contrast to the coast, but not for hot afternoons.",
                "fr": "Meilleur contraste intérieur, mais pas en après-midi chaude.",
            },
        },
        {
            "title": "Saint-Tropez - Plage de Tahiti littoral",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "stad naar strand te voet", "en": "town-to-beach walking", "fr": "ville à plage à pied"},
            "review": {
                "nl": "Sterk voor ervaren wandelaars die Saint-Tropez anders willen lezen.",
                "en": "Strong for walkers who want to read Saint-Tropez differently.",
                "fr": "Fort pour les marcheurs qui veulent lire Saint-Tropez autrement.",
            },
        },
        {
            "title": "Cap Camarat - Cap Taillat research route",
            "rating": 3,
            "price": "€",
            "best_for": {"nl": "routeonderzoek en caps", "en": "route scouting and caps", "fr": "repérage route et caps"},
            "review": {
                "nl": "Veel potentie, maar alleen voorzichtig plannen tot route en restricties lokaal kloppen.",
                "en": "High potential, but keep planning cautious until route and restrictions are checked.",
                "fr": "Fort potentiel, mais prudence tant que route et restrictions ne sont pas vérifiées.",
            },
        },
    ],
    "07-cycling": [
        {
            "title": "Collebasse loop (race, 48 km / 470 m)",
            "rating": 5,
            "price": "€",
            "best_for": {"nl": "mooiste racedag", "en": "best road-bike day", "fr": "plus belle sortie route"},
            "review": {
                "nl": "Dé lokale trainingslus: Collebasse in de schaduw, zee-uitzicht en Ramatuelle als koffiestop.",
                "en": "The local training loop: shaded Collebasse, sea views and Ramatuelle for coffee.",
                "fr": "La boucle d'entraînement locale : Collebasse à l'ombre, vue mer, café à Ramatuelle.",
            },
        },
        {
            "title": "Corniche des Maures - Col du Canadel (race, 62 km / 730 m)",
            "rating": 5,
            "price": "€",
            "best_for": {"nl": "kustpanorama", "en": "coastal panorama", "fr": "panorama côtier"},
            "review": {
                "nl": "Het mooiste balkon boven de Middellandse Zee; vroeg rijden buiten piekverkeer.",
                "en": "The finest balcony above the Mediterranean; ride early outside peak traffic.",
                "fr": "Le plus beau balcon sur la Méditerranée ; partir tôt hors trafic de pointe.",
            },
        },
        {
            "title": "Piste des Crêtes - La Garde-Freinet (gravel, 40 km / 780 m)",
            "rating": 5,
            "price": "€",
            "best_for": {"nl": "gravel-signatuurrit", "en": "signature gravel ride", "fr": "sortie gravel signature"},
            "review": {
                "nl": "De kamlijn van de Maures is de rit waar lokale gravelrijders mee thuiskomen; check zomers de massiftoegang.",
                "en": "The Maures ridge is the ride local gravel riders swear by; check summer massif access.",
                "fr": "La crête des Maures est la sortie fétiche des gravellistes locaux ; vérifier l'accès aux massifs l'été.",
            },
        },
        {
            "title": "Kustfietspad V65 naar Sainte-Maxime (gewone fiets, 23 km / 50 m)",
            "rating": 5,
            "price": "€",
            "best_for": {"nl": "gezinnen en eerste rit", "en": "families and first ride", "fr": "familles et première sortie"},
            "review": {
                "nl": "Veiligste en makkelijkste rit van de golf over de oude spoorlijn; wel druk met wandelaars.",
                "en": "Safest, easiest ride in the gulf along the old railway line; busy with walkers though.",
                "fr": "La sortie la plus sûre et facile du golfe sur l'ancienne voie ferrée ; fréquentée par les piétons.",
            },
        },
        {
            "title": "Boucle des Maures (race, 105 km / 1.650 m)",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "koninginnenrit", "en": "queen stage", "fr": "étape reine"},
            "review": {
                "nl": "Babaou, Collobrières en Taillude: stil, lang en alleen voor getrainde benen met waterplan.",
                "en": "Babaou, Collobrières and Taillude: silent, long, for trained legs with a water plan.",
                "fr": "Babaou, Collobrières et Taillude : silencieux, long, pour jambes entraînées avec plan d'eau.",
            },
        },
        {
            "title": "Rondje presqu'île (race, 55 km / 550 m)",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "kapen en stranden", "en": "capes and beaches", "fr": "caps et plages"},
            "review": {
                "nl": "Salins, Pampelonne en l'Escalet in één lus; alleen vroeg starten in het seizoen.",
                "en": "Salins, Pampelonne and l'Escalet in one loop; early starts only in season.",
                "fr": "Les Salins, Pampelonne et l'Escalet en une boucle ; départ matinal obligatoire en saison.",
            },
        },
    ],
    "08-restaurants": [
        {
            "title": "La Vague d'Or",
            "rating": 5,
            "price": "€€€€",
            "best_for": {"nl": "gastronomische hoofdavond", "en": "main gastronomic evening", "fr": "grande soirée gastronomique"},
            "review": {
                "nl": "Top van de lijst wanneer de avond zelf het reisdoel is.",
                "en": "Top of the list when the evening itself is the destination.",
                "fr": "En tête quand la soirée elle-même est la destination.",
            },
        },
        {
            "title": "La Voile",
            "rating": 5,
            "price": "€€€€",
            "best_for": {"nl": "verfijnde Ramatuelle-avond", "en": "refined Ramatuelle evening", "fr": "soirée raffinée à Ramatuelle"},
            "review": {
                "nl": "Sterk palace-alternatief met Provençaalse focus.",
                "en": "Strong palace alternative with a Provençal focus.",
                "fr": "Solide alternative palace avec accent provençal.",
            },
        },
        {
            "title": "La Tarte Tropézienne",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "iconische zoete stop", "en": "iconic sweet stop", "fr": "pause sucrée iconique"},
            "review": {
                "nl": "Beste waarde: klassiek, snel en zonder groot reserveringsritueel.",
                "en": "Best value: classic, quick and without a major reservation ritual.",
                "fr": "Meilleur rapport: classique, rapide, sans grand rituel de réservation.",
            },
        },
        {
            "title": "La Brasserie",
            "rating": 4,
            "price": "€€€",
            "best_for": {"nl": "minder formeel palace-moment", "en": "less formal palace moment", "fr": "moment palace moins formel"},
            "review": {
                "nl": "Goed compromis wanneer La Réserve gewenst is zonder volledig gastronomisch ritueel.",
                "en": "Good compromise when La Réserve is wanted without the full gastronomic ritual.",
                "fr": "Bon compromis pour La Réserve sans rituel gastronomique complet.",
            },
        },
        {
            "title": "La Réserve à La Plage",
            "rating": 4,
            "price": "€€€€",
            "best_for": {"nl": "Pampelonne-lunch", "en": "Pampelonne lunch", "fr": "déjeuner à Pampelonne"},
            "review": {
                "nl": "Werkt alleen echt met reservering, parking en strandritme op orde.",
                "en": "Only really works when booking, parking and beach rhythm are aligned.",
                "fr": "Fonctionne vraiment avec réservation, parking et rythme plage calés.",
            },
        },
        {
            "title": "Sénéquier",
            "rating": 3,
            "price": "€€€",
            "best_for": {"nl": "havenpodium", "en": "harbour theatre", "fr": "scène du port"},
            "review": {
                "nl": "Meer scène dan pure prijs-kwaliteit; kies het bewust.",
                "en": "More scene than pure value; choose it knowingly.",
                "fr": "Plus scène que rapport qualité-prix; à choisir en conscience.",
            },
        },
    ],
    "09-wine": [
        {
            "title": "Château Minuty caveau",
            "rating": 5,
            "price": "€€",
            "best_for": {"nl": "eerste wijnstop", "en": "first wine stop", "fr": "première étape vin"},
            "review": {
                "nl": "Sterkste wijnanker omdat bezoekvormen en caveau het best gedocumenteerd zijn.",
                "en": "Strongest wine anchor because visit formats and cellar are best documented.",
                "fr": "Meilleur ancrage vin car visites et caveau sont les mieux documentés.",
            },
        },
        {
            "title": "Ramatuelle rosé route",
            "rating": 4,
            "price": "€€",
            "best_for": {"nl": "wijn combineren met dorp/strand", "en": "pairing wine with village/beach", "fr": "lier vin, village et plage"},
            "review": {
                "nl": "Beste manier om wijn niet als losse stop maar als dagritme te gebruiken.",
                "en": "Best way to make wine part of the day rhythm, not a detached stop.",
                "fr": "Meilleure façon d'intégrer le vin au rythme de journée.",
            },
        },
        {
            "title": "La Vague d'Or wine pairing",
            "rating": 4,
            "price": "€€€€",
            "best_for": {"nl": "gastronomische pairing", "en": "gastronomic pairing", "fr": "accord gastronomique"},
            "review": {
                "nl": "Alleen kiezen als de hele avond rond gastronomie draait.",
                "en": "Choose only when the whole evening revolves around gastronomy.",
                "fr": "À choisir seulement si toute la soirée tourne autour de la gastronomie.",
            },
        },
        {
            "title": "Château des Marres",
            "rating": 3,
            "price": "€€",
            "best_for": {"nl": "rustiger alternatief onderzoeken", "en": "scouting a quieter alternative", "fr": "repérer une alternative plus calme"},
            "review": {
                "nl": "Interessant, maar eerst primaire bezoekinformatie bevestigen.",
                "en": "Interesting, but primary visit information needs confirmation first.",
                "fr": "Intéressant, mais les informations de visite doivent être confirmées.",
            },
        },
    ],
    "10-hidden-gems": [
        {
            "title": "Domaine du Rayol",
            "rating": 5,
            "price": "€€",
            "best_for": {"nl": "premium natuur halve dag", "en": "premium nature half-day", "fr": "demi-journée nature premium"},
            "review": {
                "nl": "Niet geheim, wel de rijkste rustige omweg buiten het strandritme.",
                "en": "Not secret, but the richest quiet detour outside beach rhythm.",
                "fr": "Pas secret, mais détour calme le plus riche hors rythme plage.",
            },
        },
        {
            "title": "Fort-Freinet",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "Maures-erfgoed", "en": "Maures heritage", "fr": "patrimoine des Maures"},
            "review": {
                "nl": "Sterke tegenpool van kustdrukte met echte wandelwaarde.",
                "en": "Strong counterpoint to coast crowds with real walking value.",
                "fr": "Vrai contrepoint à la foule côtière avec valeur de marche.",
            },
        },
        {
            "title": "Pont des Fées",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "Grimaud-erfgoedwandeling", "en": "Grimaud heritage walk", "fr": "marche patrimoine à Grimaud"},
            "review": {
                "nl": "Kleine omweg die Grimaud meer diepte geeft.",
                "en": "Small detour that gives Grimaud more depth.",
                "fr": "Petit détour qui donne plus de profondeur à Grimaud.",
            },
        },
        {
            "title": "Cimetière marin de Saint-Tropez",
            "rating": 4,
            "price": "€",
            "best_for": {"nl": "stille culturele wandeling", "en": "quiet cultural walk", "fr": "marche culturelle calme"},
            "review": {
                "nl": "Waardevol als respectvolle rustlaag onder de Citadelle.",
                "en": "Valuable as a respectful quiet layer below the Citadelle.",
                "fr": "Précieux comme couche calme et respectueuse sous la Citadelle.",
            },
        },
        {
            "title": "Moulin de Paillas",
            "rating": 3,
            "price": "€",
            "best_for": {"nl": "uitzicht bij Ramatuelle", "en": "viewpoint near Ramatuelle", "fr": "point de vue près de Ramatuelle"},
            "review": {
                "nl": "Mooi potentieel, maar toegang en parking eerst lokaal controleren.",
                "en": "Good potential, but access and parking need local checking first.",
                "fr": "Beau potentiel, mais accès et parking à vérifier localement.",
            },
        },
    ],
}


def parse_front_matter(text):
    if not text.startswith("---\n"):
        return {}, text

    end_marker = "\n---\n"
    end = text.find(end_marker, 4)
    if end == -1:
        return {}, text

    front_matter = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front_matter[key.strip()] = value.strip().strip('"')

    body = text[end + len(end_marker) :]
    return front_matter, body.lstrip()


def chapter_source_dir(root, lang="nl"):
    return Path(root) / LANGUAGES[lang]["chapter_dir"]


def collect_chapters(root=ROOT, lang="nl"):
    chapters = []
    for path in sorted(chapter_source_dir(root, lang).glob("*.md")):
        if not re.match(r"^\d{2}-", path.name):
            continue
        metadata, body = parse_front_matter(path.read_text(encoding="utf-8"))
        title = metadata.get("title") or path.stem.replace("-", " ").title()
        try:
            chapter_number = int(metadata.get("chapter", len(chapters) + 1))
        except ValueError:
            chapter_number = len(chapters) + 1

        chapters.append(
            {
                "path": path,
                "title": title,
                "chapter": chapter_number,
                "status": metadata.get("status", "concept"),
                "body": body,
                "output_name": f"{path.stem}.html",
            }
        )

    return sorted(chapters, key=lambda item: (item["chapter"], item["path"].name))


def inline_markdown(text):
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def render_markdown(markdown):
    blocks = []
    paragraph = []
    list_items = []
    code_lines = []
    table_lines = []
    in_code = False

    def flush_table():
        if table_lines:
            blocks.append(render_table(table_lines))
            table_lines.clear()

    def flush_paragraph():
        if paragraph:
            blocks.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list():
        if list_items:
            items = "\n".join(f"<li>{inline_markdown(item)}</li>" for item in list_items)
            blocks.append(f"<ul>\n{items}\n</ul>")
            list_items.clear()

    def flush_code():
        if code_lines:
            code = html.escape("\n".join(code_lines))
            blocks.append(f"<pre><code>{code}</code></pre>")
            code_lines.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()

        if line.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_paragraph()
                flush_list()
                in_code = True
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if line.startswith("|") and line.endswith("|"):
            flush_paragraph()
            flush_list()
            table_lines.append(line)
            continue
        flush_table()

        if not line:
            flush_paragraph()
            flush_list()
            continue

        heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading_match:
            flush_paragraph()
            flush_list()
            level = len(heading_match.group(1))
            text = inline_markdown(heading_match.group(2))
            blocks.append(f"<h{level}>{text}</h{level}>")
            continue

        if line.startswith("- "):
            flush_paragraph()
            list_items.append(line[2:].strip())
            continue

        paragraph.append(line)

    flush_paragraph()
    flush_list()
    flush_table()
    if in_code:
        flush_code()

    return "\n".join(blocks)


def render_table(table_lines):
    def split_row(line):
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    rows = [split_row(line) for line in table_lines]
    body_rows = [row for row in rows[1:] if not all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in row)]
    header_html = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in rows[0])
    body_html = "\n".join(
        "<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row) + "</tr>"
        for row in body_rows
    )
    return (
        '<div class="table-wrap"><table class="md-table">'
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>\n{body_html}\n</tbody></table></div>"
    )


def relative_prefix(depth):
    return "../" * depth


def language_url(target_lang, page_kind="index", output_name=None, current_lang="nl"):
    if page_kind == "chapter":
        if target_lang == "nl":
            return f"{relative_prefix(2 if current_lang != 'nl' else 1)}chapters/{output_name}"
        if current_lang == "nl":
            return f"../{LANGUAGES[target_lang]['output_dir']}/chapters/{output_name}"
        return f"../../{LANGUAGES[target_lang]['output_dir']}/chapters/{output_name}"

    if target_lang == "nl":
        return "index.html" if current_lang == "nl" else "../index.html"
    if current_lang == "nl":
        return f"{LANGUAGES[target_lang]['output_dir']}/index.html"
    if current_lang == target_lang:
        return "index.html"
    return f"../{LANGUAGES[target_lang]['output_dir']}/index.html"


def language_switcher(current_lang, page_kind="index", output_name=None):
    links = []
    for lang, config in LANGUAGES.items():
        css_class = "active" if lang == current_lang else ""
        href = language_url(lang, page_kind, output_name, current_lang)
        links.append(f'<a class="{css_class}" href="{href}">{html.escape(config["name"])}</a>')
    return "\n        ".join(links)


def display_status(status, lang):
    return STATUS_LABELS.get(lang, {}).get(status, status)


def stars(rating):
    return "★" * rating + "☆" * (5 - rating)


def chapter_image_name(chapter):
    return f"{chapter['path'].stem}.svg"


def chapter_image_exists(root, chapter):
    return (Path(root) / "assets" / "images" / "chapters" / chapter_image_name(chapter)).is_file()


def chapter_image_src(chapter, depth):
    return f"{relative_prefix(depth)}assets/images/chapters/{chapter_image_name(chapter)}"


def index_hero_image_src(lang):
    prefix = "" if lang == "nl" else "../"
    return f"{prefix}assets/images/chapters/03-saint-tropez.svg"


def price_sort_value(price):
    return price.count("€")


def localized_text(value, lang):
    if isinstance(value, dict):
        return value.get(lang) or value.get("nl") or ""
    return value


def ranking_items_for_chapter(chapter):
    items = CHAPTER_RANKINGS.get(chapter["path"].stem, [])
    return sorted(
        items,
        key=lambda item: (-item["rating"], price_sort_value(item["price"]), item["title"].lower()),
    )


def render_chapter_ranking(chapter, lang):
    items = ranking_items_for_chapter(chapter)
    if not items:
        return ""

    labels = CHAPTER_RANKING_LABELS[lang]
    key = chapter["path"].stem
    show_price = key not in CHAPTERS_WITHOUT_PRICE
    rows = []
    for index, item in enumerate(items, start=1):
        title = html.escape(item["title"])
        price = html.escape(item["price"])
        best_for = html.escape(localized_text(item["best_for"], lang))
        review = html.escape(localized_text(item["review"], lang))
        price_cell = f"\n              <td>{price}</td>" if show_price else ""
        rows.append(
            f"""            <tr data-rating="{item["rating"]}" data-price="{price_sort_value(item["price"])}" data-name="{title.lower()}" data-original-order="{index}">
              <td class="ranking-number">{index}</td>
              <th scope="row">{title}</th>
              <td><span aria-label="{labels["rating"]}: {item["rating"]} van 5">{stars(item["rating"])}</span></td>{price_cell}
              <td>{best_for}</td>
              <td>{review}</td>
            </tr>"""
        )
    rows_html = "\n".join(rows)
    price_header = f"\n              <th>{html.escape(labels['price'])}</th>" if show_price else ""
    price_sort_option = (
        f'\n            <option value="price">{html.escape(labels["sort_price"])}</option>' if show_price else ""
    )

    return f"""    <section class="chapter-ranking" aria-labelledby="ranking-{html.escape(key)}">
      <div class="ranking-header">
        <div>
          <p class="eyebrow">{html.escape(labels["eyebrow"])}</p>
          <h2 id="ranking-{html.escape(key)}">{html.escape(labels["heading"])}</h2>
          <p class="rating-note">{html.escape(labels["rating_note"])}</p>
        </div>
        <label class="sort-control">
          <span>{html.escape(labels["sort"])}</span>
          <select data-ranking-sort="{html.escape(key)}" onchange="sortRankingTable('{html.escape(key)}', this.value)">
            <option value="rating">{html.escape(labels["sort_rating"])}</option>{price_sort_option}
            <option value="name">{html.escape(labels["sort_name"])}</option>
          </select>
        </label>
      </div>
      <div class="table-wrap">
        <table data-ranking-table="{html.escape(key)}">
          <thead>
            <tr>
              <th>{html.escape(labels["rank"])}</th>
              <th>{html.escape(labels["choice"])}</th>
              <th>{html.escape(labels["rating"])}</th>{price_header}
              <th>{html.escape(labels["best_for"])}</th>
              <th>{html.escape(labels["review"])}</th>
            </tr>
          </thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>
"""


def render_editorial_card(item, labels, rank=None, featured=False):
    rank_label = f"<span class=\"rank\">{rank}</span>" if rank is not None else ""
    featured_class = " recommendation-featured" if featured else ""
    return f"""      <article class="recommendation{featured_class}">
        {rank_label}
        <div>
          <h3><a href="{html.escape(item["href"])}">{html.escape(item["title"])}</a></h3>
          <p class="meta"><span>{stars(item["rating"])}</span><span>{labels["price"]}: {html.escape(item["price"])}</span></p>
          <p><strong>{labels["best_for"]}:</strong> {html.escape(item["best_for"])}</p>
          <p><strong>{labels["avoid_if"]}:</strong> {html.escape(item["avoid_if"])}</p>
          <p><strong>{labels["review"]}:</strong> {html.escape(item["review"])}</p>
        </div>
      </article>"""


def render_editorial_sections(lang):
    labels = EDITORIAL_LABELS[lang]
    recommendations = TOP_RECOMMENDATIONS[lang]
    winner = render_editorial_card(recommendations[0], labels, featured=True)
    top_items = "\n".join(
        render_editorial_card(item, labels, rank=index)
        for index, item in enumerate(recommendations, start=1)
    )
    return f"""    <section class="winner">
      <p class="eyebrow">{labels["winner"]}</p>
{winner}
      <p class="rating-note">{labels["rating_note"]}</p>
    </section>
    <section>
      <h2>{labels["top10"]}</h2>
      <div class="recommendation-grid">
{top_items}
      </div>
    </section>"""


def home_href(lang, depth):
    if lang == "nl":
        return f"{relative_prefix(depth)}index.html"
    return "index.html" if depth == 0 else f"{relative_prefix(depth - 1)}index.html"


def page_shell(title, body, lang="nl", depth=0, page_kind="index", output_name=None):
    config = LANGUAGES[lang]
    home = home_href(lang, depth)
    switcher = language_switcher(lang, page_kind, output_name)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | {PROJECT_TITLE}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172026;
      --muted: #5f6b74;
      --line: #d9e0e5;
      --paper: #fbfaf7;
      --accent: #0f766e;
      --band: #eef5f3;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.65;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      background: #ffffff;
    }}
    .bar, main, footer {{
      width: min(1120px, calc(100vw - 32px));
      margin: 0 auto;
    }}
    .bar {{
      min-height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .brand {{
      color: var(--ink);
      font-weight: 700;
      text-decoration: none;
    }}
    nav {{
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }}
    nav a {{
      color: var(--accent);
      font-weight: 600;
      text-decoration: none;
    }}
    .languages {{
      display: flex;
      gap: 8px;
    }}
    .languages a {{
      border: 1px solid var(--line);
      color: var(--ink);
      font-size: 0.9rem;
      padding: 3px 8px;
      text-decoration: none;
    }}
    .languages a.active {{
      border-color: var(--accent);
      color: var(--accent);
      font-weight: 700;
    }}
    main {{
      padding: 40px 0 56px;
    }}
    .hero {{
      align-items: center;
      display: grid;
      gap: 24px;
      grid-template-columns: minmax(0, 1fr) minmax(260px, 480px);
      padding: 30px 0 24px;
      border-bottom: 1px solid var(--line);
    }}
    .hero img {{
      aspect-ratio: 3 / 1;
      display: block;
      height: auto;
      object-fit: cover;
      width: 100%;
    }}
    .note {{
      background: var(--band);
      border-left: 4px solid var(--accent);
      margin: 24px 0;
      padding: 14px 16px;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 0.85rem;
      font-weight: 800;
      letter-spacing: 0;
      margin: 0 0 8px;
      text-transform: uppercase;
    }}
    .winner {{
      border-bottom: 1px solid var(--line);
      padding: 24px 0 32px;
    }}
    .recommendation {{
      border-top: 1px solid var(--line);
      display: grid;
      gap: 12px;
      grid-template-columns: auto 1fr;
      padding: 18px 0;
    }}
    .recommendation-featured {{
      border-top: 0;
      padding-top: 0;
    }}
    .recommendation h3 {{
      margin: 0 0 8px;
    }}
    .recommendation h3 a {{
      color: var(--ink);
      text-decoration: none;
    }}
    .rank {{
      align-items: center;
      border: 1px solid var(--accent);
      color: var(--accent);
      display: inline-flex;
      font-weight: 800;
      height: 34px;
      justify-content: center;
      width: 34px;
    }}
    .meta {{
      color: var(--muted);
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin: 0 0 8px;
    }}
    .rating-note {{
      color: var(--muted);
      font-size: 0.92rem;
      margin-top: 6px;
    }}
    .recommendation-grid {{
      display: grid;
      gap: 0 24px;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    }}
    .chapter-ranking {{
      border-bottom: 1px solid var(--line);
      margin: 0 0 32px;
      padding: 0 0 30px;
    }}
    .ranking-header {{
      align-items: end;
      display: flex;
      gap: 16px;
      justify-content: space-between;
      margin-bottom: 16px;
    }}
    .ranking-header h2 {{
      margin-top: 0;
    }}
    .sort-control {{
      color: var(--muted);
      display: grid;
      gap: 6px;
      font-size: 0.9rem;
      font-weight: 700;
      min-width: 190px;
    }}
    .sort-control select {{
      background: #ffffff;
      border: 1px solid var(--line);
      color: var(--ink);
      font: inherit;
      padding: 8px 10px;
    }}
    .table-wrap {{
      overflow-x: auto;
    }}
    .md-table {{
      border-collapse: collapse;
      margin: 18px 0;
      min-width: 640px;
      width: 100%;
    }}
    .md-table th,
    .md-table td {{
      border-top: 1px solid var(--line);
      padding: 10px;
      text-align: left;
      vertical-align: top;
    }}
    .md-table thead th {{
      color: var(--muted);
      font-size: 0.85rem;
      text-transform: uppercase;
    }}
    .chapter-ranking table {{
      border-collapse: collapse;
      min-width: 860px;
      width: 100%;
    }}
    .chapter-ranking th,
    .chapter-ranking td {{
      border-top: 1px solid var(--line);
      padding: 11px 10px;
      text-align: left;
      vertical-align: top;
    }}
    .chapter-ranking thead th {{
      color: var(--muted);
      font-size: 0.85rem;
      text-transform: uppercase;
    }}
    .chapter-ranking tbody th {{
      min-width: 190px;
    }}
    .ranking-number {{
      color: var(--accent);
      font-weight: 800;
      width: 42px;
    }}
    .chapter-hero {{
      margin: 0 0 28px;
    }}
    .chapter-hero img {{
      aspect-ratio: 3 / 1;
      display: block;
      height: auto;
      object-fit: cover;
      width: 100%;
    }}
    h1, h2, h3, h4 {{
      line-height: 1.2;
      margin: 1.7em 0 0.5em;
    }}
    h1 {{
      font-size: clamp(2rem, 5vw, 4rem);
      margin-top: 0;
    }}
    h2 {{ font-size: 1.6rem; }}
    h3 {{ font-size: 1.25rem; }}
    p, li {{
      max-width: 760px;
      font-size: 1rem;
    }}
    a {{ color: var(--accent); }}
    .chapter-list {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 12px;
      list-style: none;
      padding: 0;
      margin: 24px 0 0;
    }}
    .chapter-list li {{
      max-width: none;
      border-top: 1px solid var(--line);
      padding: 14px 0;
    }}
    .chapter-list a {{
      display: block;
      font-weight: 700;
      text-decoration: none;
    }}
    .status {{
      color: var(--muted);
      display: block;
      font-size: 0.9rem;
      margin-top: 4px;
    }}
    pre {{
      overflow: auto;
      padding: 16px;
      background: #111820;
      color: #f7fafc;
    }}
    footer {{
      border-top: 1px solid var(--line);
      color: var(--muted);
      padding: 24px 0 40px;
    }}
    @media (max-width: 760px) {{
      .hero {{
        grid-template-columns: 1fr;
      }}
      .ranking-header {{
        align-items: stretch;
        display: grid;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="bar">
      <a class="brand" href="{home}">{PROJECT_TITLE}</a>
      <nav>
        <a href="{home}">{config["home"]}</a>
        <span class="languages">
        {switcher}
        </span>
      </nav>
    </div>
  </header>
  <main>
{body}
  </main>
  <footer>{config["footer"]}</footer>
  <script>
    function sortRankingTable(key, mode) {{
      const table = document.querySelector('[data-ranking-table="' + key + '"]');
      if (!table) return;
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));
      rows.sort((left, right) => {{
        const leftRating = Number(left.dataset.rating);
        const rightRating = Number(right.dataset.rating);
        const leftPrice = Number(left.dataset.price);
        const rightPrice = Number(right.dataset.price);
        const leftOrder = Number(left.dataset.originalOrder);
        const rightOrder = Number(right.dataset.originalOrder);
        if (mode === 'price') {{
          return leftPrice - rightPrice || rightRating - leftRating || leftOrder - rightOrder;
        }}
        if (mode === 'name') {{
          return left.dataset.name.localeCompare(right.dataset.name) || leftOrder - rightOrder;
        }}
        return rightRating - leftRating || leftPrice - rightPrice || leftOrder - rightOrder;
      }});
      rows.forEach((row, index) => {{
        row.querySelector('.ranking-number').textContent = String(index + 1);
        tbody.appendChild(row);
      }});
    }}
    document.addEventListener('DOMContentLoaded', () => {{
      document.querySelectorAll('[data-ranking-sort]').forEach((select) => {{
        sortRankingTable(select.dataset.rankingSort, select.value);
      }});
    }});
  </script>
</body>
</html>
"""


def render_index(chapters, final_check_text, lang="nl"):
    config = LANGUAGES[lang]
    chapter_items = "\n".join(
        (
            f'<li><a href="chapters/{html.escape(chapter["output_name"])}">'
            f'{html.escape(chapter["title"])}</a>'
            f'<span class="status">{config["chapter_label"]} {chapter["chapter"]} - {html.escape(display_status(chapter["status"], lang))}</span></li>'
        )
        for chapter in chapters
    )
    status_body = f"<p>{html.escape(config['note'])}</p>"
    body = f"""    <section class="hero">
      <div>
        <h1>{PROJECT_TITLE}</h1>
        <p>{config["hero"]}</p>
      </div>
      <img src="{index_hero_image_src(lang)}" alt="{html.escape(CHAPTER_IMAGE_ALTS[lang])}">
    </section>
    <section class="note">
      <strong>{config["status_heading"]}:</strong> {config["note"]}
    </section>
{render_editorial_sections(lang)}
    <section>
      <h2>{config["chapters"]}</h2>
      <ul class="chapter-list">
{chapter_items}
      </ul>
    </section>
    <section>
      <h2>{config["status_heading"]}</h2>
{status_body}
    </section>"""
    return page_shell(PROJECT_TITLE, body, lang=lang)


def render_chapter(chapter, lang="nl", root=ROOT):
    config = LANGUAGES[lang]
    depth = 1 if lang == "nl" else 2
    chapter_html = render_markdown(chapter["body"])
    image_html = ""
    if chapter_image_exists(root, chapter):
        image_html = (
            f'    <figure class="chapter-hero"><img src="{chapter_image_src(chapter, depth)}" '
            f'alt="{html.escape(CHAPTER_IMAGE_ALTS[lang])}"></figure>\n'
        )
    ranking_html = render_chapter_ranking(chapter, lang)
    body = f"""    <p><a href="{home_href(lang, depth)}">{config["back"]}</a></p>
{image_html}{ranking_html}    <article>
      <p class="status">{config["chapter_label"]} {chapter["chapter"]} - {html.escape(display_status(chapter["status"], lang))}</p>
{chapter_html}
    </article>"""
    return page_shell(chapter["title"], body, lang=lang, depth=depth, page_kind="chapter", output_name=chapter["output_name"])


def language_output_dir(output_dir, lang):
    lang_dir = LANGUAGES[lang]["output_dir"]
    return output_dir / lang_dir if lang_dir else output_dir


def copy_image_assets(root, output_dir):
    source_dir = Path(root) / "assets" / "images"
    if not source_dir.is_dir():
        return
    target_dir = Path(output_dir) / "assets" / "images"
    shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)


def build_language(root, output_dir, lang, final_check_text):
    site_dir = language_output_dir(output_dir, lang)
    (site_dir / "chapters").mkdir(parents=True, exist_ok=True)
    chapters = collect_chapters(root, lang)
    (site_dir / "index.html").write_text(render_index(chapters, final_check_text, lang), encoding="utf-8")
    for chapter in chapters:
        target = site_dir / "chapters" / chapter["output_name"]
        target.write_text(render_chapter(chapter, lang, root), encoding="utf-8")


def build_site(root=ROOT):
    root = Path(root)
    output_dir = root / "_site"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    copy_image_assets(root, output_dir)

    final_check_path = root / "Docs" / "FINAL_CHECK.md"
    final_check_text = final_check_path.read_text(encoding="utf-8") if final_check_path.exists() else ""

    for lang in LANGUAGES:
        build_language(root, output_dir, lang, final_check_text)

    return output_dir


def main():
    output_dir = build_site(ROOT)
    print(f"Built {output_dir}")


if __name__ == "__main__":
    main()
