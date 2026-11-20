from collections import Counter
#code
def analyze_nlp(words):
    if not words:
        return {"integrity_score": 0}

    diversity = len(set(words)) / len(words)
    repetition = max(Counter(words).values())

    integrity = min(10, round((diversity * 7 + (1 / repetition) * 3), 2))
    return {"integrity_score": integrity}
