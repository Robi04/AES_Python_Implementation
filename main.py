import numpy as np
from functions import *


if __name__ == "__main__":
    message = np.array(
        [
            0x00,
            0x10,
            0x20,
            0x30,
            0x40,
            0x50,
            0x60,
            0x70,
            0x80,
            0x90,
            0xA0,
            0xB0,
            0xC0,
            0xD0,
            0xE0,
            0xF0,
        ]
    )
    key = np.array(
        [
            0xD6,
            0xAA,
            0x74,
            0xFD,
            0xD2,
            0xAF,
            0x72,
            0xFA,
            0xDA,
            0xA6,
            0x78,
            0xF1,
            0xD6,
            0xAB,
            0x76,
            0xFE,
        ]
    )

    # Chiffrement en bloc
    message_2d = chiffrementBloc(message)
    print(f"Chiffrement en bloc : \n {message_2d}\n")

    # Subytes
    # En utilisant la matrice sbox on va remplacer chaque élément de message_2d
    # par son équivalent dans la matrice sbox sachant que sbox est flatten
    message_subytes = subBytes(message_2d)
    # Afficher le résultat
    print(f"Subytes : \n {message_subytes} \n")

    # ShiftRows
    message_shifted = shiftRows(message_subytes)
    print(f"ShitRows : \n {message_shifted}\n")

    # MixColumns
    message_mixed = mixColumns(message_shifted)
    print(f"MixColumns (Corrected) \n{message_mixed}\n")

    # Reshape the key to match the state matrix structure
    state_after_addroundkey = addRoundKey(message_mixed, key)
    print(f"Add round key : \n{state_after_addroundkey}\n")
