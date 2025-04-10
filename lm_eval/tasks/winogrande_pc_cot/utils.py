import re

def doc_to_text(doc):
    text = f"Given a sentence with one of the word replaced by an underscore(_) and two options 1 and 2. Choose either 1 or 2 which best replaces the underscore.\nSentence:\n{doc['sentence']}\nOptions:\n1. {doc['option1']}\n2. {doc['option2']}\nGenerate pseudocode chain-of-thought reasoning first and then generate the solution."
    
    return text

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
    gold = str(doc["answer"]).lower()

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