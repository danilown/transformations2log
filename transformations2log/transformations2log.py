import re
from typing import List, Optional, Tuple


def remove_comments(text: str) -> str:
    """Remove python-like comments from a string

    Args:
        text (str): String with python-like comments to be removed

    Returns:
        str: String with removed comments
    """

    return re.sub(r"#.*", "", text)


def get_starts(expression: str, text: str) -> List[int]:
    """Get the starting positions of the occurrences of 'expression' within
        'text'

    Args:
        expression (str): expression we are searchin within the text.
        text (str): text where the expression should be found.

    Returns:
        List[int]: List of indexes indicating the starting of each found
            expression.
    """

    return [m.start() for m in re.finditer(expression, text)]


def replace_within_marker(
    text: str, old: str, new: str, marker_pair: Optional[Tuple[str, str]] = ("(", ")")
) -> str:
    """Replace replace characters in a string within parentheses, brackets or
        other wishes right now, old and new have to be single character strings

    Args:
        text (str): Text which will have its characters replaces
        old (str): String to be substituted
        new (str): New string that will replace the old one
        marker_pair (Optional[tuple[str, str]], optional): The characters that
            delimiter the area where the substitution will take place.
            Defaults to ('(', ')').

    Raises:
        ValueError: When 'new' or 'old' have more then one character

    Returns:
        str: New string with the replaced strings only withing the markers
    """

    if len(old) > 1 or len(new) > 1:
        raise ValueError(
            "In this current version, this function can only search and"
            " substitute single character strings. len(old) = {0}"
            " and len(new) = {1}".format(len(old), len(new))
        )

    opening, closing = marker_pair
    new_text = list(text)

    pos_text = 0
    while pos_text < len(text):
        if text[pos_text] == opening:
            count = 1
            while True:
                pos_text += 1
                if text[pos_text] == closing:
                    count -= 1

                if count == 0:
                    break

                if text[pos_text] == old:
                    new_text[pos_text] = new

                if text[pos_text] == opening:
                    count += 1

        pos_text += 1

    return "".join(new_text)


def transformations2log(
    path: str, transforms2replace: Optional[Tuple[str, str]] = []
) -> List[List[str]]:
    """Read a file given a path and will extract the list of transformations
        used inside the transforms.Compose construction. It will generate a
        list in which each index is a list of the transformations inside all
        found occurrences of 'transforms.Compose' e.g. on for training and
        another one for testing/validation. The order will be the same as
        within the script.

    Args:
        path (str): Path to script which we want to log the transformations.
        transforms2replace (Optional[Tuple[str, str]], optional): List of
            Tuples indicating if some expression needs to be substituted when
            generating a log, e.g. when using a variable 'SIZE' and you want it
            to be logged as 224. Each tuple is organized as
            ('original_expression', 'new_expression'). Defaults to [].

    Returns:
        List[List[str]]: List containing the found occurrences of
            transforms.Compose and within each list you find a list of the
            transformations used.
    """

    with open(path, "r") as f:
        script = f.read()

    for org, new in transforms2replace:
        script = script.replace(org, new)

    script = remove_comments(script)

    matched_text = []
    # checking how many transformations we are looking for
    found_transforms = get_starts(r"transforms\.Compose", script)[::-1]

    # getting the text inside the array of transformations
    total_found_transforms = len(found_transforms)
    pos_text = found_transforms.pop()
    while len(matched_text) != total_found_transforms:
        if script[pos_text] == "[":
            count = 1
            text_inside = ""
            while True:
                pos_text += 1
                if script[pos_text] == "]":
                    count -= 1

                if count == 0:
                    matched_text.append(text_inside)
                    if len(found_transforms) > 0:
                        pos_text = found_transforms.pop()
                    break

                text_inside += script[pos_text]
                if script[pos_text] == "[":
                    count += 1
        else:
            pos_text += 1

    filtered_matched_text = [
        "".join(t.replace("\n", "").split(" ")) for t in matched_text
    ]

    transforms_list = []
    for text in filtered_matched_text:
        # convert the , inside the function calls to ; to facilitate the split
        function_list = replace_within_marker(text, ",", ";").split(",")

        # converting the ; back to , and appending it to the final list
        transforms_list.append(
            [t.replace(";", ",") for t in function_list if len(t) > 0]
        )

    return transforms_list
