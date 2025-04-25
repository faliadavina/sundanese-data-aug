# from eda import synonyms_dict, kelas_kata, pronouns_category, category_to_word, eda
# import argparse

# # Arguments to be parsed from command line
# ap = argparse.ArgumentParser()
# ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data (Cleaned CSV format)")
# ap.add_argument("--output_wr", required=False, type=str, help="output file of augmented data")
# ap.add_argument("--output_wd", required=False, type=str, help="output file of augmented data")
# ap.add_argument("--output_wi", required=False, type=str, help="output file of augmented data")
# ap.add_argument("--alpha_wr", required=False, type=float, help="percent of words in each sentence to be replaced by synonyms")
# ap.add_argument("--alpha_wd", required=False, type=float, help="percent of words in each sentence to be deleted")
# ap.add_argument("--alpha_wi", required=False, type=float, help="percent of words in each sentence to be inserted")
# ap.add_argument("--alpha_ws", required=False, type=float, help="percent of words in each sentence to be swapped")
# args = ap.parse_args()

# # Default output file names if not provided
# output_wr = args.output_wr if args.output_wr else args.input.replace('.csv', '_augmented_2.csv')
# output_wd = args.output_wd if args.output_wd else args.input.replace('.csv', '_augmented_2.csv')
# output_wi = args.output_wi if args.output_wi else args.input.replace('.csv', '_augmented_2.csv')

# # Augmetation rates
# alpha_wr = args.alpha_wr if args.alpha_wr is not None else 0
# alpha_wd = args.alpha_wd if args.alpha_wd is not None else 0
# alpha_wi = args.alpha_wi if args.alpha_wi is not None else 0

# #how much to swap words
# alpha_ws = args.alpha_ws if args.alpha_ws is not None else 0
    
# if alpha_wd == 0 and alpha_wi == 0 and alpha_wr == 0 and alpha_ws == 0:
#     ap.error('At least one alpha should be greater than zero')

# # Generate more data with standard augmentation
# def gen_eda(train_orig, output_synonym, output_deletion, output_insertion, alpha_wr, alpha_wd, alpha_wi):
#     # unique_sentences = set()
#     # writer = open(output_file, 'w', encoding='utf-8')
#     unique_synonyms = set()
#     unique_deletions = set()
#     unique_insertions = set()
#     # unique_pronouns = set()

#     writer_synonym = open(output_synonym, 'w', encoding='utf-8') if alpha_wr > 0 else None
#     writer_deletion = open(output_deletion, 'w', encoding='utf-8') if alpha_wd > 0 else None
#     writer_insertion = open(output_insertion, 'w', encoding='utf-8') if alpha_wi > 0 else None
#     # writer_pronoun = open(output_pronoun, 'w', encoding='utf-8')

#     with open(train_orig, 'r', encoding='utf-8') as f:  # specify encoding='utf-8' here
#         lines = f.readlines()

#     for i, line in enumerate(lines):
#         parts = line.strip().split('\t')  # Data cleaned using tab as delimiter
#         if len(parts) < 2:
#             print(f"Skipping invalid line {i}: {line}")  # Log the invalid line
#             continue  # Skip lines that don't have both a label and sentence
        
#         label = parts[0]
#         sentence = parts[1]

#         if alpha_wr > 0:    
#             synonym_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=alpha_wr, alpha_wd=0, alpha_wi=0)
#             # Simpan hasil synonym replacement ke file tersendiri
#             for aug_sentence in synonym_sentences:
#                 if isinstance(aug_sentence, str) and aug_sentence not in unique_synonyms:
#                     writer_synonym.write(label + "\t" + aug_sentence + "\n")
#                     unique_synonyms.add(aug_sentence) 
        
#         if alpha_wd > 0:
#             deletion_sentences = None
#             if deletion_sentences is None: 
#                 deletion_sentences = []
#             deletion_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=alpha_wd, alpha_wi=0)
#             if deletion_sentences is None:  #pastikan yang dari eda bukan none
#                 deletion_sentences = []
#             # Simpan hasil deletion ke file tersendiri
#             for aug_sentence in deletion_sentences:
#                 if aug_sentence not in unique_deletions:
#                     writer_deletion.write(label + "\t" + aug_sentence + "\n")
#                     unique_deletions.add(aug_sentence)

#         if alpha_wi > 0:
#             insertion_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=0, alpha_wi=alpha_wi)
#             for aug_sentence in insertion_sentences:
#                 if isinstance(aug_sentence, list):  # Jika hasilnya list kata, gabungkan menjadi kalimat
#                     aug_sentence = " ".join(aug_sentence)  
#                 if aug_sentence not in unique_insertions:
#                     writer_insertion.write(label + "\t" + aug_sentence + "\n")  # Simpan hasil augmentasi
#                     unique_insertions.add(aug_sentence)  # Tambahkan kalimat ke set unik
                    
#     if writer_synonym:
#         writer_synonym.close()
#         print(f"Generated synonym replacement data in {output_synonym}")
#     if writer_deletion:
#         writer_deletion.close()
#         print(f"Generated deletion data in {output_deletion}")
#     if writer_insertion:
#         writer_insertion.close()
#         print(f"Generated insertion data in {output_insertion}")

# # Main function
# if __name__ == "__main__":
#     # Generate augmented sentences and output into a new file
#     gen_eda(args.input, output_wr, output_wd, output_wi, alpha_wr=alpha_wr, alpha_wd=alpha_wd, alpha_wi=alpha_wi)
from eda import synonyms_dict, kelas_kata, eda, get_only_chars
import argparse
from collections import defaultdict
import random
import os

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data (Cleaned CSV format)")
ap.add_argument("--output_wr", required=False, type=str, help="output file of augmented data")
ap.add_argument("--output_wd", required=False, type=str, help="output file of augmented data")
ap.add_argument("--output_wi", required=False, type=str, help="output file of augmented data")
ap.add_argument("--alpha_wr", required=False, type=float, help="percent of words to be replaced")
ap.add_argument("--alpha_wd", required=False, type=float, help="percent of words to be deleted")
ap.add_argument("--alpha_wi", required=False, type=float, help="percent of words to be inserted")
args = ap.parse_args()

output_wr = args.output_wr if args.output_wr else args.input.replace('.txt', '_aug_wr.txt')
output_wd = args.output_wd if args.output_wd else args.input.replace('.txt', '_aug_wd.txt')
output_wi = args.output_wi if args.output_wi else args.input.replace('.txt', '_aug_wi.txt')

alpha_wr = args.alpha_wr if args.alpha_wr is not None else 0
alpha_wd = args.alpha_wd if args.alpha_wd is not None else 0
alpha_wi = args.alpha_wi is not None and args.alpha_wi or 0

if alpha_wr == 0 and alpha_wd == 0 and alpha_wi == 0:
    ap.error('At least one alpha should be greater than zero')

def augment_and_balance(train_orig, output_file, alpha_type, alpha_value):
    all_data = []  # format: [(label, original_sentence, [aug1, aug2, ...])]

    with open(train_orig, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        parts = line.strip().split('\t')
        if len(parts) < 2:
            print(f"Skipping invalid line {i}: {line}")
            continue

        # label, sentence = parts[0], parts[1]
        label, sentence = parts[0], get_only_chars(parts[1].strip()).lower()

        # Augment original sentence
        if alpha_type == "wr":
            aug_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=alpha_value, alpha_wd=0, alpha_wi=0)
        elif alpha_type == "wd":
            aug_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=alpha_value, alpha_wi=0)
        elif alpha_type == "wi":
            aug_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=0, alpha_wi=alpha_value)
        else:
            aug_sentences = []

        if isinstance(aug_sentences[0], list):  # if eda returns list of tokens
            aug_sentences = [" ".join(aug) for aug in aug_sentences]

        # Tambahkan satu entri ke data utama
        all_data.append((label, sentence, aug_sentences[1:]))  # index 0 = original, skip

    # Save file 1: balanced (plain)
    balanced_output = output_file.replace(".txt", "_balanced.txt")
    with open(balanced_output, 'w', encoding='utf-8') as out_f:
        for label, orig, aug_list in all_data:
            out_f.write(f"{label}\t{orig}\n")
            for aug in aug_list:
                out_f.write(f"{label}\t{aug}\n")

    # Save file 2: with origin label
    labeled_output = output_file.replace(".txt", "_labeled.txt")
    with open(labeled_output, 'w', encoding='utf-8') as label_out:
        for label, orig, aug_list in all_data:
            label_out.write(f"{label}\t{orig}\toriginal\n")
            for aug in aug_list:
                label_out.write(f"{label}\t{aug}\taugmented\n")

    print(f"[✓] Saved balanced data: {balanced_output}")
    print(f"[✓] Saved labeled data: {labeled_output}")

if __name__ == "__main__":
    if alpha_wr > 0:
        print("Running word replacement augmentation + balancing...")
        augment_and_balance(args.input, output_wr, "wr", alpha_wr)
    if alpha_wd > 0:
        print("Running word deletion augmentation + balancing...")
        augment_and_balance(args.input, output_wd, "wd", alpha_wd)
    if alpha_wi > 0:
        print("Running word insertion augmentation + balancing...")
        augment_and_balance(args.input, output_wi, "wi", alpha_wi)

