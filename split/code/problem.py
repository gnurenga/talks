        # problem 
        for line in new_value:
            cline = line.strip().split(":")
            cvalue = cline[1].strip()
            ckey = cline[0].strip()
            data_dict[str(index)][ckey] = cvalue
