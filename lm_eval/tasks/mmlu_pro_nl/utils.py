from functools import partial
import re
import copy

choices = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
]


def doc_to_text(doc):
    prompt = "Question:\n"
    question = doc["question"]
    options = doc["options"]
    prompt += question + "\n"
    prompt += "Options:\n"
    for i, opt in enumerate(options):
        prompt += "{}. {}\n".format(choices[i], opt)
    prompt += "\nThink step by step and in the end, finish your response with 'Response:$RESPONSE' where $RESPONSE (without quotes) is the final output expected."
    return prompt

def process_docs(dataset, subject):
    return dataset.filter(lambda x: x["category"] == subject)


def postprocess_output_help(prediction: str):
    """
    Post-process ground truth or prediction strings.

    Parameters:
        prediction (str): String corresponding to ground truth or LLM prediction

    Return:
        str: post-processed output
    """
    llmoutput = str(copy.deepcopy(prediction))
    llmoutput = llmoutput.replace("[", "")
    llmoutput = llmoutput.replace("]", "")
    llmoutput = llmoutput.replace("$", "")
    llmoutput = llmoutput.replace("'", "")
    if llmoutput.endswith("."):
        llmoutput = llmoutput[:-1]
    llmoutput = llmoutput.strip()
    return llmoutput


def clean_nl(text):
    print("Post processing NL ....")
    if "Response:" not in text:
        strict_response_prediction = postprocess_output_help(text.strip())
        truncated_output = text.rsplit("\n", 1)[-1]
        if "answer is:" in truncated_output:
            truncated_output = truncated_output.rsplit("answer is:", 1)[-1]
        elif "answer is :" in truncated_output:
            truncated_output = truncated_output.rsplit("answer is :", 1)[-1]
        loose_response_prediction = postprocess_output_help(truncated_output.strip())
    else:
        strict_response_prediction = postprocess_output_help(
            text.split("Response:")[-1].strip()
        )
        loose_response_prediction = strict_response_prediction
    # return strict_response_prediction, loose_response_prediction
    return loose_response_prediction


def process_results_gen(doc, results):
    gold = doc["answer"].lower()

    candidate = results[0]

    candidate = clean_nl(candidate)

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

process_biology = partial(process_docs, subject="biology")
process_business = partial(process_docs, subject="business")
process_chemistry = partial(process_docs, subject="chemistry")
process_computer_science = partial(process_docs, subject="computer science")
process_economics = partial(process_docs, subject="economics")
process_engineering = partial(process_docs, subject="engineering")
process_health = partial(process_docs, subject="health")
process_history = partial(process_docs, subject="history")
process_law = partial(process_docs, subject="law")
process_math = partial(process_docs, subject="math")
process_other = partial(process_docs, subject="other")
process_philosophy = partial(process_docs, subject="philosophy")
process_physics = partial(process_docs, subject="physics")
process_psychology = partial(process_docs, subject="psychology")
