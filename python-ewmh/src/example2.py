from ewmh import EWMH
ewmh = EWMH()

wins = ewmh.getClientList()

for wid in wins:
    print wid.get_wm_class()[1]
