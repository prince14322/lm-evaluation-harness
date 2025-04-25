import re
import datasets
import copy


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
    gold = str(doc["gold"]).lower()

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