import pandas as pd
import random 
from random import shuffle
import re

#cleaning up text
import re
def get_only_chars(line):

    clean_line = ""

    line = line.replace("’", "")
    line = line.replace("'", "")
    line = line.replace("-", " ") #replace hyphens with spaces
    line = line.replace("\t", " ")
    line = line.replace("\n", " ")
    line = line.lower()

    for char in line:
        if char in 'qwertyuiopasdfghjklzxcvbnm ':
            clean_line += char
        else:
            clean_line += ' '

    clean_line = re.sub(' +',' ',clean_line) #delete extra spaces
    if clean_line[0] == ' ':
        clean_line = clean_line[1:]
    return clean_line

# synonym replacement 
# load_synonyms digunakan untuk membaca file CSV yang berisi sinonim kata bahasa Sunda
def load_synonyms(file_path):
	synonyms_dict = {}	
	try:
		data = pd.read_csv(file_path)	
		for index, row in data.iterrows():	
			word = row['kata']	
			synonyms = row['sinonim'].split(',')	
			synonyms_dict[word] = [syn.strip() for syn in synonyms]	

			# Reverse Synonyms
			for synonym in synonyms: 
				synonym = synonym.strip()	
				if synonym not in synonyms_dict: 	
					synonyms_dict[synonym] = [word]		
				else: 
					synonyms_dict[synonym].append(word)

	except FileNotFoundError:
		print(f"File {file_path} not found")
	except pd.errors.EmptyDataError:
		print(f"File {file_path} is empty")
	return synonyms_dict

# get_sundanese_synonyms digunakan untuk mengambil daftar sinonim untuk sebuah kata dari dictionary
def get_sundanese_synonyms(word, synonyms_dict):
	return synonyms_dict.get(word, [])

# Kamus pronouns
def load_pronouns(filename):
	try:
		with open(filename, 'r', encoding='utf-8') as file:
			pronouns = [line.strip() for line in file.readlines() if line.strip()]
			return pronouns
	except FileNotFoundError:
		print(f"File {filename} tidak ditemukan.")
		return pronouns

def pronouns_replacement(words, index, pronouns_list):
    new_sentences = []
    target_word = words[index]
    
    if target_word in pronouns_list:
        for replacement in pronouns_list:
            if replacement != target_word:  # Hindari mengganti dengan kata yang sama
                new_words = words.copy()
                new_words[index] = replacement
                new_sentences.append(' '.join(new_words))
    
    return new_sentences

# Path ke file pronouns.txt
file_path_pronouns = 'kelas_kata/pronomina.txt'
pronouns_dict = load_pronouns(file_path_pronouns)

# synonym_replacement digunakan untuk mengganti n kata dalam kalimat dengan sinonim dari kata tersebut
# def synonym_replacement(words, index, synonyms_dict, stop_words):
#     new_words = words.copy()
#     target_word = words[index]
    
#     if target_word in stop_words:
#         return None
    
#     synonyms = get_sundanese_synonyms(target_word, synonyms_dict)
#     if not synonyms:
#         return None
    
#     synonym = random.choice(synonyms)  # Pilih satu sinonim secara acak
#     new_words[index] = synonym
    
#     return ' '.join(new_words)
def synonym_replacement(words, indices, synonyms_dict):
    new_words = words.copy()
    modified_indices = []
    
    for idx in indices:
        word = words[idx]
        synonyms = get_sundanese_synonyms(word, synonyms_dict)
        if synonyms:
            new_words[idx] = random.choice(synonyms)
            modified_indices.append(idx)
    
    return ' '.join(new_words), modified_indices


file_path_synonym = 'data/sundanese_synonyms.csv'
synonyms_dict = load_synonyms(file_path_synonym)

# Word Deletion
def load_kelas_kata(filename):
	kelas_kata = {}
	with open(filename, 'r', encoding='utf-8') as file:
		for line in file:
			kata, kelas = line.strip().split("\t") 
			kelas_kata[kata] = kelas.lower()  # Simpan dalam dictionary dengan kata sebagai key
	return kelas_kata

def get_kelas_kata(word, kelas_kata):
	return kelas_kata.get(word, [])

def word_deletion(words, kelas_kata_dict):
	#obviously, if there's only three or word less, don't delete it
	if len(words) <= 3:
		return words

	new_words = [word for word in words if kelas_kata_dict.get(word, "") != 'adverbia']
	
	return new_words

file_path_kelas_kata = 'data/dataset_kelas_kata.txt'
kelas_kata = load_kelas_kata(file_path_kelas_kata)

# Word Insertion 
def word_insertion(words, n, synonyms_dict):
	new_words = words.copy()
	for _ in range(n):
		add_word(new_words, synonyms_dict)
	return new_words

def add_word(new_words, synonyms_dict):
	synonyms = []
	counter = 0
	while len(synonyms) < 1:
		random_word = new_words[random.randint(0, len(new_words)-1)]
		synonyms = get_sundanese_synonyms(random_word, synonyms_dict)
		counter += 1
		if counter >= 10:
			return
	random_synonym = synonyms[0]
	random_idx = random.randint(0, len(new_words)-1)
	new_words.insert(random_idx, random_synonym)
	

def eda(sentence, synonyms_dict, kelas_kata_dict, pronouns_dict, alpha_wr=0.1, p_wd=0.1, alpha_wi=0.1):
	sentence = get_only_chars(sentence)
	words = sentence.split(' ')
	words = [word for word in words if word != '']
	num_words = len(words)
	
	valid_indices = [i for i, word in enumerate(words) if get_sundanese_synonyms(word, synonyms_dict)]
	
	if not valid_indices:
		return [sentence]
	
	num_to_replace = max(1, int(alpha_wr * len(valid_indices)))
	synonym_sentences = []
	pronoun_sentences = []

	#wr
	for i in range(len(valid_indices) // num_to_replace):
		selected_indices = valid_indices[i * num_to_replace:(i + 1) * num_to_replace]
		new_sentence, modified_indices = synonym_replacement(words, selected_indices, synonyms_dict)
		synonym_sentences.append(new_sentence)

        # Kalimat baru dengan kata-kata yang tidak diubah dalam iterasi ini
		remaining_indices = [idx for idx in valid_indices if idx not in modified_indices]
		if remaining_indices:
			new_sentence, _ = synonym_replacement(words, remaining_indices, synonyms_dict)
			synonym_sentences.append(new_sentence)
	# if alpha_wr > 0:
	# 	#sr
	# 	for i in range(num_words):  # Ganti setiap kata satu per satu jika ada sinonim
	# 		aug_sentence = synonym_replacement(words, i, synonyms_dict, stop_words)
	# 		if aug_sentence:
	# 			synonym_sentences.append(aug_sentence)

	# 	#pr
	# 	for i in range(num_words):  # Ganti setiap kata satu per satu jika ada sinonim
	# 		aug_sentence = pronouns_replacement(words, i, pronouns_dict)
	# 		if aug_sentence:
	# 			pronoun_sentences.append(aug_sentence)
	
    # # wd
	# if (p_wd > 0):
	# 	for _ in range(num_new_per_technique):
	# 		a_words = word_deletion(words, kelas_kata_dict)
	# 		augmented_sentences.append(' '.join(a_words))

	return synonym_sentences