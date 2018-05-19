# Grammalecte
A plugin to use Grammalecte in Sublime Text

![screenshot from 2018-05-10 21-18-10](https://user-images.githubusercontent.com/22014799/39889307-d02186c0-5497-11e8-9168-0bdbe175ee04.png)


## Installation 

### Package Control

Dans la palette de commande : __Install package__ > __Grammalecte__

### Manuellement

Ou télécharger le dernier package à partir de l'onglet "Releases" du dépôt.

## Utilisation

Dans n’importe quel document, __Clic droit__ > __Run Grammalecte__. Après quelques instants, les erreurs grammaticales détectées par Grammalecte apparaissent encadrées.  
Un clic droit sur l’une d’elles permettra d’afficher le menu contextuel du quel vous pourrez appliquer une suggestion de la correction.

Pour arrêter l’affichage des erreurs : __Clic droit__ > __Clear Grammalecte__.

Le menu contextuel permet aussi de corriger par lot certaines erreurs communes ou toutes les erreurs d’un même type.

![screenshot from 2018-05-10 21-26-11](https://user-images.githubusercontent.com/22014799/39889677-d163fc74-5498-11e8-9505-8ea5adc88021.png)


## Caveats

Le plugin ne supporte pas :
- Les __UNDO / REDO / CTRL+Z / CTRL+Y__
- Les erreurs orthographiques
- L’affichage de plus de une suggestion de correction
- Les erreurs superposées

Ce plu-gin est expérimental et pourrait causer des __pertes de données__.

## Contribution

Cloner ce dépôt et pousser vos modifications !

## Licence

Ce plug-in communautaire n’est pas affilié à Grammalecte.

Ce plug-in est sous licence MIT reproduite ci-dessous.

Grammalecte est sur licence GNU/GPL, reproduite dans ce dépôt.

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
