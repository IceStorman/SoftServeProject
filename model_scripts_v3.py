from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

nlp = None
def load_model():
    global nlp
    if nlp is None:
        model = AutoModelForTokenClassification.from_pretrained("ai_models/my_custom_model4", token="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")
        tokenizer = AutoTokenizer.from_pretrained("ai_models/my_custom_model4", token="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")
        nlp = pipeline("ner", model=model, tokenizer=tokenizer)

def nlp_teams_players_org_arr(text):
    load_model()
    sentences = [sentence.strip() for sentence in text.split('\n') if sentence.strip()]
    entities_list = nlp(sentences)
    merged_entities = []
    unique_entities = set()

    if not isinstance(entities_list, list):
        print("Expected a list but got:", type(entities_list))
        return merged_entities

    for entities in entities_list:
        if not isinstance(entities, list):
            print("Expected a list of entities but got:", type(entities))
            continue
        current_name = ""

        for item in entities:
            if isinstance(item, dict):
                entity_name = item["word"]
                if current_name == "" or not entity_name.startswith("##"):
                    if current_name:
                        merged_entities.append(current_name.strip())
                    current_name = entity_name
                else:
                    current_name += entity_name[2:]
            else:
                print(f"Unexpected item format: {item}")

        if current_name:
            merged_entities.append(current_name.strip())

    unique_entities.update(merged_entities)

    return list(unique_entities)


