from simplenlg import Lexicon
from simplenlg import NLGFactory
from simplenlg import Realiser

words = ['Month', 'Infected']
correlation_value = -0.4444

lexicon = Lexicon.getDefaultLexicon()
nlgFactory = NLGFactory(lexicon)
realiser = Realiser(lexicon)


start_s = nlgFactory.createClause("From the above scatterplot matrix we observe that")


if correlation_value > 0:
    # positive correlation
    s1 = nlgFactory.createClause("there is a positive correlation between the attributes, " +words[0]+ " and " +words[1])
elif correlation_value < 0:
    # negative correlation
    s1 = nlgFactory.createClause("there is a negative correlation between the attributes, " +words[0]+ " and " +words[1])
elif correlation_value == 0:
    # no correlation
    s1 = nlgFactory.createClause("there is a no correlation between the attributes, " +words[0]+ " and " +words[1])


if correlation_value > 0.4 or correlation_value < -0.4:
    # high correlation
    s2 = nlgFactory.createClause("the correlation between these attributes is high")
else:
    # low correlation
    s2 = nlgFactory.createClause("the correlation between these attributes is low")


# combine the sentences to generate a story
phrase_element = nlgFactory.createCoordinatedPhrase()
phrase_element.addCoordinate(start_s)
phrase_element.addCoordinate(s1)
phrase_element.addCoordinate(s2)


story = realiser.realiseSentence(phrase_element)
print(story)
