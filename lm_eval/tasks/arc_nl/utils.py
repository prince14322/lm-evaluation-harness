import re
import copy

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

    question = question + "\nThink step by step and in the end, finish your response with 'Response:$RESPONSE' where $RESPONSE (without quotes) is the final output expected."
        
    return question

def doc_to_target(doc):
    return doc["answerKey"]

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
    gold = doc["answerKey"].lower()

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