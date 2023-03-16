import sys
import os


def print(*msgs, style = "[+]", dontStyle = False):
    if dontStyle:
        msg = "".join( str(msg) for msg in msgs)
        sys.stdout.write("{}\n".format(msg))

        return None

    msg = " ".join( str(msg) for msg in msgs)
    sys.stdout.write("{} {} {}\n".format(style, msg, style))
