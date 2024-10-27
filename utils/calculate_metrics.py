import json
import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.chrf_score import corpus_chrf
import editdistance


def calculate_metrics_for_example(example):
    actual = example["middle"]
    predicted = example["completion"]

    # Exact Match
    exact_match = int(actual.strip() == predicted.strip())

    # BLEU Score (using weights for bigram matching)
    smoothie = SmoothingFunction().method1
    bleu_score = sentence_bleu(
        [actual.split()],
        predicted.split(),
        weights=(0.5, 0.5),
        smoothing_function=smoothie,
    )

    # Character-level F-Score (ChrF)
    chrf_score = corpus_chrf([actual], [predicted])

    # Levenshtein Distance
    levenshtein_dist = editdistance.eval(actual, predicted)

    return {
        "exact_match": exact_match,
        "bleu": bleu_score,
        "chrf": chrf_score,
        "levenshtein": levenshtein_dist,
    }


def calculate_metrics_for_dataset(file_path):
    with open(file_path, "r") as f:
        dataset = json.load(f)

    for example in dataset:
        example["label"] = None
        example["metrics"] = calculate_metrics_for_example(example)

    save_path = os.path.join("data", "dataset.json")
    with open(save_path, "w") as f:
        json.dump(dataset, f, indent=2)


if __name__ == "__main__":
    calculate_metrics_for_dataset(os.path.join("data", "completions.json"))
