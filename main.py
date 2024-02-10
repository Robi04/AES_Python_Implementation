from functions import *


def aes_cipher(state, key):
    # Nombre de mots de 32 bits dans la clé
    Nk = 4 
    # Nombre de round = 10 pour une clé de 128 bits
    Nr = 10  
    

    expanded_key = keyExpansion(key, Nk, Nr)
    # Rount initial (add round key)
    state = addRoundKey(state, expanded_key[:, :4])
    print(
        f"INIT addRoKey : {[format(x, '02x') for x in state.transpose().flatten()]}"
    )

    # Boucle principale
    for round in range(1, Nr):
        state = subBytes(state)
        print(
            f"{round} subBytes :    {[format(x, '02x') for x in state.transpose().flatten()]}"
        )
        state = shiftRows(state)
        print(
            f"{round} shiftRows :   {[format(x, '02x') for x in state.transpose().flatten()]}"
        )
        state = mixColumns(state)
        print(
            f"{round} mixColumns :  {[format(x, '02x') for x in state.transpose().flatten()]}"
        )
        print(f"{round} addRoundKey : {[format(x, '02x') for x in expanded_key[:, round * 4 : (round + 1) * 4].transpose().flatten()]}")
        state = addRoundKey(state, expanded_key[:, round * 4 : (round + 1) * 4])
        print(
            f"{round} addRoundKey : {[format(x, '02x') for x in state.transpose().flatten()]}"
        )

    # Dernier round
    state = subBytes(state)
    print(f"10 subBytes :   {[format(x, '02x') for x in state.transpose().flatten()]}")
    state = shiftRows(state)
    print(f"10 shiftRows :  {[format(x, '02x') for x in state.transpose().flatten()]}")
    state = addRoundKey(state, expanded_key[:, Nr * 4 : (Nr + 1) * 4])
    print(f"10 addRoKey : {[format(x, '02x') for x in state.transpose().flatten()]}")
    return state


#Fonction main pour tester le chiffrement
if __name__ == "__main__":
    message = np.array(
    [
        [0x00, 0x44, 0x88, 0xCC],
        [0x11, 0x55, 0x99, 0xDD],
        [0x22, 0x66, 0xAA, 0xEE],
        [0x33, 0x77, 0xBB, 0xFF],
    ],
    dtype=np.uint8,
    )
    key = np.array(
        [
            0x00,
            0x01,
            0x02,
            0x03,
            0x04,
            0x05,
            0x06,
            0x07,
            0x08,
            0x09,
            0x0A,
            0x0B,
            0x0C,
            0x0D,
            0x0E,
            0x0F,
        ],
        dtype=np.uint8,
    )
    #Affichage du message en output
    ciphered_message = aes_cipher(message, key)
    print(f"Message décrypté :\n{[format(byte, '02x') for byte in ciphered_message.transpose().flatten()]}")