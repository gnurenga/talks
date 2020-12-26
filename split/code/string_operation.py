def convert_to_dict(values):
    data_dict = {}
    for index, value in enumerate(values):
        data_dict[str(index)] = {}
        new_value = value.split(",")
        print("row {0}, value {1}".format(index, new_value))
        print("---------------------------------------------\n")
        # problem 
        for line in new_value:
            cline = line.strip().split(":")
            cvalue = cline[1].strip()
            ckey = cline[0].strip()
            data_dict[str(index)][ckey] = cvalue
        # Solution 1 not a good code 
        # for line in new_value:
        #     if "mac" in line or "time" in line "servicetype" in line:
        #         cline = line.strip().split()
        #         ckey = cline[0].split(":")[0]
        #         cvalue = cline[1].strip()
        #         data_dict[str(index)][ckey] = cvalue
        #     else:
        #         cline = line.strip().split(":")
        #         cvalue = cline[1].strip()
        #         ckey = cline[0].strip()
        #         data_dict[str(index)][ckey] = cvalue
        # Solution 2 using max split 
        # for line in new_value:
        #     cline = line.strip().split(":", 1)
        #     cvalue = cline[1].strip()
        #     ckey = cline[0].strip()
        #     data_dict[str(index)][ckey] = cvalue

        
    return data_dict
        
        
def convert_to_rows(filename):
    with open(filename, "r") as data:
        lines = data.readlines()
        print("The three rows from the file")
        print(lines)
        print("-------------------------------------\n")
        nlines = lines[0].strip().split("}")
        
        rows = []
        
        for _line in nlines[:-1]:
            row = _line.split("{")
            rows.append(row[1])
            
            
        print("The the three rows after split and cleaned\n")
        print(rows)
        print("-------------------------------------\n")
        cleaned_data = convert_to_dict(rows)
        print(cleaned_data)
        return cleaned_data

if __name__ == "__main__":
    convert_to_rows("data.txt")
