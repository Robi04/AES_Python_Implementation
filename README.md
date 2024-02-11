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

1. **[SubBytes](#SubBytes)** : Substitution des octets de l'état par des octets de la S-Box.
2. **[ShiftRows](#ShiftRows)** : Décalage des lignes de l'état.
3. **[MixColumns](#MixColumns)** : Mélange des colonnes de l'état.
4. **[KeyExpansion-](#KeyExpansion)**: Génération de clés pour chaque round
5. **[AddRoundKey](#AddRoundKey)** : Clé de tour XOR.

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

## **KeyExpansion** :


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

## **AddRoundKey** :
![code1](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/f92fe25f-a179-4582-b577-7b60f085b83e)

L'add round key est un étape supplémentaire ou nous allons simplement faire un XOR entre notre message de base après avoir subit quelques transformations et la clé correspondante (clé en sortie du key expansion avec l'index de notre round actuel)


## Cypher 
![code1](https://github.com/Robi04/AES_Python_Implementation/assets/63416313/d871a029-d26b-4faf-bce5-6d4565716dfa)
Finalement on applique le code cypher qui va être une suite de 10 rounds pour au final crypté notre message, pour cela j'ai simplement codé le pseudo code fournit


# Résultats
```
INIT addRoKey : ['00', '10', '20', '30', '40', '50', '60', '70', '80', '90', 'a0', 'b0', 'c0', 'd0', 'e0', 'f0']
1 subBytes :    ['63', 'ca', 'b7', '04', '09', '53', 'd0', '51', 'cd', '60', 'e0', 'e7', 'ba', '70', 'e1', '8c']
1 shiftRows :   ['63', '53', 'e0', '8c', '09', '60', 'e1', '04', 'cd', '70', 'b7', '51', 'ba', 'ca', 'd0', 'e7']
1 mixColumns :  ['5f', '72', '64', '15', '57', 'f5', 'bc', '92', 'f7', 'be', '3b', '29', '1d', 'b9', 'f9', '1a']
1 addRoundKey : ['d6', 'aa', '74', 'fd', 'd2', 'af', '72', 'fa', 'da', 'a6', '78', 'f1', 'd6', 'ab', '76', 'fe']
1 addRoundKey : ['89', 'd8', '10', 'e8', '85', '5a', 'ce', '68', '2d', '18', '43', 'd8', 'cb', '12', '8f', 'e4']
2 subBytes :    ['a7', '61', 'ca', '9b', '97', 'be', '8b', '45', 'd8', 'ad', '1a', '61', '1f', 'c9', '73', '69']
2 shiftRows :   ['a7', 'be', '1a', '69', '97', 'ad', '73', '9b', 'd8', 'c9', 'ca', '45', '1f', '61', '8b', '61']
2 mixColumns :  ['ff', '87', '96', '84', '31', 'd8', '6a', '51', '64', '51', '51', 'fa', '77', '3a', 'd0', '09']
2 addRoundKey : ['b6', '92', 'cf', '0b', '64', '3d', 'bd', 'f1', 'be', '9b', 'c5', '00', '68', '30', 'b3', 'fe']
2 addRoundKey : ['49', '15', '59', '8f', '55', 'e5', 'd7', 'a0', 'da', 'ca', '94', 'fa', '1f', '0a', '63', 'f7']
3 subBytes :    ['3b', '59', 'cb', '73', 'fc', 'd9', '0e', 'e0', '57', '74', '22', '2d', 'c0', '67', 'fb', '68']
3 shiftRows :   ['3b', 'd9', '22', '68', 'fc', '74', 'fb', '73', '57', '67', 'cb', 'e0', 'c0', '59', '0e', '2d']
3 mixColumns :  ['4c', '9c', '1e', '66', 'f7', '71', 'f0', '76', '2c', '3f', '86', '8e', '53', '4d', 'f2', '56']
3 addRoundKey : ['b6', 'ff', '74', '4e', 'd2', 'c2', 'c9', 'bf', '6c', '59', '0c', 'bf', '04', '69', 'bf', '41']
3 addRoundKey : ['fa', '63', '6a', '28', '25', 'b3', '39', 'c9', '40', '66', '8a', '31', '57', '24', '4d', '17']
4 subBytes :    ['2d', 'fb', '02', '34', '3f', '6d', '12', 'dd', '09', '33', '7e', 'c7', '5b', '36', 'e3', 'f0']
4 shiftRows :   ['2d', '6d', '7e', 'f0', '3f', '33', 'e3', '34', '09', '36', '02', 'dd', '5b', 'fb', '12', 'c7']
4 mixColumns :  ['63', '85', 'b7', '9f', 'fc', '53', '8d', 'f9', '97', 'be', '47', '8e', '75', '47', 'd6', '91']
4 addRoundKey : ['47', 'f7', 'f7', 'bc', '95', '35', '3e', '03', 'f9', '6c', '32', 'bc', 'fd', '05', '8d', 'fd']
4 addRoundKey : ['24', '72', '40', '23', '69', '66', 'b3', 'fa', '6e', 'd2', '75', '32', '88', '42', '5b', '6c']
5 subBytes :    ['36', '40', '09', '26', 'f9', '33', '6d', '2d', '9f', 'b5', '9d', '23', 'c4', '2c', '39', '50']
5 shiftRows :   ['36', '33', '9d', '50', 'f9', 'b5', '39', '26', '9f', '2c', '09', '2d', 'c4', '40', '6d', '23']
5 mixColumns :  ['f4', 'bc', 'd4', '54', '32', 'e5', '54', 'd0', '75', 'f1', 'd6', 'c5', '1d', 'd0', '3b', '3c']
5 addRoundKey : ['3c', 'aa', 'a3', 'e8', 'a9', '9f', '9d', 'eb', '50', 'f3', 'af', '57', 'ad', 'f6', '22', 'aa']
5 addRoundKey : ['c8', '16', '77', 'bc', '9b', '7a', 'c9', '3b', '25', '02', '79', '92', 'b0', '26', '19', '96']
6 subBytes :    ['e8', '47', 'f5', '65', '14', 'da', 'dd', 'e2', '3f', '77', 'b6', '4f', 'e7', 'f7', 'd4', '90']
6 shiftRows :   ['e8', 'da', 'b6', '90', '14', '77', 'd4', '65', '3f', 'f7', 'f5', 'e2', 'e7', '47', 'dd', '4f']
6 mixColumns :  ['98', '16', 'ee', '74', '00', 'f8', '7f', '55', '6b', '2c', '04', '9c', '8e', '5a', 'd0', '36']
6 addRoundKey : ['5e', '39', '0f', '7d', 'f7', 'a6', '92', '96', 'a7', '55', '3d', 'c1', '0a', 'a3', '1f', '6b']
6 addRoundKey : ['c6', '2f', 'e1', '09', 'f7', '5e', 'ed', 'c3', 'cc', '79', '39', '5d', '84', 'f9', 'cf', '5d']
7 subBytes :    ['b4', '15', 'f8', '01', '68', '58', '55', '2e', '4b', 'b6', '12', '4c', '5f', '99', '8a', '4c']
7 shiftRows :   ['b4', '58', '12', '4c', '68', 'b6', '8a', '01', '4b', '99', 'f8', '2e', '5f', '15', '55', '4c']
7 mixColumns :  ['c5', '7e', '1c', '15', '9a', '9b', 'd2', '86', 'f0', '5f', '4b', 'e0', '98', 'c6', '34', '39']
7 addRoundKey : ['14', 'f9', '70', '1a', 'e3', '5f', 'e2', '8c', '44', '0a', 'df', '4d', '4e', 'a9', 'c0', '26']
7 addRoundKey : ['d1', '87', '6c', '0f', '79', 'c4', '30', '0a', 'b4', '55', '94', 'ad', 'd6', '6f', 'f4', '1f']
8 subBytes :    ['3e', '17', '50', '76', 'b6', '1c', '04', '67', '8d', 'fc', '22', '95', 'f6', 'a8', 'bf', 'c0']
8 shiftRows :   ['3e', '1c', '22', 'c0', 'b6', 'fc', 'bf', '76', '8d', 'a8', '50', '67', 'f6', '17', '04', '95']
8 mixColumns :  ['ba', 'a0', '3d', 'e7', 'a1', 'f9', 'b5', '6e', 'd5', '51', '2c', 'ba', '5f', '41', '4d', '23']
8 addRoundKey : ['47', '43', '87', '35', 'a4', '1c', '65', 'b9', 'e0', '16', 'ba', 'f4', 'ae', 'bf', '7a', 'd2']
8 addRoundKey : ['fd', 'e3', 'ba', 'd2', '05', 'e5', 'd0', 'd7', '35', '47', '96', '4e', 'f1', 'fe', '37', 'f1']
9 subBytes :    ['54', '11', 'f4', 'b5', '6b', 'd9', '70', '0e', '96', 'a0', '90', '2f', 'a1', 'bb', '9a', 'a1']
9 shiftRows :   ['54', 'd9', '90', 'a1', '6b', 'a0', '9a', 'b5', '96', 'bb', 'f4', '0e', 'a1', '11', '70', '2f']
9 mixColumns :  ['e9', 'f7', '4e', 'ec', '02', '30', '20', 'f6', '1b', 'f2', 'cc', 'f2', '35', '3c', '21', 'c7']
9 addRoundKey : ['54', '99', '32', 'd1', 'f0', '85', '57', '68', '10', '93', 'ed', '9c', 'be', '2c', '97', '4e']
9 addRoundKey : ['bd', '6e', '7c', '3d', 'f2', 'b5', '77', '9e', '0b', '61', '21', '6e', '8b', '10', 'b6', '89']
10 subBytes :   ['7a', '9f', '10', '27', '89', 'd5', 'f5', '0b', '2b', 'ef', 'fd', '9f', '3d', 'ca', '4e', 'a7']
10 shiftRows :  ['7a', 'd5', 'fd', 'a7', '89', 'ef', '4e', '27', '2b', 'ca', '10', '0b', '3d', '9f', 'f5', '9f']
10 addRoKey : ['69', 'c4', 'e0', 'd8', '6a', '7b', '04', '30', 'd8', 'cd', 'b7', '80', '70', 'b4', 'c5', '5a']
Message décrypté :
['69', 'c4', 'e0', 'd8', '6a', '7b', '04', '30', 'd8', 'cd', 'b7', '80', '70', 'b4', 'c5', '5a']
❯ /opt/homebrew/opt/python/libexec/bin/python "/Users/robinbochu/Documents/School/TelecomSaintEtienne/TSE3/Sécurisation des échanges de données et des matériels/TDs/AES_Python_Implementation/main.py"
INIT addRoKey : ['00', '10', '20', '30', '40', '50', '60', '70', '80', '90', 'a0', 'b0', 'c0', 'd0', 'e0', 'f0']
1 subBytes :    ['63', 'ca', 'b7', '04', '09', '53', 'd0', '51', 'cd', '60', 'e0', 'e7', 'ba', '70', 'e1', '8c']
1 shiftRows :   ['63', '53', 'e0', '8c', '09', '60', 'e1', '04', 'cd', '70', 'b7', '51', 'ba', 'ca', 'd0', 'e7']
1 mixColumns :  ['5f', '72', '64', '15', '57', 'f5', 'bc', '92', 'f7', 'be', '3b', '29', '1d', 'b9', 'f9', '1a']
1 addRoundKey : ['d6', 'aa', '74', 'fd', 'd2', 'af', '72', 'fa', 'da', 'a6', '78', 'f1', 'd6', 'ab', '76', 'fe']
1 addRoundKey : ['89', 'd8', '10', 'e8', '85', '5a', 'ce', '68', '2d', '18', '43', 'd8', 'cb', '12', '8f', 'e4']
2 subBytes :    ['a7', '61', 'ca', '9b', '97', 'be', '8b', '45', 'd8', 'ad', '1a', '61', '1f', 'c9', '73', '69']
2 shiftRows :   ['a7', 'be', '1a', '69', '97', 'ad', '73', '9b', 'd8', 'c9', 'ca', '45', '1f', '61', '8b', '61']
2 mixColumns :  ['ff', '87', '96', '84', '31', 'd8', '6a', '51', '64', '51', '51', 'fa', '77', '3a', 'd0', '09']
2 addRoundKey : ['b6', '92', 'cf', '0b', '64', '3d', 'bd', 'f1', 'be', '9b', 'c5', '00', '68', '30', 'b3', 'fe']
2 addRoundKey : ['49', '15', '59', '8f', '55', 'e5', 'd7', 'a0', 'da', 'ca', '94', 'fa', '1f', '0a', '63', 'f7']
3 subBytes :    ['3b', '59', 'cb', '73', 'fc', 'd9', '0e', 'e0', '57', '74', '22', '2d', 'c0', '67', 'fb', '68']
3 shiftRows :   ['3b', 'd9', '22', '68', 'fc', '74', 'fb', '73', '57', '67', 'cb', 'e0', 'c0', '59', '0e', '2d']
3 mixColumns :  ['4c', '9c', '1e', '66', 'f7', '71', 'f0', '76', '2c', '3f', '86', '8e', '53', '4d', 'f2', '56']
3 addRoundKey : ['b6', 'ff', '74', '4e', 'd2', 'c2', 'c9', 'bf', '6c', '59', '0c', 'bf', '04', '69', 'bf', '41']
3 addRoundKey : ['fa', '63', '6a', '28', '25', 'b3', '39', 'c9', '40', '66', '8a', '31', '57', '24', '4d', '17']
4 subBytes :    ['2d', 'fb', '02', '34', '3f', '6d', '12', 'dd', '09', '33', '7e', 'c7', '5b', '36', 'e3', 'f0']
4 shiftRows :   ['2d', '6d', '7e', 'f0', '3f', '33', 'e3', '34', '09', '36', '02', 'dd', '5b', 'fb', '12', 'c7']
4 mixColumns :  ['63', '85', 'b7', '9f', 'fc', '53', '8d', 'f9', '97', 'be', '47', '8e', '75', '47', 'd6', '91']
4 addRoundKey : ['47', 'f7', 'f7', 'bc', '95', '35', '3e', '03', 'f9', '6c', '32', 'bc', 'fd', '05', '8d', 'fd']
4 addRoundKey : ['24', '72', '40', '23', '69', '66', 'b3', 'fa', '6e', 'd2', '75', '32', '88', '42', '5b', '6c']
5 subBytes :    ['36', '40', '09', '26', 'f9', '33', '6d', '2d', '9f', 'b5', '9d', '23', 'c4', '2c', '39', '50']
5 shiftRows :   ['36', '33', '9d', '50', 'f9', 'b5', '39', '26', '9f', '2c', '09', '2d', 'c4', '40', '6d', '23']
5 mixColumns :  ['f4', 'bc', 'd4', '54', '32', 'e5', '54', 'd0', '75', 'f1', 'd6', 'c5', '1d', 'd0', '3b', '3c']
5 addRoundKey : ['3c', 'aa', 'a3', 'e8', 'a9', '9f', '9d', 'eb', '50', 'f3', 'af', '57', 'ad', 'f6', '22', 'aa']
5 addRoundKey : ['c8', '16', '77', 'bc', '9b', '7a', 'c9', '3b', '25', '02', '79', '92', 'b0', '26', '19', '96']
6 subBytes :    ['e8', '47', 'f5', '65', '14', 'da', 'dd', 'e2', '3f', '77', 'b6', '4f', 'e7', 'f7', 'd4', '90']
6 shiftRows :   ['e8', 'da', 'b6', '90', '14', '77', 'd4', '65', '3f', 'f7', 'f5', 'e2', 'e7', '47', 'dd', '4f']
6 mixColumns :  ['98', '16', 'ee', '74', '00', 'f8', '7f', '55', '6b', '2c', '04', '9c', '8e', '5a', 'd0', '36']
6 addRoundKey : ['5e', '39', '0f', '7d', 'f7', 'a6', '92', '96', 'a7', '55', '3d', 'c1', '0a', 'a3', '1f', '6b']
6 addRoundKey : ['c6', '2f', 'e1', '09', 'f7', '5e', 'ed', 'c3', 'cc', '79', '39', '5d', '84', 'f9', 'cf', '5d']
7 subBytes :    ['b4', '15', 'f8', '01', '68', '58', '55', '2e', '4b', 'b6', '12', '4c', '5f', '99', '8a', '4c']
7 shiftRows :   ['b4', '58', '12', '4c', '68', 'b6', '8a', '01', '4b', '99', 'f8', '2e', '5f', '15', '55', '4c']
7 mixColumns :  ['c5', '7e', '1c', '15', '9a', '9b', 'd2', '86', 'f0', '5f', '4b', 'e0', '98', 'c6', '34', '39']
7 addRoundKey : ['14', 'f9', '70', '1a', 'e3', '5f', 'e2', '8c', '44', '0a', 'df', '4d', '4e', 'a9', 'c0', '26']
7 addRoundKey : ['d1', '87', '6c', '0f', '79', 'c4', '30', '0a', 'b4', '55', '94', 'ad', 'd6', '6f', 'f4', '1f']
8 subBytes :    ['3e', '17', '50', '76', 'b6', '1c', '04', '67', '8d', 'fc', '22', '95', 'f6', 'a8', 'bf', 'c0']
8 shiftRows :   ['3e', '1c', '22', 'c0', 'b6', 'fc', 'bf', '76', '8d', 'a8', '50', '67', 'f6', '17', '04', '95']
8 mixColumns :  ['ba', 'a0', '3d', 'e7', 'a1', 'f9', 'b5', '6e', 'd5', '51', '2c', 'ba', '5f', '41', '4d', '23']
8 addRoundKey : ['47', '43', '87', '35', 'a4', '1c', '65', 'b9', 'e0', '16', 'ba', 'f4', 'ae', 'bf', '7a', 'd2']
8 addRoundKey : ['fd', 'e3', 'ba', 'd2', '05', 'e5', 'd0', 'd7', '35', '47', '96', '4e', 'f1', 'fe', '37', 'f1']
9 subBytes :    ['54', '11', 'f4', 'b5', '6b', 'd9', '70', '0e', '96', 'a0', '90', '2f', 'a1', 'bb', '9a', 'a1']
9 shiftRows :   ['54', 'd9', '90', 'a1', '6b', 'a0', '9a', 'b5', '96', 'bb', 'f4', '0e', 'a1', '11', '70', '2f']
9 mixColumns :  ['e9', 'f7', '4e', 'ec', '02', '30', '20', 'f6', '1b', 'f2', 'cc', 'f2', '35', '3c', '21', 'c7']
9 addRoundKey : ['54', '99', '32', 'd1', 'f0', '85', '57', '68', '10', '93', 'ed', '9c', 'be', '2c', '97', '4e']
9 addRoundKey : ['bd', '6e', '7c', '3d', 'f2', 'b5', '77', '9e', '0b', '61', '21', '6e', '8b', '10', 'b6', '89']
10 subBytes :   ['7a', '9f', '10', '27', '89', 'd5', 'f5', '0b', '2b', 'ef', 'fd', '9f', '3d', 'ca', '4e', 'a7']
10 shiftRows :  ['7a', 'd5', 'fd', 'a7', '89', 'ef', '4e', '27', '2b', 'ca', '10', '0b', '3d', '9f', 'f5', '9f']
10 addRoKey : ['69', 'c4', 'e0', 'd8', '6a', '7b', '04', '30', 'd8', 'cd', 'b7', '80', '70', 'b4', 'c5', '5a']
Message décrypté :
['69', 'c4', 'e0', 'd8', '6a', '7b', '04', '30', 'd8', 'cd', 'b7', '80', '70', 'b4', 'c5', '5a']
```
