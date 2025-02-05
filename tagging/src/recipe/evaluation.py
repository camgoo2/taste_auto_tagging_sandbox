from typing import Dict
from typing import List

import nltk
import spacy
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")  # Downloads the WordNet dataset
nlp = spacy.load("en_core_web_lg")
lemmatizer = WordNetLemmatizer()


def _calculate_similarity(tag1: str, tag2: str) -> float:
    # Get the word vectors from spaCy

    word1 = nlp(tag1)
    word2 = nlp(tag2)

    # Compute cosine similarity between the two word vectors
    similarity = word1.similarity(word2)  # Cosine similarity
    return similarity


def _calculate_metrics(
    human_tags: List,
    ai_tags: List,
    use_semantic_similarity: bool = False,
    similarity_threshold: float = 0.8,
) -> Dict:
    human_tags = set(human_tags)
    ai_tags = set(ai_tags)

    tp = 0  # True Positives
    fp = 0  # False Positives
    fn = 0  # False Negatives

    # Track which human tags have been matched to prevent double counting
    matched_human_tags = set()
    tps = []
    fps = []
    fns = []

    for ai_tag in ai_tags:
        found_match = False
        for human_tag in human_tags:
            if human_tag == ai_tag:
                tp += 1  # Count as True Positive
                matched_human_tags.add(human_tag)
                tps.append((human_tag, ai_tag))
                found_match = True
                break
            elif use_semantic_similarity:
                similarity = _calculate_similarity(ai_tag, human_tag)
                if similarity >= similarity_threshold:
                    print(f"Matched gt {human_tag} with {ai_tag}: {similarity}")
                    tp += 1  # Count as True Positive
                    matched_human_tags.add(human_tag)
                    tps.append((human_tag, ai_tag))
                    found_match = True
                    break
        if not found_match:
            fps.append(ai_tag)
            fp += 1  # Count as False Positive if no match found

    for human_tag in human_tags:
        if human_tag not in matched_human_tags:
            fns.append(human_tag)  # Add unmatched human tags to FN list
            fn += 1  # Count as False Negative

    # Manually calculate Precision, Recall, and F1 based on TP, FP, FN counts
    if tp + fp == 0:
        precision = 0.0
    else:
        precision = tp / (tp + fp)

    if tp + fn == 0:
        recall = 0.0
    else:
        recall = tp / (tp + fn)

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = (2 * precision * recall) / (precision + recall)

    metrics = {
        "fp": fp,
        "tp": tp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tps": tps,  # Return the list of True Positives
        "fps": fps,  # Return the list of False Positives
        "fns": fns,  # Return the list of False Negatives
    }
    return metrics


def standardised_tag_for_comparison(unrefined_tag: str) -> str:
    # 1. Remove text in parentheses (if any) and strip extra whitespace

    refined_tag = unrefined_tag.split("(")[0].strip()

    # 2. Implementation of lemmatization
    refined_tag = lemmatizer.lemmatize(refined_tag)

    print(f"Unrefined Tag: {unrefined_tag} Refined Tag: {refined_tag} ")
    return refined_tag


def evaluate_recipe_tagging(
    ground_truth: List[Dict],
    prediction: List[Dict],
    use_semantic_similarity: bool = False,
) -> Dict:
    id_to_prediction = {}
    for pred in prediction:
        entity_id = pred["entity_id"]
        id_to_prediction[entity_id] = pred

    all_metrics = []
    for recipe in ground_truth:
        recipe_id = recipe["id"]
        pred = id_to_prediction[recipe_id]["prediction"]

        gt_tags = sorted(
            set([full_tag.split("/")[-1] for full_tag in recipe["filteredCategories"]])
        )
        gt_tags_standardised = [standardised_tag_for_comparison(tag) for tag in gt_tags]

        prediction_tags = sorted(set([tag_pred["tag"] for tag_pred in pred]))
        prediction_tags_standardised = [
            standardised_tag_for_comparison(tag) for tag in prediction_tags
        ]

        print("Prediction Tags:")
        print(prediction_tags_standardised)
        print("Ground Tags: ")
        print(gt_tags_standardised)

        recipe_metrics = _calculate_metrics(
            gt_tags_standardised, prediction_tags_standardised, use_semantic_similarity
        )
        all_metrics.append(
            {
                "recipe_id": recipe_id,
                "metrics": recipe_metrics,
                "gt_tags": gt_tags,
                "predicted_tags": prediction_tags,
            }
        )

    overall_tp = sum([metric["metrics"]["tp"] for metric in all_metrics])
    overall_fp = sum([metric["metrics"]["fp"] for metric in all_metrics])
    overall_fn = sum([metric["metrics"]["fn"] for metric in all_metrics])

    overall_precision = overall_tp / (overall_tp + overall_fp)
    overall_recall = overall_tp / (overall_tp + overall_fn)
    if overall_precision + overall_recall == 0:
        overall_f1 = 0
    else:
        overall_f1 = (2 * overall_precision * overall_recall) / (
            overall_precision + overall_recall
        )
    print(f"Overall Precision: {overall_precision}")
    print(f"Overall Recall: {overall_recall}")
    print(f"Overall F1 Score: {overall_f1}")

    return {
        "overall_precision": overall_precision,
        "overall_recall": overall_recall,
        "overall_f1": overall_f1,
        "all_metrics": all_metrics,
    }
