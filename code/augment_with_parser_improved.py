# ==============================================================================
# IMPROVED Augmentasi Data Bahasa Sunda dengan Multiple Strategies
# ==============================================================================

import argparse
import random
import re
import pandas as pd
from collections import defaultdict
import sys
import copy
from pprint import pprint

# Impor grammar dari file sundanese_cfg.py
from sundanese_cfg import grammar, TERMINALS

# --------------------------------------------------------------------------
# IMPROVED PARSER dengan Partial Parsing Support
# --------------------------------------------------------------------------
class ImprovedSundaneseParser:
    def __init__(self, grammar, lexicon, daftar_tempat):
        self.grammar = grammar
        self.lexicon = lexicon
        self.daftar_tempat = daftar_tempat
        self._memo = {}

    def _get_pos(self, word):
        return self.lexicon.get(word.lower())

    def parse_with_fallback(self, sentence): # PERBAIKAN: Nama fungsi ini yang dipanggil di main
        """
        Multi-strategy parsing:
        1. Try full CFG parsing
        2. Try partial parsing
        3. Use POS-based simple parsing
        """
        self._memo.clear()
        print(f"\n===> Parsing: '{sentence}'")
        words = sentence.lower().split()
        
        tokens_with_pos = []
        for word in words:
            pos = self._get_pos(word)
            if not pos:
                pos = 'UNK'
            tokens_with_pos.append((word, pos))

        print(f"     > Tokens: {tokens_with_pos}")

        # Strategy 1: Full CFG parsing
        parse_tree, remaining_index = self._parse_non_terminal('Kalimat', tokens_with_pos, 0)
        if parse_tree and remaining_index == len(tokens_with_pos):
            print(f"     > [FULL] CFG parsing berhasil")
            return parse_tree, 'full'

        # Strategy 2: Partial CFG parsing (accept if covers >50% of sentence)
        if parse_tree and remaining_index > len(tokens_with_pos) * 0.5:
            print(f"     > [PARTIAL] CFG parsing berhasil {remaining_index}/{len(tokens_with_pos)} tokens")
            return parse_tree, 'partial'

        # Strategy 3: Simple POS-based parsing
        simple_tree = self._create_simple_pos_tree(tokens_with_pos)
        print(f"     > [SIMPLE] POS-based parsing")
        return simple_tree, 'simple'

    def _create_simple_pos_tree(self, tokens_with_pos):
        """Create simple tree based on POS tags only"""
        children = []
        for word, pos in tokens_with_pos:
            if pos in TERMINALS:
                children.append([pos, word])
            else:
                children.append(['UNK', word])
        return ['SimpleSentence'] + children

    def _parse_non_terminal(self, non_terminal, tokens, index):
        key = (non_terminal, index)
        if key in self._memo:
            return self._memo[key]

        if non_terminal == 'EntitasTempat':
            # PENAMBAHAN: Memanggil fungsi greedy_match_tempat yang sudah didefinisikan
            matched_str, matched_len = greedy_match_tempat(
                [w for w, _ in tokens], index, self.daftar_tempat
            )
            if matched_str:
                result = (['EntitasTempat', matched_str], index + matched_len)
                self._memo[key] = result
                return result

        if non_terminal in self.grammar:
            best_match_children = None
            best_match_len = -1

            for rule in self.grammar[non_terminal]:
                children, next_index = self._parse_rule(rule, tokens, index)
                if children is not None:
                    match_len = next_index - index
                    if match_len > best_match_len:
                        best_match_len = match_len
                        best_match_children = children

            if best_match_children is not None:
                final_next_index = index + best_match_len
                sub_tree = [non_terminal] + best_match_children
                result = (sub_tree, final_next_index)
                self._memo[key] = result
                return result

        return None, index

    def _parse_rule(self, rule, tokens, index):
        children = []
        current_index = index
        for part in rule:
            sub_tree, next_index = self._parse_part(part, tokens, current_index)
            if sub_tree is None:
                return None, index
            children.append(sub_tree)
            current_index = next_index
        return children, current_index

    def _parse_part(self, part, tokens, index):
        if part in self.grammar:
            return self._parse_non_terminal(part, tokens, index)
        else:
            if index < len(tokens):
                word, pos = tokens[index]
                is_pos_match = (part in TERMINALS and pos == part)
                is_literal_match = (part not in TERMINALS and word == part)
                    
                if is_pos_match or is_literal_match:
                    label = pos if is_pos_match else part
                    return ([label, word], index + 1)
            return None, index

def tree_to_sentence(tree):
    if not isinstance(tree, list) or not tree:
        return ""
    if len(tree) == 2 and not isinstance(tree[1], list):
        return tree[1]
    parts = [tree_to_sentence(child) for child in tree[1:]]
    return ' '.join(filter(None, parts))


# --------------------------------------------------------------------------
# FUNGSI-FUNGSI BANTUAN
# --------------------------------------------------------------------------
def get_only_chars(line):
    clean_line = ""
    line = line.replace("’", "").replace("'", "")
    line = line.replace("\t", " ").replace("\n", " ") 
    
    line = line.lower()
    for char in line:
        if char in 'qwertyuiopasdfghjklzxcvbnm1234567890-':
            clean_line += char
        else:
            clean_line += ' '
            
    clean_line = re.sub(' +', ' ', clean_line)
    if clean_line and clean_line[0] == ' ':
        clean_line = clean_line[1:]
    return clean_line

def load_kelas_kata(filepath, file_entitas_tempat=None):
    kelas_kata_dict = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                kata, kelas = parts[0].strip(), parts[1].strip()
                if kata in ['jeung', 'katut', 'atawa', 'boh', 'tur', 'nu']:
                    kelas = kata
                kelas_kata_dict[kata] = kelas

    daftar_tempat_set = set()
    if file_entitas_tempat:
        with open(file_entitas_tempat, 'r', encoding='utf-8') as f:
            for line in f:
                tempat = line.strip().lower()
                daftar_tempat_set.add(tempat)
                for word in tempat.split():
                    if word not in kelas_kata_dict:
                        kelas_kata_dict[word] = 'nomina'
    return kelas_kata_dict, daftar_tempat_set

def greedy_match_tempat(tokens, index, daftar_tempat):
    """
    Melakukan pencocokan greedy dari token[index] ke depan, mencari frasa tempat
    terpanjang yang cocok di daftar_tempat.
    """
    max_len = len(tokens) - index
    for l in range(max_len, 0, -1):
        candidate = ' '.join(tokens[index:index + l])
        print(f"    >> Mencoba greedy match tempat: '{candidate}'")
        if candidate in daftar_tempat: 
            return candidate, l
    print(f"    >> Tidak ditemukan frasa tempat yang cocok setelah preposisi. ")
    return None, 0

def load_synonyms(file_path):
    synonyms_dict = defaultdict(list)
    try:
        data = pd.read_csv(file_path)
        for _, row in data.iterrows():
            word = row['kata']
            syns = [s.strip() for s in str(row['sinonim']).split(',')]
            synonyms_dict[word].extend(syns)
    except Exception as e:
        print(f"Error memuat sinonim: {e}")
    return synonyms_dict


def load_pronouns(file_path):
    kata_ke_kategori = {}
    kategori_ke_kata = defaultdict(list)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    kata, kategori = parts[0].strip(), parts[1].strip()
                    kata_ke_kategori[kata] = kategori
                    kategori_ke_kata[kategori].append(kata)
        return kata_ke_kategori, kategori_ke_kata
    except FileNotFoundError:
        print(f"[ERROR] File pronomina tidak ditemukan di: '{file_path}'")
        return {}, defaultdict(list)
# ==========================================================================
# AUGMENTASI BERBASIS STRUKTUR SINTAKSIS (DENGAN PERBAIKAN STRUKTUR POHON)
# ==========================================================================

def find_opportunities(node, target_node_types):
    """Fungsi rekursif umum untuk mencari semua node dengan tipe tertentu."""
    opportunities = []
    if not isinstance(node, list) or not node: return []
    if node[0] in target_node_types: opportunities.append(node)
    for child in node[1:]:
        if isinstance(child, list):
            opportunities.extend(find_opportunities(child, target_node_types))
    return opportunities

class AugmentationController:
    def __init__(self, grammar, lexicon, synonyms, pronomina_map):
        self.grammar = grammar
        self.lexicon = lexicon
        self.synonyms = synonyms
        self.pronomina_kata_ke_kategori, self.pronomina_kategori_ke_kata = pronomina_map
        self.adjektiva_list = [k for k, v in lexicon.items() if v == 'adjektiva']

    def _get_words_from_grammar(self, non_terminal):
        """PERBAIKAN: Mengambil semua kata literal dari sebuah aturan non-terminal."""
        words = []
        if non_terminal in self.grammar:
            for rule in self.grammar[non_terminal]:
                # Memastikan rule hanya berisi satu elemen string (terminal)
                if len(rule) == 1 and isinstance(rule[0], str):
                    words.append(rule[0])
        return words

    def _replace_node_word(self, node_to_replace):
        """Logika penggantian untuk satu node, memodifikasi node secara langsung."""
        node_type = node_to_replace[0]
        original_word = node_to_replace[1]

        if node_type == 'pronomina':
            kategori = self.pronomina_kata_ke_kategori.get(original_word)
            if not kategori: return
            kandidat_lain = [k for k in self.pronomina_kategori_ke_kata.get(kategori, []) if k != original_word]
            if kandidat_lain:
                kata_baru = random.choice(kandidat_lain)
                node_to_replace[1] = kata_baru
                print(f"       > [REPLACEMENT-PRONOUN] Mengganti '{original_word}' -> '{kata_baru}'")

        elif node_type == 'numeralia':
            try:
                num = int(original_word)
                if 1 <= num <= 9: new_num = random.randint(1,9)
                elif 10 <= num <= 99: new_num = random.randint(10,99)
                else: new_num = num + random.randint(-5, 5)
                node_to_replace[1] = str(new_num)
                print(f"       > [REPLACEMENT-NUMERAL] Mengganti '{original_word}' -> '{new_num}'")
            except ValueError: pass

        elif node_type in ['nomina', 'verba', 'adjektiva']:
            possible_synonyms = [s for s in self.synonyms.get(original_word, []) if s != original_word]
            if possible_synonyms:
                new_word = random.choice(possible_synonyms)
                if self.lexicon.get(new_word) == node_type:
                    node_to_replace[1] = new_word
                    print(f"       > [REPLACEMENT-SYNONYM] Mengganti '{original_word}' -> '{new_word}'")
    
    def replacement(self, tree, alpha):
        new_tree = copy.deepcopy(tree)
        target_types = {'nomina', 'verba', 'adjektiva', 'pronomina', 'numeralia'}
        opportunities = find_opportunities(new_tree, target_types)
        if not opportunities: return new_tree
        num_to_modify = round(alpha * len(opportunities))
        if num_to_modify == 0 and alpha > 0 and len(opportunities) > 0: num_to_modify = 1
        nodes_to_modify = random.sample(opportunities, min(num_to_modify, len(opportunities)))
        for node in nodes_to_modify: self._replace_node_word(node)
        return new_tree
    
    def _transform_nomina(self, node):
        if self.adjektiva_list:
            adjektiva_baru = random.choice(self.adjektiva_list)
            # PERBAIKAN: Memastikan struktur pohon yang baru benar
            new_children = node[1:] + [['partikelNu', 'nu'], ['adjektiva', adjektiva_baru]]
            node[1:] = new_children
            print(f"       > [INSERTION-NOMINA] Menambah 'nu {adjektiva_baru}'")

    def _transform_adjektiva(self, node):
        # PERBAIKAN: Menambahkan pengecekan untuk menghindari IndexError
        original_adjektiva_nodes = find_opportunities(node, {'adjektiva'})
        if not original_adjektiva_nodes: return
        original_adjektiva_node = original_adjektiva_nodes[0]
        original_word = original_adjektiva_node[1]
        
        panganteb_list = self._get_words_from_grammar('PangantebTingkat1')
        if not panganteb_list: return
        panganteb = random.choice(panganteb_list)

        # PERBAIKAN: Membangun ulang node dengan struktur yang benar
        node[1:] = [] 
        node.extend([['PangantebTingkat1', panganteb], original_adjektiva_node])
        print(f"       > [INSERTION-ADJ] Menjadi Tingkat 1: '{panganteb} {original_word}'")

    def _transform_verba(self, node):
        # PERBAIKAN: Menambahkan pengecekan untuk menghindari IndexError
        original_verba_nodes = find_opportunities(node, {'verba'})
        if not original_verba_nodes: return
        original_verba_node = original_verba_nodes[0]
        
        tipe_transformasi = random.choice(['aspek', 'modalitas'])
        if tipe_transformasi == 'aspek':
            kecap_aspek_list = self._get_words_from_grammar('KecapAspek')
            if not kecap_aspek_list: return
            kecap_aspek = random.choice(kecap_aspek_list)
            # PERBAIKAN: Membangun ulang node dengan struktur yang benar
            node[1:] = []
            node.extend([['KecapAspek', kecap_aspek], original_verba_node])
            print(f"       > [INSERTION-VERBA] Menambah Aspek: '{kecap_aspek}'")
        else:
            kecap_modalitas_list = self._get_words_from_grammar('KecapModalitas')
            if not kecap_modalitas_list: return
            kecap_modalitas = random.choice(kecap_modalitas_list)
            # PERBAIKAN: Membangun ulang node dengan struktur yang benar
            node[1:] = []
            node.extend([['KecapModalitas', kecap_modalitas], original_verba_node])
            print(f"       > [INSERTION-VERBA] Menambah Modalitas: '{kecap_modalitas}'")

    def insertion(self, tree, alpha):
        new_tree = copy.deepcopy(tree)
        opp_nomina = find_opportunities(new_tree, {'FrasaNomina'})
        opp_adjektiva = find_opportunities(new_tree, {'FrasaAdjektiva'})
        opp_verba = find_opportunities(new_tree, {'FrasaVerba'})
        all_opportunities = [('nomina', n) for n in opp_nomina] + \
                            [('adjektiva', a) for a in opp_adjektiva] + \
                            [('verba', v) for v in opp_verba]
        if not all_opportunities: return new_tree
        num_to_modify = round(alpha * len(all_opportunities))
        if num_to_modify == 0 and alpha > 0: num_to_modify = 1
        nodes_to_modify = random.sample(all_opportunities, min(num_to_modify, len(all_opportunities)))
        for node_type, node in nodes_to_modify:
            if node_type == 'nomina': self._transform_nomina(node)
            elif node_type == 'adjektiva': self._transform_adjektiva(node)
            elif node_type == 'verba': self._transform_verba(node)
        return new_tree
    
    def deletion(self, tree, alpha):
        new_tree = copy.deepcopy(tree)
        target_types = {'Keterangan', 'adverbia'}
        opportunities = find_opportunities(new_tree, target_types)

        if not opportunities: return new_tree

        num_to_modify = round(alpha * len(opportunities))
        if num_to_modify == 0 and alpha > 0: num_to_modify = 1

        nodes_to_delete = random.sample(opportunities, min(num_to_modify, len(opportunities)))

        def _delete_recursive(current_node, nodes_to_remove):
            if not isinstance(current_node, list): return current_node
            if any(current_node is n for n in nodes_to_remove):
                print(f"    > [DELETION] Menghapus node:  {current_node[0]}")
                return None
            new_children = [_delete_recursive(child, nodes_to_remove) for child in current_node[1:]]
            return [current_node[0]] + [child for child in new_children if child is not None]
        
        return _delete_recursive(new_tree, nodes_to_delete)
    
    def movement(self, tree, alpha):
        new_tree = copy.deepcopy(tree)
        opportunities = []

        def _find_and_move(node):
            if not isinstance(node, list): return

            node_type = node[0]
            children = node[1:]

            if node_type == 'KalimatJembar' and len(children) == 2:
                # Memastikan urutan anak benar sebelum menambah opportunity
                if children[0][0] == 'KalimatBasajan' and children[1][0] == 'Keterangan':
                    opportunities.append((node, 'move_keterangan'))

            if node_type == 'KalimahNgantetJumlah' and len(children) >= 2:
                opportunities.append((node, 'swap_klausa'))

            for child in children:
                _find_and_move(child)

        _find_and_move(new_tree)

        if not opportunities: return new_tree

        num_to_modify = round(alpha * len(opportunities))
        if num_to_modify == 0 and alpha > 0: num_to_modify = 1

        nodes_to_modify = random.sample(opportunities, min(num_to_modify, len(opportunities)))

        for node, move_type in nodes_to_modify:
            if move_type == 'move_keterangan' and len(node) > 2:
                print(f"       > [MOVEMENT] Memindahkan Keterangan ke depan.")
                node[1], node[2] = node[2], node[1]
            elif move_type == 'swap_klausa' and len(node) > 3: # Perlu minimal 2 klausa dan 1 konjungsi
                print(f"       > [MOVEMENT] Menukar posisi klausa.")
                # Contoh: [KalimahNgantet, Klausa1, jeung, Klausa2] -> [KalimahNgantet, Klausa2, jeung, Klausa1]
                node[1], node[3] = node[3], node[1]

        return new_tree


    def run_pipeline(self, tree, alphas):
        print("       > Memulai pipeline augmentasi...")
        augmented_tree = copy.deepcopy(tree)
        teknik_dipakai = []  # Buat daftar teknik yang digunakan

        # Acak urutan pipeline agar lebih variatif
        pipeline_order = ['wr', 'wi', 'wd', 'wm']
        random.shuffle(pipeline_order)

        for step in pipeline_order:
            if step == 'wr' and alphas['wr'] > 0:
                print(f"         - Menjalankan Replacement (alpha={alphas['wr']})")
                augmented_tree = self.replacement(augmented_tree, alphas['wr'])
                teknik_dipakai.append("replacement")
            elif step == 'wi' and alphas['wi'] > 0:
                print(f"         - Menjalankan Insertion (alpha={alphas['wi']})")
                augmented_tree = self.insertion(augmented_tree, alphas['wi'])
                teknik_dipakai.append("insertion")
            elif step == 'wd' and alphas['wd'] > 0:
                print(f"         - Menjalankan Deletion (alpha={alphas['wd']})")
                augmented_tree = self.deletion(augmented_tree, alphas['wd'])
                teknik_dipakai.append("deletion")
            elif step == 'wm' and alphas['wm'] > 0:
                print(f"         - Menjalankan Movement (alpha={alphas['wm']})")
                augmented_tree = self.movement(augmented_tree, alphas['wm'])
                teknik_dipakai.append("movement")
                
        return augmented_tree, teknik_dipakai
    
# ==========================================================================
# MAIN PROGRAM (DENGAN PERBAIKAN LOG FILENAME DAN KONTROL PIPELINE)
# ==========================================================================
if __name__ == "__main__":
    parser_args = argparse.ArgumentParser(description="Augmentasi Data Teks Bahasa Sunda Berbasis Pipeline Sintaksis")
    parser_args.add_argument("--input", required=True, help="File input data asli")
    parser_args.add_argument("--output", required=True, help="File output untuk hasil augmentasi")
    parser_args.add_argument("--alpha_wr", type=float, default=0.0, help="Intensitas Word Replacement (0.0 - 1.0)")
    parser_args.add_argument("--alpha_wi", type=float, default=0.0, help="Intensitas Word Insertion (0.0 - 1.0)")
    parser_args.add_argument("--alpha_wd", type=float, default=0.0, help="Intensitas Word Deletion (0.0 - 1.0)")
    parser_args.add_argument("--alpha_wm", type=float, default=0.0, help="Intensitas Word Movement (0.0 - 1.0)")
    args = parser_args.parse_args()

    active_alphas = []
    if args.alpha_wr > 0: active_alphas.append(f"wr{args.alpha_wr}")
    if args.alpha_wi > 0: active_alphas.append(f"wi{args.alpha_wi}")
    if args.alpha_wd > 0: active_alphas.append(f"wd{args.alpha_wd}")
    if args.alpha_wm > 0: active_alphas.append(f"wm{args.alpha_wm}")
    
    if not active_alphas:
        log_name_suffix = "no_aug"
    else:
        log_name_suffix = "_".join(active_alphas)

    log_filename = f"log_{log_name_suffix}.txt"

    log_file_handler = open(log_filename, "w", encoding="utf-8")
    original_stdout = sys.stdout
    sys.stdout = log_file_handler

    print("Memuat data kamus, sinonim, dan pronomina...")
    # PENAMBAHAN: Menggunakan fungsi placeholder, ganti dengan data asli Anda
    lexicon_dict, daftar_tempat_set = load_kelas_kata('data/kamus/new_dataset_kelas_kata_copy.csv', 'data/kamus/daftar_tempat.txt')
    synonyms_dict = load_synonyms('data/kamus/new_sundanese_synonyms.csv')
    pronomina_map = load_pronouns('data/kamus/pronomina.txt')
    
    # PERBAIKAN: Menggunakan nama class yang benar: ImprovedSundaneseParser
    parser = ImprovedSundaneseParser(grammar, lexicon_dict, daftar_tempat_set)
    augment_controller = AugmentationController(grammar, lexicon_dict, synonyms_dict, pronomina_map)

    output_writer = open(args.output, 'w', encoding='utf-8')
    failure_log = open("parser_failures.log", "w", encoding='utf-8')

    rekap_writer = open("rekap_augmentasi.tsv", "w", encoding="utf-8")
    rekap_writer.write("No\tLabel\tKalimat Asli\tKalimat Augmentasi\tTeknik Augmentasi\n")
    print(f"\nMemulai proses augmentasi dengan alpha: {log_name_suffix}...")
    successful_parses, failed_parses, augmented_count = 0, 0, 0

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                parts = line.strip().split('\t')
                if len(parts) != 2: continue
                label, sentence = parts
                # PENAMBAHAN: Menggunakan fungsi placeholder
                clean_sentence = get_only_chars(sentence)
                if not clean_sentence: continue
                
                output_writer.write(f"{label}\t{clean_sentence}\n")
                print(f"\n--- Memproses Kalimat #{i+1}: {clean_sentence} ---")

                # PERBAIKAN: Memanggil metode parse_with_fallback() dan menangani hasilnya
                parse_tree, parse_method = parser.parse_with_fallback(clean_sentence)

                if parse_tree:
                    successful_parses += 1 # Semua jenis parse sekarang dianggap "sukses" untuk diproses
                    print(f"     > [OK] Kalimat berhasil diparsing (Metode: {parse_method}).")
                    print(f"     > Struktur Pohon (parse_tree):")
                    pprint(parse_tree, stream=log_file_handler, width=120)

                    # BARU: Logika untuk memilih teknik augmentasi berdasarkan kualitas parse tree
                    alphas_for_augmentation = {}
                    if parse_method == 'simple':
                        print("     > Mode augmentasi: SIMPLE (Hanya Replacement & Deletion yang efektif)")
                        # Untuk pohon sederhana, nonaktifkan Insertion & Movement karena tidak akan bekerja
                        alphas_for_augmentation = {
                            'wr': args.alpha_wr,  # Replacement
                            'wi': 0.0,             # Insertion dinonaktifkan
                            'wd': args.alpha_wd,  # Deletion
                            'wm': 0.0,             # Movement dinonaktifkan
                        }
                    else: # Untuk 'full' dan 'partial'
                        print("     > Mode augmentasi: FULL (Semua teknik diaktifkan)")
                        # Gunakan semua alpha sesuai input dari command line
                        alphas_for_augmentation = {
                            'wr': args.alpha_wr,
                            'wi': args.alpha_wi,
                            'wd': args.alpha_wd,
                            'wm': args.alpha_wm,
                        }
                    
                    augmented_tree, teknik = augment_controller.run_pipeline(parse_tree, alphas_for_augmentation)
                    
                    if augmented_tree:
                        augmented_sentence = tree_to_sentence(augmented_tree)
                        if augmented_sentence != clean_sentence and augmented_sentence.strip():
                            print(f"       > Hasil Augmentasi: {augmented_sentence}")
                            output_writer.write(f"{label}\t{augmented_sentence.strip()}\n")
                            teknik_dipakai = ', '.join(sorted(teknik)) if teknik else '-'
                            rekap_writer.write(f"{i+1}\t{label}\t{clean_sentence}\t{augmented_sentence.strip()}\t{teknik_dipakai}\n")
                            augmented_count += 1
                else:
                    # Blok ini sekarang hanya akan berjalan jika parser benar-benar gagal membuat pohon apapun
                    failed_parses += 1
                    print(f"     > [FATAL FAIL] Parser tidak dapat membuat pohon sama sekali.")
                    failure_log.write(f"{clean_sentence}\n")
    finally:
        output_writer.close()
        rekap_writer.close()
        failure_log.close()
        sys.stdout = original_stdout # Kembalikan stdout
        log_file_handler.close()
    
    print("\n==================== PROSES SELESAI ====================")
    print(f"Total Kalimat Diproses: {successful_parses + failed_parses}")
    print(f"  - Berhasil Diparsing : {successful_parses}")
    print(f"  - Gagal Diparsing    : {failed_parses}")
    print(f"  - Kalimat Baru Dihasilkan : {augmented_count}")
    print(f"Hasil augmentasi disimpan di: {args.output}")
    print(f"Daftar kalimat gagal disimpan di: parser_failures.log")
    print(f"Log proses lengkap disimpan di: {log_filename}")
