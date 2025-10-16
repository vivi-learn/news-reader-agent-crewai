from crewai.tools import tool

@tool
def count_letters(sentence: str):
    """
    This function is to count the amount of letters in a sentence.
    The input is a 'sentence' string.
    the output is a number.
    """
    print(f"Counting the amount of letters in the sentence: {sentence}")
    return len(sentence)
