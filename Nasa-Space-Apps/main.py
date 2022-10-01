# -*- coding: utf-8 -*-
"""
Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ONHUbQsMdQ7ecSRoKBo9OVX3tvaU4a8Y
"""

import os
import string
import tensorflow as tf
# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

import pandas as pd

import IPython.display as display

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False

import numpy as np
import PIL.Image
import time
import functools
import tensorflow_hub as hub
import requests
import spacy
from spacy import displacy
import shutil

#Loading the Model


def get_style_uri(string1):
  string1 = str(string1)
  if(string1.lower() == 'picasso'):
    return ".\Artists\Pablo Picasso.png"
  elif(string1.lower() == 'da vinci'):
    return ".\Artists\Da vinci.jpeg"
  elif(string1.lower() == 'van gough'):
    return ".\Artists\/van gough.jpeg"

def load_img(path_to_img):
  max_dim = 512
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img

def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)

def stylize_image(uri_content, uri_style):
  hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
  content_image = load_img(uri_content) ## Input from user (aka Nasa)
  style_image = load_img(uri_style) ##Input from user (aka our database)


  stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
  return tensor_to_image(stylized_image)

def get_image_uri(raw_text):
  NER = spacy.load("en_core_web_sm")
  text1 = NER(raw_text)
  for word in text1.ents:
      if (word.label_ == 'PERSON'):
        Person  = word
      elif(word.label_ == 'LOC'):
        Location  = word
      elif(word.label_ == 'DATE'):
        Date  = word

  r = requests.get('https://images-api.nasa.gov/search?q=Saturn&media_type=image&year_start=1998&title=Saturn&nasa_id=PIA00400')
  jsonfil = r.json()
  content_img = jsonfil['collection']['items'][0]['links'][0]['href']
  style_img = get_style_uri(Person)
    #download image and return its name
    ## Set up the image URL and filename
  filename = content_img.split("/")[-1]

  # Open the url image, set stream to True, this will return the stream content.
  r = requests.get(content_img, stream = True)

  # Check if the image was retrieved successfully
  if r.status_code == 200:
      # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
      r.raw.decode_content = True
      
      # Open a local file with wb ( write binary ) permission.
      with open(filename,'wb') as f:
          shutil.copyfileobj(r.raw, f)
          
      print('Image sucessfully Downloaded: ',filename)
  else:
      print('Image Couldn\'t be retreived')


  return filename,style_img
  








