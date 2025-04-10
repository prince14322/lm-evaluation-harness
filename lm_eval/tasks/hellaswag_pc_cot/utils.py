import re
import datasets


def preprocess(text):
    text = text.strip()
    # NOTE: Brackets are artifacts of the WikiHow dataset portion of HellaSwag.
    text = text.replace(" [title]", ". ")
    text = re.sub("\\[.*?\\]", "", text)
    text = text.replace("  ", " ")
    return text

def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        ctx = doc["ctx_a"] + " " + doc["ctx_b"].capitalize()
        out_doc = {
            "query": preprocess(doc["activity_label"] + ": " + ctx),
            "choices": [preprocess(ending) for ending in doc["endings"]],
            "gold": int(doc["label"]),
        }
        return out_doc

    return dataset.map(_process_doc)

def clean_pc_cot(text):
    if "[/PSEUDOCODE]" in text:
        return text.split("[/PSEUDOCODE]")[-1].strip()

    if "[/[PSEUDOCODE]]" in text:
        return  text.split("[/[PSEUDOCODE]]")[-1].strip()
    
    pattern = re.compile(r'>>>\s*\w+\s*\([^)]*\)(.*)', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()

    return ""


def process_results_gen(doc, results):
    gold = str(doc["gold"]).lower()

    candidate = results[0]

    candidate = clean_pc_cot(candidate)

    candidate = candidate.strip().lower().split("\n")[0].split(" ")[0].strip()

    if "." in candidate:
        candidate = candidate.split(".")[0]

    retval = 0
    if candidate == gold:
        retval = 1
    
    results = {
        "exact_match": retval,
    }
    return results