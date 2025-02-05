import pandas as pd
import random 
from random import shuffle

#stop words list
stop_words = [
    "tapi", "sanajan", "salain", "ti", "ku", "kituna", "sabalikna", "malah", "saenggeus", "kitu", "boh", 
    "lain", "bae", "duka", "rek", "bari", "lantaran", "asal", "dina", "siga", "keur", "saha", "eukeur", 
    "wae", "atuh", "kawas", "lamun", "erek", "isuk", "beurang", "peuting", "kamari", "wanci", "burit", 
    "tengah", "teuing", "apal", "buleud", "taneuh", "kulon", "wetan", "kaler", "kidul", "saha", "naon", 
    "mana", "naha", "iraha", "kumaha", "sabaraha", "ieu", "eta", "dieu", "kieu", "jeung", "sareng", "nepi", 
    "jaba", "lian", "lamun", "tapi", "atawa", "atanapi", "tuluy", "terus", "teras", "yen", "majar", "nu", 
    "anu", "matak", "majar", "teh", "mah", "seug", "heug", "mun", "ketah", "ketang", "pisan", "sok", "be", 
    "wae", "we", "weh", "mung", "ngan", "ukur", "keur", "nuju", "masih", "keneh", "pikeun", "kanggo", "da", 
    "kapan", "kapanan", "apan", "pan", "apanan", "deui", "deuih", "ge", "oge", "ongkoh", "nya", "nyah", 
    "enya", "lain", "sanes", "abi", "euy", "dan", "na", "ari", "sama", "ka", "ku", "lah", "atuh", "da", 
    "aduh", "ini", "we", "weh", "ada", "adanya", "adalah", "adapun", "agak", "agaknya", "agar", "akan", 
    "akankah", "akhirnya", "aku", "akulah", "amat", "amatlah", "anda", "andalah", "antar", "diantaranya", 
    "antara", "antaranya", "diantara", "apa", "apaan", "mengapa", "apabila", "apakah", "apalagi", "apatah", 
    "atau", "ataukah", "ataupun", "bagai", "bagaikan", "sebagai", "sebagainya", "bagaimana", "bagaimanapun", 
    "sebagaimana", "bagaimanakah", "bagi", "bahkan", "bahwa", "bahwasanya", "sebaliknya", "banyak", 
    "sebanyak", "beberapa", "seberapa", "begini", "beginian", "beginikah", "beginilah", "sebegini", 
    "begitu", "begitukah", "begitulah", "begitupun", "sebegitu", "belum", "belumlah", "sebelum", 
    "sebelumnya", "sebenarnya", "berapa", "berapakah", "berapalah", "berapapun", "betulkah", "sebetulnya", 
    "biasa", "biasanya", "bila", "bilakah", "bisa", "bisakah", "sebisanya", "boleh", "bolehkah", 
    "bolehlah", "buat", "bukan", "bukankah", "bukanlah", "bukannya", "cuma", "percuma", "dahulu", 
    "dalam", "dan", "dapat", "dari", "daripada", "dekat", "demi", "demikian", "demikianlah", "sedemikian", 
    "dengan", "depan", "di", "dia", "dialah", "dini", "diri", "dirinya", "terdiri", "dong", "dulu", 
    "enggak", "enggaknya", "entah", "entahlah", "terhadap", "terhadapnya", "hal", "hampir", "hanya", 
    "hanyalah", "harus", "haruslah", "harusnya", "seharusnya", "hendak", "hendaklah", "hendaknya", 
    "hingga", "sehingga", "ia", "ialah", "ibarat", "ingin", "inginkah", "inginkan", "ini", "inikah", 
    "inilah", "itu", "itukah", "itulah", "jangan", "jangankan", "janganlah", "jika", "jikalau", "juga", 
    "justru", "kala", "kalau", "kalaulah", "kalaupun", "kalian", "kami", "kamilah", "kamu", "kamulah", 
    "kan", "kapan", "kapankah", "kapanpun", "dikarenakan", "karena", "karenanya", "ke", "kecil", 
    "kemudian", "kenapa", "kepada", "kepadanya", "ketika", "seketika", "khususnya", "kini", "kinilah", 
    "kiranya", "sekiranya", "kita", "kitalah", "kok", "lagi", "lagian", "selagi", "lah", "lain", 
    "lainnya", "melainkan", "selaku", "lalu", "melalui", "terlalu", "lama", "lamanya", "selama", 
    "selama", "selamanya", "lebih", "terlebih", "bermacam", "macam", "semacam", "maka", "makanya", 
    "makin", "malah", "malahan", "mampu", "mampukah", "mana", "manakala", "manalagi", "masih", 
    "masihkah", "semasih", "masing", "mau", "maupun", "semaunya", "memang", "mereka", "merekalah", 
    "meski", "meskipun", "semula", "mungkin", "mungkinkah", "nah", "namun", "nanti", "nantinya", 
    "nyaris", "oleh", "olehnya", "seorang", "seseorang", "pada", "padanya", "padahal", "paling", 
    "sepanjang", "pantas", "sepantasnya", "sepantasnyalah", "para", "pasti", "pastilah", "per", 
    "pernah", "pula", "pun", "merupakan", "rupanya", "serupa", "saat", "saatnya", "sesaat", "saja", 
    "sajalah", "saling", "bersama", "sama", "sesama", "sambil", "sampai", "sana", "sangat", "sangatlah", 
    "saya", "sayalah", "se", "sebab", "sebabnya", "sebuah", "tersebut", "tersebutlah", "sedang", 
    "sedangkan", "sedikit", "sedikitnya", "segala", "segalanya", "segera", "sesegera", "sejak", 
    "sejenak", "sekali", "sekalian", "sekalipun", "sesekali", "sekaligus", "sekarang", "sekarang", 
    "sekitar", "sekitarnya", "sela", "selain", "selalu", "seluruh", "seluruhnya", "semakin", 
    "sementara", "sempat", "semua", "semuanya", "sendiri", "sendirinya", "seolah", "seperti", 
    "sepertinya", "sering", "seringnya", "serta", "siapa", "siapakah", "siapapun", "disini", 
    "disinilah", "sini", "sinilah", "sesuatu", "sesuatunya", "suatu", "sesudah", "sesudahnya", 
    "sudah", "sudahkah", "sudahlah", "supaya", "tadi", "tadinya", "tak", "tanpa", "setelah", 
    "telah", "tentang", "tentu", "tentulah", "tentunya", "tertentu", "seterusnya", "tapi", "tetapi", 
    "setiap", "tiap", "setidaknya", "tidak", "tidakkah", "tidaklah", "toh", "waduh", "wah", 
    "wahai", "sewaktu", "walau", "walaupun", "wong", "yaitu", "yakni", "yang", "gera", "ga", 
    "ya", "geus", "si", "kang", "punya", "ni", "asa", "dek", "fans", "haha", "hahaha", "hahahaaa", 
    "ha", "hahaha", "wk", "wkw", "wkwk", "wkwkw", "wkwkwk", "wkwkwkw", "wkwkwkwk", "wkwkwkwkw", 
    "wkwkwkwkwk"
]

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

# synonym_replacement digunakan untuk mengganti n kata dalam kalimat dengan sinonim dari kata tersebut
def synonym_replacement(words, n, synonyms_dict, stop_words):
	new_words = words.copy()
	random_word_list = list(set([word for word in words if word not in stop_words]))
	random.shuffle(random_word_list)
	num_replaced = 0

	for random_word in random_word_list:
		# dapatkan sinonim dari kata tersebut, termasuk reverse synonyms
		synonyms = get_sundanese_synonyms(random_word, synonyms_dict)
		if len(synonyms) >= 1:
			# pilih sinonim secara acak
			synonym = random.choice(list(synonyms))
			new_words = [synonym if word == random_word else word for word in new_words]
			print("replaced", random_word, "with", synonym)
			num_replaced += 1
			
		if num_replaced >= n: #only replace up to n words
			break

	#this is stupid but we need it, trust me
	sentence = ' '.join(new_words)
	new_words = sentence.split(' ')

	return new_words

file_path_synonym = 'data/sundanese_synonyms.csv'
sundanese_synonyms = load_synonyms(file_path_synonym)

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
	

def eda(sentence, synonyms_dict, kelas_kata_dict, alpha_sr=0.1, p_wd=0.1, alpha_wi=0.1, num_aug=9):
	# sentence = get_only_chars(sentence)
	words = sentence.split(' ')
	words = [word for word in words if word != '']
	num_words = len(words)
	
	augmented_sentences = []
	num_new_per_technique = int(num_aug/4)+1

	# Track jumlah kalimat per operasi 
	num_unchanged = 0 

	#sr
	if (alpha_sr > 0):
		n_sr = max(1, int(alpha_sr*num_words))	# Jumlah kata yang akan diganti dengan sinonim
		for _ in range(num_new_per_technique):
			a_words = synonym_replacement(words, n_sr, synonyms_dict, stop_words)
			augmented_sentences.append(' '.join(a_words))


    # wd
	if (p_wd > 0):
		for _ in range(num_new_per_technique):
			a_words = word_deletion(words, kelas_kata_dict)
			augmented_sentences.append(' '.join(a_words))
			
	# augmented_sentences = [get_only_chars(sentence) for sentence in augmented_sentences]
	augmented_sentences = [sentence for sentence in augmented_sentences]
	shuffle(augmented_sentences)
	
	#wi
	if (alpha_wi > 0):
		n_ri = max(1, int(alpha_wi*num_words))
		for _ in range(num_new_per_technique):
			a_words = word_insertion(words, n_ri, synonyms_dict)
			augmented_sentences.append(' '.join(a_words))

	#trim so that we have the desired number of augmented sentences
	if num_aug >= 1:
		augmented_sentences = augmented_sentences[:num_aug]
	else:
		keep_prob = num_aug / len(augmented_sentences)
		augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

	return augmented_sentences