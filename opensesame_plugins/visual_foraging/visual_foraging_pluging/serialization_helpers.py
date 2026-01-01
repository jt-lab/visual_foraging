import json

def serialize_elements(elements):
    """
    Serialize a list of dicts into OpenSesame-safe angle-brace format.

    Args:
        elements (list of dict): List of element dictionaries.

    Returns:
        str: Multi-line string, one element per line.
    """

    if type(elements) == dict:
        elements = [elements]

    lines = []
    for element in elements:
        j = json.dumps(element)
        j = j.replace("{", "<").replace("}", ">")
        lines.append(j)
    return "\n".join(lines)


def deserialize_elements(text):
    """
    Deserialize OpenSesame-safe angle-brace formatted string into a list of dicts.

    Args:
        text (str): Serialized elements string.

    Returns:
        list of dict: Parsed element dictionaries.
    """
    result = []
    if not text:
        return result

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        try:
            j = line.replace("<", "{").replace(">", "}")
            element = json.loads(j)
            result.append(element)
        except Exception as e:
            print("Failed to parse element:", e)
    if len(result) == 1:
        return result[0]
    return result

