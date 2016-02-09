# Grammatically informed topic modelling

## Abstract


## Overview

A common approach to topic modelling involves analysing which lexical items co-occur within texts. LDA is used to do this. Stopword listts are used to remove the very common, generally closed-class words that seldom do much obvious work in construing topics.

A key issue with this approach is that lexis is not solely responsible for carrying topic information in texts. Grammar also plays an important role. In theories of language such as systemic functional linguistics (SFL), lexis and grammar are treated as two ends of the same system, with lexis acting as the most delicate realisation of grammar. The extent to which a single word carries topic information is dependent upon its position within the clause, with predicators and the heads of their arguments generally taking more central roles than, for example, the objects of prepositional phrases.

Moreover, some elements of lexis do not play a role in topic. Verb tenses are a good example: in a corpus of news articles, we would typically prefer a retrospective article about the Vietnam War written predominantly in past tense to be grouped alongside 1960s/1970s reporting on Vietnam War in present tense. Less central to the purpose of topic modelling would be grouping of article by their dominant tense choices.

## Aim

We aim to distinguish between different topics in a corpus of articles containing 'risk words' (operationalised as the regular expression '\brisk') in major U.S. newspaper articles from 1987--2014.

## Approach

To do this, we created a topic model of our unparsed corpus, and a lemmatised version of it, using MALLET. We parsed the corpus with spaCy, and created a set of adjustable weights for each dependency function, with each initially set to zero, aside from root and nsubj, set to one.

Looping over the parsed data, we:

    1. Created a new corpus of plaintext, where each token was duplicated by its weight
    2. Assessed whether or not the newest topic model improved on the previous iteration
    3. Adjusted the weights: if the newest model is best, increment the most recently incremented weight again; if the newest topic model is worse, unincrement the previous weight, and increment the next weight

This loop continues until all functions have been weighted to their optimal level.

## Results

It worked!

## Discussion

We can improve performance in topic modelling tasks by taking advantage of parser output: some grammatical roles are more likely than others to index meaningful information about topic/field.

The method also presents an empirically driven approach to stopword removal.

A key advantage of the approach is that weighting is determined based on the content of the corpus itself. Given that spoken language has a richer verbal inventory, and written language has a richer nominal inventory, determining weights in this manner is desirable.

## Theoretical implications

We found support for theoretical notions concerning the importance of particular grammatical components in construing experience.

## Limitations

Dependency grammars do necessarily contain all functional labels that may be relevant for topic modelling. They are also prone to conflations and internal inconsistencies: "nsubj" conflates word class and grammatical position; labelling prioritises transitivity in some cases (dobj, iobj) and mood (nsubj, nsubjpass) in others. These isssues may reduce accuracy

In defining governor/dependent relationships, dependency grammar also makes it difficult to retrieve potentially important constistuency information. For example: "and" within a subject noun phrase may play a more important role than "and" as a conjoining conjunction of two clauses: "I watch Law and Order" / "I watched the show and fell asleep". The uncollapsed dependency grammar used in the investigation, however, labels both tokens as 'conj'. Writing rules to traverse trees and make new labels involves much guesswork.

## Future research

There is some ambiguity inherent to the idea of simply grouping texts into topics. In a news corpus, are elections topics, or are candidates topics? Grouping by either feature may be desirable. Using our approach, by weighting words with emphasis on processes, or on participants, we could potentially distinguish between different senses of 'topic'. If we wanted individual topics for Donald Trump, Barack Obama and Hillary Clinton, we could amplify the weighting of participant-like roles; to distinguish between articles on voting, campaigning and meeting with donors, however, we could give more weight to process-like roles.
