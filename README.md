# AES_Python_Implementation

## Rappel

Le chiffrement AES est un système d'encodage/codage de messages qui utilise une clé de chiffrement de 128 bits, 192 bits ou 256 bits. Il est utilisé pour protéger les informations sensibles et est largement utilisé dans les systèmes de sécurité et de protection des données.
Pour ce td nous n'allons utilisé qu'une clé de 128 bits

## Sommaire

> 1.  [Introduction](#introduction)
> 2.  [Prérequis](#prérequis)
> 3.  [Fonctionnement + Explication du code](#Fonctionnement)

# Introduction

## Explication de toutes les étapes du AES

1. **SubBytes** : Substitution des octets de l'état par des octets de la S-Box.
2. **ShiftRows** : Décalage des lignes de l'état.
3. **MixColumns** : Mélange des colonnes de l'état.
4. **AddRoundKey** : Clé de tour XOR.

# Prérequis / Installation
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
Chaque case ici  représente un octet. Par la suite, les opérations du chiffrement et du déchiffrement se font octet par octet.
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
Le code prend chaque byte du message original (parcourant d'abord chaque ligne avec for row in message_2d, puis chaque byte dans ces lignes avec for byte in row), et le remplace par un autre byte selon la S-box (Sbox[byte]). Cela se fait pour chaque byte du message initial.



