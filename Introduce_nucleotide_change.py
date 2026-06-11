input_file = input("Input FASTA file path: ")
output_file = input("Output FASTA file path: ")
position = int(input("Position to change: "))
new_base = input("New nucleotide: ").upper()

with open(input_file) as f:
    lines = f.readlines()

header = lines[0]
seq = "".join(line.strip() for line in lines[1:]).upper()

seq = seq[:position - 1] + new_base + seq[position:]

with open(output_file, "w") as f:
    f.write(header)
    f.write(seq)