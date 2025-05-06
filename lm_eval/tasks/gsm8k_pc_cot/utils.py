import re
import copy

def doc_to_target(doc):
    return doc["answer"]


def clean_pc_cot(text):
    if "[/PSEUDOCODE]" in text:
        return text.split("[/PSEUDOCODE]")[-1].strip()

    if "[/[PSEUDOCODE]]" in text:
        return  text.split("[/[PSEUDOCODE]]")[-1].strip()
    
    pattern = re.compile(r'>>>\s*\w+\s*\([^)]*\)(.*)', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()

    return text

def process_results_gen(doc, results):
    gold = doc["answer"].lower()

    candidate = results[0]

    candidate = clean_pc_cot(candidate)

    for prefix in ["answer is", "answer:", "answer :"]:
        if prefix in candidate.lower():
            candidate = candidate.lower().split(prefix)[-1].strip()
            break

    # candidate = candidate.strip().lower().split("\n")[0].split(" ")[0].strip()

    # Remove everything after the first period
    if "." in candidate:
        candidate = candidate.split(".")[0]

    candidate = candidate.strip()

    retval = 0
    if candidate == gold:
        retval = 1
    
    results = {
        "exact_match": retval,
    }
    return results