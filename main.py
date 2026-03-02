from script.main import compress, decompress
from sys import argv
import os

def command(arguments: list):
    mode = "text"
    for index in range(len(arguments)):
        if arguments[index].startswith("-"):
            argument = arguments[index].lstrip("-")
            if argument != "mode": print()
            match argument:
                case "help":
                    print("> yz -help")
                    print("> yz -compress [input file] [output file]")
                    print("> yz -decompress [input file] [output file]")
                    print("> yz -mode [text (standard) or binary]")
                    # !!! COPY TO END !!!
                case "mode":
                    if index + 1 >= len(arguments) or arguments[index + 1].startswith("-"):
                        print("No mode providet")
                        print("> -mode [text or binary]")
                        return
                    else:
                        match arguments[index + 1]:
                            case "text": mode = "text"
                            case "binary":
                                mode = "binary"
                                print("\n\"binary\" mode can make the file larger!")
                            case _:
                                print("Not suportet mode")
                                print("> -mode [text or binary]")
                case "compress":
                    if index + 1 >= len(arguments) or arguments[index + 1].startswith("-"):
                        print("No input file providet")
                        print("> -compress [input file] [output file]")
                        return
                    elif index + 2 >= len(arguments) or arguments[index + 2].startswith("-"):
                        print("No output file providet")
                        print("> -compress [input file] [output file]")
                        return
                    else:
                        input_path = arguments[index + 1]
                        output_path = arguments[index + 2]
                        if not os.path.isfile(input_path):
                            print("Coudent find input file")
                            return
                        
                        compress.startF(
                            open(input_path, "r").read() if mode == "text" else open(input_path, "rb").read().hex(),
                            output_path,
                            mode
                        )
                case "decompress":
                    if index + 1 >= len(arguments) or arguments[index + 1].startswith("-"):
                        print("No input file providet")
                        print("> -decompress [input file] [output file]")
                        return
                    elif index + 2 >= len(arguments) or arguments[index + 2].startswith("-"):
                        print("No output file providet")
                        print("> -decompress [input file] [output file]")
                        return
                    else:
                        input_path = arguments[index + 1]
                        output_path = arguments[index + 2]
                        if not os.path.isfile(input_path):
                            print("Coudent find input file")
                            return
                        
                        decompress.startF(
                            open(input_path, "rb").read(),
                            output_path,
                            mode
                        )
                case _:
                    print(f"Unknow argument \"{argument}\"")

if __name__ == "__main__":
    if len(argv) <= 1:
        print()
        print("> yz -help")
        print("> yz -compress [input file] [output file]")
        print("> yz -decompress [input file] [output file]")
        print("> yz -mode [text (standard) or binary]")

        while True:
            print()
            splits = input("> yz ").split("\"")
            index = 0
            arguments = []
            for split in splits:
                if index % 2 == 0:
                    for new_split in split.split(" "):
                        if new_split != "":
                            arguments.append(new_split)
                elif split != "":
                    arguments.append(split)
                index += 1
            command(arguments)
    else:
        command(argv)