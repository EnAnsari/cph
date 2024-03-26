import random

def read_quotes(filename):
    with open(filename, 'r') as f:
        quotes = f.readlines()
    return quotes

def format_quote(quote, max_words_per_line=10):
    words = quote.strip().split()
    formatted_quote = ""
    current_line = ""
    for word in words:
        if len(current_line.split()) + 1 > max_words_per_line:
            formatted_quote += current_line + "\n"
            current_line = ""
        current_line += word + " "
    formatted_quote += current_line.strip()

    return formatted_quote


def print_random_quote(quotes, max_words_per_line=10):

    random_quote = random.choice(quotes)
    formatted_quote = format_quote(random_quote, max_words_per_line)
    print(formatted_quote)


if __name__ == "__main__":
    quotes_file = "quotes.txt"
    quotes = read_quotes(quotes_file)
    print_random_quote(quotes)
