from transformers import pipeline
from huggingface_hub import login
import re

login(token='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')
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english",
                            aggregation_strategy="simple")

def what_teams_here(text):
    sentences = [sentence.strip() for sentence in text.split('\n') if sentence.strip()]
    entities_list = []

    for sentence in sentences:
        entities_list.extend(ner_pipeline(sentence))

    sports_teams = []
    current_word = ""

    for entity in entities_list:
        if entity['entity_group'] == 'ORG':
            word = entity['word']
            if word.startswith("##"):
                current_word += word[2:]
            else:
                if current_word:
                    sports_teams.append(current_word.strip())
                current_word = word

        if current_word:
            sports_teams.append(current_word.strip())
            current_word = ""

    team_like_entities = [team for team in sports_teams if not re.match(r'^[A-Z][a-z]* [A-Z][a-z]*$', team)]
    return list(set(team_like_entities))