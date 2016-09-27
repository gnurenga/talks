from ewmh import EWMH

ewmh = EWMH()

def filter_window(wins, windowclass):
    for w in wins:
        if w.get_wm_class()[1] == windowclass:
            return w


wins = ewmh.getClientList()

user_input = raw_input("Enter a Valid Input:")

diawin = filter_window(wins, 'Dia-normal')

ewmh.setActiveWindow(diawin)

if user_input == "1":
    ewmh.setWmState(diawin, 1, '_NET_WM_STATE_FULLSCREEN')

ewmh.display.flush()
