import pytest

from app.utils.strings import pluralize


def test_convert_words():
	assert pluralize("cat") == "cats"
	assert pluralize("box") == "boxes"
	assert pluralize("baby") == "babies"
	assert pluralize("wolf") == "wolves"
	assert pluralize("potato") == "potatoes"
	assert pluralize("knife") == "knives"

def test_empty_input_raises_error():
    with pytest.raises(ValueError, match="Word must be a non-empty string"):
        pluralize("")
