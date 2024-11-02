from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from tensorflow import keras
import pickle
import json
from .forms import CommentForm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from .data_cleaning import process_text, clean_text
from .clean_data import clean_text, remove_diacritics, remove_emoji
from .post_scraping import youtube_scrap, twitter_scrap, instagram_scrap
# Create your views here.


def get_predict(request):
    return render(request, 'myapp/by_post.html')

def get_predict_link(request):
    return render(request, 'myapp/by_link.html')


# def get_prediction(request, comment):
#     mymodel = keras.models.load_model(r"c:\Users\FOX\Desktop\project sentiment analysis\model_with_using_svm.pkl")
#     with open(r"C:\Users\zakaria\Desktop\projects\npl_arab\Arabic-Sentiment-Analysis-main\Model\saved_tokenizer.pickle", 'rb') as handle:
#         tokenizer = pickle.load(handle)
#     x = pad_sequences(tokenizer.texts_to_sequences([comment]),
#                         maxlen = 180)
#     y_pred = mymodel.predict(x)
#     if y_pred[0][0]>=0.5:
#         print(y_pred[0][0])
#         #  messages.success(request, 'Positive')
#         #  return HttpResponse("Positive")
#         return HttpResponse(json.dumps({'message':'Positive'}), content_type='application/json')
#     else:
#         print(y_pred[0][0])
#         #  messages.success(request, 'Negative')
#         #  return HttpResponse("Negative")
#         return HttpResponse(json.dumps({'message':'Negative'}), content_type='application/json')
    
with open(r"c:\Users\FOX\Desktop\project sentiment analysis\model_with_using_svm.pkl", 'rb') as handle:
        model = pickle.load(handle)

def get_prediction(request, comment):

    comment = process_text(clean_text(comment))
    print(comment)
    y_pred = model.predict(np.array([comment]))
    
    return HttpResponse(json.dumps({'message':f'{y_pred[0]}'}), content_type='application/json')
     

# def get_prediction_link(request, link_post):

#      mymodel = keras.models.load_model(r"c:\Users\FOX\Desktop\project sentiment analysis\model_with_using_svm.pkl")
#      with open(r"C:\Users\zakaria\Desktop\projects\npl_arab\Arabic-Sentiment-Analysis-main\Model\saved_tokenizer.pickle", 'rb') as handle:
#          tokenizer = pickle.load(handle)
#      if 'youtube' in link_post or 'youtu.be' in link_post:
#          print(request.GET['v'])
#          data = youtube_scrap(request.GET['v'])

#      if 'twitter' in link_post or 'x.com' in link_post:
#          data = twitter_scrap(link_post)

#      if 'instagram' in link_post:
#          print(link_post)
#          data = instagram_scrap(link_post)

#      predictions = []
#      for elt in data:
#          text_cleaned = clean_text(elt)
#          x = pad_sequences(tokenizer.texts_to_sequences([text_cleaned]),
#                          maxlen = 180)
#          y_pred = mymodel.predict(x)
#          if y_pred[0][0]>=0.5:
#              predictions.append([elt, text_cleaned, 'Positive'])
#          else:
#              predictions.append([elt, text_cleaned, 'Negative'])
#      print(data)
    
#      print(y_pred)
#      return HttpResponse(json.dumps(predictions), content_type='application/json')


def get_prediction_link(request, link_post):

    if 'youtube' in link_post or 'youtu.be' in link_post:
        print(request.GET['v'])
        data = youtube_scrap(request.GET['v'])

    if 'twitter' in link_post or 'x.com' in link_post:
        data = twitter_scrap(link_post)

    if 'instagram' in link_post:
        print(link_post)
        data = instagram_scrap(link_post)

    predictions = []
    for elt in data:
        comment = process_text(clean_text(elt))
        y_pred = model.predict(np.array([comment]))
        print(comment)
        print(y_pred)
        predictions.append([elt, comment, y_pred[0]])

    return HttpResponse(json.dumps(predictions), content_type='application/json')
    
     
