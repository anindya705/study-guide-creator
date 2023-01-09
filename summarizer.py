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
    for i in range(1):
      summarize_text.append("".join(ranked_sentence[i][1]))

    print("Summarize Text: \n", ". ".join(summarize_text))

summarize("In an attempt to build an AI-ready workforce, Microsoft announced Intelligent Cloud Hub which has been launched to empower the next generation of students with AI-ready skills. Envisioned as a three-year collaborative program, Intelligent Cloud Hub will support around 100 institutions with AI infrastructure, course content and curriculum, developer support, development tools and give students access to cloud and AI services. As part of the program, the Redmond giant which wants to expand its reach and is planning to build a strong developer ecosystem in India with the program will set up the core AI infrastructure and IoT Hub for the selected campuses. The company will provide AI development tools and Azure AI services such as Microsoft Cognitive Services, Bot Services and Azure Machine Learning.According to Manish Prakash, Country General Manager-PS, Health and Education, Microsoft India, said, With AI being the defining technology of our time, it is transforming lives and industry and the jobs of tomorrow will require a different skillset. This will require more collaborations and training and working with AI. That’s why it has become more critical than ever for educational institutions to integrate new cloud and AI technologies. The program is an attempt to ramp up the institutional set-up and build capabilities among the educators to educate the workforce of tomorrow. The program aims to build up the cognitive skills and in-depth understanding of developing intelligent cloud connected solutions for applications across industry. Earlier in April this year, the company announced Microsoft Professional Program In AI as a learning track open to the public. The program was developed to provide job ready skills to programmers who wanted to hone their skills in AI and data science with a series of online courses which featured hands-on labs and expert instructors as well. This program also included developer-focused AI school that provided a bunch of assets to help build AI skills.", 2)