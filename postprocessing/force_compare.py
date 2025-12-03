import argparse
import csv
import os
import re


def parse_properties(header_line):
    m = re.search(r'Properties=([^ ]+)', header_line)
    if not m:
        return {}
    toks = m.group(1).split(':')
    positions, col = {}, 0
    for i in range(0, len(toks), 3):
        name = toks[i]
        dim = int(toks[i + 2])
        positions[name] = (col, dim)
        col += dim
    return positions


def process_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f, \
         open(output_path, "w", newline="", encoding="utf-8") as out_f:

        writer = csv.writer(out_f)

        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            n_atoms = int(line)
            header_line = f.readline()
            if not header_line:
                break

            pos = parse_properties(header_line)
            if "forces" not in pos or "MACE_forces" not in pos:
                print("Warning: 'forces' or 'MACE_forces' not found in Properties. No output written.")
                return
            forces_start, forces_dim = pos["forces"]
            mace_start, mace_dim = pos["MACE_forces"]

            for _ in range(n_atoms):
                atom_line = f.readline()
                if not atom_line:
                    return
                atom_line = atom_line.strip()
                if not atom_line:
                    continue

                tokens = atom_line.split()
                f_dft = [float(tokens[forces_start + i]) for i in range(forces_dim)]
                f_mace = [float(tokens[mace_start + i]) for i in range(mace_dim)]

                for i in range(3):  # x, y, z
                    writer.writerow([abs(f_dft[i]), abs(f_mace[i])])


def main():
    parser = argparse.ArgumentParser(
        description="Extract absolute 'forces' and 'MACE_forces' from an extxyz file to CSV."
    )
    parser.add_argument("input", help="Input xyz (extxyz) file path.")
    args = parser.parse_args()

    root, _ = os.path.splitext(args.input)
    output_path = root + "_forces_abs.csv"

    process_file(args.input, output_path)


if __name__ == "__main__":
    main()
