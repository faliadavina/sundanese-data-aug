import pandas as pd

# Baca file txt dengan separator tab
# df = pd.read_csv("data\balancing\eksperimen_deletion_balanced.txt", sep='\t', header=None, names=['label', 'text'])
df = pd.read_csv("data/test/word_deletion02_balanced.txt", sep='\t', header=None, names=['label', 'text'])

# Hitung jumlah label
label_counts = df['label'].value_counts()

# Cetak hasilnya
print("Distribusi Label Emosi:")
for label, count in label_counts.items():
    print(f"{label}: {count}")
