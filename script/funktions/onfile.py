from sys import argv
import os

file = open(argv[1], "r").read()
file_lines = file.splitlines()

line_index = 0
for line in file_lines:
    paths = []
    if line.lstrip(" ").startswith("from"):
        import_data = line.lstrip(" ").split(" ")
        if os.path.isdir(import_data[1].replace(".", "\\")):

            paths.append(import_data[1].replace(".", "\\") + "\\" + import_data[3].rstrip(",") + ".py")

            if import_data[3].endswith(","):
                index = 3
                while import_data[index].endswith(","):
                    paths.append(import_data[1].replace(".", "\\") + "\\" + import_data[index + 1].rstrip(",") + ".py")
                    index += 1
        
        index = 0
        for path in paths:
            print(line_index, "->", path)
            import_data = open(path, "r").read().splitlines()

            functions = []
            for line in import_data:
                if line.lstrip(" ").startswith("def"):
                    functions.append(line.lstrip(" ").lstrip("def ").split("(")[0])
            functions.sort(key=len, reverse=True)

            class_name = path.split("\\")[-1].rstrip(".py")

            index2 = 0
            imports = []
            for line in import_data:
                import_data[index2] = (" " * (len(file_lines[line_index]) - len(file_lines[line_index].lstrip(" ")) + 4)) + import_data[index2]

                for function in functions:
                    if function in line and not line.lstrip(" ").startswith("def"):
                        import_data[index2] = import_data[index2].replace(function + "(", class_name + "." + function + "(")
                        break
                
                if "import" in line:
                    imports.append(line)
                    import_data.pop(index2)

                if "f\"" in line:
                    import_data[index2] = import_data[index2].replace("f\"", "\"").replace("{", "\" + str(").replace("}", ") + \"")
                
                if "__name__" in line and "\"__main__\"" in line:
                    main_hight = len(line) - len(line.lstrip(" "))
                    index3 = index2 + 1
                    try:
                        while len(import_data[index3]) - len(import_data[index3].lstrip(" ")) > main_hight:
                            import_data.pop(index2 + 1)
                            index3 += 1
                    except: pass
                    import_data.pop(index2)

                index2 += 1

            if len(imports) <= 0:
                new_text = f"class {class_name}:\n{"\n".join(import_data)}"
            else:
                new_text = f"{"\n".join(imports)}\nclass {class_name}:\n{"\n".join(import_data)}"

            if index <= 0:
                file_lines[line_index] = new_text
            else:
                file_lines[line_index] += f"\n\n{new_text}"
            
            index += 1
    
    line_index += 1

#print("-"*25)
#print("\n".join(file_lines))
open(argv[2], "w").write("\n".join(file_lines))