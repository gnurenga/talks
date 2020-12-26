# this is for M-x insert-file  emacs
# Solution 1 not a good code 
        for line in new_value:
            if "mac" in line or "time" in line:
                cline = line.strip().split()
                ckey = cline[0].split(":")[0]
                cvalue = cline[1].strip()
                data_dict[str(index)][ckey] = cvalue
            else:
                cline = line.strip().split(":")
                cvalue = cline[1].strip()
                ckey = cline[0].strip()
                data_dict[str(index)][ckey] = cvalue
