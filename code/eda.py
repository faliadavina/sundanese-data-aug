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

def load_kelas_kata(filename):
	kelas_kata = {}
	with open(filename, 'r', encoding='utf-8') as file:
		for line in file:
			kata, kelas = line.strip().split("\t") 
			kelas_kata[kata] = kelas.lower()  # Simpan dalam dictionary dengan kata sebagai key
	return kelas_kata

def get_kelas_kata(word, kelas_kata):
	return kelas_kata.get(word, [])

# file_path_kelas_kata = 'data/kamus/dataset_kelas_kata.txt'
file_path_kelas_kata = 'data/kamus/new_dataset_kelas_kata.txt'
kelas_kata = load_kelas_kata(file_path_kelas_kata)

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
    pronouns_category = {}
    category_to_word = {}
    
    try:
        with open(filename, 'r', encoding='utf-8-sig') as file:
            for line in file:
                line = line.strip()
                if not line or '\t' not in line:
                    continue  # Lewati baris kosong atau format tidak valid
                
                word, category = line.split("\t", 1)
                word, category = word.strip(), category.strip()
                
                # Simpan dalam dict pertama
                pronouns_category[word] = category
                
                # Simpan dalam dict kedua
                category_to_word.setdefault(category, []).append(word)
        
        return pronouns_category, category_to_word

    except FileNotFoundError:
        print(f"[ERROR] File '{filename}' tidak ditemukan.")
        return {}, {}

# Path to pronouns.txt file
pronouns_category = {}
category_to_word = {}

file_path_pronouns = 'data/kamus/pronomina.txt'
pronouns_category, category_to_word = load_pronouns(file_path_pronouns)


# PROSES AUGMENTASI SYNONYM REPLACEMENT, PRONOMINA REPLACEMENT, NUMBER REPLACEMENT
# Pronomina Replacement
def pronouns_replacement(words, kelas_dict, pronouns_category, category_to_word):
    new_words = words.copy()  # Salinan kata asli
    modified_indices = []  # Menyimpan indeks yang telah diganti

    # Temukan semua kata pronomina
    for i, word in enumerate(words):
        clean_word = word.strip().lower()
        print(f"Memeriksa kata: {clean_word}")  # Debugging
        if kelas_dict.get(clean_word) == 'pronomina' and clean_word in pronouns_category:
            category = pronouns_category.get(clean_word)

            if not category:
                print(f"Kategori tidak ditemukan untuk {clean_word}")  # Debugging
                continue

            print(f"Kategori ditemukan untuk {clean_word}: {category}")  # Debugging

            # Cari pengganti di kategori yang sama, selain kata aslinya
            candidates = [w for w in category_to_word.get(category, []) if w != clean_word]
            if candidates:
                replacement = random.choice(candidates)
                new_words[i] = replacement
                modified_indices.append(i)
                print(f"[PRONOUN] '{clean_word}' diganti jadi '{replacement}'")  # Debugging
            else:
                print(f"Tidak ada pengganti untuk {clean_word} dalam kategori {category}")  # Debugging

    return new_words, modified_indices

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
def number_replacement(words):
    number_indexes = []

    for i, word in enumerate(words):
        replace, tipe = is_valid_number(word)
        if replace:
            number_indexes.append((i, tipe))

    random.shuffle(number_indexes)

    modified_indices = []
    new_words = words.copy()

    for i, tipe in number_indexes:
        if tipe == 'satuan':
            new_words[i] = str(random.randint(1, 9))
        elif tipe == 'puluhan':
            new_words[i] = str(random.choice(range(10, 100, 5)))
        elif tipe == 'ratusan':
            new_words[i] = str(random.choice(range(100, 1000, 50)))
        elif tipe == 'ribuan':
            new_words[i] = str(random.choice(range(1000, 10000, 1000)))
        modified_indices.append(i)
        break  # hanya satu penggantian

    return new_words, modified_indices

def is_valid_number(word):
    if(
        re.search(r'[\-@%#).,]', word) or
        re.match(r'^[a-zA-Z]+\d+$', word) or
        re.match(r'^\d+[a-zA-Z]+$', word) or
        re.search(r'[a-zA-Z]+\d+[a-zA-Z]*', word) or
        (re.match(r'^\d{4}$', word) and 1900 <= int(word) <= 2099)
    ):
        return False, None
    
    if word.isdigit():
        n = int(word)
        if n < 10:
            return True, 'satuan'
        elif n < 100:
            return True, 'puluhan'
        elif n < 1000: 
            return True, 'ratusan'
        else:
            return True, 'ribuan'
    return False, None

# ----------------------------------------- #
#											#
#              WORD INSERTION 	     		#
#											# 
# ----------------------------------------- # 
def add_word(new_words, selected_indices, kelas_kata):
    print(f"\n--- Starting add_word ---")
    for idx in sorted(selected_indices):
        word = new_words[idx]
        kelas = get_kelas_kata(word, kelas_kata)

        if kelas == "adjektiva":
            rule = random.choice(["a", "b", "c"])
            print(f"\n[INDEX: {idx}] Word: '{word}', Class: {kelas}, Rule chosen: {rule}")

            if rule == "a":
                if idx > 0 and new_words[idx - 1] in ["kacida", "leuwih", "mani"]:
                    print("  -> Skipped (rule a): emphatic word already before.")
                    continue
                emph_word = random.choice(["kacida", "leuwih", "mani"])
                new_words.insert(idx, emph_word)
                print(f"  -> Inserted before: '{emph_word}'")

            elif rule == "b":
                if idx < len(new_words) - 1 and new_words[idx + 1] in ["pisan", "teuing"]:
                    print("  -> Skipped (rule b): emphatic word already after.")
                    continue
                emph_word = random.choice(["pisan", "teuing"])
                new_words.insert(idx + 1, emph_word)
                print(f"  -> Inserted after: '{emph_word}'")

            elif rule == "c":
                pohara_phrase = f"pohara {word}na"
                new_words[idx] = pohara_phrase
                print(f"  -> Replaced with: '{pohara_phrase}'")

        elif kelas == "verba":
            rule = "d"
            print(f"\n[INDEX: {idx}] Word: '{word}', Class: {kelas}, Rule applied: {rule}")
            
            if idx > 0 and new_words[idx - 1] == "bari":
                print("  -> Skipped (rule d): 'bari' already exists before.")
                continue
            new_words.insert(idx, "bari")
            print(f"  -> Inserted 'bari' before '{word}'")

    print(f"\nFinal sentence after add_word: {' '.join(new_words)}")
    return new_words

def word_insertion(words, selected_indices, kelas_kata):
    print(f"\nOriginal words: {' '.join(words)}")
    new_words = words.copy()
    new_words = add_word(new_words, selected_indices, kelas_kata)
    print(f"After word_insertion: {' '.join(new_words)}\n")
    return new_words

# ----------------------------------------- #
#											#
#              WORD DELETION 	     		#
#											# 
# ----------------------------------------- # 

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

# ----------------------------------------- #
#											#
#              WORD MOVEMENT 	     		#
#											# 
# ----------------------------------------- # 
def load_adverbia(filepath):
    time_adverb = []
    with open(filepath, 'r', encoding='utf-8') as f:
        time_adverb = [line.strip().lower() for line in f if line.strip()]
    return time_adverb

file_path_adverbia = 'data/kamus/adverbia.txt'
time_adverb = load_adverbia(file_path_adverbia)

pronomina = [k for k, v in kelas_kata.items() if v == 'pronomina']
admin_keywords = {"kota", "kabupaten", "desa", "provinasi", "kecamatan", "kelurahan", "negara", "alam"}

def get_position(sentence, phrase):
    if sentence.startswith(phrase):
        return "awal"
    elif sentence.endswith(phrase):
        return "akhir"
    else:
        return "tengah"

def find_adverbia(sentence):
    tokens = sentence.lower().split()
    time_adverbials = []
    place_adverbials = []

    for i in range(len(tokens)):
        for j in range(1,4):
            multi_word = ' '.join(tokens[i:i+j])
            if multi_word in time_adverb:
                time_adverbials.append((multi_word, get_position(sentence, multi_word)))

    for i in range(len(tokens)):
        if tokens[i] in ["di", "ka", "ti"]:
            if i+1 < len(tokens) and tokens[i+1] in admin_keywords:
                for j in range(2, 4):
                    end = i + j
                    if end <= len(tokens):
                        phrase = ' '.join(tokens[i:end])
                        place_tokens = tokens[i+1:end]
                        place_adverbials.append((phrase, get_position(sentence, phrase)))
            
            for j in range(1, 4):
                end = i + j + 1
                if end <= len(tokens):
                    phrase = ' '.join(tokens[i:end])
                    place_tokens = tokens[i+1:end]
                    if place_tokens and all(w in kelas_kata and kelas_kata[w] in ["nomina", "adjektiva"] for w in place_tokens):
                        place_adverbials.append((phrase, get_position(sentence, phrase)))

    return time_adverbials, place_adverbials

def word_movement(sentence, adverbials_to_move):
    if not adverbials_to_move:
        return sentence
    
    tokens = sentence.strip().split()
    word_of_pronouns = [i for i, t in enumerate(tokens) if t.lower() in pronomina]
    subject_idx = word_of_pronouns[0] if word_of_pronouns else 0

    if word_of_pronouns:
         print(f"[WM] Found subject: '{tokens[subject_idx]}' at index {subject_idx}")
    else:
        print("[WM] No subject found, using index 0 as default.")

    for phrase, first_position in adverbials_to_move:
        tokens_phrase = phrase.split()
        len_phrase = len(tokens_phrase)

        for i in range(len(tokens) - len_phrase + 1):
            if tokens[i:i + len_phrase] == tokens_phrase:
                tokens = tokens[:i] + tokens[i + len_phrase:]
                break
        
        position = ["awal", "tengah", "akhir"]
        if first_position in position:
            position.remove(first_position)
        new_position = random.choice(position)

        if new_position == "awal":
            tokens = tokens_phrase + tokens
        elif new_position == "tengah":
            pred_idx = next((i for i in range(subject_idx + 1, len(tokens)) if get_kelas_kata(tokens[i], kelas_kata) == "verba"), None)
            if pred_idx and pred_idx > subject_idx:
                insert_pos = subject_idx + 1
            else:
                insert_pos = len(tokens)
            tokens = tokens[:insert_pos] + tokens_phrase + tokens[insert_pos:]
        elif new_position == "akhir":
            tokens = tokens + tokens_phrase

    return ' '.join(tokens)

def eda(sentence, synonyms_dict, kelas_dict, alpha_wr, alpha_wd, alpha_wi, alpha_wm):
    sentence = get_only_chars(sentence)
    words = sentence.split()
    words = [word for word in words if word]

    augmented_sentences = []
    original_sentence = ' '.join(words)

    # ======== Word Replacement (WR) ========
    if alpha_wr > 0:
        valid_synonym_indices = [i for i, word in enumerate(words) if get_sundanese_synonyms(word, synonyms_dict)]
        valid_number_indices = [i for i, word in enumerate(words) if is_valid_number(word)]
        all_valid_indices = valid_synonym_indices + valid_number_indices

        if all_valid_indices:
            num_to_replace = max(1, int(alpha_wr * len(all_valid_indices)))
            used_synonyms_map = {}
            remaining_indices = all_valid_indices[:]

            # Kumpulkan hasil synonym replacement (plus number replacement) dulu
            while remaining_indices:
                selected_indices = random.sample(remaining_indices, min(num_to_replace, len(remaining_indices)))
                new_words = words[:]
                for idx in selected_indices:
                    if idx in valid_synonym_indices:
                        new_words[idx] = get_unique_synonym(words[idx], synonyms_dict, used_synonyms_map)
                    elif idx in valid_number_indices:
                        new_words, _ = number_replacement(new_words)
                augmented_sentences.append(' '.join(new_words))
                remaining_indices = [i for i in remaining_indices if i not in selected_indices]

            # Setelah semua WR selesai, baru apply pronomina ke hasil2 WR tadi (tanpa nambah kalimat baru)
            for i in range(len(augmented_sentences)):
                temp_words = augmented_sentences[i].split(' ')
                temp_words, _ = pronouns_replacement(temp_words, kelas_dict, pronouns_category, category_to_word)
                augmented_sentences[i] = ' '.join(temp_words)

            print(f"Hasil WR (synonym + number + pronoun): {len(augmented_sentences)}")
        else:
            print("Tidak ada kata yang bisa dimodifikasi untuk WR.")


    # ======== Word Deletion (WD) ========
    if alpha_wd > 0:
        sentence = get_only_chars(sentence)
        adverbia_words = [word for word in words if kelas_dict.get(word, "") == 'adverbia']
        num_to_delete = min(len(adverbia_words), max(1, int(round(alpha_wd * len(words)))))
        deleted_words = word_deletion(words, kelas_dict, num_to_delete)
        if deleted_words:
            augmented_sentences.append(' '.join(deleted_words))


    # ======== Word Insertion (wi) ========
    if alpha_wi > 0:
        adj_indices = [i for i, word in enumerate(words) if get_kelas_kata(word, kelas_dict) == 'adjektiva']
        verb_indices = [i for i, word in enumerate(words) if get_kelas_kata(word, kelas_dict) == 'verba']
        total_candidates = adj_indices + verb_indices

        print(f"Adjektiva indices: {adj_indices}")
        print(f"Verba indices: {verb_indices}")
        print(f"Total candidates for word insertion: {total_candidates}")

        if not total_candidates:
            print("No candidate words found for insertion.")
            return [sentence]

        n_wi = max(1, int(round(alpha_wi * len(total_candidates))))
        print(f"Number of words to insert (n_wi): {n_wi}")

        selected_indices = random.sample(total_candidates, min(n_wi, len(total_candidates)))
        print(f"Selected indices for insertion: {selected_indices}")

        new_words = words.copy()
        print(f"Original sentence: {' '.join(new_words)}")

        new_words = add_word(new_words, selected_indices, kelas_dict)
        print(f"Augmented sentence: {' '.join(new_words)}")

        augmented_sentences.append(' '.join(new_words))
        

    # ======== Word Movement (wm) ========
    if alpha_wm > 0: 
        print(f"\n>>> [WM] Processing sentence: '{original_sentence}'")
        time_adverb, place_adverb = find_adverbia(original_sentence)
        
        print(f"[WM] Detected time adverbials: {time_adverb}")
        print(f"[WM] Detected place adverbials: {place_adverb}")
        
        all_adverbials = time_adverb + place_adverb
        
        if all_adverbials:
            n_move = max(1, round(alpha_wm * len(all_adverbials)))
            selected_adverbials = random.sample(all_adverbials, min(n_move, len(all_adverbials)))
            print(f"Selected adverbials for movement: {selected_adverbials}")
            moved_sentence = word_movement(original_sentence, selected_adverbials)
            print(f"[WM] Moved sentence: '{moved_sentence}'\n")
            augmented_sentences.append(moved_sentence)
        else: 
            print("[WM] No adverbials found for movement.")

    # ======== Return ========
    return [original_sentence] + augmented_sentences if augmented_sentences else [original_sentence]
