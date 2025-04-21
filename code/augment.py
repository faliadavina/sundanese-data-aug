from eda import synonyms_dict, kelas_kata, pronouns_category, category_to_word, eda
import argparse

# Arguments to be parsed from command line
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data (Cleaned CSV format)")
ap.add_argument("--output_wr", required=False, type=str, help="output file of augmented data")
ap.add_argument("--output_wd", required=False, type=str, help="output file of augmented data")
ap.add_argument("--output_wi", required=False, type=str, help="output file of augmented data")
ap.add_argument("--alpha_wr", required=False, type=float, help="percent of words in each sentence to be replaced by synonyms")
ap.add_argument("--alpha_wd", required=False, type=float, help="percent of words in each sentence to be deleted")
ap.add_argument("--alpha_wi", required=False, type=float, help="percent of words in each sentence to be inserted")
ap.add_argument("--alpha_ws", required=False, type=float, help="percent of words in each sentence to be swapped")
args = ap.parse_args()

# Default output file names if not provided
output_wr = args.output_wr if args.output_wr else args.input.replace('.csv', '_augmented_2.csv')
output_wd = args.output_wd if args.output_wd else args.input.replace('.csv', '_augmented_2.csv')
output_wi = args.output_wi if args.output_wi else args.input.replace('.csv', '_augmented_2.csv')

# Augmetation rates
alpha_wr = args.alpha_wr if args.alpha_wr is not None else 0
alpha_wd = args.alpha_wd if args.alpha_wd is not None else 0
alpha_wi = args.alpha_wi if args.alpha_wi is not None else 0

#how much to swap words
alpha_ws = args.alpha_ws if args.alpha_ws is not None else 0
    
if alpha_wd == 0 and alpha_wi == 0 and alpha_wr == 0 and alpha_ws == 0:
    ap.error('At least one alpha should be greater than zero')

# Generate more data with standard augmentation
def gen_eda(train_orig, output_synonym, output_deletion, output_insertion, alpha_wr, alpha_wd, alpha_wi):
    # unique_sentences = set()
    # writer = open(output_file, 'w', encoding='utf-8')
    unique_synonyms = set()
    unique_deletions = set()
    unique_insertions = set()
    # unique_pronouns = set()

    writer_synonym = open(output_synonym, 'w', encoding='utf-8') if alpha_wr > 0 else None
    writer_deletion = open(output_deletion, 'w', encoding='utf-8') if alpha_wd > 0 else None
    writer_insertion = open(output_insertion, 'w', encoding='utf-8') if alpha_wi > 0 else None
    # writer_pronoun = open(output_pronoun, 'w', encoding='utf-8')

    with open(train_orig, 'r', encoding='utf-8') as f:  # specify encoding='utf-8' here
        lines = f.readlines()

    for i, line in enumerate(lines):
        parts = line.strip().split('\t')  # Data cleaned using tab as delimiter
        if len(parts) < 2:
            print(f"Skipping invalid line {i}: {line}")  # Log the invalid line
            continue  # Skip lines that don't have both a label and sentence
        
        label = parts[0]
        sentence = parts[1]

        if alpha_wr > 0:    
            synonym_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=alpha_wr, alpha_wd=0, alpha_wi=0)
            # Simpan hasil synonym replacement ke file tersendiri
            for aug_sentence in synonym_sentences:
                if isinstance(aug_sentence, str) and aug_sentence not in unique_synonyms:
                    writer_synonym.write(label + "\t" + aug_sentence + "\n")
                    unique_synonyms.add(aug_sentence) 
        
        if alpha_wd > 0:
            deletion_sentences = None
            if deletion_sentences is None: 
                deletion_sentences = []
            deletion_sentences = eda(sentence, synonyms_dict, kelas_kata, pronouns_category, category_to_word, alpha_wr=0, alpha_wd=alpha_wd, alpha_wi=0)
            if deletion_sentences is None:  #pastikan yang dari eda bukan none
                deletion_sentences = []
            # Simpan hasil deletion ke file tersendiri
            for aug_sentence in deletion_sentences:
                if aug_sentence not in unique_deletions:
                    writer_deletion.write(label + "\t" + aug_sentence + "\n")
                    writer_deletion.write(label + "\t" + sentence + "\n")
                    unique_deletions.add(aug_sentence)

        if alpha_wi > 0:
            insertion_sentences = eda(sentence, synonyms_dict, kelas_kata, alpha_wr=0, p_wd=0, alpha_wi=alpha_wi)
            for aug_sentence in insertion_sentences:
                if isinstance(aug_sentence, list):  # Jika hasilnya list kata, gabungkan menjadi kalimat
                    aug_sentence = " ".join(aug_sentence)  
                if aug_sentence not in unique_insertions:
                    writer_insertion.write(label + "\t" + aug_sentence + "\n")  # Simpan hasil augmentasi
                    writer_insertion.write(label + "\t" + sentence + "\n")  # Simpan kalimat asli sebagai referensi
                    unique_insertions.add(aug_sentence)  # Tambahkan kalimat ke set unik


        # for aug_sentence in aug_sentences:
        #     if aug_sentence not in unique_sentences:
        #             writer.write(label + "\t" + aug_sentence + "\n")
        #             unique_sentences.add(aug_sentence)
        # Flatten jika ada list of lists
        # if any(isinstance(aug, list) for aug in aug_sentences):
        #     aug_sentences = [sent for sublist in aug_sentences for sent in sublist]

        # Simpan hasil pronomina replacement ke file tersendiri
        # for aug_sentence in pronoun_sentences:
        #     if isinstance(aug_sentence, str) and aug_sentence not in unique_pronouns:
        #         writer_pronoun.write(label + "\t" + aug_sentence + "\n")
        #         unique_pronouns.add(aug_sentence)
    if writer_synonym:
        writer_synonym.close()
        print(f"Generated synonym replacement data in {output_synonym}")
    if writer_deletion:
        writer_deletion.close()
        print(f"Generated deletion data in {output_deletion}")
    if writer_insertion:
        writer_insertion.close()
        print(f"Generated insertion data in {output_insertion}")

# Main function
if __name__ == "__main__":
    # Generate augmented sentences and output into a new file
    gen_eda(args.input, output_wr, output_wd, output_wi, alpha_wr=alpha_wr, alpha_wd=alpha_wd, alpha_wi=alpha_wi)