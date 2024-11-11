from collections import Counter
import requests
import random

# Liste fixe de caractères et de bigrammes (256 symboles)
caracteres = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô']
bicaracteres = ['e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
symboles = caracteres + bicaracteres

def load_text_from_web(url):
    """Charger le texte à partir de l'URL donnée."""
    response = requests.get(url)
    response.encoding = 'utf-8'  # Assurer que l'encodage est correct
    return response.text

def calculate_frequency(text, caracteres, bicaracteres):
    """Calculer la fréquence de chaque symbole dans le texte."""
    frequencyFr = {}

    # Compter les caractères uniques
    for char in caracteres:
        frequencyFr[char] = text.count(char)

    # Compter les séquences de bigrammes
    for bi_char in bicaracteres:
        frequencyFr[bi_char] = text.count(bi_char)

    return frequencyFr

# Charger le texte à partir des URL spécifiées
url1 = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # URL d'exemple
url2 = "https://www.gutenberg.org/ebooks/4650.txt.utf -8"  # URL d'exemple
text = load_text_from_web(url1) + load_text_from_web(url2)

frequencyFr = calculate_frequency(text, caracteres, bicaracteres)

def sort_frequencies(frequencyFr):
    """Trier le dictionnaire de fréquence par valeurs dans l'ordre décroissant."""
    sorted_frequency = dict(sorted(frequencyFr.items(), key=lambda item: item[1], reverse=True))
    return sorted_frequency

frequencyFr = sort_frequencies(frequencyFr)

def divide_ciphertext(C):
    # Initialiser un dictionnaire vide pour stocker la fréquence de chaque octet
    frequency_dict = {}

    # Itérer à travers le texte chiffré par morceaux de 8 bits (1 octet)
    for i in range(0, len(C), 8):
        # Obtenir l'octet actuel (8 bits)
        byte = C[i:i+8]
        
        # S'assurer que nous avons un octet complet
        if len(byte) == 8:
            # Mettre à jour le compte de fréquence dans le dictionnaire
            if byte in frequency_dict:
                frequency_dict[byte] += 1
            else:
                frequency_dict[byte] = 1

    return frequency_dict

def create_mapping(cipher_freq, language_freq):
    mapping = {}
    
    # Trier les deux dictionnaires par fréquence
    sorted_cipher = sorted(cipher_freq.items(), key=lambda item: item[1], reverse=True)
    sorted_language = sorted(language_freq.items(), key=lambda item: item[1], reverse=True)
    
    # Créer un mapping basé sur la fréquence
    for (cipher_text, _), (lang_text, _) in zip(sorted_cipher, sorted_language):
        mapping[cipher_text] = lang_text
    
    return mapping

# Fonction pour décoder le texte chiffré en utilisant le mapping
def decode_ciphertext(C, mapping):
    decoded_text = ''
    
    # Itérer à travers le texte chiffré par morceaux de 8 bits
    for i in range(0, len(C), 8):
        byte = C[i:i+8]
        decoded_text += mapping.get(byte, byte)  # Utiliser le mapping ou garder l'octet s'il n'est pas trouvé
    
    return decoded_text

# Exemple d'utilisation
french_dictionary_url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"  # Remplacer par une URL de dictionnaire français réelle
C = "11010101011011000111010011001111000011100110110011001111110011000000110111001010010111010111111011001100011011001100111101101100011000011100111100001110011011001100111111001100000011011100101001011101011111101100110001101100011101001100111100001110011011001100111100111111000100100000011000111101000100100110110011001111011011000110000110010101000011000000111001101100110011110010000011001110011000010110110001110100110011110000111001101100110011110010000011001110011000010110110011001111011011000110000111001111000011100110110011001111001111110001001000000110001111010001001001101100011111001100111101011010001011011100101011001111011011001101010111001111"  # Remplacer par votre texte chiffré réel

# Calculer la fréquence du texte chiffré
def decrypt(C):
    cipher_freq = divide_ciphertext(C)
    # Créer un mapping des fréquences du texte chiffré aux fréquences de la langue
    mapping = create_mapping(cipher_freq, frequencyFr)

    # Décoder le texte chiffré
    decoded_text = decode_ciphertext(C, mapping)

    print("Texte décodé final :", decoded_text)

decrypt(C)
