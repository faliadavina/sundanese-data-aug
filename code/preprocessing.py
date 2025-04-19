# Baca file input
with open('data\kamus\sundanese_synonyms.csv', 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

output_lines = []
for line in lines:
    line = line.strip()
    parts = line.split(',')
    if parts[0] == 'kata':
        output_lines.append('kata,sinonim')
    else:
        kata = parts[0]
        sinonim = parts[1:]
        
        if len(sinonim) > 2:
            sinonim_str = ",".join(sinonim)
            output_lines.append(f'{kata},"{sinonim_str}"')
        else:
            output_lines.append(f'{kata},{",".join(sinonim)}')

# Langsung tulis manual TANPA pakai csv.writer
with open('output.csv', 'w', encoding='utf-8') as outfile:
    outfile.write('\n'.join(output_lines))
