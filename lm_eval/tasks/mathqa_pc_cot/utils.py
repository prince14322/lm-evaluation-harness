import re
import copy

def doc_to_choice(doc):
    choices = [
        c[4:].rstrip(" ,")
        for c in re.findall(r"[abcd] \) .*?, |e \) .*?$", doc["options"])
    ]
    return choices

def doc_to_target(doc):
    return doc["correct"]

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
    gold = doc["correct"].lower()

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