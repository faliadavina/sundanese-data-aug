# ==============================================================================
# AUGMENTASI DATA BAHASA SUNDA BERBASIS PARSER EARLEY (VERSI FINAL)
# ==============================================================================
# Deskripsi:
# Skrip ini melakukan augmentasi data teks Bahasa Sunda dengan alur berikut:
# 1. Membaca kalimat dari file input.
# 2. Membersihkan dan melakukan tokenisasi (mengubah kalimat menjadi daftar kata).
# 3. Menggunakan lexicon untuk mendapatkan kelas kata (PoS Tag).
# 4. Membuat 'grammar dinamis': menggabungkan grammar sintaksis utama dari
#    sundanese_cfg.py dengan aturan leksikal yang dibuat 'on-the-fly'
#    untuk setiap kalimat.
# 5. Mem-parsing kalimat menggunakan Algoritma Earley dari NLTK.
# 6. Jika parsing berhasil, alur augmentasi (Replacement, Insertion, Deletion,
#    Movement) dijalankan pada setiap kemungkinan pohon sintaksis yang ditemukan.
# 7. Menyimpan hasil augmentasi, log proses, dan rekapitulasi.
# ==============================================================================

import argparse
import random
import re
import pandas as pd
from collections import defaultdict
import sys
import copy
import nltk

# Langkah 1: Impor grammar dan terminals dari file konfigurasi terpisah.
# Pastikan file `sundanese_cfg.py` ada di direktori yang sama.
try:
    from sundanese_cfg import grammar, TERMINALS
except ImportError:
    print("[FATAL ERROR] File 'sundanese_cfg.py' tidak ditemukan.")
    print("Pastikan file tersebut berada di direktori yang sama dengan skrip ini.")
    sys.exit(1)

# ==============================================================================
# FUNGSI-FUNGSI BANTUAN
# ==============================================================================

def get_only_chars(line):
    """Membersihkan kalimat dari karakter yang tidak diinginkan, hanya menyisakan huruf dan spasi."""
    clean_line = ""
    line = line.replace("’", "").replace("'", "")
    line = line.replace("\t", " ").replace("\n", " ")
    line = line.lower()
    for char in line:
        if char in 'qwertyuiopasdfghjklzxcvbnm ':
            clean_line += char
        else:
            clean_line += ' '
    clean_line = re.sub(' +', ' ', clean_line).strip()
    return clean_line

def load_kelas_kata(filepath):
    """Memuat lexicon dari file CSV (format: kata<tab>kelas_kata)."""
    kelas_kata_dict = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                kata, kelas = parts[0].strip().lower(), parts[1].strip()
                kelas_kata_dict[kata] = kelas
    return kelas_kata_dict

def load_synonyms(file_path):
    """Memuat sinonim dari file CSV."""
    synonyms_dict = defaultdict(list)
    try:
        data = pd.read_csv(file_path)
        for _, row in data.iterrows():
            word = str(row['kata']).lower()
            if pd.notna(row['sinonim']):
                syns = [s.strip().lower() for s in str(row['sinonim']).split(',') if str(s).strip()]
                synonyms_dict[word].extend(syns)
    except Exception as e:
        print(f"[ERROR] Gagal memuat sinonim: {e}")
    return synonyms_dict

def load_pronouns(file_path):
    """Memuat kategori pronomina untuk augmentasi."""
    kata_ke_kategori = {}
    kategori_ke_kata = defaultdict(list)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    kata, kategori = parts[0].strip().lower(), parts[1].strip()
                    kata_ke_kategori[kata] = kategori
                    kategori_ke_kata[kategori].append(kata)
    except FileNotFoundError:
        print(f"[ERROR] File pronomina tidak ditemukan di: '{file_path}'")
    return kata_ke_kategori, kategori_ke_kata

def convert_grammar_to_nltk_format(grammar_dict, terminals):
    """
    Mengubah grammar dari format dictionary Python ke format string NLTK.
    Fungsi ini juga secara otomatis mengganti spasi di nama non-terminal
    dengan garis bawah (_) agar valid untuk NLTK.
    """
    all_non_terminals = set(grammar_dict.keys())
    nltk_rules = []
    for non_terminal, rules in grammar_dict.items():
        lhs = non_terminal.replace(' ', '_')
        for rule in rules:
            if isinstance(rule, str): rule = [rule]
            rhs_parts = []
            for part in rule:
                if part in all_non_terminals:
                    rhs_parts.append(part.replace(' ', '_'))
                elif part in terminals:
                    rhs_parts.append(part)
                else:
                    rhs_parts.append(f"'{part}'")
            nltk_rules.append(f"{lhs} -> {' '.join(rhs_parts)}")
    return "\n".join(nltk_rules)

def tree_to_sentence(tree):
    """Mengubah objek nltk.Tree kembali menjadi kalimat string."""
    return ' '.join(tree.leaves())

def find_opportunities(node, target_node_types):
    """Fungsi rekursif untuk mencari semua sub-pohon dengan tipe tertentu."""
    opportunities = []
    if not isinstance(node, nltk.Tree): return []
    if node.label() in target_node_types:
        opportunities.append(node)
    for child in node:
        opportunities.extend(find_opportunities(child, target_node_types))
    return opportunities

# ==========================================================================
# KELAS AUGMENTASI LENGKAP
# ==========================================================================
class AugmentationController:
    def __init__(self, grammar, lexicon, synonyms, pronomina_map):
        self.grammar = grammar
        self.lexicon = lexicon
        self.synonyms = synonyms
        self.pronomina_kata_ke_kategori, self.pronomina_kategori_ke_kata = pronomina_map
        self.adjektiva_list = [k for k, v in lexicon.items() if v == 'adjektiva']

    def _replace_node_word(self, node_to_replace):
        """Logika penggantian untuk satu node (pre-terminal)."""
        if not isinstance(node_to_replace, nltk.Tree) or len(node_to_replace) != 1 or not isinstance(node_to_replace[0], str): return
        
        node_type = node_to_replace.label()
        original_word = node_to_replace[0]

        if node_type == 'pronomina':
            kategori = self.pronomina_kata_ke_kategori.get(original_word)
            if not kategori: return
            kandidat_lain = [k for k in self.pronomina_kategori_ke_kata.get(kategori, []) if k != original_word]
            if kandidat_lain:
                node_to_replace[0] = random.choice(kandidat_lain)
                print(f"       > [REPLACEMENT] Mengganti '{original_word}' -> '{node_to_replace[0]}'")
        elif node_type in ['nomina', 'verba', 'adjektiva']:
            possible_synonyms = [s for s in self.synonyms.get(original_word, []) if s != original_word]
            if possible_synonyms:
                new_word = random.choice(possible_synonyms)
                if self.lexicon.get(new_word) == node_type:
                    node_to_replace[0] = new_word
                    print(f"       > [REPLACEMENT] Mengganti '{original_word}' -> '{new_word}'")

    def replacement(self, tree, alpha):
        new_tree = tree.copy(deep=True)
        target_types = {'nomina', 'verba', 'adjektiva', 'pronomina'}
        opportunities = [st for st in new_tree.subtrees() if st.label() in target_types and len(st) == 1 and isinstance(st[0], str)]
        if not opportunities: return new_tree
        num_to_modify = max(1, round(alpha * len(opportunities)))
        nodes_to_modify = random.sample(opportunities, min(num_to_modify, len(opportunities)))
        for node in nodes_to_modify: self._replace_node_word(node)
        return new_tree

    def insertion(self, tree, alpha):
        new_tree = tree.copy(deep=True)
        opportunities = find_opportunities(new_tree, {'Frasa_Nomina'})
        if not opportunities or not self.adjektiva_list: return new_tree
        num_to_modify = max(1, round(alpha * len(opportunities)))
        nodes_to_modify = random.sample(opportunities, min(num_to_modify, len(opportunities)))
        for node in nodes_to_modify:
            adjektiva_baru = random.choice(self.adjektiva_list)
            node.append(nltk.Tree('partikelNu', ['nu']))
            node.append(nltk.Tree('adjektiva', [adjektiva_baru]))
            print(f"       > [INSERTION] Menambah 'nu {adjektiva_baru}' pada Frasa_Nomina")
        return new_tree

    def deletion(self, tree, alpha):
        new_tree = tree.copy(deep=True)
        target_types = {'Keterangan', 'Frasa_Adverbial'}
        opportunities = find_opportunities(new_tree, target_types)
        if not opportunities: return new_tree
        num_to_modify = max(1, round(alpha * len(opportunities)))
        nodes_to_delete = random.sample(opportunities, min(num_to_modify, len(opportunities)))
        nodes_to_delete_ids = {id(n) for n in nodes_to_delete}
        def _delete_recursive(current_node):
            if not isinstance(current_node, nltk.Tree): return current_node
            if id(current_node) in nodes_to_delete_ids:
                print(f"       > [DELETION] Menghapus node: '{current_node.label()}'")
                return None
            new_children = [_delete_recursive(child) for child in current_node]
            current_node[:] = [child for child in new_children if child is not None]
            return current_node
        return _delete_recursive(new_tree)

    def movement(self, tree, alpha):
        new_tree = tree.copy(deep=True)
        opportunities = []
        for node in new_tree.subtrees():
            if node.label() == 'Kalimat_Jembar' and len(node) == 2:
                if isinstance(node[0], nltk.Tree) and node[0].label() == 'Kalimat_Basajan' and \
                   isinstance(node[1], nltk.Tree) and node[1].label() == 'Keterangan':
                    opportunities.append(node)
        if not opportunities: return new_tree
        num_to_modify = max(1, round(alpha * len(opportunities)))
        nodes_to_modify = random.sample(opportunities, min(num_to_modify, len(opportunities)))
        for node in nodes_to_modify:
            print(f"       > [MOVEMENT] Memindahkan Keterangan ke depan.")
            node[0], node[1] = node[1], node[0]
        return new_tree
    
    def run_pipeline(self, tree, alphas):
        print(f"     > Menjalankan pipeline augmentasi...")
        augmented_tree = tree.copy(deep=True)
        teknik_dipakai = []
        if alphas.get('wr', 0) > 0:
            augmented_tree = self.replacement(augmented_tree, alphas['wr'])
            teknik_dipakai.append("replacement")
        if alphas.get('wi', 0) > 0:
            augmented_tree = self.insertion(augmented_tree, alphas['wi'])
            teknik_dipakai.append("insertion")
        if alphas.get('wd', 0) > 0:
            augmented_tree = self.deletion(augmented_tree, alphas['wd'])
            teknik_dipakai.append("deletion")
        if alphas.get('wm', 0) > 0:
            augmented_tree = self.movement(augmented_tree, alphas['wm'])
            teknik_dipakai.append("movement")
        return augmented_tree, teknik_dipakai

# ==========================================================================
# FUNGSI UTAMA (MAIN PROGRAM)
# ==========================================================================
def main():
    parser_args = argparse.ArgumentParser(description="Augmentasi Data Teks Bahasa Sunda Berbasis Parser Earley")
    parser_args.add_argument("--input", required=True, help="File input data asli (contoh: data3_final.txt)")
    parser_args.add_argument("--output", required=True, help="File output untuk hasil augmentasi")
    parser_args.add_argument("--alpha_wr", type=float, default=0.0, help="Intensitas Word Replacement")
    parser_args.add_argument("--alpha_wi", type=float, default=0.0, help="Intensitas Word Insertion")
    parser_args.add_argument("--alpha_wd", type=float, default=0.0, help="Intensitas Word Deletion")
    parser_args.add_argument("--alpha_wm", type=float, default=0.0, help="Intensitas Word Movement")
    args = parser_args.parse_args()

    active_alphas = []
    if args.alpha_wr > 0: active_alphas.append(f"wr{args.alpha_wr}")
    if args.alpha_wi > 0: active_alphas.append(f"wi{args.alpha_wi}")
    if args.alpha_wd > 0: active_alphas.append(f"wd{args.alpha_wd}")
    if args.alpha_wm > 0: active_alphas.append(f"wm{args.alpha_wm}")
    log_name_suffix = "_".join(active_alphas) if active_alphas else "no_aug"
    log_filename = f"log_{log_name_suffix}.txt"

    with open(log_filename, "w", encoding="utf-8") as log_file_handler:
        original_stdout = sys.stdout
        sys.stdout = log_file_handler

        print("="*50)
        print("MEMULAI PROSES AUGMENTASI DENGAN EARLEY PARSER")
        print(f"Waktu Mulai: {pd.Timestamp.now(tz='Asia/Jakarta').strftime('%Y-%m-%d %H:%M:%S WIB')}")
        print(f"Argumen: {args}")
        print("="*50)

        print("\n[1] Memuat semua data pendukung...")
        try:
            lexicon_dict = load_kelas_kata('data/kamus/new_dataset_kelas_kata_copy.csv')
            synonyms_dict = load_synonyms('data/kamus/new_sundanese_synonyms.csv')
            pronomina_map = load_pronouns('data/kamus/pronomina.txt')
        except FileNotFoundError as e:
            sys.stdout = original_stdout
            print(f"\n[FATAL ERROR] File data tidak ditemukan: {e}")
            sys.exit(1)

        print("\n[2] Mempersiapkan Grammar Sintaksis Utama...")
        nltk_grammar_string = convert_grammar_to_nltk_format(grammar, TERMINALS)
        
        print("\n[3] Mempersiapkan Kontroler Augmentasi...")
        augment_controller = AugmentationController(grammar, lexicon_dict, synonyms_dict, pronomina_map)

        print(f"\n[4] Memulai pemrosesan file: {args.input}...")
        with open(args.output, 'w', encoding='utf-8') as output_writer, \
             open("parser_failures.log", "w", encoding='utf-8') as failure_log, \
             open("rekap_augmentasi.tsv", "w", encoding="utf-8") as rekap_writer:
            
            rekap_writer.write("No\tLabel\tKalimat Asli\tKalimat Augmentasi\tTeknik Augmentasi\tJmlPohon\n")
            successful_parses, failed_parses, augmented_count, total_lines = 0, 0, 0, 0

            with open(args.input, 'r', encoding='utf-8') as f_in:
                lines = [line for line in f_in if line.strip()]
                total_lines = len(lines)

            for i, line in enumerate(lines):
                parts = line.strip().split('\t')
                if len(parts) != 2: continue
                
                label, sentence = parts
                clean_sentence = get_only_chars(sentence)
                if not clean_sentence: continue
                
                print(f"\n--- ({i+1}/{total_lines}) Memproses: '{clean_sentence}' ---")
                output_writer.write(f"{label}\t{clean_sentence}\n")
                
                words = clean_sentence.split()
                
                lexical_rules = []
                for word in set(words):
                    pos = lexicon_dict.get(word)
                    if pos: lexical_rules.append(f"{pos.replace(' ', '_')} -> '{word}'")

                sentence_specific_grammar_string = nltk_grammar_string + "\n" + "\n".join(lexical_rules)
                
                possible_trees = []
                try:
                    sentence_cfg = nltk.CFG.fromstring(sentence_specific_grammar_string)
                    earley_parser = nltk.EarleyChartParser(sentence_cfg)
                    possible_trees = list(earley_parser.parse(words))
                except ValueError as e:
                    print(f"    > [ERROR] Gagal membuat grammar atau parsing: {e}")

                if possible_trees:
                    successful_parses += 1
                    num_trees = len(possible_trees)
                    print(f"    > [OK] Berhasil diparsing. Ditemukan {num_trees} kemungkinan pohon.")
                    print("    > Menampilkan semua kemungkinan pohon sintaksis:")
                    for tree_idx, tree in enumerate(possible_trees):
                        print(f"\n      --- Pohon Kemungkinan #{tree_idx + 1} ---")
                        # .pretty_print() akan mencetak pohon dengan format yang rapi ke log
                        tree.pretty_print(stream=sys.stdout)
                    print("\n      ------------------------------------------")
                    augmented_sentences = set()
                    alphas = {'wr': args.alpha_wr, 'wi': args.alpha_wi, 'wd': args.alpha_wd, 'wm': args.alpha_wm}
                    if sum(alphas.values()) > 0:
                        for tree_idx, tree in enumerate(possible_trees):
                            augmented_tree, teknik = augment_controller.run_pipeline(tree, alphas)
                            if augmented_tree:
                                augmented_sentence = tree_to_sentence(augmented_tree)
                                if augmented_sentence and augmented_sentence != clean_sentence:
                                    augmented_sentences.add(augmented_sentence)
                    
                    for aug_sentence in augmented_sentences:
                        print(f"    > Hasil Augmentasi: '{aug_sentence}'")
                        output_writer.write(f"{label}\t{aug_sentence.strip()}\n")
                        rekap_writer.write(f"{i+1}\t{label}\t{clean_sentence}\t{aug_sentence.strip()}\t{','.join(teknik)}\t{num_trees}\n")
                        augmented_count += 1
                else:
                    failed_parses += 1
                    print(f"    > [GAGAL] Tidak ada struktur valid yang ditemukan.")
                    failure_log.write(f"{clean_sentence}\n")

        sys.stdout = original_stdout
        
        print("\n==================== PROSES SELESAI ====================")
        total_processed = successful_parses + failed_parses
        success_rate = (successful_parses / total_processed * 100) if total_processed > 0 else 0
        print(f"Total Kalimat Diproses: {total_processed}")
        print(f"  - Berhasil Diparsing : {successful_parses} ({success_rate:.2f}%)")
        print(f"  - Gagal Diparsing    : {failed_parses}")
        print(f"  - Kalimat Baru Dihasilkan : {augmented_count}")
        print("-" * 52)
        print(f"Hasil augmentasi disimpan di: {args.output}")
        print(f"Daftar kalimat gagal disimpan di: parser_failures.log")
        print(f"Rekap augmentasi disimpan di: rekap_augmentasi.tsv")
        print(f"Log proses lengkap disimpan di: {log_filename}")

if __name__ == "__main__":
    main()