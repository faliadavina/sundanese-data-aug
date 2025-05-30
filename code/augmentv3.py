from eda import synonyms_dict, kelas_kata, eda, get_only_chars, is_valid_number, find_adverbia
import argparse
from collections import defaultdict, Counter
import random
import os

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data (Cleaned CSV format)")
ap.add_argument("--output_wr", required=False, type=str, help="output file of augmented data")
ap.add_argument("--output_wd", required=False, type=str, help="output file of augmented data")
ap.add_argument("--output_wi", required=False, type=str, help="output file of augmented data")
ap.add_argument("--output_wm", required=False, type=str, help="output file of augmented data")
ap.add_argument("--alpha_wr", required=False, type=float, help="percent of words in each sentence to be replaced by synonyms")
ap.add_argument("--alpha_wd", required=False, type=float, help="percent of words in each sentence to be deleted")
ap.add_argument("--alpha_wi", required=False, type=float, help="percent of words in each sentence to be inserted")
ap.add_argument("--alpha_wm", required=False, type=float, help="percent of words in each sentence to be moved")
ap.add_argument("--output_combined", required=False, type=str, help="output file for combined augmented data")
args = ap.parse_args()

# Default output file names if not provided
output_wr = args.output_wr if args.output_wr else args.input.replace('.csv', '_augmented_2.csv')
output_wd = args.output_wd if args.output_wd else args.input.replace('.csv', '_augmented_2.csv')
output_wi = args.output_wi if args.output_wi else args.input.replace('.csv', '_augmented_2.csv')
output_wm = args.output_wm if args.output_wm else args.input.replace('.csv', '_augmented_2.csv')
output_combined = args.output_combined if args.output_combined else args.input.replace('.csv', '_augmented_combined.txt')

alpha_wr = args.alpha_wr if args.alpha_wr is not None else 0
alpha_wd = args.alpha_wd if args.alpha_wd is not None else 0
alpha_wi = args.alpha_wi if args.alpha_wi is not None else 0
alpha_wm = args.alpha_wm if args.alpha_wm is not None else 0

if alpha_wr == 0 and alpha_wd == 0 and alpha_wi == 0 and alpha_wm == 0:
    ap.error('At least one alpha should be greater than zero')

# ================================== #
#   Fungsi bantu: modifiable count   #
# ================================== #
def count_modifiable_words(sentence, technique):
    words = sentence.split()
    if technique == "wr":
        count = sum([
            1 for w in words
            if w in synonyms_dict or
               kelas_kata.get(w) == 'pronomina' or
               is_valid_number(w)[0]
        ])
    elif technique == "wd":
        count = sum(1 for w in words if kelas_kata.get(w) == 'adverbia')
    elif technique == "wi":
        count = sum(1 for w in words if kelas_kata.get(w) in ['adjektiva', 'verba'])
    elif technique == "wm":
        time_adv, place_adv = find_adverbia(sentence)
        count = len(time_adv) + len(place_adv)
    else:
        count = 0
    return count

# ================================= #
#    Apply teknik augmentasi EDA    #
# ================================= #
def apply_eda(sentence, technique, alpha):
    if technique == "wr":
        return eda(sentence, synonyms_dict, kelas_kata, alpha_wr=alpha, alpha_wd=0, alpha_wi=0, alpha_wm=0)
    elif technique == "wd":
        return eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=alpha, alpha_wi=0, alpha_wm=0)
    elif technique == "wi":
        return eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=0, alpha_wi=alpha, alpha_wm=0)
    elif technique == "wm":
        return eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=0, alpha_wi=0, alpha_wm=alpha)
    else:
        return [sentence]

# =========================================== #
#     Proses utama augmentasi + balancing     #
# =========================================== #
def augment_and_balance(train_orig, output_file, technique, alpha):
    all_data = []
    label_to_data = defaultdict(list)

    with open(train_orig, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # === Augmentasi Awal ===
    for i, line in enumerate(lines):
        parts = line.strip().split('\t')
        if len(parts) < 2:
            print(f"Skipping invalid line {i}: {line}")
            continue

        label = parts[0].strip()
        sentence = get_only_chars(parts[1].strip()).lower()
        aug_sentences = apply_eda(sentence, technique, alpha)

        if isinstance(aug_sentences[0], list):
            aug_sentences = [" ".join(x) for x in aug_sentences]

        label_to_data[label].append((sentence, aug_sentences[1:]))

    # === Balancing ===
    label_counts = {label: len(data) for label, data in label_to_data.items()}
    max_count = max(label_counts.values())

    # Tambahkan hasil awal
    for label, sent_list in label_to_data.items():
        for orig, aug_list in sent_list:
            all_data.append((label, orig, "original"))
            for aug in aug_list:
                all_data.append((label, aug, "augmented"))

    # Tambahkan augmentasi tambahan jika dibutuhkan
    for label, sent_list in label_to_data.items():
        current_total = len(sent_list)
        needed = max_count - current_total

        print(f"\n[INFO] Label '{label}': butuh {needed} data tambahan")

        if needed <= 0:
            continue

        additional_augmented = []

        sorted_sentences = sorted(
            sent_list,
            key=lambda x: count_modifiable_words(x[0], technique),
            reverse=True
        )

        for orig, _ in sorted_sentences:
            if len(additional_augmented) >= needed:
                break

            aug_sentences = apply_eda(orig, technique, alpha)
            if isinstance(aug_sentences[0], list):
                aug_sentences = [" ".join(x) for x in aug_sentences]

            for aug in aug_sentences[1:]:
                if len(additional_augmented) >= needed:
                    break
                additional_augmented.append((label, aug, "augmented"))

        if len(additional_augmented) < needed:
            print(f"[WARNING] Data untuk label '{label}' tidak cukup. Dapat {len(additional_augmented)} dari {needed}.")

        all_data.extend(additional_augmented)

    # === Simpan hasil ===
    balanced_data = all_data.copy()
    random.shuffle(balanced_data)

    balanced_output = output_file.replace(".txt", "_balanced.txt")
    with open(balanced_output, 'w', encoding='utf-8') as out_f:
        for label, sentence, _ in balanced_data:
            out_f.write(f"{label}\t{sentence}\n")

    labeled_output = output_file.replace(".txt", "_labeled.txt")
    with open(labeled_output, 'w', encoding='utf-8') as out_f:
        for label, sentence, status in all_data:
            out_f.write(f"{label}\t{sentence}\t{status}\n")

    print(f"\n[✓] Saved balanced data: {balanced_output}")
    print(f"[✓] Saved labeled data: {labeled_output}")

def augment_with_combination(input_file, output_file, active_techniques):
    seen_sentences = set()
    all_grouped_data = []

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        parts = line.strip().split('\t')
        if len(parts) < 2:
            continue
        label = parts[0].strip()
        original = get_only_chars(parts[1].strip()).lower()
        augmented_versions = [original]

        # Terapkan teknik kombinasi sesuai urutan
        for technique, alpha in active_techniques:
            new_versions = []
            for s in augmented_versions:
                aug_result = apply_eda(s, technique, alpha)
                new_versions.extend(aug_result[1:] if len(aug_result) > 1 else [])
            augmented_versions.extend(new_versions)

        # Hapus duplikat sambil menjaga urutan (original dulu)
        unique_augmented = []
        added = set()
        for aug in augmented_versions:
            if aug not in added:
                unique_augmented.append(aug)
                added.add(aug)

        # Simpan satu blok: original + semua hasilnya
        block = []
        for j, aug in enumerate(unique_augmented):
            status = "original" if j == 0 else "augmented"
            block.append((label, aug, status))
            seen_sentences.add(aug)
        all_grouped_data.append(block)

    # Simpan labeled: sesuai urutan original
    base_path = output_file.replace(".txt", "")
    labeled_file = base_path + "_labeled.txt"
    balanced_file = base_path + "_balanced.txt"

    with open(labeled_file, 'w', encoding='utf-8') as f:
        for block in all_grouped_data:
            for label, sentence, status in block:
                f.write(f"{label}\t{sentence}\t{status}\n")

    # Simpan balanced: semua kalimat dicampur
    balanced_data = [entry for block in all_grouped_data for entry in block]
    import random
    random.shuffle(balanced_data)
    with open(balanced_file, 'w', encoding='utf-8') as f:
        for label, sentence, _ in balanced_data:
            f.write(f"{label}\t{sentence}\n")

    print(f"\n[✓] Saved grouped labeled file to: {labeled_file}")
    print(f"[✓] Saved balanced file to: {balanced_file}")

active_techniques = []
if alpha_wr > 0: active_techniques.append(('wr', alpha_wr))
if alpha_wd > 0: active_techniques.append(('wd', alpha_wd))
if alpha_wi > 0: active_techniques.append(('wi', alpha_wi))
if alpha_wm > 0: active_techniques.append(('wm', alpha_wm))

# =============================== #
#              Main               #
# =============================== #
if __name__ == "__main__":
    if len(active_techniques) == 1:
        technique, alpha = active_techniques[0]
        print(f"Running single augmentation: {technique}")
        output_map = {
            'wr': output_wr,
            'wd': output_wd,
            'wi': output_wi,
            'wm': output_wm
        }
        augment_and_balance(args.input, output_map[technique], technique, alpha)
    elif len(active_techniques) > 1:
        if args.output_combined:
            print("Running combined augmentation...")
            augment_with_combination(args.input, args.output_combined, active_techniques)
        else:
            raise ValueError("Untuk kombinasi teknik, tambahkan --output_combined")