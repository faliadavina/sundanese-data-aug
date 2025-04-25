from eda import synonyms_dict, kelas_kata, pronouns_category, category_to_word, eda, get_only_chars
import argparse
from collections import defaultdict
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
args = ap.parse_args()

# Default output file names if not provided
output_wr = args.output_wr if args.output_wr else args.input.replace('.csv', '_augmented_2.csv')
output_wd = args.output_wd if args.output_wd else args.input.replace('.csv', '_augmented_2.csv')
output_wi = args.output_wi if args.output_wi else args.input.replace('.csv', '_augmented_2.csv')
output_wm = args.output_wm if args.output_wm else args.input.replace('.csv', '_augmented_2.csv')

alpha_wr = args.alpha_wr if args.alpha_wr is not None else 0
alpha_wd = args.alpha_wd if args.alpha_wd is not None else 0
alpha_wi = args.alpha_wi is not None and args.alpha_wi or 0
alpha_wm = args.alpha_wm if args.alpha_wm is not None else 0

if alpha_wr == 0 and alpha_wd == 0 and alpha_wi == 0 and alpha_wm == 0:
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

        label, sentence = parts[0], get_only_chars(parts[1].strip()).lower()

        # Augment original sentence
        if alpha_type == "wr":
            aug_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=alpha_value, alpha_wd=0, alpha_wi=0, alpha_wm=0)
        elif alpha_type == "wd":
            aug_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=alpha_value, alpha_wi=0, alpha_wm=0)
        elif alpha_type == "wi":
            aug_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=0, alpha_wi=alpha_value, alpha_wm=0)
        elif alpha_type == "wm":
            aug_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, alpha_wd=0, alpha_wi=0, alpha_wm=alpha_value)
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
    if alpha_wm > 0:
        print("Running word movement augmentation + balancing...")
        augment_and_balance(args.input, output_wm, "wm", alpha_wm)

