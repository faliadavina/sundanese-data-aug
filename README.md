### **README: Data Augmentation Command**

#### **Deskripsi**

File ini berisi informasi tentang perintah yang digunakan untuk menjalankan proses data augmentation pada dataset bahasa Sunda menggunakan script `augment.py`.

#### **Command yang Digunakan**

```bash
python code/augment.py --input=data/main_data/data2.txt --output_sr=data/data_augmented_new/dataset_sundanese_augmented_sr_alpha01.txt --alpha_wr=0.1
```

#### **Penjelasan Argumen**

- `python code/augment.py` → Menjalankan script augmentasi `augment.py` yang terletak di folder `code/`.
- `--input=data/main_data/data2.txt` → Menentukan file input yang akan diproses (`data2.txt`).
- `--output_sr=data/data_augmented_new/dataset_sundanese_augmented_sr_alpha01.txt` → Menentukan lokasi dan nama file hasil augmentasi.
- `--alpha_wr=0.1` → Menentukan nilai alpha untuk Word Replacement (penggantian kata) dengan nilai 0.1.
