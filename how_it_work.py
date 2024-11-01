'''
Все що потрібно для роботи це зробити імпорт та передати текст в середину функції
Форматувати його не потрібно, скрипт всередині все зробе сам
Результат ретурниться у форматі list: ['a','b','c']
Чи є обмеження по розміру текста я хз, максимум перевіряв на 3000 слів і воно працює
Повертає значення ORG i PER
'''

from model_scripts_v3 import nlp_teams_players_org_arr

# Приклад роботи
test_sentences = '''
World Series champs! How Dodgers validated their dominanceNEW YORK -- Two days before the Los Angeles Dodgers' postseason began, Freddie Freeman felt a twinge in his rib cage when he took a swing during a simulated game. 
He vowed to ignore it. It's not as if he wasn't already in pain. 
Over the previous week, Freeman had nursed a sprained right ankle sustained trying to avoid a tag while running to first base. 
He needed no more impediments. 
The Dodgers had a World Series to win.A day later, Oct. 4, after Freeman finished a news conference in which he declared himself ready to play despite the ankle injury, he retreated to the batting cage at Dodger Stadium. 
He wanted to take some swings in preparation for a live batting-practice session. 
His side tingled with each of his first dozen swings. 
On the 13th swing, Freeman felt a jolt through his body and crumpled to the ground.Unable to even pick himself off the floor, Freeman was helped into the X-ray room next to Los Angeles' dugout. 
The results were inconclusive, and around 9:30 p.m., he received a call. 
The Dodgers wanted him to drive to Santa Monica for more imaging. He hopped in the car, then in an MRI tube. 
Around 11:30 p.m., the results arrived: Freeman had broken the costal cartilage in his sixth rib, an injury that typically sidelines players for months.
Devastation set in. Walking hurt. Breathing stung. Swinging a bat felt like an impossibility.
Freeman's father, Fred, worried about his youngest son, whom he raised after Freeman's mother, Rosemary, died of melanoma when Freddie was 10.
He saw the anguish in every minuscule movement. Considering the injuries to his rib and ankle and the lasting soreness from a middle finger he fractured in August, surely Freeman was too beaten up to keep playing. 
Surely there would be more postseasons, more opportunities."I actually told him to stop," Fred said. "I said, 'Freddie, this is not worth it. 
I know you love baseball. I love baseball. But it's not worth what you're going through.' 
And he looked at me like I was crazy, and he said, 'Dad, I'm never going to stop.'
"NOT ONLY DID Freeman never stop, he put on one of the Dodgers' greatest Fall Classic performances in history and readied the franchise for its first victory parade in 36 years.
The championship was won in a Game 5 that saw the Dodgers stake the New York Yankees a five-run lead, claw back for a 7-6 victory thanks to one of the most horrific half-innings in the Yankees' storied history, and seal the championship with bravura performances from their bullpen and manager.
Los Angeles never got to fete the Dodgers for their World Series victory in 2020. 
Beyond the lack of a celebration, the title had been demeaned and denigrated by those who regarded it as a lesser championship, the product of a 60-game season played in front of no fans and a postseason run inside a pseudo-bubble. 
To the Dodgers, that always registered as unfair, and they used the slight as fuel."Twenty-nine other teams wanted to win the last game, too, regardless of the circumstances," said right-hander Walker Buehler, who pitched the ninth inning of Game 5 to close the series for the Dodgers. 
"Like, everyone that talks about it, fine. ... But 29 other professional, billion-dollar organizations would've liked to have won the last one.The Dodgers wanted this championship for so many reasons beyond the obvious. 
Regardless of a baseball team's talent or payroll -- both areas in which this team finds itself at the game's apex -- October is a baseball funhouse mirror. A team fat on ability can look waifish in a hurry. 
The short series, the odd schedule, the capacity for a lesser team to beat a better one simply because it gets hot at the right time -- all of it conspires to render April through September inert. 
Teams built for the six-month marathon that is the regular season aren't necessarily well-constructed for the postseason's one-month sprint. A team's ability to code-switch is its greatest quality.
This year, Los Angeles craved validation for its regular-season dominance. Something to silence those who malign its 2020 championship and chalk up its success not to sound decision-making processes and elite player development but an endless flow of cash. 
The Dodgers cannot deny the power of the dollar after guaranteeing $700 million in free agency to star designated hitter Shohei Ohtani and another $325 million to Japanese right-hander Yoshinobu Yamamoto. 
Ohtani hit 54 home runs and stole 59 bases during the regular season. Yamamoto threw six brilliant innings in his first World Series game. 
Money plays."World Series champions come in all different sizes and shapes and forms," Dodgers president of baseball operations Andrew Friedman said. "And there are different strengths that help you win a World Series."Their lineup was an obvious one. 
Even a hobbled Freeman is still an eight-time All-Star -- and a former MVP, just like the two men ahead of him in the lineup, Ohtani and Mookie Betts. The Dodgers led major league baseball in home runs and slugging percentage while finishing second in runs scored and on-base percentage . 
For all the depth the Dodgers' lineup featured, though, the pitching staff was threadbare on account of a mess of injuries. With just three starting pitchers and a half-dozen trusted relievers -- not to mention the necessity of throwing bullpen games, further taxing arms -- Los Angeles required a deft touch with its pitching.
Championships take luck and timing and depth and open-mindedness and savvy. World Series are won as much on the margins as they are in the core. 
And every championship team features something beyond that, a separator, a je ne sais quoi. Like, say, a starter suffering through his worst season emerging to close out a World Series game. 
Or someone who refuses to let his broken body impede a quest so meaningful to those who rely on him.IN 2005, WHEN Freddie Freeman was 15 years old, he was hit by a pitch that broke his wrist. 
Freeman was scheduled to play for Team USA's 16-and-under national team, and he couldn't let the opportunity pass. So he simply didn't tell anyone about his wrist injury and gritted through the agony.Almost two decades later, Freeman started Game 1 of the division series against San Diego without publicly divulging his broken rib cartilage. Even the slightest competitive advantage can separate win from loss, and Freeman understood the sort of challenge the Padres posed. 
They had constructed their roster for postseason baseball: heavy on power hitters and front-line bullpen arms, light on offensive swing-and-miss. San Diego ousted the Dodgers from the postseason in 2022 and was prepared to do the same in 2024.
While Chelsea knows baseball well enough to understand it's never that easy, in the next few games, Freddie continued to make it look so. He blasted another home run off a fastball in a Game 2 win. His two-run, first-inning shot on a high inside 93 mph Clarke Schmidt cutter in Game 3 gave the Dodgers a lead they held for their second consecutive 4-2 victory. 
For the series' first three games, Freeman was single-handedly carrying the Dodgers' offense, just the way it had collectively carried him through the NLCS. 
Muncy was hitless. Betts cooled down. And Ohtani partially dislocated his shoulder sliding into second base during Game 2 and was never a factor in the series.The presence of Ohtani, who had absconded from the Los Angeles Angels in pursuit of a championship, as well as that of Yankees slugger Aaron Judge, had turned this World Series into a supersized event -- but Freeman was the one owning it. 
He hit another two-run shot in the first inning of Game 4, marking an MLB-record sixth consecutive World Series game with a home run, his streak dating back to 2021 with Atlanta. 
The Dodgers' attempt at a sweep fizzled with a third-inning grand slam by Yankees shortstop Anthony Volpe and eventually turned into an 11-4 blowout, not exactly a surprise considering Roberts stayed away from using his best relievers in hopes of keeping them fresh for a potential Game 5.Game 4 marked the Dodgers' fourth all-bullpen effort of the postseason, a staggering number for a team with as much talent as Los Angeles.
Consider the names on L.A.'s injured list come October. Longtime ace and future Hall of Famer Clayton Kershaw made only seven starts before a toe injury ended his season. 
Tyler Glasnow, acquired to help anchor the rotation over the winter, never returned from a mid-August elbow injury. Stone, the Dodgers' best starter this season, was out. 
So was Dustin May after an esophageal tear. Emmet Sheehan, River Ryan and Tony Gonsolin all were on the shelf following Tommy John surgery, and the Dodgers had signed Ohtani, 
MLB's first two-way player in nearly a century, knowing he wouldn't pitch in 2024 because of elbow reconstruction.Losing a rotation-and-a-half worth of starting pitchers would have torpedoed any other team. Los Angeles had figured out how to weather the deficiency, with Roberts and pitching coach Mark Prior puppeteering their 13-man pitching staff without excessive fatigue or overexposure to Yankees hitters. 
It was a delicate balance, one they feared could collapse if Game 5 went the wrong way.AROUND 3 P.M. on Wednesday, Walker Buehler boarded the Dodgers' team bus to Yankee Stadium, looked at general manager Brandon Gomes and said: "I'm good tonight if you need me." Two nights earlier, Buehler had spun magic in Game 3, shutting down New York in five scoreless innings. He was scheduled to throw a between-starts bullpen session; 
if he needed to forgo it to instead throw in a World Series game, he was ready.Buehler is 30 and coming off the worst regular season of his career, winning just one of his 16 starts and posting a 5.38 ERA. He missed all of 2023 after undergoing his second Tommy John surgery and returned a much lesser version of the cocksure right-hander whose postseason badassery earned him a reputation as one of baseball's finest big-game pitchers. 
His fastball lacked life and his breaking balls sharpness, and with free agency beckoning, Buehler had looked positively ordinary.This was October, though, and the month has always brought out something different in him. He dotted his fastball in all four quadrants of the strike zone in Game 3, flummoxing Yankees hitters. It revved past them with the sort of carry he displayed over four shutout innings against the Mets in the NLCS.
Back, too, was Buehler's self-assuredness. Just in case Gomes and the rest of the Dodgers' staff didn't understand what he meant, Buehler reiterated at the stadium: "If things get a little squirrelly, then I'll be ready."The game was all Yankees to start. Judge hit his first home run of the series in the first inning. 
Jazz Chisholm Jr. followed with another. An RBI single from Verdugo in the second inning chased Flaherty after he had recorded just four outs. For the second consecutive night, Roberts would need to lean on his bullpen. He went into break-glass-in-case-of-emergency mode. 
Left-hander Anthony Banda escaped a bases-loaded jam in the second. Ryan Brasier allowed a third-inning leadoff home run to Giancarlo Stanton. Michael Kopech pitched the fourth and wriggled out of a first-and-second-with-one-out situation.Best of 2024 MLB PlayoffsOlney: Yanks fans cheer despite letdown »Gonzalez: The Dodgers' unsung hero »Castillo: Inside Weaver's rise to closer »
Passan: Mets' run just the beginning »In the meantime, Cole was cruising. He held the Dodgers hitless through four innings. Hernández broke that streak with a leadoff single in the fifth. Edman lined a ball to center that clanked off Judge's glove, his first error on a fly ball since 2017. After Volpe fielded a ground ball and tried to nab the lead runner at third, Hernández almost Eurostepped into his throwing lane, a brilliant bit of baserunning that illustrated the difference between Los Angeles' and New York's fundamentals. 
Volpe bounced the throw for a second error in the inning, loading the bases.Cole bore down, striking out Lux and Ohtani, and Betts squibbed a ball at 49.8 mph toward Yankees first baseman Anthony Rizzo. 
Even with the English spinning the ball away from the first-base bag, Rizzo likely could have tagged first to end the inning. He expected to flip the ball to Cole, who anticipated Rizzo would take the out himself. 
Once Rizzo realized Cole had not covered the bag, he shuffled toward first. Betts beat him there, and the mental blunder gave the Dodgers their first run of the day.Freeman served a single on an inner-third, two-strike, 99.5 mph fastball -- the hardest pitch Cole threw all season -- to center for two more runs. 
And on another 1-2 pitch that caught too much of the plate, Teoscar Hernandez drove the ball 404 feet to center field. Because it hopped against the wall instead of over it, Freeman hauled all the way from first to home. 
Just like that, a 5-0 advantage had evaporated into a 5-5 tie.Yankee Stadium, minutes earlier a madhouse, flatlined. Buehler had adjourned to the weight room, loosening his arm with a yellow plyometric ball. He saw Slater, who works out during the game to calm his nerves."Is it squirrelly yet?" Buehler asked.It was squirrelly, all right. 
Friedman had come downstairs to consult with the rest of the front office about the logistics of finding a lie-flat airplane seat to fly Yamamoto back to Los Angeles ahead of the team for a potential Game 6. Now, instead of expending energy on that, they focused on how the Dodgers would possibly secure the final 15 outs of the game if they could steal a lead.Inside the dugout, Roberts and Prior were doing the same. They were counting on left-hander Alex Vesia for more than one inning. With his pitch count run to 23 after weathering a bases-loaded situation by getting Gleyber Torres to fly out to right field, Vesia was done after the fifth. Buehler had returned to the dugout, and Prior asked whether he had thrown all day. 
'''

print(nlp_teams_players_org_arr(test_sentences))