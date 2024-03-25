
import nltk
from glob import glob
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import re
import os



class President_Speech_Analysis:
    def __init__(self, filepath, pres_name):
        self.filepath = filepath
        self.pres_name = pres_name
        self.corpus, self.corpus_aslist = self.make_corpus()


    def read_file(self, filename):
        with open(filename, encoding='utf8') as infile:
            contents = infile.read()
        return contents

    def tokenize_and_filter(self, sent):
        return [token.lower() for token in nltk.word_tokenize(sent)
            if token not in ".,?!:;()[]''``*"]

    def preprocess(self, text):
        return [self.tokenize_and_filter(sent) for sent in nltk.sent_tokenize(text)]

    def make_corpus(self): 
        corpus = []
        corpus_aslist = []
        filenames = glob(f'D:/Dokumentumok/egyetemek/AdvancedMA/scripting_languages/finalp/texts/{self.pres_name}/*.txt')
        for filename in filenames:
            text = self.read_file(filename)
            corpus.append(self.preprocess(text))
        for text in corpus:
            corpus_aslist.extend(word for sent in text for word in sent)
        return corpus, corpus_aslist

        # Compute average words per sentence
    def words_per_sentence(self):
        total_words = sum(len(sent) for text in self.corpus for sent in text)
        total_sentences = sum(len(text) for text in self.corpus)
        average_words_per_sentence = total_words / total_sentences if total_sentences > 0 else 0
        return average_words_per_sentence

        # Compute hapax ratio
    def hapax_ratio(self):
        freq_dist = FreqDist(self.corpus_aslist)
        hapaxes = freq_dist.hapaxes()
        hapax_ratio = len(hapaxes) / len(self.corpus_aslist) if len(self.corpus_aslist) > 0 else 0
        return hapax_ratio

        # Compute unique words
    def unique_word_ratio(self):
        unique_words = len(set(self.corpus_aslist))
        unique_word_ratio = unique_words / len(self.corpus_aslist) if len(self.corpus_aslist) > 0 else 0
        return unique_word_ratio

        # 
    def war_or_peace (self):
        stopWords = set(stopwords.words('english'))
        words = self.corpus_aslist
        contentwords = [w for w in words if w not in stopWords] # remove stopwords
        tagged_words = nltk.pos_tag(contentwords) # tag remaining corpus
        only_nn = [word for word, tag in tagged_words if tag in ('NN', 'NNS')] # select just nouns

        freq_nns = nltk.FreqDist(only_nn)
        
        war_rank = None
        for rank, (word, count) in enumerate(freq_nns.most_common(), start=1):
            if word == "war":
                war_rank = rank
                break
        peace_rank = None
        for rank, (word, count) in enumerate(freq_nns.most_common(), start=1):
            if word == "peace":
                peace_rank = rank
                break
        return war_rank, peace_rank


foldernames = os.listdir('D:/Dokumentumok/egyetemek/AdvancedMA/scripting_languages/finalp/texts/')

for foldername in foldernames[:10]:

    pres_analysis = President_Speech_Analysis('D:/Dokumentumok/egyetemek/AdvancedMA/scripting_languages/finalp/texts/', foldername)

    average_words_per_sentence = pres_analysis.words_per_sentence()
    hapax_ratio = pres_analysis.hapax_ratio()
    unique_word_ratio = pres_analysis.unique_word_ratio()
    war_rank, peace_rank = pres_analysis.war_or_peace()

    print(f"President Name : {foldername}")
    print(f"Average Words per Sentence: {average_words_per_sentence:.2f}")
    print(f"Hapax Ratio: {hapax_ratio}")
    print(f"Unique Word Ratio: {unique_word_ratio}")
    print(f"War score: {war_rank}")
    print(f"Peace score: {peace_rank}")
    print("/n")