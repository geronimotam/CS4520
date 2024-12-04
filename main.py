import re
import string
from collections import Counter
from functools import reduce
import math
path_cipher1 = "ciphers/cipher1.txt"
path_cipher2 = "ciphers/cipher2.txt"
path_cipher3 = "ciphers/cipher3.txt"
path_cipher4 = "ciphers/cipher4.txt"

# General variables needed for frequency analysis.
alphabet = string.ascii_lowercase
english_freq = Counter()
english = {'a':8.2,'b': 1.5 ,'c': 2.8, 'd':4.2, 'e':12.7, 'f':2.2,'g':2.0,'h':6.1,'i':7.0,'j':0.1,'k':0.8,'l':4.0,'m':2.4,'n':6.7,'o':7.5,'p':1.9,'q':0.0,'r':6.0,'s':6.3,'t':9.0,'u':2.8,'v':1.0,'w':2.4,'x':0.0,'y':2.0,'z':0.0}
english_freq.update(english)

# Helper functions for decryption and encryption detection

def prep_text(path): # prepares the text, stripes all special characters and stores relevant information
    pattern = r'[^a-z]'
    with open(path, "r") as cipher_file:
        original_text = cipher_file.read()
    capitalization_info = [i for i,item in enumerate(original_text) if item.isupper()]
    cipher_text = original_text.lower()
    character_info = {item.start() : item.group() for item in re.finditer(pattern, cipher_text)}
    cleaned_text = re.sub(pattern,'',cipher_text)
    return  original_text,cleaned_text, capitalization_info ,character_info


def move_values(counter:Counter,move): # move the probability distribution of a frequency layout. Used for statisctial distances
    counter = dict(sorted(counter.items()))
    keys = list(counter.keys())
    values = list(counter.values())
    for i in range(len(keys)):
        counter[keys[i]] = values[(i-move) % len(keys)]
    return counter


def calc_freq(text): # function that claculates the ltter frequency in the cipher text, compares with the english frequency and calculates the statistical distance
    letter_count = Counter(text)
    total_letter = letter_count.total()
    for key in letter_count:
        letter_count[key] = round((letter_count[key] / total_letter) * 100,1)
    for i in alphabet:
        if i not in letter_count.keys():
            letter_count[i] = 0.0
    last_check = {}
    for r in range(26):
        if r == 0:
            check = round(sum([0.5* abs(english_freq[key] - letter_count[key]) for key in english_freq.keys()]),2)
            last_check[r] = check
        else:
            letter_count = move_values(letter_count,1)
            check = round(sum([0.5* abs(english_freq[key] - letter_count[key]) for key in english_freq.keys()]),2)
            last_check[r] = check
    return last_check,letter_count


def shift_text(text,steps,special_characters, cap): # shifts the text based on the steps variable. Also reintroduces special characters and capatilization
    new_text = []
    start = 97
    for char in text:
        shifted_char = chr(start + (ord(char) - start + steps) % 26)
        new_text.append(shifted_char)
    for pos,char in special_characters.items():
        new_text.insert(pos,char)
    for i in cap:
        new_text[i] = new_text[i].upper()
    return ''.join(new_text)

def count_biagrams(text): # counts the frequency of the biagrams in the ciphertext, claculates teh spaces betweeen the most occuring biagrams and takes the gcd of those. This is done until a gcd != 1 is found. This is the keyword lenght.
    biagrams = [text[i:i+2] for i in range(len(text) - 1)]

    biagrams_count = Counter(biagrams)
    gcd = 1
    while gcd == 1:
        most_freq_bia = max(biagrams_count,key=biagrams_count.get)
        positions = [i for i in range(len(text) - 1) if text[i:i+2] == most_freq_bia]
        space = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
        gcd = reduce(math.gcd,space)
        if gcd == 1 :
            remove_most = biagrams_count.pop(most_freq_bia)
            # print("removed biagram: ",most_freq_bia,":",remove_most)
    return biagrams_count,gcd

def count_triagrams(text): # count triagrams frequency.
    triagrams = [text[i:i+3] for i in range(len(text) - 1)]

    triagrams_count = Counter(triagrams)
    return triagrams_count


def freq_count_text(text,position,step): 
# calculates and compares the letter frequency at specific positions of the cipher text with the english frequency. Calculates the minimum statistical distane to find the corresponfding letter of the keyword.
    char_list = []
    for i,char in enumerate(text):
            if i % position == step :
                char_list.append(char)
    count_char = Counter(char_list)
    total_letter = count_char.total()
    alphabet = string.ascii_lowercase
    for key in count_char:
        count_char[key] = round((count_char[key] / total_letter) * 100,1)
    for i in alphabet:
        if i not in count_char.keys():
            count_char[i] = 0.0
    last_check = {}
    for r in range(26):
        if r == 0:
            check = round(sum([0.5* abs(english_freq[key] - count_char[key]) for key in english_freq.keys()]),2)
            last_check[r] = check
        else:
            count_char = move_values(count_char,1)
            check = round(sum([0.5* abs(english_freq[key] - count_char[key]) for key in english_freq.keys()]),2)
            last_check[r] = check
    min_distance = min(last_check, key=last_check.get)
    output = alphabet[26 -min_distance]
    return output, min_distance, last_check
    

def shift_with_key(text,key):
# shift the cipher text based on a keyword rather than a fixed amount of steps.
    new_text = []
    keylen = len(key)
    start = 97
    for i,char in enumerate(text):
        steps = ord(key[i %keylen]) - start
        shifted_char = chr(start + (ord(char) - start - steps) % 26)
        new_text.append(shifted_char)
    return ''.join(new_text)


def decrypt(choice):
# general function to decrypt a ciphertext that uses the shift and vinegere cipher. 
    if choice == 1 :
        path = path_cipher1
    elif choice == 2 :
        path = path_cipher2
    elif choice == 3 :
        path = path_cipher3  
    elif choice == 4 :
        path = path_cipher4
    else:
        path = path_cipher1
    
    parameters = prep_text(path)
    output,letter_freq = calc_freq(parameters[1])
    min_distance = min(output, key=output.get)
    if output[min_distance] < 18.0:
        encryption = "Shift cypher"
        final_text = shift_text(parameters[1],min_distance,parameters[3],parameters[2])
        return parameters[0],final_text , encryption , min_distance
    else:
        encryption = "Vigenere cypher"
        biagram_c, space,  = count_biagrams(parameters[1])
        triagram_c = count_triagrams(parameters[1])
        idk = []
        for i in range(space):
            test_text,min_dis,check_idk = freq_count_text(parameters[1],space,i)
            idk.append([test_text,min_dis,check_idk])
        keyword = [i[0] for i in idk]
        keyword = "".join(keyword)
        final_text = shift_with_key(parameters[1],keyword)
        final_text = shift_text(final_text,0,parameters[3],parameters[2])
        return parameters[0],final_text, encryption, keyword
    
ciphered_text,plaintext, encryption, key = decrypt(2)

#Print statements output
print("The cipher text: \n", ciphered_text,"\n")
print("The plaintext is given: \n",plaintext, "\n")
print("Encyption that was identified:", encryption, "\n")
print("The key that was found:",key, "\n")



