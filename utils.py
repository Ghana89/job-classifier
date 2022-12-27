import pickle
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from unidecode import unidecode
import contractions
import re
import numpy as np

class predictor_class():

    def __init__(self ,data):
        self.data = data['job_description']
    
    def model_call(self):
        with open ('word2vec.model' , 'rb') as file:
            self.wordvec_model = pickle.load(file)

        with open ('svc_hyp.pkl' , 'rb') as file1:
            self.svm_model = pickle.load(file1) 


    def word2_vec(self ,data):
        self.model_call()
        feature = [] # to append vector of each review
        for rew in self.data : # iterate over reviews
            zero_vector = np.zeros( self.wordvec_model.vector_size) # zero vector for handling key error
            vectors = [] # append vector of each word
            for word in rew:
                if word in self.wordvec_model.wv : # we are checking if word is present in model
                    try :
                        vectors.append(self.wordvec_model.wv[word]) # get vector

                    except KeyError:
                        continue
            if vectors:
                vectors = np.asarray(vectors) #  merging all arrays into a single array
                avg_vec = vectors.mean(axis=0) # average of all vectors
                feature.append(avg_vec) # appending vector of each review
            else :
                feature.append(zero_vector) 
        return feature

    def remove_special_char(self , data):
        text = re.sub('\W' , ' ' ,self.data ) #  output only alpha numeric string
        text1 = re.sub('\s+' , ' ' , text) # to remove extra space from string
        expanded_text = contractions.fix(text1) # To expand Text
        data_decoded = unidecode(expanded_text) #to handle_accented characters
        tokens =word_tokenize(data_decoded) # to create token from data
        stop_words = stopwords.words('English') # to remove word not from stopwords
            # In Below Cean Text we Normalize data , we remove stopwords from data , we taken alphabatic
            # data , length of word is greater than 2 , and free from punctuations
        clean_text = [word.lower() for word in tokens if (word.lower() not in stop_words)
                        and (word not in punctuation) and (len(word) >2 and word.isalpha())]
        lemmetzier=WordNetLemmatizer()
        root_words =[lemmetzier.lemmatize(data_clean) for data_clean in clean_text ]
        input_word2vec = [[word for word in root_words ]]
        vector_ = self.word2_vec(input_word2vec)

        
        result = self.svm_model.predict([vector_[0]])[0]


        if result == 0:
         return print('Business Development & Support')

        if result == 1: 
            return print('Data Science & Analytics')
        if result == 2: 
            return 'Customer Service'
        if result == 3: 
            return 'Finance & Legal'
        if result == 4: 
            return 'Product'
        if result == 5: 
            return 'Leadership'
        if result == 6: 
            return 'Design & User Experience '
        if result == 7: 
            return 'Engineering '
        if result == 8: 
            return 'Marketing & Communications'
        if result == 9: 
            return 'IT Services'
        if result == 10: 
            return 'Finance'
        if result == 11: 
            return 'Security & Infrastructure'
        if result == 12: 
            return 'Legal & Public Affairs'
        if result == 13: 
            return 'People'




    

