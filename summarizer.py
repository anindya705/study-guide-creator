from nltk.cluster import cosine_distance
from nltk import tokenize
import nltk
import networkx as nx
import numpy as np
import re
from nltk.corpus import stopwords


def get_sentences(text):
    # sentences = re.split(r"[.!?]\s*", text)
    # sentences.pop()
    # return sentences
    return tokenize.sent_tokenize(text)

def cos_dist(first_sentence, second_sentence):
    lower_first = []
    lower_second = []
    s_words = stopwords.words('english')
    
    for word in first_sentence:
        lower_first.append(word.lower())

    for word in second_sentence:
        lower_second.append(word.lower())

    total_words = list(set(lower_first + lower_second))   

    vec1 = [0] * len(total_words)
    vec2 = [0] * len(total_words)

    for word in lower_first:
        if word not in s_words:
            vec1[total_words.index(word)] += 1
    
    for word in lower_second:
        if word not in s_words:
            vec2[total_words.index(word)] += 1
    

    return 1 - cosine_distance(vec1, vec2)

def similarity_matrix(sens):
    matrix = np.zeros((len(sens), len(sens)))

    for i in range(len(sens)):
        for j in range(len(sens)):
            if i != j:
                matrix[i][j] = cos_dist(sens[i], sens[j])
    print(matrix)
    return matrix

def summarize(text, num_sentences):
    summarize_text = []
    sentences = get_sentences(text)
    sim_matrix = similarity_matrix(sentences)
    sim_graph = nx.from_numpy_array(sim_matrix)
    rankings = nx.pagerank(sim_graph)
    ranked_sentence = sorted(((rankings[i],s) for i,s in enumerate(sentences)), reverse=True)    
    print("Indexes of top ranked_sentence order are ", ranked_sentence)
    for i in range(num_sentences):
      summarize_text.append("".join(ranked_sentence[i][1]))

    return "Summarize Text:", "  ".join(summarize_text)


