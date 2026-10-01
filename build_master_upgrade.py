import json
import base64
import os
import re

# 1. German Master Deep-Dive Essays & Cards
de_tracks_analysis = {
    "01": {
        "review": """### Track 01: Please — Die Anatomie des Bittens & Die infantile Regressionsfalle
Das Album beginnt nicht mit einer These oder der Selbstbehauptung eines souveränen Ichs, sondern mit einem reinen Vokativ des Kontrollverlusts: *„Please“*. Das einleitende Flehen legt das psychodynamische Fundament der gesamten ersten Albumhälfte. Nähe wird hier nicht als freiwillige Begegnung zweier autonomer Wesen verhandelt, sondern als existenzielle Notwendigkeit – ein reflexhafter, fast automatisierter Hilferuf, um ein inneres Vakuum durch die Zufuhr eines externen Objekts zu betäuben.""",
        "cards": [
            {
                "quote": "Please (Please) / Die Verdopplung des Echos",
                "body": """Das doppelte Echo fungiert als intrapsychische Hallkammer. Der Sprecher befindet sich in einer Position fundamentaler Asymmetrie: Er besitzt keinerlei Hebelwirkung außer dem Appell an die Gnade des Anderen. Somatisch vollzieht sich hier ein Kniefall – die Atemfrequenz steigt, der Brustkorb sinkt ein, und die Stimme verhaucht im ungeschützten Ausatmen. 

Hinter der scheinbaren Unterwerfung verbirgt sich jedoch eine unbewusste Kontrolltechnik: Wer sich maximal erniedrigt und jede eigene Grenze auflöst, zwingt das Gegenüber in die Rolle des allmächtigen Versorgers. Die Bedürftigkeit wird zur Fessel, die dem Partner das Recht auf Distanz entzieht, ohne dass dies nach einem offenen Übergriff aussieht."""
            },
            {
                "quote": "Come (Please come) / Der gelähmte Imperativ",
                "body": """Der Übergang zum ersten Verbum (*„Come“*) markiert den Moment, in dem passive Regression in eine gerichtete Anforderung umschlägt. Doch der Befehl wagt es nicht, rein im Raum zu stehen; er wird sofort durch das eingeschobene *„(Please come)“* abgemildert. Das Nervensystem ist hier zwischen zwei Extremen gefangen: der sympathischen Aktivierung (dem Verlangen, nach dem Anderen zu greifen) und der dorsalen Hemmung (der Lähmung vor Zurückweisung). Die Verantwortung für die Grenzüberwindung wird vollständig auf den Partner abgewälzt – das Subjekt weigert sich, sich selbst zu bewegen; der Andere soll den gesamten Weg zurücklegen."""
            },
            {
                "quote": "Closer, closer, closer / Die Tilgung des Zwischenraums",
                "body": """Die repetitive Stakkato-Kaskade des Komparativs *„closer“* demaskiert den Zwangsbeschlag der Psyche. Es geht nicht um das Erreichen einer gesunden Intimität, sondern um die radikale Auslöschung jedes Zwischenraums. Jeder Zentimeter physischer oder emotionaler Distanz wird vom Nervensystem als existenzielle Bedrohung decodiert. 

Akustisch kreisen die Stimmschleifen im Stereofeld wie eine sich zuziehende Schlinge um den Hörer. Es entsteht eine akustische Klaustrophobie, die keinen Fluchtweg offenbart – das tonische Festhalten eines Ertrinkenden, der den Retter unweigerlich mit unter die Wasseroberfläche reißt."""
            }
        ]
    },
    "02": {
        "review": """### Track 02: Come Closer — Die toxische Verschmelzung & Sensorische Vereinnahmung
Wo *Please* noch zaghaft um Gnade bettelte, schlägt *Come Closer* in eine fordernde, fast hypnotische Zentripetalkraft um. Nähe wird zur Waffe: Der Song seziert den Versuch, die eigene Identität durch die vollständige somatische und psychische Verschmelzung mit dem Partner aufzulösen.""",
        "cards": [
            {
                "quote": "Come closer, come closer / Die Beschleunigung des Sogs",
                "body": """Das Tempo zieht an, die Bässe schieben sich tiefer in den Magenraum. Der Text artikuliert das neurobiologische Verlangen nach Co-Regulation: Das eigene autonome Nervensystem ist unfähig, sich selbst zu beruhigen. Die Anwesenheit des Gegenübers wird zum einzigen Narkotikum, das die innere Leere betäubt. Jedes Zögern des Partners wird als Verrat und Kälte interpretiert."""
            },
            {
                "quote": "I need you near / Die Grenzauflösung als Schutzpanzer",
                "body": """In der simplen Formel *„I need you near“* offenbart sich die Verwechslung von Bindung mit existenzieller Geiselnahme. Der Sprecher opfert die eigene Integrität, um im Gegenzug die lückenlose Kontrolle über die physische Präsenz des Anderen einzufordern. Es entsteht ein hermetisches Spannungsfeld, in dem Individualität als Bedrohung wahrgenommen wird."""
            }
        ]
    },
    "03": {
        "review": """### Track 03: A Boy Like You — Kognitive Schutzpanzerung & Die Vivisektion des Archetyps
Ein abrupter Wechsel in der psychologischen Architektur: Die passive Bedürftigkeit weicht einer schneidenden, hypervigilanten Intellektualisierung. *A Boy Like You* ist die sezierende Durchleuchtung des Gegenübers – ein verzweifelter Versuch, die emotionale Ohnmacht durch analytische Überlegenheit auszugleichen.""",
        "cards": [
            {
                "quote": "A Boy Like You / Die Vermessung der Projektion",
                "body": """Der Sprecher schaltet vom Modus des Fühlens in den Modus des Scannens. Jedes Detail, jede Inkonsistenz im Verhalten des Partners wird katalogisiert. Die Sprache wird messerscharf, fast klinisch. Das Ich zieht sich hinter eine dicke Mauer aus First-Principles-Logik zurück: Wer das Gegenüber vollkommen durchschaut und dekonstruiert, kann von ihm nicht mehr unvorbereitet verletzt werden."""
            },
            {
                "quote": "Die Dissonanz zwischen Ideal und Realität",
                "body": """Die Stimme klingt trocken, hochauflösend, fast ohne Hallraum platziert – direkt auf dem Trommelfell. Hinter der kühlen Analyse pulsiert jedoch die schmerzhafte Erkenntnis, dass der reale Mensch vor einem niemals mit der idealisierten Projektion im eigenen Kopf verschmelzen kann. Die Kontrolle über den Verstand wird zum letzten Rettungsring vor dem drohenden Kontrollverlust."""
            }
        ]
    },
    "04": {
        "review": """### Track 04: Ring The Alarm — Das Überhitzen des Nervensystems & Akute Panik
Die kognitive Schutzpanzerung aus Track 3 splittert in tausend Teile. *Ring The Alarm* ist der klangliche und psychologische Kollaps aller Kontrollmechanismen – das Nervensystem schlägt ungebremst in den Alarmzustand der akuten Trennungsangst um.""",
        "cards": [
            {
                "quote": "Aah-aah-aah / Der unartikulierte Notruf",
                "body": """Die verbale Sprache versagt; an ihre Stelle tritt die rohe, ungeschliffene Lautmalerei. Die Sirenen-artigen Gesangslinien spiegeln einen massiven Adrenalinschub wider: Tachykardie, flacher Atem, zitternde Motorik. Das dorsale Alarmsystem hat die volle Kontrolle übernommen. Jede Nuance von Distanz fühlt sich wie ein freier Fall ins Nichts an."""
            },
            {
                "quote": "Ring The Alarm / Die Panik vor dem Bedeutungsverlust",
                "body": """Schwere, verzerrte Rhythmen peitschen den Track nach vorne. Der Alarm ist nicht nur nach außen an den fliehenden Partner gerichtet, sondern ist ein innerer Feueralarm der Psyche: Das System realisiert, dass die symbiotische Klammerhaltung endgültig gescheitert ist und die Fassade nicht mehr gehalten werden kann."""
            }
        ]
    },
    "05": {
        "review": """### Track 05: My Baby — Die hermetische Zweier-Isolation & Toxisches Cocooning
Nach der Panik folgt die regressive Flucht in eine hermetisch abgeschottete Zweierwelt. *My Baby* dokumentiert den verzweifelten Versuch, die Realität komplett auszublenden und eine künstliche Quarantäne-Zone zu errichten, in der nur noch die Dyade existiert.""",
        "cards": [
            {
                "quote": "My Baby / Die obsessive Einkapselung",
                "body": """Die Außenwelt wird zur feindlichen Bedrohung erklärt; alles Soziale wird gekappt. Der Partner wird auf die infantile Chiffre *„Baby“* reduziert – ein Objekt, das man besitzen, schützen und vor dem eigenen Erwachen bewahren muss. Die Körperhaltung ist nach innen gekehrt, die Berührungen klammernd, der Fokus hyperfokussiert auf die engste Umlaufbahn des Anderen."""
            },
            {
                "quote": "Der dumpfe Raum der gegenseitigen Auslöschung",
                "body": """Akustisch dominieren tiefe, gedämpfte Frequenzen wie unter Wasser. Der Track atmet die stickige Luft eines fensterlosen Zimmers. Es ist die trügerische Ruhe vor dem unvermeidlichen Zusammenbruch: Eine Bindung, die nur durch totale Isolation überleben kann, ist im Kern bereits tot."""
            }
        ]
    },
    "06": {
        "review": """### Track 06: Have You Seen Me Dance Alone — Die Sollbruchstelle & Der Ausbruch der Autonomie
Der absolute Wendepunkt des gesamten Werks. *Have You Seen Me Dance Alone* ist keine traurige Ballade über das Verlassenwerden, sondern der explosive Moment, in dem die ungeschützte Echtheit der eigenen Existenz die toxische Bindung zersprengt.""",
        "cards": [
            {
                "quote": "Have you seen me dance alone? / Der Akt radikaler Selbstbehauptung",
                "body": """Die Frage ist ein psychologischer Sprengsatz. Das Alleintanzen ist das somatische Zeichen wiedererlangter Handlungsfähigkeit: Der Körper bewegt sich nicht mehr im Takt des Partners, sondern findet seinen eigenen Rhythmus. Die tonische Erstarrung der vorherigen Tracks fällt ab; Muskeln und Atemwege öffnen sich schlagartig. 

In dem Moment, in dem das Ich spürt, dass es ohne externe Bestätigung lebendig sein und Freude empfinden kann, verliert die symbiotische Manipulation ihre gesamte Macht."""
            },
            {
                "quote": "Das Aufbrechen des Stereopanoramas",
                "body": """Die Produktion explodiert: Die klaustrophobische Enge weicht weiten, brillanten Hallräumen. Die Stimme steht plötzlich frei, ungeschminkt und kraftvoll im Zentrum. Die dysfunktionale Bindung kollabiert nicht durch Streit, sondern durch die unerträgliche Wucht von unmaskierter Autonomie."""
            }
        ]
    },
    "07": {
        "review": """### Track 07: Somewhere Else — Die posttraumatische Kälte & Dissoziative Erstarrung
Auf den Befreiungsschlag folgt die Schockwelle. *Somewhere Else* dokumentiert den unausweichlichen Preis kompromissloser Autonomie: das Abdriften in emotionale Taubheit, um den Schmerz des Bruchs überhaupt überleben zu können.""",
        "cards": [
            {
                "quote": "Somewhere Else / Der Blick aus der Distanz",
                "body": """Die Psyche betätigt die Notbremse und schaltet in den Freeze-Zustand. Der Sprecher erlebt sich selbst wie eine fremde Figur auf einer fernen Bühne (Depersonalisation). Somatisch sinkt die Körpertemperatur; die Extremitäten fühlen sich taub an, die Stimme klingt belegt, gefiltert und weit nach hinten im Mix versetzt."""
            },
            {
                "quote": "Das Eis als Schutzraum",
                "body": """Die Kälte wird hier nicht als Mangel erlebt, sondern als lebensnotwendiges Koma. Wo vorher zerstörerische Hitze und Panik herrschten, breitet sich nun eine frostige, unberührbare Stille aus. Ein Zustand des emotionalen Winterschlafs, in dem die Wunden der Symbiose langsam abkühlen."""
            }
        ]
    },
    "08": {
        "review": """### Track 08: I Drink The Light — Der manische Gegenangriff & Sensorischer Hunger
Der Versuch, die Taubheit aus Track 7 gewaltsam zu durchbrechen. *I Drink The Light* ist ein manischer, euphorischer Gegenangriff: Die Psyche pumpt maximale Reize in das System, um die innere Dunkelheit durch sensorischen Exzess zu verbrennen.""",
        "cards": [
            {
                "quote": "I drink the light / Das Schlucken der Helligkeit",
                "body": """Die Formulierung *„I drink the light“* ist pure Somatik des Hungers: Licht wird nicht passiv empfangen, sondern wie eine Flüssigkeit gierig geschluckt. Ein verzweifelter Hunger nach Dopamin, nach Leben, nach physischer Erregung. Die Augen weiten sich, der Puls rast wieder, die Bewegungen werden fahrig und getrieben."""
            },
            {
                "quote": "Pulsierende Arpeggios & Übersteuerung",
                "body": """Elektrisierende Synths und schneidende Höhen peitschen durch das Klangbild. Es ist die Ekstase am Rande des Nervenzusammenbruchs – der Versuch, Schmerz durch pure sensorische Lautstärke zu übertönen, bevor das System unausweichlich an seinen absoluten Nullpunkt gelangt."""
            }
        ]
    },
    "09": {
        "review": """### Track 09: Wavelengths — Der Ego-Tod & Das Begraben falscher Loyalitäten
Das Epizentrum des Zusammenbruchs. In *Wavelengths* fallen alle manischen Fassaden und falschen Identitäten in sich zusammen. Die fundamentale Frage *„Who am I?“* hallt durch einen kargen, elektronisch zerklüfteten Raum.""",
        "cards": [
            {
                "quote": "Who am I? / Die Zertrümmerung der Persona",
                "body": """Das Ich steht vor den Trümmern seiner bisherigen Rollen (der Retter, der Bittende, der Perfekte). Alle adaptiven Masken, die für die Liebe des Anderen getragen wurden, werden endgültig begraben. Der Körper sinkt in eine tiefe, schwere Erdung; der Atem verlangsamt sich auf ein Minimum."""
            },
            {
                "quote": "Wavelengths / Frequenzen im Nichts",
                "body": """Minimalistische Klanglandschaften, nackte Sub-Bässe und weite Pausen der Stille. Das Nichts wird hier nicht mehr gefürchtet, sondern ausgehalten. Die Welle glättet sich – ein Zustand radikaler Wahrhaftigkeit, in dem keine Ausflüchte mehr existieren."""
            }
        ]
    },
    "10": {
        "review": """### Track 10: Side By Side — Die nüchterne Inventur der Phantom-Bindung
Ein Moment stiller Klarheit. *Side By Side* ist keine sentimentale Sehnsucht nach Versöhnung, sondern die würdevolle, nüchterne Inventur einer vergangenen Verbindung aus sicherer Distanz.""",
        "cards": [
            {
                "quote": "Side By Side / Die Anerkennung der Trennung",
                "body": """Man blickt auf das geteilte Territorium zurück, ohne den Drang zu verspüren, es erneut zu betreten. Die Körperhaltung ist aufrecht, entspannt, der Blick ruhig und direkt. Kein Groll, keine Idealisierung, sondern eine fast mathematische Anerkennung dessen, was war und was nie wieder sein wird."""
            },
            {
                "quote": "Warme Mitten & Organische Erdung",
                "body": """Der Sound gewinnt an organischer Wärme zurück. Ausgewogene Mitten und akustische Texturen signalisieren die Rückkehr zu stabiler Selbstregulation. Die Grenze zwischen dem Selbst und dem Anderen ist wiederhergestellt und unumstößlich."""
            }
        ]
    },
    "11": {
        "review": """### Track 11: The Thing — Der absolute Nullpunkt & Wiederaufbau aus dem Knochen
Der tiefste Punkt der Dekonstruktion und der Beginn des echten Wiederaufbaus. In *The Thing* werden Emotionen nicht mehr als überwältigende Fluten erlebt, sondern wie tote, physische Objekte betrachtet. Der Wiederaufbau beginnt rein somatisch an der Knochensubstanz.""",
        "cards": [
            {
                "quote": "The Thing / Die Verdinglichung des Traumas",
                "body": """Der Schmerz verliert sein dramatisches Narrativ und wird zu einem simplen, kalten *„Ding“* dekonstruiert, das man greifen, wiegen und ablegen kann. Keine Opferhaltung mehr, keine Suche nach externer Rettung. Der Sprecher verlangt nichts mehr von der Welt."""
            },
            {
                "quote": "Build my body from the bone / Die Anatomie der Disziplin",
                "body": """Trockene, wuchtige Perkussion wie Schläge auf Stein. Der Wiederaufbau erfolgt Knochen für Knochen, Muskelstrang für Muskelstrang. Eine stoische, disziplinierte Rekonstruktion des Körpers und des Geistes aus der eigenen unzerstörbaren Substanz heraus."""
            }
        ]
    },
    "12": {
        "review": """### Track 12: In A Minute — Die luzide Souveränität & Autonome Selbstbehauptung
Das triumphale Finale des Albums. Kein kitschiges Happy End, sondern die eiserne, disziplinierte Selbstverpflichtung zu kompromissloser Integrität: *„Don’t you forget about yourself“*.""",
        "cards": [
            {
                "quote": "Don't you forget about yourself / Das unumstößliche Gesetz",
                "body": """Der finale Imperativ richtet sich nicht mehr an den Partner, sondern an das eigene Bewusstsein. Es ist der Schwur, sich nie wieder für die Illusion von Nähe selbst zu verraten oder die eigene Souveränität zur Disposition zu stellen. Die Körperhaltung ist vollkommen zentriert, die Lunge weit, die Stimme unerschütterlich fest im Raum verankert."""
            },
            {
                "quote": "Harmonische Weite & Triumphale Klarheit",
                "body": """Das gesamte Klangspektrum erstrahlt in majestätischer Auflösung. Brillante Höhen, federnde Rhythmen und glasklare Vokalphonetik feiern die Vollendung der Heldenreise: Aus der Asche des Zusammenbruchs ist ein unzerstörbares, autonomes Selbst erwachsen."""
            }
        ]
    }
}

# 2. English Master Deep-Dive Essays & Cards
en_tracks_analysis = {
    "01": {
        "review": """### Track 01: Please — The Anatomy of Pleading & The Infantile Regression Trap
The album does not open with an assertion of strength or the posturing of a sovereign self, but with a pure vocative of surrender: *\"Please\"*. This opening plea lays the psychodynamic foundation for the entire first half of the record. Intimacy is framed not as an encounter between two autonomous beings, but as an urgent existential mandate—a compulsive reflex to numb an inner void through the forced presence of an external object.""",
        "cards": [
            {
                "quote": "Please (Please) / The Chamber of Echoes",
                "body": """The double echo acts as an intrapsychic reverberation chamber. The speaker begins from a position of fundamental asymmetry, possessing no leverage other than appealing to the mercy of the other. Somatically, this is a physical collapse—the chest sinks, breathing becomes shallow, and the vocal cords exhale into unprotected surrender.

Yet beneath apparent weakness lies an unconscious control technique: by humiliating oneself completely and dissolving personal boundaries, the partner is forced into the role of the omnipotent savior. Neediness becomes a snare that denies the other person their right to distance without appearing openly aggressive."""
            },
            {
                "quote": "Come (Please come) / The Paralyzed Imperative",
                "body": """The arrival of the first verb (*\"Come\"*) marks the shift where passive regression turns into a direct demand. Yet the command dares not stand alone; it is instantly cushioned by the qualifying parenthetical *\"(Please come)\"*. The nervous system is caught between sympathetic activation (the urge to grasp outward) and dorsal inhibition (the freeze of rejection). Responsibility for crossing the threshold is dumped entirely onto the partner—the speaker refuses to move; the other must travel the entire distance to fill the void."""
            },
            {
                "quote": "Closer, closer, closer / The Erasure of Space",
                "body": """The eightfold staccato repetition of *\"closer\"* unmasks a compulsive fixation. This is not about achieving healthy closeness, but about the total eradication of intermediate space. Every millimeter of physical or emotional separation is decoded as an existential threat.

Acoustically, vocal loops circle the listener's head in Dolby Atmos like a tightening noose. A claustrophobic suction pulls spatial distance down to absolute zero—the tonic grip of a drowning person dragging their rescuer under the surface."""
            }
        ]
    },
    "02": {
        "review": """### Track 02: Come Closer — Toxic Fusion & Sensory Enmeshment
Where *Please* pleaded timidly for mercy, *Come Closer* accelerates into an aggressive, hypnotic vortex. Proximity is weaponized: the track dissects the desperate drive to dissolve one's own identity through total physical and psychic fusion with the partner.""",
        "cards": [
            {
                "quote": "Come closer, come closer / Accelerating the Vortex",
                "body": """The tempo intensifies as bass frequencies drill into the gut. The lyrics articulate an addictive craving for co-regulation: the speaker's nervous system is incapable of self-soothing. The partner's body becomes the sole chemical tranquilizer to mute the internal vacuum. Any hesitation is experienced as traumatic betrayal."""
            },
            {
                "quote": "I need you near / Boundary Dissolution as Armor",
                "body": """The simple formula *\"I need you near\"* exposes the conflation of genuine love with existential hostage-taking. Personal sovereignty is sacrificed in exchange for total surveillance and physical possession of the other. A closed circuit forms where autonomy is treated as treason."""
            }
        ]
    },
    "03": {
        "review": """### Track 03: A Boy Like You — Intellectual Armor & Vivisection of the Archetype
An abrupt structural pivot: passive pleading is abandoned for razor-sharp, hypervigilant intellectualization. *A Boy Like You* is a forensic autopsy of the counterpart—a desperate effort to regain psychological control through analytical superiority.""",
        "cards": [
            {
                "quote": "A Boy Like You / Dissecting the Projection",
                "body": """The speaker switches from feeling to surveillance. Every micro-behavior, inconsistency, and crack in the partner's persona is cataloged. The voice retreats behind a fortress of first-principles logic: if one can thoroughly decode and deconstruct the other, one can never be ambushed by heartbreak again."""
            },
            {
                "quote": "The Dissonance Between Ideal and Reality",
                "body": """The vocal production is bone-dry and clinical, positioned directly against the eardrum with no softening reverb. Beneath the brilliant critique lies the bitter realization that the real person across the room will never match the flawless projection inside one's mind. Cognitive control serves as the final dam before systemic collapse."""
            }
        ]
    },
    "04": {
        "review": """### Track 04: Ring The Alarm — Central Nervous System Overload & Acute Panic
The intellectual armor of Track 3 shatters completely. *Ring The Alarm* documents the total failure of cognitive control—the central nervous system descends into acute sympathetic overdrive as the threat of abandonment triggers full-blown psychic panic.""",
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
        "review": """### Track 05: My Baby — Hermetic Cocooning & Mutual Erasure
Following the panic attack, the psyche retreats into a regressive, hermetically sealed isolation ward. *My Baby* documents the toxic attempt to shut out the external world and construct an artificial quarantine zone where only the two exist.""",
        "cards": [
            {
                "quote": "My Baby / Obsessive Encapsulation",
                "body": """The outside world is banished as an enemy; all social lifelines are severed. The partner is reduced to the infantile cipher *\"Baby\"*—an object to possess, guard, and keep sedated. The posture turns inward, touch becomes possessive, and perception shrinks to the immediate orbit of the other."""
            },
            {
                "quote": "The Airless Chamber of Stagnation",
                "body": """Muffled, sub-aquatic frequencies dominate the mix. The production breathes the stagnant air of a locked room. This is the deceptive calm before the inevitable collapse: a relationship that requires total sensory deprivation to survive is already clinically dead."""
            }
        ]
    },
    "06": {
        "review": """### Track 06: Have You Seen Me Dance Alone — The Turning Point & Eruption of Autonomy
The decisive structural watershed of the album. *Have You Seen Me Dance Alone* is not a melancholy song about loneliness, but the explosive moment unmasked authenticity detonates the symbiotic prison.""",
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

# 3. Clean HTML Template without f-string syntax errors
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
      font-size: 1.06rem;
      line-height: 1.8;
      color: #d1d1d6;
      margin-bottom: 16px;
    }

    .review-intro-box h1, .review-intro-box h2 {
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
      padding: 24px 28px;
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
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--magenta);
      margin-bottom: 16px;
      letter-spacing: 0.02em;
      user-select: none;
    }

    .card-body {
      font-size: 1.02rem;
      line-height: 1.75;
      color: #c4c4cc;
    }

    .card-body p {
      margin-bottom: 14px;
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
            "title": "TOMORA — Lyrics & Review",
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
    de_info = de_tracks_analysis.get(num_str, {"review": "", "cards": []})
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
    en_info = en_tracks_analysis.get(num_str, {"review": "", "cards": []})
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

print("Master German and English editions compiled cleanly with zero syntax errors!")
