import re


def normalise(text):
    # make it lowercase and remove punctuation like dots or commas and collapse whitespace
    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def is_correct(response, answer):
    # check if the answer we get is anywhere in the actual response of ai
    norm_answer = normalise(answer)
    norm_response = normalise(response)
    if re.search(r'\b' + re.escape(norm_answer) + r'\b', norm_response):
        return True
    else:
        return False


def label_response(response, answer):
    # fake citations have no answer so it is basically hallucinated
    if answer is None:
        return 1
    if is_correct(response, answer):
        return 0
    else:
        return 1
