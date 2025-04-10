import re

def doc_to_text(doc):
    option_labels = ""
    
    for index in range(len(doc['choices']['label'])):
        if index != (len(doc['choices']['label'])-1):
            option_labels = option_labels + doc['choices']['label'][index] + ", "
        else:
            option_labels = option_labels + "or " + doc['choices']['label'][index] + " "

    option_labels = option_labels.strip()

    question = f"Given a question and {len(doc['choices']['label'])} options, generate one of {option_labels} which best answers the question.\nQuestion: {doc['question']}\nOptions:"
    
    for index in range(len(doc['choices']['label'])):
        question = question + f"\n{doc['choices']['label'][index]}. {doc['choices']['text'][index]}"

    question = question + "\nGenerate pseudocode chain-of-thought reasoning first and then generate the solution."
        
    return question

def doc_to_target(doc):
    return doc["answerKey"]

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
    gold = doc["answerKey"].lower()

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