from transformers import pipeline
from huggingface_hub import login
import re
login(token='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')
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english",
                            aggregation_strategy="simple")

def filter_sports_teams(text):
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
test_sentences = """NBA Power Rankings: Important role players for Knicks, Warriors and all 30 teams2dNBA Insiders
The 360-degree windmill to start it. The head-scratching slam that ended with half of Carter's arm in the rim. And of course, the between-the-legs jam caught off a bounce pass from Raptors teammate and cousin Tracy McGrady.
Toronto's 2024-25 City Edition uniform, unveiled Thursday, pays tribute to that iconic dunk with the original Raptors' logo from 1995 emulating the play. The uniform will also be celebrated by a statue at the Art Gallery of Ontario. Fans can visit Nov. 14-17 before it moveslating the play. The uniform will also be celebrated by a statue at the Art Gallery of Ontario. Fans can visit Nov. 14-17 before it moves to the Scotiabank Arena.
 to the Scotiabank Arena.
"This 30th anniversary is a season to celebrate the people and moments who have made this franchise who we are," Raptors president and vice chairman Masai Ujiri said in a news release. "Is there a better example of that feeling than the image of Vince's unbelievable dunk? I"This 30th anniversary is a season to celebrate the people and moments who have made this franchise who we are," Raptors president and vice chairman Masai Ujiri said in a news release. "Is there a better example of that feeling than the image of Vince's unbelievable dunk? It reminds us that we can inspire. It allows us to dream of flying. It is proudly Toronto. And this uniform is unique in the league -- just reminds us that we can inspire. It allows us to dream of flying. It is proudly Toronto. And this uniform is unique in the league -- just like the team and fans who will proudly wear it."
The team will debut the uniforms Nov. 21 against theMinnesota Timberwolvesand will wear them five times in the season. There will also bet like the team and fans who will proudly wear it."
The team will debut the uniforms Nov. 21 against theMinnesota Timberwolvesand will wear them five times in the season. There will also be a special court to accompany the threads with a similar logo.
Working in conjunction with the NBA and Nike, the Raptors' idea of how to commemorate their 30th anniversary came to the forefront in 202 a special court to accompany the threads with a similar logo.
Working in conjunction with the NBA and Nike, the Raptors' idea of how to commemorate their 30th anniversary came to the forefront in 2022, Shannon Hosford, chief marketing officer of MLSE, told ESPN. It also coincided with an idea of retiring Carter's jersey this season and how they could celebrate that in a significant way.
2, Shannon Hosford, chief marketing officer of MLSE, told ESPN. It also coincided with an idea of retiring Carter's jersey this season and how they could celebrate that in a significant way.
They went back and forth with the NBA and Nike on initial concepts, but didn't feel it encapsulated what they wanted as a team. Therefore, they asked if they could take it away to a local artist, Kevin Briones, and asked about the Raptor doing the dunk, an idea thought of bThey went back and forth with the NBA and Nike on initial concepts, but didn't feel it encapsulated what they wanted as a team. Therefore, they asked if they could take it away to a local artist, Kevin Briones, and asked about the Raptor doing the dunk, an idea thought of by Toronto's head of merchandise.
y Toronto's head of merchandise.
"As soon as we saw [the mockup], we knew -- that was it. We were like, that's exactly what we want," Hosford said. "We know no other team"As soon as we saw [the mockup], we knew -- that was it. We were like, that's exactly what we want," Hosford said. "We know no other team has done something like this in terms of bringing an iconic moment of the team's history onto the front of the jersey. Everything about  has done something like this in terms of bringing an iconic moment of the team's history onto the front of the jersey. Everything about it just spoke to us."
it just spoke to us."
The uniform includes all of Toronto's brand colors through the years -- purple, red, gold and silver. It's the first jersey in franchise history to include just the crest without text on the front." It's a purposeful decision, according to Hosford, because they felt like that dunk "ignited a nation" and wanted it to be for all Raptors fans.
There's "tone-on-tone" claw scratch pinstripes, a nod to the Raptors' 1995 look. Toronto's "We The North" slogan appears above the jersey tag.
Hosford said Carter's dunk changed the trajectory for Canadian basketball and the franchise. It also inspired a new generation of players, including members of the current Raptors roster.
"When they saw this, they're so proud to wear it. They speak of it so highly," Hosford said. "Everything about it, our team, our front office to players, are in love with it."
Toronto didn't know at the time that their uniform release would coincide with Carter's induction into the Basketball Hall of Fame this year. The franchise wanted to make the jersey "a significant part of our history and where we were going."
"Landing on this design was very important to us," Hosford said.
Carter had been part of the process and bought in instantly. The uniform was one of the first things the Raptors thought of when planning on how to celebrate him this season.
During his jersey retirement news conference, Carter emphasized that a celebration of his time in Toronto was all he wanted. But he began to get choked up when discussing the honor of being on a Raptors' uniform, saying it's equivalent to Jerry West's silhouette being the NBA logo on a sock or backboard.
"Do you know how big that is? Even if this day did not happen, wherever I am working, watching TV, I would get to watch a Raptor game with a picture of me dunking a basketball on the jersey," hesaid. "That's just crazy. I look at that like a Hall of Fame. I look at that like a jersey retirement."""""
teams = filter_sports_teams(test_sentences)
print(teams)