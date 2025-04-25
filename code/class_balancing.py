from eda import eda, get_only_chars, get_kelas_kata, get_sundanese_synonyms, get_unique_synonym, load_synonyms, load_kelas_kata, load_pronouns
import pandas as pd
import random
from tqdm import tqdm

# Fungsi membaca file txt ke DataFrame
def load_txt_dataset(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                label, text = parts
                data.append({'label': label, 'text': text})
    return pd.DataFrame(data)

# Fungsi menyimpan DataFrame ke txt
def save_txt_dataset(df, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        for _, row in df.iterrows():
            file.write(f"{row['label']}\t{row['text']}\n")

# Fungsi balancing
def balance_dataset(df, eda_function, synonyms_dict, kelas_dict, alpha_wr=0.1, alpha_wd=0.1, alpha_wi=0.1, threshold=1.5):
    label_groups = df.groupby('label')
    label_counts = label_groups.size().to_dict()
    max_count = max(label_counts.values())
    min_count = min(label_counts.values())
    ratio = max_count / min_count

    print(f"\nJumlah data per label sebelum balancing: {label_counts}")
    print(f"Rasio max/min = {ratio:.2f}")

    balanced_data = []

    for label, group_df in label_groups:
        samples = group_df.copy()
        texts = samples['text'].tolist()

        if ratio > threshold:
            # Undersample
            if len(texts) > min_count:
                texts = random.sample(texts, min_count)
        else:
            # Oversample using augmentation
            augmented_texts = texts[:]
            index = 0
            while len(augmented_texts) < max_count:
                original = texts[index % len(texts)]
                augmented = eda_function(original, synonyms_dict, kelas_dict, alpha_wr, alpha_wd, alpha_wi)
                augmented_texts += augmented[1:]  # skip original
                index += 1
            texts = augmented_texts[:max_count]

        for t in texts:
            balanced_data.append({'label': label, 'text': t})

    final_df = pd.DataFrame(balanced_data)
    print("Jumlah data per label setelah balancing:", final_df['label'].value_counts().to_dict())
    return final_df

if __name__ == "__main__":
    # Load data txt
    df = load_txt_dataset("data/falia/eksperimen_fix.txt")

    # Dummy dict, ganti ini juga dengan kamusmu nanti
    file_path_synonym = 'data/kamus/sundanese_synonyms.csv'
    synonyms_dict = load_synonyms(file_path_synonym)
    used_synonyms_map = {}

    file_path_kelas_kata = 'data/kamus/new_dataset_kelas_kata.txt'
    kelas_dict = load_kelas_kata(file_path_kelas_kata)

    # Balancing dataset
    balanced_df = balance_dataset(
        df,
        eda_function=eda,
        synonyms_dict=synonyms_dict,
        kelas_dict=kelas_dict,
        alpha_wr=0.1,
        alpha_wd=0.1,
        alpha_wi=0.1
    )

    # Simpan ke file
    save_txt_dataset(balanced_df, "data/falia/eksperimen_fix1.txt")
