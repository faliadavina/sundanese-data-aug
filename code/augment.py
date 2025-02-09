from eda import sundanese_synonyms, kelas_kata, eda
import argparse

# Arguments to be parsed from command line
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data (Cleaned CSV format)")
ap.add_argument("--output", required=False, type=str, help="output file of augmented data")
ap.add_argument("--num_aug", required=False, type=int, help="number of augmented sentences per original sentence")
ap.add_argument("--alpha_sr", required=False, type=float, help="percent of words in each sentence to be replaced by synonyms")
ap.add_argument("--alpha_wd", required=False, type=float, help="percent of words in each sentence to be deleted")
ap.add_argument("--alpha_wi", required=False, type=float, help="percent of words in each sentence to be inserted")
args = ap.parse_args()

# Output file
output = args.output if args.output else args.input.replace('.csv', '_augmented_2.csv')

# Number of augmented sentences to generate per original sentence
num_aug = args.num_aug if args.num_aug else 9

# How much to replace each word by synonyms
alpha_sr = args.alpha_sr if args.alpha_sr is not None else 0

#how much to delete words
alpha_wd = args.alpha_wd if args.alpha_wd is not None else 0

#how much to insertion words
alpha_wi = args.alpha_wi if args.alpha_wi is not None else 0
    
if alpha_wd == 0 and alpha_wi == 0 and alpha_sr == 0:
    ap.error('At least one alpha should be greater than zero')

# Generate more data with standard augmentation
def gen_eda(train_orig, output_file, alpha_sr, alpha_wd, alpha_wi):
    unique_sentences = set()
    writer = open(output_file, 'w', encoding='utf-8')

    with open(train_orig, 'r', encoding='utf-8') as f:  # specify encoding='utf-8' here
        lines = f.readlines()

    for i, line in enumerate(lines):
        parts = line[:-1].split('\t')  # Data cleaned using tab as delimiter
        if len(parts) < 2:
            print(f"Skipping invalid line {i}: {line}")  # Log the invalid line
            continue  # Skip lines that don't have both a label and sentence
        
        label = parts[0]
        sentence = parts[1]
        aug_sentences = eda(sentence, sundanese_synonyms, kelas_kata, alpha_sr=alpha_sr if alpha_sr > 0 else 0, p_wd=alpha_wd if alpha_wd > 0 else 0,
                             alpha_wi=alpha_wi if alpha_wi > 0 else 0) 
        
        for aug_sentence in aug_sentences:
            if aug_sentence not in unique_sentences:
                    writer.write(label + "\t" + aug_sentence + "\n")
                    unique_sentences.add(aug_sentence)
                
    writer.close()
    print("Generated augmented sentences with EDA for " + train_orig + " to " + output_file + " with num_aug=")

# Main function
if __name__ == "__main__":
    # Generate augmented sentences and output into a new file
    gen_eda(args.input, output, alpha_sr=alpha_sr, alpha_wd=alpha_wd, alpha_wi=alpha_wi)