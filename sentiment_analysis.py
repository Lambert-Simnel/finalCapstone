import os
import string
import spacy
import pandas as pd
from textblob import TextBlob
#loading the medium set for spacy
nlp = spacy.load('en_core_web_md')
#importing the reviews from external file
dataframe = pd.read_csv(os.path.join(os.path.dirname(__file__),"archive\\Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv"))
#removing all other columns and any empty rows
review_data = dataframe['reviews.text'].dropna()
#due to ' being integra to words like "we're" and the propensity for reviews to include phrases like.this we need to keep those, so making a modified punctuation set
unneeded_punctuation = string.punctuation.replace('.','').replace('\'','')
#Creating a function that takes a review and returns the polarity
def review_to_polairty(review):
    #Cleaning the reviews by first replacing all . with spaces, then removing all other uneeded punctuation, making it all lower case and stripping extra spaces.
    clean_review = str(review).strip().lower().translate(str.maketrans('', '', unneeded_punctuation)).replace('.',' ')
    #Using spacy to tokenise the reviews, then removing all stop words, then turning back into text
    token_review = nlp(clean_review)
    nonstop_review = str([token.text for token in token_review if not token.is_stop])
    #Using TextBlob to turn the review string into a text blob, so it can then try to fix spelling as bets it can
    blob_review = TextBlob(nonstop_review)
    clean_blob_review = blob_review.correct()
    #Finally using TextBlob for sentiment analysis
    return clean_blob_review.sentiment.polarity
#Setting up a loop for basic user input
i = 0
while i == 0:
    request = str(input("Please enter the id of the reviews you want to compare, starting with the first review id number only, or all for a list of all reviews with polarity: "))
    #Making the pogram iterate though every reviews and make a dictionary of reviews with their polarity, could be modified to export this to a file afterwards
    if request.lower() == "all":
        i = 1
        review_polarity = []
        for review in review_data:
            review_polarity.append(review_to_polairty(review))
        reviews_reviewed = dict(zip(review_data,review_polarity))
        print(reviews_reviewed)
        break
    #Having the program compare two reviews, giving the text and polarity of each
    if request.isdigit():
        input1 = int(request)
        request = str(input("Please enter the second id of the review you want to compare: "))
        if request.isdigit():
            input2 = int(request)
            print(f"The first review's polarity was {review_to_polairty(review_data[input1])} and the second was {review_to_polairty(review_data[input2])}.\nThe first review verbatum was \"{review_data[input1]}\".\nThe second review verbatum was \"{review_data[input2]}\".")
            i = 1
            break
    #If the inpout isn't valid, it loops back
    print("Invalid input")

        
