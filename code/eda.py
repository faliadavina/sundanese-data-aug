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
        if char in 'qwertyuiopasdfghjklzxcvbnm1234567890 ':
            clean_line += char
        else:
            clean_line += ' '

    clean_line = re.sub(' +',' ',clean_line) #delete extra spaces
    if clean_line[0] == ' ':
        clean_line = clean_line[1:]
    return clean_line

# ----------------------------------------- #
#											#
#            SYNONYM REPLACEMENT 			#
#											# 
# ----------------------------------------- # 
# MEMBACA KAMUS SUNDANESE SYNONYMS
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

# Digunakan untuk memilih sinonim yang unik dari daftar sinonim yang ada
def get_unique_synonym(word, synonyms_dict, used_synonyms_map):
    all_synonyms = synonyms_dict.get(word, [])
    used_synonyms = used_synonyms_map.get(word, [])

    available_synonyms = [syn for syn in all_synonyms if syn not in used_synonyms]

    if available_synonyms:
        chosen = random.choice(available_synonyms)
        used_synonyms.append(chosen)
    elif all_synonyms:
        chosen = random.choice(all_synonyms)
    else:
        return word

    used_synonyms_map[word] = used_synonyms
    return chosen

file_path_synonym = 'data/kamus/sundanese_synonyms.csv'
synonyms_dict = load_synonyms(file_path_synonym)

# MEMBACA KAMUS PRONOUNS
def load_pronouns(filename):
	try:
		with open(filename, 'r', encoding='utf-8') as file:
			pronouns = [line.strip() for line in file.readlines() if line.strip()]
			return pronouns
	except FileNotFoundError:
		print(f"File {filename} tidak ditemukan.")
		return pronouns

# Path ke file pronouns.txt
file_path_pronouns = 'data/kamus/pronomina.txt'
pronouns_dict = load_pronouns(file_path_pronouns)

# PROSES AUGMENTASI SYNONYM REPLACEMENT, PRONOMINA REPLACEMENT, NUMBER REPLACEMENT
# Pronomina Replacement
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

# Synonym Replacement
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

# Number Replacement 
def number_replacement(sentence): 
	words = sentence.split()
	new_words = []

	for word in words:
		# Pola yang menempel di akhir kata (word2)
		if re.match(r'^[a-zA-Z]+2$', word):  # Mendeteksi kata yang diakhiri '2'
			new_word = word[:-1]  # Hapus angka 2
			new_words.append(f"{new_word}-{new_word}")

		# Pola angka tunggal < 4 angka
		elif re.match(r'^\d{3}$', word):
			new_words.append(str(random.randint(0, 999)))	# Angka diganti dengan angka random
		
		elif re.match(r'^\d{4,}$', word):
			new_words.append(word)	# Angka > 3 digit tidak diubah
		else:
			new_words.append(word)	# Kata lain tidak diubah

	return ' '.join(new_words)	

def is_valid_number_replacement(word):
    """
    Mengecek apakah kata memenuhi syarat untuk number replacement:
    1. Murni angka (misal: '02', '123')
    2. Kata diakhiri angka '2' (misal: 'gara2', 'pasien2')
    """
    # Jika kata adalah angka murni
    if re.match(r'^\d+$', word):  
        return True  

    # Jika kata diakhiri angka '2' (seperti gara2, pasien2, anak2)
    if re.match(r'^[a-zA-Z]+2$', word):  
        return True  

    return False  # Selain itu tidak valid


# ----------------------------------------- #
#											#
#              WORD DELETION 	     		#
#											# 
# ----------------------------------------- # 
def load_kelas_kata(filename):
	kelas_kata = {}
	with open(filename, 'r', encoding='utf-8') as file:
		for line in file:
			kata, kelas = line.strip().split("\t") 
			kelas_kata[kata] = kelas.lower()  # Simpan dalam dictionary dengan kata sebagai key
	return kelas_kata

def get_kelas_kata(word, kelas_kata):
	return kelas_kata.get(word, [])

def word_deletion(words, kelas_kata_dict, num_to_delete):
	#obviously, if there's only three or word less, don't delete it
	if len(words) <= 3:
		return words
	# Identifikasi kata adverbia 
	adverbia_words = [word for word in words if kelas_kata_dict.get(word, "") == 'adverbia']

	if not adverbia_words:
		return words
	
	# Pilih secara acak adverbia yang akan dihapus
	words_to_delete = random.sample(adverbia_words, num_to_delete)
	# Buat kalimat baru tanpa kata-kata yang dihapus
	new_words = [word for word in words if word not in words_to_delete]
	
	return new_words

# file_path_kelas_kata = 'data/kamus/dataset_kelas_kata.txt'
file_path_kelas_kata = 'data/kamus/new_dataset_kelas_kata.txt'
kelas_kata = load_kelas_kata(file_path_kelas_kata)

# ----------------------------------------- #
#											#
#               WORD INSERTION 	  			#
#											# 
# ----------------------------------------- #  
def add_word(new_words, kelas_kata, n_wi): 
	# Cari adjektiva dalam kalimat
	adj_indices = [i for i, word in enumerate(new_words) if get_kelas_kata(word, kelas_kata) == 'adjektiva']
	# adj_words = [new_words[i] for i in adj_indices]

	# Hitung adjektiva
	num_adj = len(adj_indices)

	# Jika tidak ada adjektiva, keluar
	if num_adj == 0: 
		return
	
	n_insertion = min(n_wi, num_adj)
	
	selected_indices = random.sample(adj_indices, n_insertion)

	for idx in selected_indices:
		if (idx > 0 and new_words[idx - 1] == "kacida") or (idx < len(new_words) - 1 and new_words[idx + 1] == "pisan") or (idx < len(new_words) - 1 and new_words[idx + 1] == "teuing"):
			continue  # Lewati jika sudah ada penekanan sebelumnya

		emphasis_word = random.choice(["kacida", "pisan", "teuing"])  # Pilih salah satu secara acak
		
		if emphasis_word == "kacida":
			new_words.insert(idx, emphasis_word)  # Sisipkan sebelum adjektiva
		else:
			new_words.insert(idx + 1, emphasis_word)  # Sisipkan setelah adjektiva

def word_insertion(words, n_wi, kelas_kata):
    new_words = words.copy()
    add_word(new_words, kelas_kata, n_wi)
    return new_words

def eda(sentence, synonyms_dict, kelas_kata_dict, pronouns_dict, alpha_wr, alpha_wd, alpha_wi):
	sentence = get_only_chars(sentence)
	words = sentence.split(' ')
	words = [word for word in words if word != '']
	num_words = len(words)
	swapped_sentences = []
	
	valid_synonym_indices = [i for i, word in enumerate(words) if get_sundanese_synonyms(word, synonyms_dict)]
	valid_number_indices = [i for i, word in enumerate(words) if is_valid_number_replacement(word)]

	all_valid_indices = valid_synonym_indices + valid_number_indices

	if not all_valid_indices:
		return [sentence]
	
	num_to_replace = max(1, int(alpha_wr * len(all_valid_indices)))
	augmented_sentences = []
	remaining_indices = all_valid_indices[:]

	#wr
	if alpha_wr > 0:
		used_synonyms_map = {}		
		while remaining_indices: 
			selected_indices = random.sample(remaining_indices, min(num_to_replace, len(remaining_indices)))
			new_words = words[:]
			modified_indices = []
			synonym_count = 0 
			number_count = 0
			
			print("\n=== Augmentasi Baru ===")
			print(f"Kalimat awal: {sentence}")
			print(f"Kalimat: {words}")
			print(f"Total kata yang bisa dimodifikasi: {len(all_valid_indices)}")
			print(f"Target modifikasi (num_to_replace): {num_to_replace}")
			print(f"Indeks terpilih: {selected_indices}")
			
			for idx in selected_indices: 
				original_word = words[idx]
				if idx in valid_synonym_indices:
					new_words[idx] = get_unique_synonym(original_word, synonyms_dict, used_synonyms_map)
					synonym_count += 1
					print(f"Sinonim: '{original_word}' -> '{new_words[idx]}'")
				elif idx in valid_number_indices:
					new_words[idx] = number_replacement(words[idx])
					number_count += 1
					print(f"Number Replacement: '{original_word}' -> '{new_words[idx]}'")

			modified_indices.append(idx)
			augmented_sentences.append(' '.join(new_words))

			print(f"Jumlah total kata yang diubah: {len(modified_indices)}")
			print(f"Jumlah yang diubah dengan sinonim: {synonym_count}")
			print(f"Jumlah angka yang diubah: {number_count}")
			print(f"Hasil augmentasi: {augmented_sentences}")
			
			remaining_indices = [idx for idx in remaining_indices if idx not in modified_indices]
		
		augmented_sentences.insert(0, sentence)
		return augmented_sentences	
	
    # wd
	if (alpha_wd > 0):
		adverbia_words = [word for word in words if kelas_kata_dict.get(word, "") == 'adverbia']
		# Tentukan jumlah kata yang akan dihapus 
		num_to_delete = min(len(adverbia_words), max(1, int(round(alpha_wd * len(words)))))
		a_words = word_deletion(words, kelas_kata_dict, num_to_delete)
		if a_words: 
			augmented_sentences.append(' '.join(a_words))
		return augmented_sentences if augmented_sentences else [sentence]

	augmented_sentences = [sentence for sentence in augmented_sentences]
	shuffle(augmented_sentences)

	#wi
	if (alpha_wi > 0):
		n_wi = max(1, int(alpha_wi*num_words))
		a_words = word_insertion(words, n_wi, kelas_kata)
		augmented_sentences.append(' '.join(a_words))
		return augmented_sentences
