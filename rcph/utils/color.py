def colored_text(text, color,  *features, reset = True):

    colors = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magneta": "35",
        "cyan": "36",
        "gray": "37",

        "reset": "0",
        "bold": "1",
        "faint": "2",
        "italic": "3",
        "underline": "4",
        "blink": "5",
        "negative": "7",
        "crossed": "9",
    }

    light = None
    if len(color.split()) == 2:
        light, color = color.split()

    result = f'\033[{1 if light else 0};{colors.get(color.lower(), "")}m'
    for feature in features:
        if feature.lower() in colors.keys():
            result += f'\033[{colors[feature.lower()]}m'

    return result + str(text) + ("\033[0m" if reset else '')