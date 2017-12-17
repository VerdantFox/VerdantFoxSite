def vigenere_cipher(cipher_key, plain_text):
    # Define ALPHABET LENGTH
    ALPHABETLENGTH = 26
    # Define lowercase unicode conversion
    MOD_a = (ord("a") % ALPHABETLENGTH)
    # Define uppercase unicode conversion
    MOD_A = (ord("A") % ALPHABETLENGTH)

    encypted_character_list = []
    encrypted_text = ""

    # cipher_key_counter for separate iterating from plain_text
    cipher_key_counter = 0
    for PlainTextLetter in range(len(plain_text)):
        # 1st layer if statement makes sure to iterate
        #  over only plain text letters
        if plain_text[PlainTextLetter].isalpha():
            # 2nd layer if branch ciphers lower case letters of Cipher Key.
            if cipher_key[cipher_key_counter % len(cipher_key)].islower():
                # 3rd layer if statement ciphers lower case plain text letters.
                if plain_text[PlainTextLetter].islower():
                    # Index plain text character to 0, index key character to 0,
                    # add the two together. Mod by alphabet length,
                    # index back up
                    # to lower case plaintext character.
                    encypted_character_list.append(
                        chr((
                            ((ord(plain_text[PlainTextLetter]) - MOD_a) +
                              (ord(cipher_key[cipher_key_counter % len(cipher_key)])
                               - MOD_a)) % ALPHABETLENGTH
                            ) + ord('a'))
                    )
                    # Move to next letter of Cipher Key.
                    cipher_key_counter += 1
                # 3rd layer if statement ciphers upper case plain text letters.
                if plain_text[PlainTextLetter].isupper():
                    # Index plain text character to 0, index key character to 0,
                    # add the two together. Mod by alphabet length,
                    # index back up to upper case plaintext character.
                    encypted_character_list.append(chr((((ord(plain_text[PlainTextLetter]) - MOD_A)
                                + (ord(cipher_key[cipher_key_counter
                                                  % len(cipher_key)]) - MOD_a))
                              % ALPHABETLENGTH) + ord('A')))
                    # Move to next letter of Cipher Key.
                    cipher_key_counter += 1
            # 2nd layer else branch ciphers upper case key character.
            else:
                # 3rd layer if statement ciphers lower case plain text letters.
                if plain_text[PlainTextLetter].islower():
                    # Index plain text character to 0, index key character to 0,
                    # add the two together. Mod by alphabet length,
                    # index back up to lower case plaintext character.
                    encypted_character_list.append(chr((((ord(plain_text[
                                                            PlainTextLetter]) - MOD_a)
                                + (ord(cipher_key[cipher_key_counter
                                                  % len(cipher_key)]) - MOD_A))
                          % ALPHABETLENGTH) + ord('a')))
                    # Move to next letter of Cipher Key.
                    cipher_key_counter += 1
                # 3rd layer if statement ciphers upper case plain text letters.
                if plain_text[PlainTextLetter].isupper():
                    # Index plain text character to 0, index key character to 0,
                    # add the two together. Mod by alphabet length, index
                    # back up to upper case plaintext character.
                    encypted_character_list.append(chr((((ord(plain_text[
                                                            PlainTextLetter]) - MOD_A)
                                + (ord(cipher_key[cipher_key_counter
                                                  % len(cipher_key)]) - MOD_A))
                          % ALPHABETLENGTH) + ord('A')))
                    # Move to next letter of Cipher Key.
                    cipher_key_counter += 1
        # If plain text character is not a letter.
        else:
            # Print it without advancing the Cipher Key.
            encypted_character_list.append(plain_text[PlainTextLetter])
    # Line break at end of Cipher text
    encrypted_text = encrypted_text.join(encypted_character_list)
    return encrypted_text


if __name__ == "__main__":
    # Get Cypher Key (one word, all text)
    Cipher_key = input("Please give cipher key (One word, all text): ")
    # while cipher_key.isalpha() is False:
    #         cipher_key = input("Cipher key must be single word in letters,"
    #                           " try again! ")

    Plain_text = input("What plain text would you like to encipher? ")

    vigenere_cipher(Cipher_key, Plain_text)
