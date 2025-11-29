# EOG Project

## Description

Extraction d'Objets Géographiques (EOG)
Outil pour extraire des objets géographiques d'une image ou d'un raster (en couleur). Il est indispensable d'avoir installé la boite à outil Orfeo Tool Box (OTB) pour faire fonctionner l'outil. Précisez les couches de sortie dans un répertoire afin que le processus se déroule bien. Pour l'étape 2 il suffit à l'utilisateur de sélectionner dans la couche vecteur (résultat de la segmentation) les objets qu'il souhaite extraire. L'outil créera une couche géographique de ces objets. L'étape 3 est un nettoyage de la couche résultante, testez différents paramétrages pour le rendu que vous souhaitez. 

## Fonctionnalités

- segmentation d'une image  
- typologie dynamiquepar moyenne des écarts normalisés
- nettoyage géométrique et topologique avec simplification et lissage

## Installation

-installer le .zip sous qgis dans le menu "extension"
-installer depuis un ZIP

## Utilisation

1. Etape 1 : précisez dans le menu le raster sur lequel vous souhaitez travailler  / Précisez le répertoir de sortie de la couche vecteur
2. Etape 2 : ouvrez le .shp de l'image vectorisée et faite une sélection des objets que vous souhaitez extraire : attention si vos objets ont des différences de contraste, de colorimétrie, bien sélectionner plusieurs objets, ils serviront d'échantillon. Vous pouvez jouer sur le seuil de typologie en fonction de la qualité de votre raster. Précisez le dossier de sortie de votre couche d'objets.
3. Etape 3 : une fois ce travail effectué vous pouvez nettoyer la couche SIG résultante pour éviter les problèmes géométriques et topologiques, jouez sur la tolérance de simplification, les itérations de lissage en fonction de ce que vous recherchez. Précisez le dossier de sortie de votre couche SIG d'objets. Il ne vous reste plus qu'à compléter la table attributaire à votre convenance.


## Prérequis

-Orfeo ToolBox : https://www.orfeo-toolbox.org/download/

## Contribution

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou soumettre une pull request.

## Licence

GPL v2

## Contact

Pour toute question, contactez dioupa@gmail.com
