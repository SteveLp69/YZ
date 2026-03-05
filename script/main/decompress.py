from bitstring import BitArray
from sys import exit
#import json

def startF(data: bytes, filepath: str = "file.txt", mode: str = "text"):
    """Writes the output to a file"""
    data = tree(data)
    print("-"*25)
    file_text = repeating_decompress(data)
    
    if mode == "text":
        open(filepath, "w").write(file_text)
    elif mode == "binary":
        open(filepath, "wb").write(gen_binary_from_bin(file_text))

def startR(data: bytes, mode: str = "text"):
    """Returns the output"""
    data = tree(data)
    print("-"*25)
    file_text = repeating_decompress(data)

    if mode == "text":
        return file_text
    elif mode == "binary":
        return gen_binary_from_bin(file_text)

def repeating_decompress(data: str):
    print("Repeating decompresser")

    lines = data.splitlines()
    index = 0
    for line in lines:
        if line.startswith("<") and line.endswith(">"):
            line_index = int(line.lstrip("<").rstrip(">").split(":")[0])
            spaces = int(line.lstrip("<").rstrip(">").split(":")[1])
            
            lines[index] = (" "*spaces) + lines[line_index].lstrip(" ")
            
        index += 1

    return "\n".join(lines)

def tree(data: bytes):
    print("Tree decompression")
    data = BitArray(hex=data.hex()).bin
    
    tabel_length = bitstring_to_int(data[:8])
    data = data[8:]
    bin_values = data[len(data) - (tabel_length * 8):]
    values = gen_list_form_bin(bin_values)
    lock_up_table, tree = gen_tree(values)
    #print(json.dumps(lock_up_table, indent=4))
    data = data[:len(data) - (tabel_length * 8)]

    file_text = ""
    last_file_text = ""
    index = 0
    while len(data) > 0:
        for index in range(len(lock_up_table.values())):
            bin_combi = list(lock_up_table.values())[index]
            if data.startswith(bin_combi):
                file_text += list(lock_up_table.keys())[index]
                #print(data[:len(bin_combi)], "->", list(lock_up_table.keys())[index])
                data = data[len(bin_combi):]
                break
        if file_text == "":
            exit()
        if file_text == last_file_text:
            break
        
        last_file_text = file_text
        index += 1

    return file_text

def gen_list_form_bin(bitstring: str) -> list:
    if len(bitstring) % 8 != 0:
        exit()

    values = []

    for index in range(int(len(bitstring) / 8)):
        values.append(
            chr(bitstring_to_int(bitstring[index * 8:(index + 1) * 8]))
        )
    
    return values

def gen_binary_from_bin(bitstring: str):
    if len(bitstring) % 8 != 0:
        exit()

    values = []

    for index in range(int(len(bitstring) / 8)):
        values.append(
            ord(bitstring_to_int(bitstring[index * 8:(index + 1) * 8]))
        )
    
    return bytes(values)

def gen_tree(values: list, death = 0):
    if len(values) <= 0:
        return {}

    tree = []
    lock_up_table = {}
    tree.append(values[0])
    lock_up_table.update(
        {
            values[0]:
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

def bitstring_to_int(bitstring):
    if len(bitstring) != 8:
        exit()
    
    return int(bitstring, 2)

def bitstring_to_bytes(bitstring):
    if len(bitstring) % 8 != 0:
        exit()
    
    byte_array = []
    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i+8]
        byte_array.append(int(byte, 2))
    
    return bytes(byte_array)

if __name__ == "__main__":
    startF(open("test.yz", "rb").read(), "test.txt")
