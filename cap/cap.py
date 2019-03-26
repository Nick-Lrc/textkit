from reader.config_reader import ConfigReader

CONFIGS = ConfigReader.read("./cap/cap.json")
TITLE_CONFIGS = CONFIGS["cap_title"]

def cap_title(title, delim=" "):
    input = title.split(delim)
    if len(input) < 1:
        return []
    output = [input[0].capitalize()]
    for word in input[1:]:
        if word in TITLE_CONFIGS["articles"] \
                or word in TITLE_CONFIGS["preps"] \
                or word in TITLE_CONFIGS["coord_conjs"]:
            output.append(word)
        else:
            output.append(word.capitalize())
    return delim.join(output)
