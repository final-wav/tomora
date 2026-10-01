import json
import os
import re

# 1. DEUTSCHE MASTER-TIEFENANALYSE (Hochgradig literarisch, psychodynamisch & klanglich fundiert)
de_tracks_deep = {
    "01": {
        "review": """### Track 01: Please — Die Anatomie des Bittens & Die infantile Regressionsfalle
Das Album beginnt nicht mit einer Behauptung von Autonomie oder einem kühlen Überblick, sondern mit dem nackten Vokativ der totalen Entäußerung: *„Please“*. Es ist ein Einstieg von schmerzhafter Intimität. Hier spricht kein souveränes Subjekt, das um Liebe bittet, sondern ein auf den Nullpunkt reduziertes Ich, dessen gesamte Existenzberechtigung von der Resonanz des Anderen abhängt. Nähe wird in *Please* nicht als partnerschaftliche Begegnung verhandelt, sondern als neurobiologische Überlebensnotwendigkeit – ein reflexhafter, automatisierter Notruf, um das gähnende innere Vakuum durch die physische Zufuhr des Objekts zu stopfen.""",
        "cards": [
            {
                "quote": "Please (Please) / Die Verdopplung des Echos als Hallraum der Ohnmacht",
                "body": """Das doppelte, fast geisterhafte Echo `(Please)` fungiert als intrapsychische Hallkammer. Der Sprecher befindet sich von der ersten Sekunde an in einer fundamentalen Asymmetrie: Er besitzt keinerlei emotionale Hebelwirkung außer dem Appell an die Gnade des Gegenübers. 

Somatisch vollzieht sich hier ein vollständiger Spannungsabfall im posturalen System – der Brustkorb fällt nach innen, der Atem wird flach und hochfrequent, die Stimme verhaucht im ungeschützten Ausatmen. Doch hinter dieser scheinbaren Unterwerfung liegt eine unbewusste, hochgradig manipulative Machtdynamik: Wer sich maximal erniedrigt und jede eigene Würde zur Disposition stellt, zwingt das Gegenüber in die Rolle des allmächtigen Versorgers. Die eigene Ohnmacht wird instrumentalisiert, um dem Partner das Recht auf gesunde Distanz zu entziehen, ohne dass dies wie ein offener Übergriff wirkt."""
            },
            {
                "quote": "Come (Please come) / Der gelähmte Imperativ",
                "body": """Der Übergang zum ersten Verbum (*„Come“*) markiert den brüchigen Moment, in dem passive Regression in eine gerichtete Anforderung umschlägt. Doch das Ich wagt es nicht, den Befehl ungeschützt im Raum stehen zu lassen – er wird sofort durch das flehende *„(Please come)“* abgefedert und relativiert. 

Hier spiegelt sich die Lähmung des Nervensystems wider: Der sympathische Impuls (das verzweifelte Verlangen, nach dem Anderen zu greifen) kollidiert frontal mit der dorsalen Schockstarre (der Panik vor Zurückweisung). Die Verantwortung für die Überwindung des Abstands wird vollständig auf den Partner abgewälzt: Das Subjekt weigert sich, sich selbst zu bewegen; der Andere soll den gesamten Weg zurücklegen, um die innere Leere aufzufüllen."""
            },
            {
                "quote": "Closer, closer, closer / Die Tilgung des Zwischenraums",
                "body": """Die repetitive Stakkato-Kaskade des Komparativs *„closer“* offenbart den Zwangsbeschlag der Psyche. Es geht hier längst nicht mehr um gesunde Intimität, sondern um die radikale Auslöschung jedes Zwischenraums. Jeder Millimeter physischer oder emotionaler Distanz wird vom Alarmsystem des Sprechers als existenzielle Vernichtung decodiert.

Akustisch verengen die zirkulierenden Stimmschleifen den Raum zu einer akustischen Schlinge. Die Produktion erzeugt ein klaustrophobisches Vakuum: Die Stimme sitzt direkt auf dem Hörnerv des Hörers und simuliert eine Unmittelbarkeit, die jede rationale Reflexion ausschaltet – das krampfhafte Festhalten eines Ertrinkenden, der den Retter unweigerlich mit in die Tiefe reißt."""
            }
        ]
    },
    "02": {
        "review": """### Track 02: Come Closer — Die toxische Verschmelzung & Der Hunger nach Co-Regulation
Was in *Please* als schüchternes Flehen begann, beschleunigt sich in *Come Closer* zu einem unerbittlichen Sog. Nähe wird nun endgültig als Narkotikum instrumentalisiert. Der Song seziert die gefährliche Illusion, dass die eigene innere Zerrissenheit durch die vollständige somatische und seelische Verschmelzung mit dem Körper des Partners geheilt werden könnte.""",
        "cards": [
            {
                "quote": "Come closer, come closer / Die Beschleunigung des Sogs",
                "body": """Das Tempo zieht an, die Bässe dringen tiefer in den Magenraum. Der Text artikuliert das verzweifelte Verlangen nach externer Co-Regulation: Das eigene Nervensystem ist unfähig, sich selbst zu beruhigen oder Einsamkeit auszuhalten. Die physische Berührung des Partners fungiert als chemischer Betäubungsstoff gegen die innere Panik. Jedes kleinste Zögern des Gegenübers wird sofort als Liebesentzug und existenzielle Bedrohung fehlinterpretiert."""
            },
            {
                "quote": "I need you near / Das Tilgen der Ich-Grenzen",
                "body": """In der simplen Formel *„I need you near“* offenbart sich die Verwechslung von Liebe mit existenzieller Geiselnahme. Der Sprecher opfert die eigene Autonomie, fordert im Gegenzug jedoch die lückenlose Verfügbarkeit des Anderen ein. Es entsteht ein hermetisches Spannungsfeld, in dem jede individuelle Grenze des Partners als Verrat gebrandmarkt wird."""
            }
        ]
    },
    "03": {
        "review": """### Track 03: A Boy Like You — Kognitive Schutzpanzerung & Die Vivisektion des Archetyps
Ein radikaler Bruch in der psychologischen Architektur des Werks: Das hilflose Flehen schlägt in eine kühle, schneidende Intellektualisierung um. *A Boy Like You* ist die sezierende Durchleuchtung des Gegenübers. Aus Angst vor der eigenen emotionalen Verwundbarkeit zieht sich das Ich hinter ein Bollwerk aus First-Principles-Logik und schonungsloser Mustererkennung zurück.""",
        "cards": [
            {
                "quote": "A Boy Like You / Die Vermessung der Projektion",
                "body": """Der Sprecher schaltet vom Modus des Fühlens in den Modus des Scannens. Jedes Detail, jede Charakterschwäche und jede Inkonsistenz im Verhalten des Partners wird katalogisiert und dekonstruiert. Die Sprache wird messerscharf, fast klinisch. Das Motiv ist Selbstschutz: Wer den Anderen vollkommen durchschaut, klassifiziert und entmystifiziert, kann von ihm nicht mehr unvorbereitet verletzt werden."""
            },
            {
                "quote": "Die Dissonanz zwischen Ideal und Realität",
                "body": """Die Stimme klingt trocken, hochauflösend und ohne jeden wärmenden Hall – direkt auf dem Trommelfell platziert. Hinter der brillanten analytischen Kritik pulsiert jedoch die schmerzhafte Tragik des Verstandes: Das Ich erkennt, dass der reale Mensch vor ihm niemals mit dem idealisierten Archetyp in seinem Kopf verschmelzen kann. Die intellektuelle Überlegenheit ist der letzte Damm vor dem drohenden Kontrollverlust."""
            }
        ]
    },
    "04": {
        "review": """### Track 04: Ring The Alarm — Das Überhitzen des Nervensystems & Akute Panik
Die kognitive Schutzpanzerung aus Track 3 splittert unter der Wucht der Realität in tausend Teile. *Ring The Alarm* ist der klangliche und emotionale Zusammenbruch aller Dämme – das Nervensystem schlägt ungebremst in den Alarmzustand der akuten Trennungsangst um.""",
        "cards": [
            {
                "quote": "Aah-aah-aah / Der unartikulierte Notruf",
                "body": """Die verbale Sprache kapituliert; an ihre Stelle tritt die rohe, sirenenhafte Lautmalerei. Die Gesangslinien spiegeln einen massiven Adrenalinschub wider: Herzrasen, Hyperventilation, zitternde Motorik. Das Alarmsystem des Körpers hat die volle Kontrolle übernommen. Die drohende Distanz zum Partner fühlt sich für das Gehirn nicht wie ein Beziehungsstreit an, sondern wie der physische Erstickungstod."""
            },
            {
                "quote": "Ring The Alarm / Der Feueralarm der Psyche",
                "body": """Verzerrte, treibende Rhythmen peitschen den Track nach vorne. Der Alarm ist nicht nur ein Ruf nach dem fliehenden Partner, sondern ein innerer Feueralarm: Die Psyche begreift schlagartig, dass die bisherige symbiotische Strategie endgültig kollabiert ist und das System vor der totalen Reizüberflutung steht."""
            }
        ]
    },
    "05": {
        "review": """### Track 05: My Baby — Der Schutzrausch der Verleugnung & Die geheime Festung
Nach dem katastrophalen Überhitzen in *Ring The Alarm* vollzieht die Psyche eine hochfaszinierende Fluchtbewegung: Sie flüchtet in die totale Verleugnung (*Denial*). In *My Baby* blendet die Person das soeben erlebte Trauma komplett aus. Wenn man jetzt hier zusammen im Halbdunkel liegt, fühlt sich plötzlich alles wieder betörend „richtig“ an. Es ist ein toxischer Schutzrausch: Die beiden kapseln sich hermetisch von der Realität ab – eine verbotene Festung zu zweit, die niemand sehen und niemand wissen darf, weil jeder Blick von außen die fragile Illusion sofort zerstören würde.""",
        "cards": [
            {
                "quote": "My Baby / Die betäubende Illusion von Geborgenheit",
                "body": """Nach dem Panikanfall schüttet das erschöpfte System massive Dosen an Bindungshormonen aus, um den Schmerz zu betäuben. Der Partner wird auf die verkleinernde, zärtliche Chiffre *„Baby“* reduziert. In diesem Moment redet sich die Psyche ein: *Solange wir uns berühren, ist nichts passiert.* Es ist der klassische Mechanismus der Verleugnung: Man weiß um den Abgrund, entscheidet sich aber aktiv dafür, die Augen zu schließen und im warmen Morast der Illusion zu versinken."""
            },
            {
                "quote": "Niemand darf es wissen / Die hermetische Quarantäne",
                "body": """Die Außenwelt wird zur tödlichen Bedrohung erklärt, weil sie die Wahrheit ausspricht. Die Beziehung wird zum geheimen Kult stilisiert: *Nur wir zwei gegen den Rest der Welt.* Akustisch ist der Track von dumpfen, intimen Bässen geprägt – wie ein schalldichter Raum, in dem der Sauerstoff langsam ausgeht. Es ist die unheimliche Ruhe vor dem endgültigen Einsturz: Eine Bindung, die nur durch das Verleugnen der Realität existieren kann, ist im Kern bereits tot."""
            }
        ]
    },
    "06": {
        "review": """### Track 06: Have You Seen Me Dance Alone — Die Sollbruchstelle & Der Ausbruch der Autonomie
Der absolute emotionale und dramaturgische Wendepunkt des Werks. *Have You Seen Me Dance Alone* ist keine sentimentale Trennungsklage, sondern der seismische Moment, in dem die unmaskierte, ungeschützte Lebendigkeit des Ichs die toxische Verleugnung aus Track 5 wie Glas zersprengt.""",
        "cards": [
            {
                "quote": "Have you seen me dance alone? / Der Akt radikaler Selbstbehauptung",
                "body": """Die Frage ist ein psychologischer Sprengsatz. Das Alleintanzen ist der somatische Durchbruch: Der Körper verweigert den gemeinsamen Takt und findet seinen ureigenen Rhythmus wieder. Die tonische Erstarrung fällt schlagartig ab; die Lunge füllt sich mit frischer Luft. 

In dem Moment, in dem das Ich spürt, dass es ohne die Bestätigung und Erlaubnis des Partners lebendig sein, tanzen und Freude empfinden kann, verliert das gesamte System der Abhängigkeit mit einem Schlag seine Macht."""
            },
            {
                "quote": "Das Aufbrechen des Stereopanoramas",
                "body": """Die Produktion explodiert förmlich: Die klaustrophobische, dumpfe Enge von *My Baby* weicht weiten, glanzvollen Hallräumen. Die Stimme steht plötzlich frei, ungeschminkt und kraftvoll im Zentrum. Die dysfunktionale Bindung kollabiert nicht durch Streit, sondern durch die unerträgliche Strahlkraft unmaskierter Selbstständigkeit."""
            }
        ]
    },
    "07": {
        "review": """### Track 07: Somewhere Else — Die posttraumatische Schockwelle & Das Einfrieren des Kerns
Auf den Rausch der Befreiung folgt der unvermeidliche Preis: der Eintritt in die dissoziative Kältestarre. *Somewhere Else* dokumentiert den Schutzmechanismus des Einfrierens (*Freeze*). Um die Wucht des Bindungsabrisses zu überleben, zieht sich das Bewusstsein weit hinter die eigenen Augen zurück.""",
        "cards": [
            {
                "quote": "Somewhere Else / Die depersonalisierte Vogelperspektive",
                "body": """Das Ich betätigt die seelische Notbremse: Depersonalisation. Der Sprecher erlebt sich selbst wie eine fremde Marionette auf einer fernen Bühne. Somatisch sinkt die Temperatur, die Hände und Füße fühlen sich taub an, die Stimme klingt belegt, gefiltert und weit in den Hintergrund gemischt – ein Geist, der durch den eigenen Körper wandelt."""
            },
            {
                "quote": "Das Eis als lebenserhaltendes Koma",
                "body": """Die Kälte wird hier nicht als Mangel erlebt, sondern als lebensnotwendige Anästhesie. Wo zuvor zerstörerische Hitze und Panik herrschten, breitet sich nun eine unantastbare, gläserne Stille aus. Ein emotionaler Winterschlaf, in dem die tiefen Wunden der Symbiose langsam abkühlen und taub werden können."""
            }
        ]
    },
    "08": {
        "review": """### Track 08: I Drink The Light — Der manische Gegenangriff & Sensorischer Hunger
Der gewaltsame Versuch, die Taubheit aus Track 7 zu durchbrechen. *I Drink The Light* ist ein manischer, hochenergetischer Sturmlauf: Die Psyche pumpt maximale Reize, Licht und Lautstärke in das System, um die innere Leere durch sensorischen Exzess zu verbrennen.""",
        "cards": [
            {
                "quote": "I drink the light / Die Somatik des Reizhungers",
                "body": """Die Metapher *„I drink the light“* ist pure Somatik des Hungers: Licht wird nicht passiv betrachtet, sondern wie eine rettende Flüssigkeit gierig hinuntergeschluckt. Ein verzweifeltes Verlangen nach Dopamin, nach Puls, nach elektrischer Erregung. Die Augen weiten sich, der Herzschlag rast wieder empor, die Bewegungen werden fahrig, manisch und getrieben."""
            },
            {
                "quote": "Elektrisierende Synths & Übersteuerung",
                "body": """Messerscharfe Synthesizer-Arpeggios peitschen durch das Stereofeld. Es ist die hemmungslose Ekstase am Rande des Nervenzusammenbruchs – der Versuch, Schmerz und Trauer durch pure Reizüberflutung zu betäuben, bevor das System unausweichlich an seinen absoluten Nullpunkt gelangt."""
            }
        ]
    },
    "09": {
        "review": """### Track 09: Wavelengths — Der Ego-Tod & Das Begraben der falschen Masken
Das Epizentrum der Dekonstruktion. In *Wavelengths* brechen alle manischen Schutzschichten und antrainierten Identitäten endgültig in sich zusammen. Die fundamentale Frage *„Who am I?“* hallt durch einen kargen, elektronisch zerklüfteten Raum.""",
        "cards": [
            {
                "quote": "Who am I? / Die Zertrümmerung der adaptiven Persona",
                "body": """Das Ich steht fassungslos vor den Trümmern seiner bisherigen Rollen (der Retter, das brave Kind, der bedürftige Liebhaber). Alle Masken, die jemals getragen wurden, um Liebe und Sicherheit zu erbetteln, werden feierlich begraben. Der Körper sinkt in eine tiefe, schwere Erdung; die Atmung verlangsamt sich auf einen meditativen Grundrhythmus."""
            },
            {
                "quote": "Wavelengths / Frequenzen im Nichts",
                "body": """Minimalistische Soundscapes, nackte Sub-Bässe und weite, atmende Pausen. Das Nichts wird hier nicht mehr gefürchtet, sondern ausgehalten. Die Welle glättet sich – ein Zustand unbestechlicher, nackter Wahrhaftigkeit, in dem keine Ausreden und keine Lügen mehr existieren."""
            }
        ]
    },
    "10": {
        "review": """### Track 10: Side By Side — Die nüchterne Inventur der Phantom-Bindung
Ein Moment kristallener Klarheit. *Side By Side* ist keine sentimentale Hoffnung auf ein Comeback, sondern die würdevolle, nüchterne Inventur einer vergangenen Verbindung aus sicherer, stabiler Distanz.""",
        "cards": [
            {
                "quote": "Side By Side / Die Anerkennung der unüberbrückbaren Distanz",
                "body": """Man blickt über das einstige gemeinsame Territorium, ohne den Drang zu verspüren, die Grenze erneut zu übertreten. Die Körperhaltung ist aufrecht, entspannt, der Blick ruhig und direkt. Kein Groll, keine Idealisierung, sondern eine fast mathematische Anerkennung dessen, was war und was nie wieder sein wird."""
            },
            {
                "quote": "Warme Mitten & Organische Erdung",
                "body": """Die Produktion gewinnt an natürlicher Wärme zurück. Ausgewogene Mitten und akustische Texturen signalisieren die Rückkehr zu stabiler, autonomer Selbstregulation. Die Grenze zwischen dem Selbst und dem Anderen ist wiederhergestellt und unumstößlich."""
            }
        ]
    },
    "11": {
        "review": """### Track 11: The Thing — Der absolute Nullpunkt & Der Wiederaufbau aus dem Knochen
Der tiefste Punkt der Dekonstruktion und das Fundament der Auferstehung. In *The Thing* werden Emotionen nicht mehr als überwältigende Katastrophen erlebt, sondern wie tote, physische Objekte seziert. Der Wiederaufbau beginnt rein somatisch an der Knochensubstanz.""",
        "cards": [
            {
                "quote": "The Thing / Die Verdinglichung des Schmerzes",
                "body": """Das Trauma verliert sein melodramatisches Narrativ und wird zu einem simplen, schweren *„Ding“* dekonstruiert, das man greifen, wiegen und ablegen kann. Keine Opferhaltung mehr, kein Warten auf einen Retter. Der Sprecher verlangt absolut nichts mehr von der Welt."""
            },
            {
                "quote": "Build my body from the bone / Die Anatomie der Disziplin",
                "body": """Trockene, wuchtige Perkussion wie Hammerschläge auf Granit. Der Wiederaufbau erfolgt Knochen für Knochen, Muskelstrang für Muskelstrang. Eine stoische, kompromisslos disziplinierte Rekonstruktion des Charakters aus der eigenen unzerstörbaren Substanz heraus."""
            }
        ]
    },
    "12": {
        "review": """### Track 12: In A Minute — Die unerschütterliche Souveränität & Das Gesetz der Integrität
Das triumphale Finale des Werks. Kein kitschiges Hollywood-Happy-End, sondern die eiserne, feierliche Selbstverpflichtung zu kompromissloser Integrität: *„Don’t you forget about yourself“*.""",
        "cards": [
            {
                "quote": "Don't you forget about yourself / Der heilige Eid nach innen",
                "body": """Der finale Imperativ richtet sich nicht mehr an den Partner, sondern an das eigene Bewusstsein. Es ist der lebenslange Schwur, sich nie wieder für die Illusion von Nähe selbst zu verraten oder die eigene Souveränität zur Disposition zu stellen. Die Körperhaltung ist vollkommen zentriert, die Lunge weit, die Stimme unerschütterlich fest im Raum verankert."""
            },
            {
                "quote": "Harmonische Weite & Triumphale Klarheit",
                "body": """Das gesamte Klangspektrum erstrahlt in majestätischer Auflösung. Brillante Höhen, federnde Rhythmen und glasklare Vokalphonetik feiern die Vollendung der Reise: Aus der Asche des totalen Zusammenbruchs ist ein unzerstörbares, autonomes Selbst erwachsen."""
            }
        ]
    }
}

# 2. ENGLISCHE MASTER-TIEFENANALYSE (Fully fleshed out literary & psychoanalytic depth)
en_tracks_deep = {
    "01": {
        "review": """### Track 01: Please — The Anatomy of Pleading & The Infantile Regression Trap
The album opens not with an assertion of strength or the posturing of a sovereign self, but with a pure vocative of total surrender: *\"Please\"*. It is an entry point of devastating intimacy. The speaker begins from a position of zero leverage, where the right to exist is entirely dependent on the responsiveness of the other. Closeness in *Please* is framed not as mutual affection, but as a neurobiological emergency—a compulsive, automated distress signal to numb an inner vacuum through the forced presence of an external object.""",
        "cards": [
            {
                "quote": "Please (Please) / The Chamber of Echoes",
                "body": """The double, ghostly echo `(Please)` acts as an intrapsychic reverberation chamber. From the first second, the speaker exists in fundamental asymmetry: possessing no emotional leverage other than appealing to the mercy of the other.

Somatically, this is a physical collapse of the postural system—the chest caves inward, breathing turns shallow and rapid, and the voice exhales into defenseless surrender. Yet beneath apparent weakness lies an unconscious, manipulative control technique: by humiliating oneself completely and dissolving all personal boundaries, the partner is coerced into the role of the omnipotent savior. Neediness becomes a snare that denies the other person their right to distance without appearing openly aggressive."""
            },
            {
                "quote": "Come (Please come) / The Paralyzed Imperative",
                "body": """The arrival of the first verb (*\"Come\"*) marks the fragile transition where passive regression turns into a targeted demand. Yet the ego dares not let the command stand bare; it is instantly cushioned by the qualifying plea *\"(Please come)\"*.

The nervous system is paralyzed between two opposing forces: sympathetic activation (the desperate urge to grasp outward) and dorsal inhibition (the freeze of impending rejection). Responsibility for crossing the threshold is dumped entirely onto the partner: the speaker refuses to move; the other must travel the entire distance to fill the void."""
            },
            {
                "quote": "Closer, closer, closer / The Erasure of Space",
                "body": """The eightfold staccato repetition of the comparative *\"closer\"* unmasks a compulsive fixation. This is no longer about achieving healthy intimacy, but about the total eradication of intermediate space. Every millimeter of physical or emotional distance is decoded by the alarm system as existential annihilation.

Acoustically, circulating vocal loops tighten around the listener's head like a noose. The production constructs a claustrophobic vacuum: the voice sits directly on the auditory nerve, disabling rational reflection—the frantic grip of a drowning person dragging their rescuer under the surface."""
            }
        ]
    },
    "02": {
        "review": """### Track 02: Come Closer — Toxic Fusion & The Hunger for Co-Regulation
What began as timid pleading in *Please* accelerates into an aggressive, hypnotic vortex in *Come Closer*. Closeness is now fully weaponized as a narcotic. The track dissects the dangerous illusion that internal fragmentation can be healed by completely dissolving one's psychic and bodily boundaries into the partner.""",
        "cards": [
            {
                "quote": "Come closer, come closer / Accelerating the Vortex",
                "body": """The tempo quickens as low-end frequencies drill deep into the gut. The lyrics articulate an addictive craving for external co-regulation: the speaker's nervous system is incapable of self-soothing or enduring solitude. Physical contact acts as a chemical tranquilizer against internal panic. Any hesitation from the partner is instantly misinterpreted as betrayal and existential threat."""
            },
            {
                "quote": "I need you near / Dissolving the Boundaries of the Self",
                "body": """The simple formula *\"I need you near\"* exposes the conflation of love with emotional hostage-taking. Personal sovereignty is surrendered in exchange for total physical access and possession of the other. A closed circuit forms where any individual boundary of the partner is branded as treason."""
            }
        ]
    },
    "03": {
        "review": """### Track 03: A Boy Like You — Intellectual Armor & Vivisection of the Archetype
A radical pivot in the psychological architecture of the album: helpless pleading is abandoned for razor-sharp, hypervigilant intellectualization. *A Boy Like You* is a forensic autopsy of the counterpart. Fearing emotional vulnerability, the ego retreats behind a fortress of first-principles logic and ruthless pattern recognition.""",
        "cards": [
            {
                "quote": "A Boy Like You / Dissecting the Projection",
                "body": """The speaker switches from feeling to surveillance. Every micro-behavior, character flaw, and inconsistency in the partner's demeanor is cataloged and dissected. Language becomes clinical and razor-sharp. The motive is self-defense: if one can thoroughly decode, classify, and demystify the other, one can never be ambushed by heartbreak again."""
            },
            {
                "quote": "The Dissonance Between Ideal and Reality",
                "body": """The vocal production is bone-dry and clinical, positioned directly against the eardrum without softening reverb. Beneath the brilliant critique lies the bitter realization that the real person across the room will never match the flawless projection inside one's mind. Cognitive control serves as the final dam before systemic collapse."""
            }
        ]
    },
    "04": {
        "review": """### Track 04: Ring The Alarm — Central Nervous System Overload & Acute Panic
The intellectual armor of Track 3 shatters completely under the weight of reality. *Ring The Alarm* documents the catastrophic failure of cognitive control—the central nervous system descends into acute sympathetic overdrive as the threat of abandonment triggers full-blown psychic panic.""",
        "cards": [
            {
                "quote": "Aah-aah-aah / The Wordless Siren",
                "body": """Verbal language fails; primal vocalization takes over. Siren-like vocal trajectories mirror severe physiological distress: racing heart, dilated pupils, trembling extremities, and hyperventilation. The ancient alarm system has hijacked the psyche; distance feels like a freefall into the abyss."""
            },
            {
                "quote": "Ring The Alarm / The Terror of Loss",
                "body": """Brutal, distorted drum hits propel the track forward. The alarm is not merely an SOS to the fleeing lover, but an internal fire siren: the psyche realizes that the symbiotic contract has failed and the illusion of control is gone forever."""
            }
        ]
    },
    "05": {
        "review": """### Track 05: My Baby — The Euphoric Refuge of Denial & The Secret Fortress
Following the catastrophic burnout of *Ring The Alarm*, the psyche executes a fascinating psychological maneuver: it retreats into total denial. In *My Baby*, the speaker banishes the trauma they just experienced. Lying together in the dark, everything suddenly feels deceptively, intoxicatingly \"right.\" It is a toxic refuge of denial: the two hermetically seal themselves off from reality—a forbidden fortress where no outside gaze is allowed, because any intrusion of sanity would instantly shatter the fragile fantasy.""",
        "cards": [
            {
                "quote": "My Baby / The Sedative Illusion of Safety",
                "body": """Following the panic attack, the exhausted system floods itself with attachment hormones to numb the agony. The partner is reduced to the tender, infantile cipher *\"Baby.\"* In this moment, the psyche convinces itself: *As long as we touch, nothing has happened.* It is the classic mechanism of denial: conscious of the abyss, one actively chooses to close one's eyes and sink into the warm mud of the illusion."""
            },
            {
                "quote": "No One Can Know / The Hermetic Quarantine",
                "body": """The outside world is declared a mortal enemy because it speaks the truth. The relationship is styled as a secret cult: *Just the two of us against everything.* Acoustically, the track breathes the muffled, intimate low-end of a soundproof room where oxygen is steadily running out. This is the eerie calm before the final collapse: a bond that requires the denial of reality to exist is already clinically dead."""
            }
        ]
    },
    "06": {
        "review": """### Track 06: Have You Seen Me Dance Alone — The Turning Point & Eruption of Autonomy
The decisive structural and emotional watershed of the entire album. *Have You Seen Me Dance Alone* is not a melancholy song about loneliness, but the explosive moment unmasked authenticity detonates the symbiotic prison.""",
        "cards": [
            {
                "quote": "Have you seen me dance alone? / Radical Self-Reclamation",
                "body": """The question is a psychological depth charge. Dancing in solitude is the somatic proof of reclaimed agency: the body ceases to move to the partner's tempo and discovers its own rhythm. Postural rigidity dissolves; the diaphragm and chest expand.

The instant the self experiences that joy, vitality, and rhythm exist without external validation, the entire mechanism of symbiotic manipulation loses its grip."""
            },
            {
                "quote": "Opening the Panoramic Horizon",
                "body": """The sonic production expands dramatically: suffocating compression gives way to lush, panoramic reverb. The vocal stands bare, powerful, and central. The dysfunctional bond collapses not from conflict, but under the sheer, unbearable weight of raw autonomy."""
            }
        ]
    },
    "07": {
        "review": """### Track 07: Somewhere Else — Post-Traumatic Frost & Dissociative Freeze
Following the explosive liberation comes the shockwave. *Somewhere Else* documents the inevitable cost of radical sovereignty: drifting into emotional anesthesia to survive the post-rupture void.""",
        "cards": [
            {
                "quote": "Somewhere Else / Observing from the Stratosphere",
                "body": """The psyche pulls the emergency brake and enters a dorsal vagal freeze state. The speaker watches their own life like a detached observer watching a distant screen (depersonalization). Somatically, body temperature plummets; extremities numb, and the vocal sits pushed back into an icy, distant hall."""
            },
            {
                "quote": "The Protective Armor of Ice",
                "body": """The cold is not experienced as a deficit, but as a vital temporary coma. Where destructive heat and panic once reigned, an untouchable silence now spreads—a winter hibernation where the wounds of fusion can cool and crystallize."""
            }
        ]
    },
    "08": {
        "review": """### Track 08: I Drink The Light — Manic Counter-Offensive & Sensory Hunger
A frantic effort to shatter the freeze of Track 7. *I Drink The Light* is an aggressive, manic surge: the psyche floods the system with extreme stimuli to incinerate depression through sensory overload.""",
        "cards": [
            {
                "quote": "I drink the light / The Ingestion of Radiance",
                "body": """The phrasing *\"I drink the light\"* represents the raw somatics of hunger: radiance is not passively received, but greedily gulped down like liquid. A ravenous hunger for dopamine, sensation, and vitality. Pupils dilate, the pulse surges, and physical movements turn restless and electric."""
            },
            {
                "quote": "Pulsating Arpeggios & Overdrive",
                "body": """Razor-sharp synthesizer lines tear through the soundscape. This is ecstasy on the verge of exhaustion—a manic bid to outrun internal grief through sheer acoustic velocity before arriving at ground zero."""
            }
        ]
    },
    "09": {
        "review": """### Track 09: Wavelengths — Ego Death & The Burial of False Masks
The epicenter of the breakdown. In *Wavelengths*, all manic armor and defensive personas disintegrate. The fundamental inquiry *\"Who am I?\"* echoes through a barren, electronic wasteland.""",
        "cards": [
            {
                "quote": "Who am I? / Shattering the Persona",
                "body": """The ego stands among the ruins of its former survival roles (the savior, the pleader, the performer). Every adaptive mask worn to secure love is buried in cold clarity. The physical body sinks into deep stillness; respiration slows to a rhythmic baseline."""
            },
            {
                "quote": "Wavelengths / Frequencies in the Void",
                "body": """Minimalist textures, subterranean sub-bass, and vast spaces of silence. The void is no longer feared, but inhabited. The waves smooth out into a state of uncompromising truth where excuses cease to exist."""
            }
        ]
    },
    "10": {
        "review": """### Track 10: Side By Side — Auditing the Residual Phantom Bond
A moment of crystalline lucidity. *Side By Side* is not a nostalgic bid for reunion, but a dignified, objective audit of a past connection viewed from a position of secure boundaries.""",
        "cards": [
            {
                "quote": "Side By Side / Acknowledging the Divide",
                "body": """Looking across the shared history without the urge to cross the line again. The physical posture is balanced, shoulders relaxed, the gaze steady. No bitterness, no romantic idealization—simply a mathematical recognition of what was and what will never be again."""
            },
            {
                "quote": "Warm Mid-Ranges & Organic Grounding",
                "body": """The sonic palette regains organic warmth. Balanced acoustic textures signal the return of stable internal self-regulation. The perimeter of the sovereign self is firmly re-established."""
            }
        ]
    },
    "11": {
        "review": """### Track 11: The Thing — Absolute Zero & Rebuilding from the Bone
The deepest floor of deconstruction and the bedrock of genuine resurrection. In *The Thing*, emotions are no longer treated as overwhelming floods, but examined as cold, physical objects. Reconstruction begins somatically from the bare bone.""",
        "cards": [
            {
                "quote": "The Thing / Objectifying Trauma",
                "body": """Pain is stripped of its melodramatic narrative and reduced to a concrete, heavy *\"thing\"* that can be held, inspected, and set down. No victimhood, no appeals for external salvation. The speaker demands nothing from the outside world."""
            },
            {
                "quote": "Build my body from the bone / The Somatic Blueprint",
                "body": """Heavy, bone-dry percussion strikes like chisels on stone. The body is rebuilt bone by bone, muscle strand by muscle strand. A stoic, disciplined reconstruction of character from one's own indestructible marrow."""
            }
        ]
    },
    "12": {
        "review": """### Track 12: In A Minute — Sovereign Reclamation & Autonomous Authority
The triumphant culmination of the album. Not a sentimental fantasy, but a battle-tested, disciplined covenant of uncompromising integrity: *\"Don’t you forget about yourself\"*.""",
        "cards": [
            {
                "quote": "Don't you forget about yourself / The Sovereign Law",
                "body": """The final command is directed inward, not outward. It is the unshakeable vow never again to barter personal sovereignty for the illusion of intimacy. The posture is fully integrated, the chest open, the voice rooted and immovable in the acoustic space."""
            },
            {
                "quote": "Expansive Harmonic Resolution",
                "body": """The full acoustic spectrum blazes in majestic clarity. Sparkling high frequencies, resilient rhythms, and effortless vocal power celebrate the completion of the journey: out of the ashes of total collapse, a sovereign, autonomous self has arisen."""
            }
        ]
    }
}

# 3. Clean Master HTML Template (No f-string issues)
html_template_raw = """<!DOCTYPE html>
<html lang="[[LANG]]">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[[UI_TITLE]]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg: #0c0c0f;
      --bg-surface: #141418;
      --text: #ffffff;
      --text-muted: #8e8e93;
      --magenta: #ff007a;
      --magenta-dim: rgba(255, 0, 122, 0.12);
      --magenta-glow: rgba(255, 0, 122, 0.35);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    html {
      scroll-behavior: smooth;
      background-color: var(--bg);
    }

    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.65;
      overflow-x: hidden;
      position: relative;
    }

    /* Animierter 35mm Analog-Film-Grain Canvas */
    #grainCanvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 9999;
      opacity: 0.11;
      mix-blend-mode: screen;
    }

    ::selection {
      background-color: var(--magenta);
      color: #ffffff;
    }

    /* Minimalistische Navbar */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 65px;
      background: rgba(12, 12, 15, 0.85);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      padding: 0 32px;
      z-index: 1000;
    }

    .burger-icon {
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 6px;
      width: 24px;
      height: 24px;
      padding: 0;
      background: none;
      border: none;
    }

    .burger-icon span {
      display: block;
      width: 100%;
      height: 2px;
      background-color: #ffffff;
      transition: all 0.2s;
    }

    .burger-icon:hover span {
      background-color: var(--magenta);
    }

    .nav-brand {
      font-size: 1.4rem;
      font-weight: 900;
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: var(--magenta);
      text-decoration: none;
      text-align: center;
    }

    .nav-spacer { width: 24px; }

    /* Inhaltsverzeichnis (Drawer) */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      z-index: 1100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }
    .drawer-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }

    .drawer {
      position: fixed;
      top: 0;
      left: -340px;
      width: min(320px, 85vw);
      height: 100vh;
      background-color: #111115;
      z-index: 1200;
      padding: 20px 32px 36px 32px;
      display: flex;
      flex-direction: column;
      transition: left 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      overflow-y: auto;
    }
    .drawer.active { left: 0; }

    .drawer-header {
      height: 25px;
      display: flex;
      align-items: center;
      gap: 20px;
      margin-bottom: 36px;
    }

    .drawer-close-btn {
      background: none;
      border: none;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: center;
      width: 24px;
      height: 24px;
      padding: 0;
      position: relative;
    }

    .drawer-close-btn span {
      display: block;
      width: 24px;
      height: 2px;
      background-color: var(--magenta);
      position: absolute;
      top: 11px;
      left: 0;
      transition: background-color 0.2s;
    }

    .drawer-close-btn span:nth-child(1) { transform: rotate(45deg); }
    .drawer-close-btn span:nth-child(2) { transform: rotate(-45deg); }
    .drawer-close-btn:hover span { background-color: #ffffff; }

    .drawer-title {
      font-size: 0.85rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--magenta);
      line-height: 1;
    }

    .drawer-nav {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .drawer-nav a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 1rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      display: block;
      padding: 4px 0;
      transition: all 0.2s;
    }

    .drawer-nav a:hover {
      color: #ffffff;
      padding-left: 6px;
    }

    /* FULL BLEED HERO VIDEO */
    .hero-fullbleed {
      margin-top: 65px;
      width: 100%;
      max-height: 75vh;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #000000;
    }

    .hero-video {
      width: 100%;
      height: 100%;
      max-height: 75vh;
      object-fit: cover;
      object-position: center;
      display: block;
    }

    /* Content Area */
    .page-container {
      max-width: 1380px;
      margin: 0 auto;
      padding: 80px 32px 140px 32px;
    }

    /* Track Block */
    .track-block {
      margin-bottom: 160px;
      scroll-margin-top: 90px;
    }

    .track-heading {
      font-size: clamp(2.4rem, 5.5vw, 3.8rem);
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 48px;
      color: var(--magenta);
      display: flex;
      align-items: baseline;
      gap: 16px;
      user-select: none;
      cursor: default;
    }

    .track-heading .num {
      color: #ffffff;
      font-size: 0.75em;
    }

    /* 2 Columns: Left Lyrics, Right Analysis */
    .track-grid {
      display: grid;
      grid-template-columns: 1fr 1.35fr;
      gap: 70px;
      align-items: start;
    }

    /* Lyrics Column */
    .lyrics-col {
      padding-right: 20px;
    }

    .col-header {
      font-size: 0.85rem;
      font-weight: 900;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--magenta);
      margin-bottom: 24px;
      user-select: none;
      cursor: default;
    }

    .stanza-block {
      margin-bottom: 32px;
    }

    .stanza-title {
      font-size: 0.8rem;
      font-weight: 800;
      color: var(--magenta);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 10px;
      opacity: 0.85;
      user-select: none;
      cursor: default;
    }

    .lyric-line {
      font-size: 1.18rem;
      line-height: 1.9;
      color: #f4f4f5;
      padding: 4px 10px;
      margin: 3px -10px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .lyric-line:hover {
      background: rgba(255, 0, 122, 0.18);
      color: #ffffff;
      transform: translateX(4px);
    }

    .lyric-line.active-line {
      background: var(--magenta);
      color: #ffffff;
      font-weight: 700;
      transform: translateX(6px);
      box-shadow: 0 4px 20px var(--magenta-glow);
    }

    /* Analysis Column */
    .analysis-col {
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .review-intro-box {
      font-size: 1.08rem;
      line-height: 1.85;
      color: #d1d1d6;
      margin-bottom: 16px;
    }

    .review-intro-box h1, .review-intro-box h2, .review-intro-box h3 {
      display: none;
    }

    .review-intro-box p {
      margin-bottom: 18px;
    }

    .review-intro-box strong {
      color: #ffffff;
    }

    /* Analysis Cards */
    .analysis-card {
      background: var(--bg-surface);
      border-radius: 6px;
      padding: 26px 30px;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      border-left: 3px solid transparent;
      scroll-margin-top: 100px;
    }

    .analysis-card:hover {
      background: #18181e;
    }

    .analysis-card.highlighted {
      background: #201322;
      border-left-color: var(--magenta);
      box-shadow: 0 6px 30px rgba(255, 0, 122, 0.22);
      transform: scale(1.015);
    }

    .card-quote {
      font-size: 1.18rem;
      font-weight: 800;
      color: var(--magenta);
      margin-bottom: 16px;
      letter-spacing: 0.02em;
      user-select: none;
    }

    .card-body {
      font-size: 1.04rem;
      line-height: 1.8;
      color: #c4c4cc;
    }

    .card-body p {
      margin-bottom: 16px;
    }
    .card-body p:last-child {
      margin-bottom: 0;
    }

    .card-body strong {
      color: #ffffff;
      font-weight: 600;
    }

    .card-body ul {
      margin: 12px 0 12px 18px;
    }

    .card-body li {
      margin-bottom: 10px;
    }

    /* Responsive */
    @media (max-width: 960px) {
      .track-grid {
        grid-template-columns: 1fr;
        gap: 50px;
      }
      .page-container {
        padding: 40px 20px 100px 20px;
      }
      .navbar {
        padding: 0 20px;
      }
    }
  </style>
</head>
<body>

  <!-- Animated Analog Noise Canvas -->
  <canvas id="grainCanvas"></canvas>

  <!-- Minimalist Navbar -->
  <nav class="navbar">
    <button class="burger-icon" onclick="toggleDrawer()" aria-label="[[UI_MENU_ARIA]]">
      <span></span>
      <span></span>
      <span></span>
    </button>
    
    <a href="#" class="nav-brand">TOMORA</a>
    
    <div class="nav-spacer"></div>
  </nav>

  <!-- Track Navigation Drawer -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer()"></div>
  <aside class="drawer" id="drawer">
    <div class="drawer-header">
      <button class="drawer-close-btn" onclick="toggleDrawer()" aria-label="[[UI_CLOSE_ARIA]]">
        <span></span>
        <span></span>
      </button>
      <div class="drawer-title">[[UI_DRAWER_TITLE]]</div>
    </div>
    <ul class="drawer-nav" id="drawerTrackLinks">
      <!-- Tracks injected via JS -->
    </ul>
  </aside>

  <!-- Full-Bleed Video Banner -->
  <header class="hero-fullbleed">
    <video class="hero-video" autoplay loop muted playsinline src="hero_video.mp4"></video>
  </header>

  <!-- Main Content: All 12 Tracks -->
  <main class="page-container" id="tracksContainer">
    <!-- Tracks injected via JS -->
  </main>

  <script>
    // 1. Moving 35mm Film Grain Canvas Animation
    const canvas = document.getElementById('grainCanvas');
    const ctx = canvas.getContext('2d');
    let grainFrame = 0;

    function resizeGrain() {
      canvas.width = Math.ceil(window.innerWidth / 2.5);
      canvas.height = Math.ceil(window.innerHeight / 2.5);
    }
    window.addEventListener('resize', resizeGrain);
    resizeGrain();

    function animateGrain() {
      grainFrame++;
      if (grainFrame % 2 === 0) {
        const w = canvas.width;
        const h = canvas.height;
        const imgData = ctx.createImageData(w, h);
        const buf = new Uint32Array(imgData.data.buffer);
        const len = buf.length;
        for (let i = 0; i < len; i++) {
          if (Math.random() < 0.22) {
            buf[i] = Math.random() > 0.45 ? 0x40ffffff : 0x40000000;
          }
        }
        ctx.putImageData(imgData, 0, 0);
      }
      requestAnimationFrame(animateGrain);
    }
    animateGrain();

    // 2. Track Data & App Logic
    const tracks = [[TRACKS_DATA]];

    function toggleDrawer() {
      const drawer = document.getElementById('drawer');
      const overlay = document.getElementById('drawerOverlay');
      drawer.classList.toggle('active');
      overlay.classList.toggle('active');
    }

    function renderMarkdown(md) {
      if (window.marked && typeof window.marked.parse === 'function') {
        return window.marked.parse(md);
      }
      return md
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\\*\\*(.*)\\*\\*/gim, '<strong>$1</strong>')
        .replace(/\\*(.*)\\*/gim, '<em>$1</em>')
        .replace(/\\n\\n/gim, '</p><p>');
    }

    // Precise Interactive Highlighting
    function handleLyricClick(trackIdx, cardIdx, el) {
      const trackSec = document.getElementById('track-' + tracks[trackIdx].num);
      trackSec.querySelectorAll('.lyric-line').forEach(l => l.classList.remove('active-line'));
      trackSec.querySelectorAll('.analysis-card').forEach(c => c.classList.remove('highlighted'));

      el.classList.add('active-line');

      if (cardIdx >= 0) {
        const targetCard = document.getElementById(`card-${trackIdx}-${cardIdx}`);
        if (targetCard) {
          targetCard.classList.add('highlighted');

          const offset = 100;
          const bodyRect = document.body.getBoundingClientRect().top;
          const elementRect = targetCard.getBoundingClientRect().top;
          const elementPosition = elementRect - bodyRect;
          const offsetPosition = elementPosition - offset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      }
    }

    const container = document.getElementById('tracksContainer');
    const drawerLinks = document.getElementById('drawerTrackLinks');

    tracks.forEach((track, tIdx) => {
      // Drawer Link
      const li = document.createElement('li');
      li.innerHTML = `<a href="#track-${track.num}" onclick="toggleDrawer()">${track.num}. ${track.title}</a>`;
      drawerLinks.appendChild(li);

      // Track Section
      const sec = document.createElement('section');
      sec.className = 'track-block';
      sec.id = 'track-' + track.num;

      // Build Stanzas HTML
      let lyricsHtml = '';
      track.stanzas.forEach((stanza) => {
        lyricsHtml += `<div class="stanza-block">`;
        if (stanza.title) {
          lyricsHtml += `<div class="stanza-title">${stanza.title}</div>`;
        }
        stanza.lines.forEach((lineObj) => {
          lyricsHtml += `<div class="lyric-line" onclick="handleLyricClick(${tIdx}, ${lineObj.target_card}, this)">${lineObj.text}</div>`;
        });
        lyricsHtml += `</div>`;
      });

      // Build Analysis Cards HTML
      let analysisCardsHtml = '';
      track.analysis_cards.forEach((card, cIdx) => {
        analysisCardsHtml += `
          <div class="analysis-card" id="card-${tIdx}-${cIdx}">
            ${card.quote ? `<div class="card-quote">${card.quote}</div>` : ''}
            <div class="card-body">${renderMarkdown(card.body)}</div>
          </div>
        `;
      });

      sec.innerHTML = `
        <h2 class="track-heading">
          <span class="num">${track.num}.</span> ${track.title}
        </h2>
        <div class="track-grid">
          <!-- Left: Lyrics -->
          <div class="lyrics-col">
            <div class="col-header">[[UI_LYRICS_HEADER]]</div>
            <div class="lyrics-wrapper">${lyricsHtml}</div>
          </div>
          <!-- Right: Interpretation & Deconstruction -->
          <div class="analysis-col">
            <div class="col-header">[[UI_ANALYSIS_HEADER]]</div>
            ${track.review ? `<div class="review-intro-box">${renderMarkdown(track.review)}</div>` : ''}
            ${analysisCardsHtml}
          </div>
        </div>
      `;

      container.appendChild(sec);
    });
  </script>
</body>
</html>
"""

def generate_file(lang, tracks_data, out_local, out_sub, out_drive):
    labels = {
        "de": {
            "title": "TOMORA — Lyrics & Tiefenanalyse",
            "drawer_title": "12 TRACKS",
            "lyrics_header": "Songtext / Lyrics",
            "analysis_header": "Interpretation & Tiefenanalyse",
            "close_aria": "Schließen",
            "menu_aria": "Menü"
        },
        "en": {
            "title": "TOMORA — Lyrics & Deep Analysis",
            "drawer_title": "12 TRACKS",
            "lyrics_header": "Lyrics",
            "analysis_header": "Interpretation & Deep Analysis",
            "close_aria": "Close",
            "menu_aria": "Menu"
        }
    }[lang]

    content = html_template_raw
    content = content.replace('[[LANG]]', lang)
    content = content.replace('[[UI_TITLE]]', labels["title"])
    content = content.replace('[[UI_DRAWER_TITLE]]', labels["drawer_title"])
    content = content.replace('[[UI_LYRICS_HEADER]]', labels["lyrics_header"])
    content = content.replace('[[UI_ANALYSIS_HEADER]]', labels["analysis_header"])
    content = content.replace('[[UI_CLOSE_ARIA]]', labels["close_aria"])
    content = content.replace('[[UI_MENU_ARIA]]', labels["menu_aria"])
    content = content.replace('[[TRACKS_DATA]]', json.dumps(tracks_data))

    with open(out_local, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(out_sub, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(out_drive, 'w', encoding='utf-8') as f:
        f.write(content)

# 4. Extract lyrics stanzas cleanly
phase1_dir = 'album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion'

track_names_map = {
    "01": "Please",
    "02": "Come Closer",
    "03": "A Boy Like You",
    "04": "Ring The Alarm",
    "05": "My Baby",
    "06": "Have You Seen Me Dance Alone",
    "07": "Somewhere Else",
    "08": "I Drink The Light",
    "09": "Wavelengths",
    "10": "Side By Side",
    "11": "The Thing",
    "12": "In A Minute"
}

def clean_txt(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def extract_stanzas_for_track(num_str, title, analysis_cards):
    p1_file = f"{num_str}_{title.replace(' ', '_')}.md"
    p1_path = os.path.join(phase1_dir, p1_file)
    if not os.path.exists(p1_path):
        for f in os.listdir(phase1_dir):
            if f.startswith(num_str):
                p1_path = os.path.join(phase1_dir, f)
                break
                
    lyrics_raw = ""
    if os.path.exists(p1_path):
        with open(p1_path, 'r', encoding='utf-8', errors='ignore') as f:
            p1_content = f.read()
        lyrics_match = re.search(r'### 1\.\s*Transkribierter Textkorpus\s*```text(.*?)```', p1_content, re.DOTALL)
        lyrics_raw = lyrics_match.group(1).strip() if lyrics_match else ""

    stanzas = []
    current_stanza = {"title": "", "lines": []}
    
    raw_lines = lyrics_raw.split('\n')
    cleaned_raw_lines = []
    for line in raw_lines:
        line_s = line.strip()
        is_title_line = False
        c_line = clean_txt(line_s)
        c_title = clean_txt(title)
        c_num = str(int(num_str))
        if (c_title in c_line and (c_num in c_line or num_str in c_line)) or line_s.lower() == f"{title.lower()} {c_num}." or line_s.lower() == f"{c_num}. {title.lower()}":
            is_title_line = True
            
        if not is_title_line:
            cleaned_raw_lines.append(line)

    total_valid_lines = len([l for l in cleaned_raw_lines if l.strip() and not (l.strip().startswith('[') and l.strip().endswith(']'))])
    line_idx_tracker = 0

    for line in cleaned_raw_lines:
        line_s = line.strip()
        if line_s.startswith('[') and line_s.endswith(']'):
            if current_stanza["lines"]:
                stanzas.append(current_stanza)
            current_stanza = {"title": line_s, "lines": []}
        elif line_s:
            matched_card_idx = 0
            if len(analysis_cards) > 1:
                ratio = line_idx_tracker / max(1, total_valid_lines)
                matched_card_idx = min(int(ratio * len(analysis_cards)), len(analysis_cards) - 1)

            current_stanza["lines"].append({
                "text": line_s,
                "target_card": matched_card_idx
            })
            line_idx_tracker += 1
        else:
            if current_stanza["lines"]:
                stanzas.append(current_stanza)
                current_stanza = {"title": "", "lines": []}
    if current_stanza["lines"]:
        stanzas.append(current_stanza)

    return stanzas

# Prepare DE Data
de_tracks = []
for num_str, title in track_names_map.items():
    de_info = de_tracks_deep.get(num_str, {"review": "", "cards": []})
    stanzas = extract_stanzas_for_track(num_str, title, de_info["cards"])
    de_tracks.append({
        "num": num_str,
        "title": title,
        "stanzas": stanzas,
        "review": de_info["review"],
        "analysis_cards": de_info["cards"]
    })

# Prepare EN Data
en_tracks = []
for num_str, title in track_names_map.items():
    en_info = en_tracks_deep.get(num_str, {"review": "", "cards": []})
    stanzas = extract_stanzas_for_track(num_str, title, en_info["cards"])
    en_tracks.append({
        "num": num_str,
        "title": title,
        "stanzas": stanzas,
        "review": en_info["review"],
        "analysis_cards": en_info["cards"]
    })

# Build German Edition
generate_file(
    "de",
    de_tracks,
    "c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER.html",
    "c:/Users/Hakan/Documents/antigravity/modest-meitner/album_review_und_interpretation/index.html",
    "H:/Meine Ablage/Album_Review_und_Interpretation/ALBUM_REVIEW_READER.html"
)

# Build English Edition
generate_file(
    "en",
    en_tracks,
    "c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER_EN.html",
    "c:/Users/Hakan/Documents/antigravity/modest-meitner/album_review_und_interpretation/index_en.html",
    "H:/Meine Ablage/Album_Review_und_Interpretation/ALBUM_REVIEW_READER_EN.html"
)

print("Comprehensive Deep Narrative Master Editions compiled and synced!")
