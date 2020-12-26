# This will be used for demo in emacs
# Solution 2 using max split 
        for line in new_value:
            cline = line.strip().split(":", 1)
            cvalue = cline[1].strip()
            ckey = cline[0].strip()
            data_dict[str(index)][ckey] = cvalue
