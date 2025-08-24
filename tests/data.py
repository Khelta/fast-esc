import pytest


@pytest.fixture(scope="session")
def country_import_data():
    yield [
        {
            "name": "Germany",
            "alpha2": "de"
        },
        {
            "name": "Switzerland",
            "alpha2": "ch"
        },
    ]


@pytest.fixture(scope="session")
def contest_import_data():
    yield [
        {
            "year": 2025,
            "country": "Switzerland",
            "city": "Basel",
            "location": "St. Jakobshalle",
            "broadcaster": "SSR SRG",
            "final": 0,
            "date": "17.5.2025",
            "hosts": [
                "Hazel Brugger",
                "Michelle Hunzike",
                "Sandra Studer"
            ]
        },
        {
            "year": 2011,
            "country": "Germany",
            "city": "D\u00fcsseldorf",
            "location": "Fortuna D\u00fcsseldorf Arena",
            "broadcaster": "ARD",
            "final": 2,
            "date": "12.5.2011",
            "hosts": [
                "Anke Engelke",
                "Judith Rakers",
                "Stefan Raab"
            ]
        },
        {
            "year": 1956,
            "country": "Switzerland",
            "city": "Lugano",
            "location": "Teatro Kursaal",
            "broadcaster": "SSR SRG",
            "final": 0,
            "date": "24.5.1956",
            "hosts": [
                "Lohengrin Filipello"
            ]
        }
    ]


@pytest.fixture(scope="session")
def song_import_data():
    yield [
        {"year": 2025,
         "final": 0,
         "participations": [{
             "artist": "Zo\u00eb M\u00eb",
             "title": "Voyage",
             "people": {
                 "ARTIST": [
                     "Zo\u00eb M\u00eb"
                 ],
                 "SONGWRITER": [
                     "Emily Middlemas",
                     "Tom Oehler",
                     "Zo\u00eb M\u00eb"
                 ],
                 "STAGE DIRECTOR": [
                     "Theo Adams"
                 ],
                 "SPOKESPERSON": [
                     "M\u00e9lanie Freymond",
                     "Sven Epiney"
                 ],
                 "COMMENTATOR": [
                     "Ellis Cavallini",
                     "Gian-Andrea Costa",
                     "Jean-Marc Richard",
                     "Nicolas Tanner",
                     "Sven Epiney"
                 ],
                 "JURY MEMBER": [
                     "Cyrill Camenzind",
                     "Gabriela Mennel",
                     "Giordano Tatum Rush",
                     "Mary Clapasson",
                     "Tiffany Athena Limacher"
                 ]
             },
             "country": "ch",
             "place": 10,
             "running": 19,
             "points": 214,
             "public_points": 0,
             "jury_points": 214,
             "text": "Mes yeux candides découvrent le monde\nD'une façon naïve à faire confondre\nLes démons de la nuit\nMmh, mmh\nTu me balances des mots qui m'étouffent\nQuoi qu'il advienne je me couche\nPrès de toi ce soir\nMmh, mmh\n\nTu comprendras un jour\nQue les fleurs sont plus belles\nQuand tu les arroses\nTu m'as coupé tellement de…\n\n…fois\nSi tu veux je pars\nAvec toi pour faire un voyage\nFaire un voyage, voyage\nFaire un voyage avec toi\n\nLaisse-moi t'aimer même si tu m'aimes pas\nJe vais me noyer dans tes larmes\nJe vais partager ton vague à l'âme\nTu me bouffes avec ton regard\nQuoi qu'il advienne je ne cesserai jamais\nDe chanter pour toi\n\nTu comprendras un jour\nQue les fleurs sont plus belles\nQuand tu les arroses\nTu m'as coupé tellement de…\n\n…fois\nSi tu veux je pars\nAvec toi pour faire un voyage\nFaire un voyage, voyage\nFaire un voyage avec toi\n\nFaire un, faire un voyage\nFaire un, faire un voyage\nFaire un, faire un voyage\nAvec moi\n\nFaire un, faire un voyage\nFaire un, faire un voyage\nFaire un, faire un voyage\nAvec moi, avec…\n\n…moi\nSi tu veux je parѕ\nAvec toi pour faire un voyage\nFaire un voyage, voyage\nFaire un voyage аvec toi",
             "languages": ["French", ]
         }]},
        {"year": 1956,
         "final": 0,
         "participations": [{
             "artist": "Lys Assia",
             "title": "Das alte Karussell",
             "people": {
                 "ARTIST": [
                     "Lys Assia"
                 ],
                 "BACKING": [
                     "Anita Traversi",
                     "Athos Beretta",
                     "Carmen Tumiati",
                     "Luciano Rezzonico",
                     "Silvano Beretta"
                 ],
                 "SONGWRITER": [
                     "Fernando Paggi",
                     "George Betz-Stahl"
                 ],
                 "CONDUCTOR": [
                     "Fernando Paggi"
                 ],
                 "COMMENTATOR": [
                     "Georges Hardy"
                 ]
             },
             "country": "ch2",
             "place": None,
             "running": 2,
             "points": None,
             "public_points": None,
             "jury_points": None,
             "text": "Das alte Karussell\nDas geht nicht mehr so schnell\nDie Pferdchen und die Wagen\nDie woll'n nicht von der Stell'\n\nDa hilft auch kein flattiern\nUnd auch kein neu Lattiern\nDa hilft nur noch das Eine:\nMan muss es einmal schmiern\n\nUnd auch das alte Orgelspiel\nDas piepst wie eine Maus\nVon Zeit zu Zeit wird's ihm zu viel\nDann setzt es einfach aus\n\nDas alte Karussell\nDas geht nicht mehr so schnell\nDie Pferdchen und die Wagen\nDie woll'n nicht von der Stell'\n\nDie Kleinen und Großen\nSie ziehen und stoßen\nUnd so geht es im Kreise herum\n\nDie Pferdchen, die traben\nUnd ziehn an den Wagen\nUnd die Orgel, die wird wieder jung\n\nEin komischer Gesell'\nDieses alte Karussell\nVon unten bis oben ist alles verschoben\nDoch im Kreis geht es doch noch herum\n\nDas alte Karussell\nDas geht nicht mehr so schnell\nDie Pferdchen und die Wagen\nDie woll'n nicht von der Stell'\n\nDas alte Karussell, oo…\nDas alte Kаrusѕell",
             "languages": ["German", ]
         }]}
    ]
