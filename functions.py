from constants import * 


# def conversion(message, key):
#     message_arr = []
#     key_arr = []
#     for i in range(0, len(message), 2):
#         message_arr.append(f"0x{message[i : i + 2]}")
#     for i in range(0, len(key), 2):
#         key_arr.append(f"0x{key[i : i + 2]}")
#     return message_arr, key_arr

def shiftRows(message_subytes):
    message_shifted = np.array(message_subytes)
    for i in range(4):
        message_shifted[i] = np.roll(message_shifted[i], -i)
    return message_shifted

def subBytes(message_2d):
    message_subytes = np.array([[Sbox[byte] for byte in row] for row in message_2d])
    return message_subytes

def multiply_in_gf(a, b):
    result = 0
    # On itere 8 fois car on travaille avec des octets
    for _ in range(8):  
        # Si le bit de poids faible de b est 1
        if b & 1:  
            # On fait un XOR entre a et le resultat
            result ^= a  

        # On check si le bit de poids fort de a est 1
        is_msb_set = a & 0x80

        # On decale a d'un bit vers la gauche
        a <<= 1

        # Si le bit de poids fort etait 1, on fait un XOR entre le resultat et 0x1B (polynome irreductible GF(2^8))
        if is_msb_set:
            a ^= 0x1B

        # On decale b d'un bit vers la droite
        b >>= 1

    return result


def mixColumns(message_shifted):
    message_mixed = np.zeros_like(message_shifted, dtype=np.uint8)
    # Pour chaque colonne de la matrice
    for col in range(4): 
        # Pour chaque ligne de la matrice
        for row in range(4):
            # On initialise temp a 0 pour accumuler les resultats des multiplications dans le champ de Galois (GF)
            temp = 0
            # Pour chaque element de la ligne de la matrice mix_column_matrix et de la colonne de la matrice message_shifted
            for k in range(4):
                # On fait un XOR entre temp et le resultat de la multiplication dans le champ de Galois
                # On utilise la fonction multiply_in_gf pour faire la multiplication
                temp ^= multiply_in_gf(
                    mix_column_matrix[row][k], message_shifted[k][col]
                )
            # On stocke le resultat dans la matrice message_mixed
            message_mixed[row][col] = temp
    return message_mixed


def subWord(word):
    return np.array([Sbox[b] for b in word], dtype=np.uint8)


def rotWord(word):
    # On decale le mot d'un byte vers la gauche
    return np.roll(word, -1)


def keyExpansion(key, Nk=4, Nr=10):
    # on initialise la matrice W avec des 0 de taille 4x(Nk*(Nr+1)) qui est la taille de la clé étendue
    W = np.empty((4, Nk * (Nr + 1)), dtype=np.uint8)
    # On copie la clé dans les 4 premiers mots de la matrice W
    # i va de 0 à Nk 
    for i in range(Nk):
        # On copie chaque byte de la clé dans la matrice W
        W[:, i] = key[4 * i : 4 * (i + 1)]
    # On applique RotWord, SubWord, et XOR avec Rcon si i est un multiple de Nk
    for i in range(Nk, 4 * (Nr + 1)):
        temp = W[:, i - 1].copy()
        if i % Nk == 0:
            temp = subWord(rotWord(temp)) ^ Rcon[i // Nk - 1]
        # On fait un XOR entre le mot i-Nk et temp
        W[:, i] = W[:, i - Nk] ^ temp
    return W


def addRoundKey(state, roundKey):
    return state ^ roundKey