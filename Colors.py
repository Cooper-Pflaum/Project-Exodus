class colors:
    reset     = '\033[0m'
    bold      = '\033[1m'
    faint     = '\033[2m'
    italics   = '\033[3m'
    underline = '\033[4m'
    red       = '\033[91m'
    green     = '\033[92m'
    blue      = '\033[94m'
    cyan      = '\033[96m'
    white     = '\033[97m'
    yellow    = '\033[93m'
    purple    = '\033[95m'
    grey      = '\033[90m'
    black     = '\033[90m'

    info = reset + grey + "[*]"
    good = reset + green + "[✓]"
    bad = reset + red + "[" + red + "!" + red + "]"
