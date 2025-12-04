Cahier des charges — Tower-Defense 2D (PC, Python) avec module idle
1. Vue d'ensemble

Jeu 2D PC (Python). Partie solo, durée max 15 minutes. Mécanique principale : tower-defense autour d’un fournil central (production/stockage de pain pour nourrir les troupes). Ajout d’un module idle : ressources gagnées sur les vagues permettent achats/améliorations persistantes entre parties (ou progressives pendant la partie si design le permet).

2. Objectifs de la partie

Défendre le fournil pendant 15 minutes.

Si après 15 min des vagues restent vivantes → Game Over.

Calcul des récompenses à la fin : total mobs tués et ressources collectées (exp, or, chair, pain).

3. Difficulté & rythme des vagues

Trois niveaux (choix avant début de partie) :

Facile : 1 vague toutes les 2 minutes (soit ~7 vagues en 15min).

Moyen : 1 vague par minute (15 vagues).

Difficile : 2 vagues par minute (30 vagues).

Chaque vague contient un ensemble de mobs dont la quantité et stats augmentent avec l’indice de vague.

4. Map & UI

Vue 2D top-down (ou orthographique).

FourniL au centre (bâtiment cliquable pour upgrades).

Rempart gardant le fournil (anneau autour).

Zones de spawn ennemis aux bords.

HUD : temps restant, vague courante, ressources (exp, or, chair, pain), barre vie du fournil et du rempart, boutons d’amélioration.

5. Ressources

exp

or

chair (chair a mob)

pain

Les mobs dropent or/exp/chair/pain selon type (probabilités réglables). Ces ressources servent pour upgrades (fournil, rempart, troupes).

6. FourniL — stats & mécanique

Quatre stats modifiables via upgrades (coûts en or/chair) :

Production de pain (par minute) — peut produire un % de la capacité de place disponible. Augmentable via or.

Capacité de stockage de pain (max pain) — augmente via or et chair.

Vitesse de production (temps par pain).

Vie (hitpoints) — le fournil est protégé par le rempart ; si rempart tombe, le fournil reçoit des dégâts. Reset à chaque partie.

Remarques :

Si pas assez de pain, les troupes subissent une pénalité : perte de stamina / réduction de DPS.

Le fournil produit pain automatiquement (idle). Le joueur peut améliorer pour augmenter production ou capacité.

7. Rempart — stats & enchantements

Résistance (vie) : points de vie. Doit être attaqué X fois pour tomber. Reset à chaque partie.

Enchantements : deux types (à débloquer puis améliorer) ; nombre d’emplacements d’enchantement augmentable.

Épine : renvoie une portion des dégâts subis (réflexion).

Barrier : au début de la vague, active une protection pour le rempart pendant 5 à 15 secondes (durée améliorable).

Notes : Enchantements doivent être débloqués avant d’y placer des améliorations.

8. Troupes — types & stats

Quatre types :

Épéiste : corps à corps.

Archer : attaque à distance (peut viser volants).

Nécromancien : invoque mobs morts (si au moins un mob est mort dans la partie). L’efficacité dépend de la stat force.

Assassin : attaque mêlée et à distance (hybride).

Stats communes pour chaque troupe :

Force : taux de dégâts. Augmentable via or et chair.

Stamina : endurance / capacité d’action ; améliorable via chair et pain.

Effets :

Si pain insuffisant → baisse de stamina → baisse de vitesse d’attaque/déplacement.

Nécromancien : ne peut pas invoquer si aucun cadavre disponible. Les invocations consomment chair (si on veut limiter).

9. Mobs — types et relations entre stats

Types principaux : rempant, volant, géant.

Règles de proportion (constantes) :

Le rempant a toujours +10% de vie par rapport au volant.

rempant_vie = volant_vie * 1.10

Le géant a toujours +40% de vie par rapport au rempant.

geant_vie = rempant_vie * 1.40

Le volant a toujours +20% de force par rapport au rempant.

volant_force = rempant_force * 1.20

Le géant a toujours +20% de force par rapport au volant.

geant_force = volant_force * 1.20

Exemple numérique (vague 1) donné :

Rempant : 15 PV, 20 force

Volant : 13.5 PV (15 / 1.10), 24 force (20 * 1.2)

Géant : 21 PV (15 * 1.4), 28.8 force (24 * 1.2)

Composition de vague (exemples) :

Vague 1 : 20 mobs — 15 rempant, 3 volants, 2 géants.

Vague 10 (exemple fourni) : 140 mobs — 60 rempant, 30 volants, 50 géants.

Évolution par vague : proposer une formule de scaling (ex. progression linéaire ou exponentielle) — voir section Formules.

10. Formules recommandées & exemples
10.1 Scaling du nombre de mobs

Exemple linéaire simple (paramétrable) :

base_count_per_wave = 20
growth_per_wave = 12   # nombre additionnel par vague
count_wave(n) = base_count_per_wave + (n-1) * growth_per_wave


Pour répartir les types, on peut utiliser des ratios variables par palier :

Ratio rempant : 0.6

Ratio volant : 0.2

Ratio géant : 0.2
(ajuster par vague)

10.2 Scaling des PV/Force

Soit base_vie_rempant(w) et base_force_rempant(w) qui augmentent par vague :

vie_rempant(w) = base_vie_rempant * (1 + 0.05*(w-1))   # +5% PV par vague
force_rempant(w)= base_force_rempant * (1 + 0.04*(w-1)) # +4% force par vague


Ensuite appliquer les multiplicateurs pour volant/géant comme vu en §9.

10.3 Exemple calcul (vague 1)

base_vie_rempant = 15, base_force_rempant = 20

volant_vie = 15 / 1.10 = 13.636... → arrondir selon besoin (13.6)

volant_force = 20 * 1.2 = 24

geant_vie = 15 * 1.4 = 21

geant_force = 24 * 1.2 = 28.8

10.4 Production & stockage du fournil

production_rate (pain/min) = base_prod * (1 + level_prod * prod_multiplier)

stockage_max = base_cap + level_cap * cap_increment + chair_bonus * k

coût d’upgrade = fonction exponentielle (ex : coût_or = floor(100 * 1.5^level))

11. Système d’upgrades & progression (idle)

Upgrades persistants (entre parties) : débloquables via or/exp/ chair.

Arbres d’upgrade :

FourniL : prod, capacité, vitesse, vie.

Rempart : vie, slots enchantement, niveau enchantement.

Troupes : force, stamina, coût d’entraînement.

Les enchantements sont débloqués avant d’être placés (système de slots).

12. Conditions de fin & récompenses

Victoire : défendre pendant 15min ET aucune vague restante à la fin.

Défaite : au bout de 15min il reste des mobs vivants.

Récompenses : total mobs tués, or obtenu, exp, chair, classement selon niveau de difficulté. Afficher un écran résumé.

13. UX / Contrôles / Interactions

Souris : sélectionner bâtiments, upgrades, recruter troupes.

Raccourcis clavier paramétrables.

Bouton pause, accélérer (x2 pour idle?) — attention à l’équilibrage.

Notifications : “Pain insuffisant → stamina réduite”.

14. Tech & assets recommandés (stack Python)

Framework graphique : Pygame (simple, bien pour protos 2D). Alternatives : pyglet, Godot (GDscript) si tu veux sortir de Python pur.

Structure projet : MVC ou ECS léger pour entités (mobs, troupes, bâtiments).

Sauvegarde : fichier JSON pour upgrades persistants.

Assets : sprites 2D (tuiles pour sol, icônes ressources, animations simples).

15. Livrables & critères d’acceptation

Prototype jouable en 2D (Pygame) : fournil central, rempart, spawns ennemis, vagues, troupes automatiques.

Systeme de production du pain + consommation par troupes.

Upgrades (au moins 6) achetables via or/chair.

Trois niveaux de difficulté, timer 15min, conditions de fin & écran résumé.

Documentation (README) : comment lancer, commandes clavier, formule d’upgrade.

Tests unitaires basiques pour fonctions de calcul (scaling vagues, calculs PV/force, coûts upgrades).

Critères QA

Les ratios PV/force respectent les règles définies (§9).

Au lancement, la vague 1 correspond aux exemples fournis.

Les ressources sont persistantes si prévu (idle upgrades).

Pas de crash à la fin de la partie.


Prompt type 

Prompt (FR) — Génère un prototype jouable en Python (Pygame) d’un tower-defense 2D conforme au cahier des charges suivant :

FourniL central (production/stockage de pain), rempart autour avec barre de vie et enchantements (Épine, Barrier).

Troupes automatiques (4 types : Épéiste, Archer, Nécromancien, Assassin) avec stats Force et Stamina. Consommation de pain influence la stamina.

Mobs (rempant, volant, géant) avec proportions et multipliers de vie/force définis : rempant_vie = volant_vie * 1.10 ; geant_vie = rempant_vie * 1.40 ; volant_force = rempant_force * 1.20 ; geant_force = volant_force * 1.20.

Trois difficultés (intervalle de vague : 120s, 60s, 30s). Partie max 15 minutes. Game Over si au bout de 15min il reste des mobs vivants.

Ressources : exp, or, chair, pain. Drops par mob. Upgrades (or/chair) pour fournil, rempart, troupes. Système idle : production de pain continue et upgrades persistants entre parties (sauvegarde JSON).

Interface de base (HUD) : temps, ressources, vie fournil/rempart, boutons upgrade/recrutement.

Fournir README et code clair: classes Entité/Mob/Troupe/Bâtiment, fonctions de scaling des vagues, exemples de paramètres initiaux.

Livrables : code Pygame exécutable, assets placeholders (rectangles/sprites), README, 5 tests unitaires pour calculs.



        A      B      C      D      E      F      G      H
      ---------------------------------------------------------
8  |       |       |       |       |       |       |       | SPAWN |
      ---------------------------------------------------------
7  |       |       |       |       |       |       |       |       |
      ---------------------------------------------------------
6  |   R   |   R   |   R   |       |       |       |       | SPAWN |
      ---------------------------------------------------------
5  |       | FOURN |   R   |       |       |       |       |       |
      ---------------------------------------------------------
4  |   R   |   R   |   R   |       |       |       |       |       |
      ---------------------------------------------------------
3  |       |       |       |       |       |       |       | SPAWN |
      ---------------------------------------------------------
2  | MENU  | MENU  | MENU  | MENU  | MENU  | MENU  | MENU  | MENU  |
      ---------------------------------------------------------
1  | MENU  | MENU  | MENU  | MENU  | MENU  | MENU  | MENU  | MENU  |
      ---------------------------------------------------------
FOURN = fournil 

R = rempart 

MENU = ligne de placement des troupes

SPAWN = points d’arrivée ennemis 