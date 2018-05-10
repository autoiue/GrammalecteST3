# GrammalectST3
A plugin to use Grammalecte in Sublime Text

![screenshot from 2018-05-10 21-18-10](https://user-images.githubusercontent.com/22014799/39889307-d02186c0-5497-11e8-9168-0bdbe175ee04.png)

## Attention !

Ce plugin est expérimental et pourrait causer des __pertes de données__.

## Installation 

GrammalecteST3 requiert que `grammalecte-cli.py` soit dans le chemin système. Le plus facile est d’installer Grammalecte CLI&Serveur à partir de https://www.dicollecte.org/?download_div et d’exécuter `setup.py install` avec les droits administrateurs.

Ensuite, cloner ce dépot git dans le répertoire de packages de Sublime Text : __Préférences__ > __Browse packages…__ puis `git clone https://github.com/procsynth/GrammalecteST3` dans ce dossier.

Ce plugin n’est pas actuellement disponible via Package Control (à venir).

## Utilisation

Dans n’importe quel document, __Clic droit__ > __Run Grammalecte__. Après quelques instants, les erreurs grammaticales détectées par Grammalecte apparaissent encadrées.  
Un clic droit sur l’une d’elles permettra d’afficher le menu contextuel du quel vous pourrez appliquer une suggestion de la correction.

L’affichage des erreurs ne se met pas à jour de manière dynamique (à venir) il faut relancer Grammalecte pour l’actualiser : __Clic droit__ > __Rerun Grammalecte__.

Pour désactiver l’affichage : __Clic droit__ > __Clear Grammalecte__.

Le menu contextuel permet aussi de corriger par lot certaines erreurs communes ou toutes les erreurs d’un même type.

![screenshot from 2018-05-10 21-26-11](https://user-images.githubusercontent.com/22014799/39889677-d163fc74-5498-11e8-9505-8ea5adc88021.png)


## Caveats

Le plugin ne supporte pas :
- Les __UNDO / REDO / CTRL+Z / CTRL+Y__
- Les erreurs orthographiques
- La mise à jour dynamique des l’affichage des erreurs
- L’affichage de plus de une suggestion de correction
- Les erreurs superposées
- La configuration via les fichiers de configuration de Sublime Text
- Sublime Text 2

Ce plugin est expérimental et pourrait causer des __pertes de données__.

## Contribution

Cloner ce dépot et pousser vos modifications !

## Licence

Ce plugin communautaire n’est pas affilié à Grammalecte.

Ce plugin est sous license MIT reproduite ci-dessous.

Ce plugin est expérimental et pourrait causer des __pertes de données__.

MIT License

Copyright (c) 2018 Antoine Pintout

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions :

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
