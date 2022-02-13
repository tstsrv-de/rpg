# Letzte Aufgaben

## Offene Punkte

./.

## Zurückgestellt (= nicht mehr machen)

- Schriftart der Gamelog-Box / Intro-Text-Box ändern

## Wer macht was bis wann?

### Julian

- Worldmap zeichnen und einbauen >> Freitag

- Trainigslevel Bilder zeichnen einbauen >> Freitag
- Friedhof Grafiken zeichnen (Prio) >> Sonntag, 16 Uhr

- Julian Doku Kapitel >> Bis Samstag
  - Frontend
  - Grafiken

- Reflektionen schreiben >> Bis Samstag

- Henning Scan von deiner Unterschrift und die Matrikelnummer schicken (haenno@web.de) >> Asap

### Henning

- Datenbank zurücksetzten (User, Chars und Games löschen) >> Sonntag, 16 Uhr

- Unterschriften und Matrikelnummern in Doku einpflegen (lokal! nicht im Git) >> Bitte asap, spätestens Samstag

- Henning Doku Kapitel *Code-Entwicklung*: >> Freitag
  - Rundenlogik
  - Websockets

### Rico >> Bitte selbst einmal drüber schauen und Zeiten planen *yay

- Reflektionen schreiben << Samstag

- Henning Scan von deiner Unterschrift und die Matrikelnummer schicken (haenno@web.de) << done

- Traingslevel Texte und Werte anpassen << done, nur noch nicht committet

- Texte für Home-Seite (in Zustand an- und abgemeldet) << done, nur noch nicht committet

- Welcome-Texte müssen für alle Level noch geupdatet werden. << done

### Gemeinsam

- Trainingslevel gemeinsam testen >> Samstag 16 Uhr

- Kommentare und ToDos im Code rausnehmen >> Sonntag, 14 Uhr

- Durchlesen, korrigieren >> Sonntag, 14 Uhr

- Texte von Rico mit Formatierungen (fett, krusiv, unterstreichungen... ) auflockern (Wall-of-Text) >> Sonntag, 14 Uhr

- Anhang: Bildbeschreibungen anpassen und ggfls. aussortieren >> Sonntag, 14 Uhr

- Impressum/Credits geben/Lizenz
  - RPG-Gui
  - Chat-Howto
  - Traefik Server

### Backup des Dojo Levels

```json
  {
    "model": "rjh_rpg.gamescenes",
    "pk": 6,
    "fields": {
      "name": "🧸 Monsterjäger-Dojo",
      "req_players": 3,
      "welcome_text": "Hier wird niemand sterben. Zumindest ist hier bis jetzt noch niemand gestorben!<br><br>",
      "boss_welcome_text": "Schlag mich!",
      "enemy_name": "🎯 Trainigsziel 🎯",
      "enemy_hp": 1000,
      "enemy_ap": 1,
      "enemy_image": "training_dummy.mp4",
      "enemy_dead_image": "dojo_background.jpeg",
      "intro_image": "dojo_intro.jpg",
      "intro_text":"„Es tut nicht weh. Keine Angst.“ Genau das hat euer Trainer immer gesagt als er euch durch den Trainingsparcours gescheucht hat. Ihr habt es gehasst, denn natürlich tat es weh, als er mit euch trainiert hat. Immer wenn ihr eure Deckung vernachlässigt habt, hat er es euch schmerzhaft spüren lassen. Und selbstverständlich seid ihr ihm dankbar für diese Lektionen, denn sie haben euch bis heute am Leben gehalten. <br>Heute wird es allerdings anders sein, denn ihr seid nur hier, um ein paar neue Techniken an der Trainingspuppe zu testen!",
      "win_text": "Holla! Das war nicht überraschend. Aber dass die Trainingspuppe nach eurem letzten sauberen Hieb in ihre Einzelteile zerfällt, das hattet ihr nicht erwartet.",
      "gameover_text": "Oh, da muss die Trainingspuppe locker gewesen sein. Durch einen eurer heftigen Schläge muss sie sich gedreht und euch unglücklich am Kopf getroffen haben."
    }
  },
```
