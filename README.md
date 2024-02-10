# AES_Python_Implementation

## Rappel

Le chiffrement AES est un système d'encodage/codage de messages qui utilise une clé de chiffrement de 128 bits, 192 bits ou 256 bits. Il est utilisé pour protéger les informations sensibles et est largement utilisé dans les systèmes de sécurité et de protection des données.
Pour ce td nous n'allons utilisé qu'une clé de 128 bits

## Sommaire

> 1.  [Introduction](#introduction)
> 2.  [Installation](#Installation)
> 3.  [Fonctionnement + Explication du code](#Fonctionnement)
# Introduction

## Architecture du code

```
$Racine du projet
├── constants.py     # Contient les constantes
├── functions.py     # Contient les fonctions (étapes)
├── main.py          # Contient le code principal
└── README.md        # CR et explications
```

## Explication de toutes les étapes du AES

1. **SubBytes** : Substitution des octets de l'état par des octets de la S-Box.
2. **ShiftRows** : Décalage des lignes de l'état.
3. **MixColumns** : Mélange des colonnes de l'état.
4. **Key Expansion**: Génération de clés pour chaque round
5. **AddRoundKey** : Clé de tour XOR.

# Installation

1. Installer python -> Ajouter python au PATH (Variable d'environnement)
2. Ouvrir votre terminal de commandes et rentrer la commande suivant qui va permettre d'installer les dépendances pour que le projet se lance

```
pip install numpy
```

3. Ensuite aller dans le repértoire du projet et lancer le projet en écrivant dans votre terminal de commande

```
python3 main.py
```

Le code se découpe en 2 fichiers un fichier main qui contient l'entiereté de l'encodage et le fichier functions qui contient toutes les fonctions que l'on va appeler dans notre main pour garder une bonne visibilité de code.

# Fonctionnement

## **Initialisation des variables **

```
message = np.array(
        [
            0x00, 0x10, 0x20,  0x30, 0x40,   0x50,  0x60,   0x70,   0x80,      0x90,  0xA0,   0xB0,    0xC0,      0xD0,    0xE0,   0xF0,
        ]
    )
    key = np.array(
        [
            0xD6,0xAA,0x74,0xFD,0xD2,0xAF,0x72,0xFA,0xDA,0xA6,0x78,0xF1,0xD6,0xAB,0x76, 0xFE,
        ]
    )
```

## **Chiffrement par Bloc**

Chaque case ici représente un octet. Par la suite, les opérations du chiffrement et du déchiffrement se font octet par octet.
De base notre vecteur de test est Flat et ici on va passer sur des matrices de dimensions 2 de taille 4x4
![image](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/91aaa7d8-8518-49d2-add9-62da6aa8c1a0)

Pour ce faire j'ai utilisé cette fonction :
![image](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/a2679615-6a3e-4571-ae1a-6d2a288cfe3c)

Découpage par rapport à la taille de notre matrice :

```python
message_2d = [message[i : i + 4] for i in range(0, len(message), 4)]
```

Permet d'appliquer une transposition à notre matrice pour l'avoir sous le même format que durant le td

```python
  message_2d = np.array(list(zip(*message_2d)))
```

## **SubBytes** : Substitution des octets de l'état par des octets de la S-Box.

Ici on va prendre notre message sous forme de matrice à la sortie de notre fonction chiffrement par bloc. A cette matrice on va séparer le bit de poids fort et le bit de poids et trouver l'octet correspondant en se basant sur la s-box:
![image](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/da2de4af-c86a-40c4-af7b-fe85451b33dd)

Pour ce faire en python avec numpy j'ai fait cette fonction avec un sbox représenté par un vecteur :
![image](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/8762ebb0-7c05-4fb9-a263-9fce10a782e2)

```python
    message_subytes = np.array([[Sbox[byte] for byte in row] for row in message_2d])
```

Le code prend chaque byte du message original (parcourant d'abord chaque ligne avec for row in message_2d, puis chaque byte (chaque colonne de notre tableau2d) dans ces lignes avec for byte in row), et le remplace par un autre byte selon la S-box (Sbox[byte]). Cela se fait pour chaque byte du message initial.

## **ShiftRows** : Décalage des lignes de l'état.

Ici le but va être de décaler chaque bloc contenant un byte après notre étape de SubBytes
![image](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/51482485-f74f-43d7-8f2c-da446a9277a0)
Pour ce faire on va juste calculer les nouvelles position par rapport à notre matrice de base
![image](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/26d22d4e-c002-4c6b-b883-485dde498d32)

- La première rangée (index 0) n'est pas décalée.
- La deuxième rangée (index 1) est décalée d'une position vers la gauche.
- La troisième rangée (index 2) est décalée de deux positions vers la gauche.
- La quatrième rangée (index 3) est décalée de trois positions vers la gauche.
  Ce décalage signifie que, par exemple, si une rangée est [a, b, c, d] et qu'elle doit être décalée de deux positions, elle deviendra [c, d, a, b].
  Pour réussir à faire en sorte que si l'index d'un des bloc est trop grand > 4 on va utiliser np.roll qui une fois au dela des limite d'indexage de notre array va redonner l'index 0.

## **MixColumns** :

### Multiplication dans GF(2^8)

La fonction multiply_in_gf(a, b) multiplie deux nombres a et b dans GF(2^8). La multiplication se fait bit par bit, avec une attention particulière aux débordements (quand le bit le plus significatif est 1 avant le décalage). L'opération principale est le XOR (^), qui remplace l'addition et la soustraction dans GF(2^n).

![image](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/e6403f85-e9af-40d2-a978-ed68e30ac36c)

Décalage et XOR: Le décalage à gauche de a et le décalage à droite de b servent à simuler la multiplication des polynômes. Le XOR simule l'addition/soustraction de polynômes.
Condition : Si le bit le plus significatif de a est à 1 avant le décalage, cela signifie que le polynôme résultant dépasserait le degré 7, donc on fait un XOR avec 0x1B pour effectuer la réduction modulo le polynôme irréductible.
MixColumns dans AES

On va donc itérer sur tout les bits de nos bytes, dans un premier temps on va checker si le bit de poids faible de b est 1, si oui alors on fait un XOR entre a et le resultat qui de base est init à 0. Ensute on regarde si le bit de poids fort de a est = 1, en parralèle on on décale a d'un bit vers la gauche et si le bid de poids fort était 1 on faut un XOR entre le résultat et 0x1B qui est le polynome irréductible.
Pour finir on décale b d'un bit vers la droite.

![image](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/d5605de2-acc5-4298-b00b-a61af55c7da7)

La matrice mix_column_matrix contient des coefficients spécifiques qui sont appliqués à chaque colonne de la matrice de l'état (ici représentée par message_shifted).

Opération de matrice: Pour chaque élément de la nouvelle matrice (message_mixed), on calcule la somme (XOR) des multiplications dans GF(2^8) de chaque élément de la ligne correspondante de la matrice mix_column_matrix par chaque élément de la colonne correspondante de message_shifted.

#### Initialisation de message_mixed:

On crée une nouvelle matrice de même taille que message_shifted, initialisée à zéro. Cette matrice stockera le résultat.

#### Boucles imbriquées sur les colonnes et les rangées:

On parcourt chaque colonne et chaque rangée de la matrice. Pour chaque élément, on effectue une opération spécifique de mélange qui implique la multiplication dans le champ de Galois.

#### Accumulation des résultats:

Pour chaque élément, on accumule les résultats des multiplications entre les éléments de la matrice mix_column_matrix (non montrée ici, mais c'est une matrice prédéfinie utilisée dans AES pour le mélange) et les éléments correspondants de message_shifted. Ces multiplications sont effectuées via la fonction multiply_in_gf.

#### Stockage du résultat:

Le résultat de ces opérations est stocké dans message_mixed.

## **Key Expansion** :


### Fonction subWord
![code1](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/b17d4015-c904-4eb8-a889-fadf22c4e38c)
Pour chaque byte du mot, elle cherche la correspondance la matrice Sbox.


### Fonction rotWord
![code1](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/a52685cb-34f7-4498-b90a-4b5d7baf4837)
On décale notre mot d'un index sur la gauche
Si le mot était "abcd", après l'application de rotWord, il deviendrait "bcda"

### Fonction keyExpansion
![code1](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/d1cf2976-ee8b-4665-9702-7f675fb96acb)
On prend la clé et prépare une version étendue de cette clé (10 nouvelle clés dans notre cas)
On créer une matrice appelée W, qui sera remplie avec des versions transformées de la clé originale.
Les premières parties de cette matrice sont directement remplies avec la clé originale.
Ensuite, pour chaque "mot" suivant dans la matrice, va effectuer une série d'opérations (rotword, subword, et un XOR avec la matrice rcon) pour générer de nouveaux mots à partir des précédents.

## **Add Round Key** :
![code1](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/f92fe25f-a179-4582-b577-7b60f085b83e)
L'add round key est un étape supplémentaire ou nous allons simplement faire un XOR entre notre message de base après avoir subit quelques transformations et la clé correspondante (clé en sortie du key expansion avec l'index de notre round actuel)
