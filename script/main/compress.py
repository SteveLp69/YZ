#import json

def startF(data: str, filepath: str = "file.yz", mode: str = "text"):
    """Writes the output to a file"""
    if mode == "text":
        og_file_size = len(data)
    elif mode == "binary":
        og_file_size = len(data) / 2

    data = repeating_optimizer(data)
    print("-" * 25)
    print()
    file_bits = tree(data)

    print("-" * 25)
    print()
    print(f"All optimizetions made the file ~{round(len(file_bits) / 8 / og_file_size * 100, 2)}% of the original size")

    open(filepath, "wb").write(bitstring_to_bytes(file_bits))

def startR(data: str, mode: str = "text"):
    """Returns the output"""
    og_file_size = len(data)

    data = repeating_optimizer(data)
    print("-" * 25)
    print()
    file_bits = tree(data)

    print("-" * 25)
    print()
    print(f"All optimizetions made the file ~{round(len(file_bits) / 8 / og_file_size * 100, 2)}% of the original size")

    return file_bits

def repeating_optimizer(data: str):
    print("Repeating optimizer")

    og_data_size = len(data)

    lines = data.splitlines()
    line_positions = {}
    index = 0
    for line in lines:
        if line.lstrip(" ") != "":
            if line.lstrip(" ") not in line_positions.keys():
                line_positions.update({line.lstrip(" "): index})
            else:
                lines[index] = f"<{line_positions[line.lstrip(" ")]}:{len(line) - len(line.lstrip(" "))}>"
            
        index += 1

    print("-" * 25)
    print(og_data_size, "->", len("\n".join(lines)), f"(~{round(len("\n".join(lines)) / og_data_size * 100, 2)}%)")

    return "\n".join(lines)

def tree(data: str):
    """Can compress the data down to ~75% off the original size"""

    print("Tree compression")

    og_data_size = len(data)

    symbels = {}
    for symbel in data:
        if not symbel in symbels.keys():
            symbels.update({symbel: [1, symbel]})
        else:
            symbels[symbel][0] += 1
    
    values = list(symbels.values())
    values.sort(reverse=True)

    lock_up_table, tree = gen_tree(values)
    #print(json.dumps(lock_up_table, indent=4))

    values = list(symbels.values())
    values.sort(reverse=True)

    bit_tabel = bit_list(values)

    extension = format(len(values), "08b")

    file_bits = ""
    for symbel in data:
        file_bits += lock_up_table[symbel]

    while len(file_bits) % 8 > 0:
        file_bits += "0"

    file_bits = extension + file_bits + bit_tabel

    print("-" * 25)
    print(og_data_size, "->", len(file_bits) / 8, f"(~{round(len(file_bits) / 8 / og_data_size * 100, 2)}%)")

    return file_bits

def bit_list(values: list) -> str:
    bits = ""

    for value in values:
        new_value = format(ord(value[1]), "08b")
        bits += new_value
    
    return bits

def gen_tree(values: list, death = 0):
    if len(values) <= 0:
        return {}

    tree = []
    lock_up_table = {}
    tree.append(values[0][1])
    lock_up_table.update(
        {
            values[0][1]:
            "0" + "0"*death + "1" if death <= 8 else get_number(int(str(death / 8).split(".")[0])) + "0" + "0" * (death - int(str(death / 8).split(".")[0]) * 8) + "1"
        }
    )
    
    new_values = values
    new_values.pop(0)
    returns = gen_tree(values, death + 1)
    try:
        returned_lock_up_table, returned_tree = returns
        if returned_tree:
            tree.append(returned_tree)
        lock_up_table.update(returned_lock_up_table)
    except: pass

    return lock_up_table, tree

def get_number(n: int) -> str:
    return "1" * n

def bitstring_to_bytes(bitstring):
    if len(bitstring) % 8 != 0:
        raise ValueError("Die Länge des Bitstrings muss ein Vielfaches von 8 sein.")
    
    byte_array = []
    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i+8]
        byte_array.append(int(byte, 2))
    
    return bytes(byte_array)

if __name__ == "__main__":
    startF(open("C:\\Users\\PC 2025\\Documents\\Arduino\\ring_power_button\\ring_power_button.ino", "r").read(), "test.yz")