def pluralize(word: str) -> str:
    """Convert an English word to its plural form.

    Implements common English pluralization rules:
        - Most words: add 's' (cat → cats)
        - Words ending in s, sh, ch, x, z: add 'es' (box → boxes)
        - Words ending in consonant + y: y → ies (baby → babies)
        - Words ending in f or fe: f/fe → ves (wolf → wolves, knife → knives)
        - Words ending in o: add 'es' (potato → potatoes)

    Note:
        This function handles regular pluralization rules only.
        Irregular plurals (person → people, child → children) are not handled
        and should be handled separately or added to exceptions list.

    Args:
        word (str): The singular English word to pluralize.
            Must be non-empty string containing only letters.

    Returns:
        str: The plural form of the input word.

    Raises:
        ValueError: If input word is empty or contains non-alphabetic characters.

    Example:
        >>> pluralize("cat")
        'cats'
        >>> pluralize("box")
        'boxes'
        >>> pluralize("baby")
        'babies'
        >>> pluralize("wolf")
        'wolves'
        >>> pluralize("potato")
        'potatoes'
        >>> pluralize("knife")
        'knives'
    """
    if not word or not isinstance(word, str):
        raise ValueError("Word must be a non-empty string")

    if not word.isalpha():
        raise ValueError("Word must contain only letters")

    word_lower = word.lower()

    if word_lower.endswith(("s", "sh", "ch", "x", "z")):
        return word + "es"

    elif (
        word_lower.endswith("y")
        and len(word_lower) > 1
        and word_lower[-2] not in "aeiou"
    ):
        return word[:-1] + "ies"

    elif word_lower.endswith("f"):
        return word[:-1] + "ves"
    elif word_lower.endswith("fe"):
        return word[:-2] + "ves"

    elif word_lower.endswith("o"):
        return word + "es"

    return word + "s"
