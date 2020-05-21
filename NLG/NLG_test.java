/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package nlgtest;

/**
 *
 * @author ananya
 */
    import simplenlg.framework.*;
    import simplenlg.lexicon.*;
    import simplenlg.realiser.english.*;
    import simplenlg.phrasespec.*;
    import simplenlg.features.*;


    public class NLGtest {

            public static void main(String[] args) {
                    Lexicon lexicon = Lexicon.getDefaultLexicon();
                    NLGFactory nlgFactory = new NLGFactory(lexicon);
                    Realiser realiser = new Realiser(lexicon);
                    
//                    NLGElement s = nlgFactory.createSentence("my dog is happy");
//
//                    String output = realiser.realiseSentence(s);
//                    System.out.println(output);

                    
//                    SPhraseSpec p = nlgFactory.createClause();
//                    p.setSubject("Mary");
//                    p.setVerb("chase");
//                    p.setObject("the monkey");
//
//                    String output2 = realiser.realiseSentence(p); // Realiser created earlier.
//                    System.out.println(output2);
                    
                    
                    SPhraseSpec s1 = nlgFactory.createClause("my cat", "like", "fish");
                    SPhraseSpec s2 = nlgFactory.createClause("my dog", "like", "big bones");
                    SPhraseSpec s3 = nlgFactory.createClause("my horse", "like", "grass");

                    CoordinatedPhraseElement c = nlgFactory.createCoordinatedPhrase();
                    c.addCoordinate(s1);
                    c.addCoordinate(s2);
                    c.addCoordinate(s3);
                    
                    String output = realiser.realiseSentence(c);
                    System.out.println(output);

                    
            }

    }
