import nltk
from nltk.corpus import wordnet

File = open("input_text.txt")  # open file
lines = File.read()  # read all lines
sentences = nltk.sent_tokenize(lines)  # tokenize sentences
nouns = []  # empty to array to hold all nouns

list_lexical_chains = []

#Extract all the nouns from the input text.
for sentence in sentences:
    for word, pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
        if (pos == 'NN' or pos == 'NNS'):
            nouns.append(word)

print("\n\nList of nouns in the text::\n", nouns)

# Creating first lexical chain
dictionary_obj = {nouns[0]: 1}
list_lexical_chains.append(dictionary_obj)

for word in nouns[1:]:
    synonyms = []
    antonyms = []
    hypernyms = []
    hyponyms = []
    word_added_flag = 0
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
        for synset_hyponyms in synset.hyponyms():
            for nm in synset_hyponyms.lemma_names():
                hyponyms.append(nm)
        for synset_hypernym in synset.hypernyms():
            for nm in synset_hypernym.lemma_names():
                hypernyms.append(nm)

    for a_lexical_chain_dictionary in list_lexical_chains:
        for dictionary_word in a_lexical_chain_dictionary:
            if dictionary_word == word:
                a_lexical_chain_dictionary[dictionary_word] = a_lexical_chain_dictionary[dictionary_word] + 1;
                word_added_flag = 1
                break
            if dictionary_word in synonyms:
                a_lexical_chain_dictionary.update({word: 1})
                word_added_flag = 1
                break
            if dictionary_word in antonyms:
                a_lexical_chain_dictionary.update({word: 1})
                word_added_flag = 1
                break
            if dictionary_word in hypernyms:
                a_lexical_chain_dictionary.update({word: 1})
                word_added_flag = 1
                break
            if dictionary_word in hyponyms:
                a_lexical_chain_dictionary.update({word: 1})
                word_added_flag = 1
                break
    if word_added_flag == 0:
        new_dict_obj = {word: 1}
        list_lexical_chains.append(new_dict_obj)

print("\n\nAll lexical chains::\n", list_lexical_chains)

# Sorting lexical chains in descending order of lengths to get strong chains first
list_lexical_chains.sort(key=lambda s: len(s), reverse=True)

print(list_lexical_chains)

strong_lexical_chain_list = []

# Filtering out strong chains based on the length of the chain. We know first chain in the list is strong chain as we sorted in descending order.
length_for_strong_chain = len(list_lexical_chains[0])
strong_lexical_chain_list.append(list_lexical_chains[0])
for a_lexical_chain in list_lexical_chains[1:]:
    if len(a_lexical_chain) == length_for_strong_chain:
        strong_lexical_chain_list.append(a_lexical_chain)
# print(strong_lexical_chain_list)

# Filtering out strong chains based on the frequency of words. We know frequency of first chain in the list is strong as we sorted in descending order.
for a_lexical_chain in list_lexical_chains:
    if sum(a_lexical_chain.values()) >= sum(strong_lexical_chain_list[0].values()):
        if a_lexical_chain not in strong_lexical_chain_list:
            strong_lexical_chain_list.append(a_lexical_chain)
print("\n\nStrong chain final list:\n", strong_lexical_chain_list)

#Assigning score or weight to every sentence in the text to find strong sentences for Summary.
sentence_score = {}
for sentence in sentences:
    new_dict_obj = {sentence: 0}
    sentence_score.update(new_dict_obj)
    for word in nltk.word_tokenize(str(sentence)):
        for a_lexical_chain in strong_lexical_chain_list:
            if word in a_lexical_chain:
                sentence_score[sentence] = sentence_score[sentence] + a_lexical_chain[word]
print("\n\nSentence score dictionary:\n", sentence_score)

sentence_score = sorted(sentence_score, key=sentence_score.get, reverse=True)
#print("Sentence score dictionary sorted:", sentence_score)

#assigning one third length of text as length for summary
summary_length = int(len(sentences)/3)
print("\n\nSummary Length:\n", int(len(sentences)/3))

#Strong sentence list with sentences to be added to summary.
sentence_score = sentence_score[:summary_length]

#Retrieving summary sentences in the order which they were found in the text to maintain cohersion.
summary = ""
for sentence in sentences:
    if sentence in sentence_score:
        summary = summary + sentence
print("\n\nSummary:\n", summary)
