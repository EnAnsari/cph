from rcph.utils import random
from rcph.config.constant import *

def make_a_quote(quotes):
    random_quote = random.choice(quotes)
    words = random_quote.strip().split()
    formatted_quote = ""
    current_line = ""
    for word in words:
        if len(current_line.split()) + 1 > MAXSIGNLINE:
            formatted_quote += "\t" + current_line + "\n"
            current_line = ""
        current_line += word + " "
    formatted_quote += "\t" + current_line.strip()
    return formatted_quote