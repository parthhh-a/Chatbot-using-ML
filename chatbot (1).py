# -*- coding: utf-8 -*-
"""Chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PyUvT8IhrxEMrCKE-u-GcLCUq1FbI7ju
"""

#importing the libraries
import tensorflow as tf
import numpy as np
import pandas as pd
import json
import nltk
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Input , Embedding , LSTM , Dense , GlobalMaxPooling1D , Flatten
from tensorflow.keras.models import Model 
import matplotlib.pyplot as plt



# Commented out IPython magic to ensure Python compatibility.
# %%writefile content.json
# {"intents": [
#     {"tag": "greeting",
#      "patterns": ["Hi there", "Hello", "Hola","Hey","Hi", "Hello", "Good morning","Good Evening"],
#      "responses": ["Hello, Welcome to Parth's IT support Chatbot", "Good to see you, Welcome to my Chatbot", "Hi there, how can I help?"],
#      "context": [""]
#     },
#     {"tag": "goodbye",
#      "patterns": ["Bye", "See you later", "Goodbye", "Nice chatting to you, bye", "Till next time","Bye Chatbot"],
#      "responses": ["See you!", "Have a nice day", "Bye! Come back again soon.","Happy to help"],
#      "context": [""]
#     },
#     {"tag": "thanks",
#      "patterns": ["Thanks", "Thank you", "That's helpful", "Awesome, thanks", "Thanks for helping me"],
#      "responses": ["Happy to help! Any other issues?", "Any time! Any other issues I can help with?", "My pleasure! Any other Issues I can help with?"],
#      "context": [""]
#     },
#     {"tag": "noanswer",
#      "patterns": ["q","random","abcdef"],
#      "responses": ["Sorry, can't understand you", "Please give me more info", "Not sure I understand"],
#      "context": [""]
#     },
#     {"tag": "options",
#      "patterns": ["How you could help me?", "What you can do?", "What help you provide?", "How you can be helpful?", "What support is offered","What services do you provide?","What can you help me with"],
#      "responses": ["I can guide you through\n 1)Password Reset\n2) Trouble-Shooting issues\n3) Virus Issues\n4) Printing Issues\n5) many more IT issues", "Offering support for \n1) Password Reset\n2) Trouble-Shooting issues\n3) Virus Issues\n4) Printer issues\n5) Other IT tasks"],
#      "context": [""]
#     },
#     {"tag": "Password Reset",
#      "patterns": ["How to reset my password?","I’m unable to log in!","My Password is Lost, need to Reset.","Open password reset module", "Reset my password", "Forgot password", "how do i reset my password?","Hi,I have problem with my password","Problem with Login ID" ],
#      "responses": ["Confirm your email address"],
#      "context_set": ["email"]
#     },
#     {"tag": "E-mail id",
#      "patterns": ["@gmail.com", "@outlook.com", "@yahoo.com", "@hotmail.in"],
#      "responses": ["The reset pin has been sent on your registered mobile number"],
#      "context_filter": ["email"]
#     },
#     
#     {"tag": "Blue Sreen issue",
#      "patterns": ["I’ve got the dreaded blue screen of death!","blue screen issue"],
#      "responses": ["This problem is usually related to hardware or a driver that is not working correctly. It usually happens after you install a new piece of hardware or update some drivers."],
#      "context": [""]
#     },
#     {"tag": "Deleted files",
#      "patterns": ["I deleted some important files!", "Find my deleted files", "removed neccesary files","I by mistake deleted my folders","Can you help me with deleted files issue","I am unable to find my files"],
#      "responses": ["The first step is to check the recycle bin. If that fails, you can contact your IT Support partner."],
#      "context": ["search_pharmacy_by_name"]
#     },
#     {"tag": "Unsaved Document",
#      "patterns": ["I just closed my document without saving!","Unsaved Document","Forgot to save my work"],
#      "responses": ["However, all your work is not definitely lost. If you have Auto-Recover options enabled in Microsoft Office, then there are some easy steps to recover your work.\nIf not, you can also search for Word backup files by clicking “open”, “computer” and then browsing to the folder where the file was last saved.\nYou may also be able to find your file by performing a search on your computer for temporary files with a .tmp file extension or a ~ prefix."],
#      "context": [""]
#     },
#     {"tag": "Slow Computer",
#      "patterns": ["Slow Computer", "My computer is running too slowly!", "Computer is not fast"],
#      "responses": ["Here are my 10 quick tips for things you can do to speed up your PC\n1. Cut down on start-up items\n2. Uninstall programs you no longer use\n3. Clean up your hard drive\n4. Clean your browser\n5. Scan for and remove malware\n6. Adjust for better performance\n7. Defrag your hard drive\n8. Add more RAM.\n9. Upgrade to an SSD drive\n10. Don’t shut down, use Hibernate "],
#      "context": [""]
#     },
#     {"tag": "Unexpected Shut Down",
#      "patterns": ["My computer just shut down unexpectedly!","computer shut down unexpected","Computer keeps shutting down","computer shutdown","pc shutdown"],
#      "responses": ["This could be related to overheating. Check your computer for dust, and make sure it is in a cool and ventilated place. If this is not the issue, then it is likely a virus problem. Disconnect the PC from any networks and call your IT Support experts!"],
#      "context": ["search_hospital_by_type"]
#     },
#     {"tag": "Printing issues",
#      "patterns": ["I can’t print anything!","Printing issue","My printer isn’t printing","Can’t seem to use my department’s printer"],
#      "responses": ["Check the printer is turned on, has paper, has ink/toner, paper in the correct tray etc."],
#      "context": [""]
#     },
#     {"tag": "Vague",
#      "patterns": ["Nothing works","I have issues","I need Help","I have problems"],
#      "responses": ["Hey, I cant seems that you have not listed you Issue here.\n I can help you out with the following issues: \n 1)Password Reset\n 2) Trouble-Shooting issues\n 3) Virus Issues \n 4)Printing Issues and many more IT issues"],
#      "context": [""]
#     },
#     {"tag": "Virus",
#      "patterns": ["I have virus in my laptop","Virus issues","Computer has a virus","I have problems"],
#      "responses": ["A detailed step by step guide to remove the virus from the computer has been provided on the following link: \nhttps://www.easeus.com/file-recovery/remove-virus-without-antivirus.html \nand\nhttps://www.pcworld.com/article/243818/how-to-remove-malware-from-your-windows-pc.html\nIf the issues are still there, consult the IT team"],
#      "context": [""]
#     },
#     {"tag": "Mouse",
#      "patterns": ["My Mouse is not working","The mouse is dead","Bluetooth mouse not working","Mouse issues","trackpad not working","I need help with trackpad problems"],
#      "responses": ["a) If you encounter a mouse problem, you should first try these options:\n1) If it is a first-time issue, restarting your PC can resolve the issue instantly.\n2) Confirm that the mouse or the wireless adaptor is firmly connected to the PC.\n3) You may also try to unplug the mouse cable or the wireless adaptor and reconnect using a different port.\n4)Check the mouse and the ports for damages and even try the mouse on a different computer.\n4 If none of these solves the problem, you can now proceed to other solutions.\nb) Troubleshoot Hardware and Devices\nc) Updating Incompatible Mouse Drivers\nd) Roll Back or Reinstall Mouse Drivers\ne) Deactivate Enhanced Pointer Precision\nf) Adjusting the Mouse Sensitivity\ng) Configure Touchpad Delay\nh) Disable Touchpad"],
#      "context": [""]
#     },
#     {"tag": "USB",
#      "patterns": ["My computer does not recognise my USB device!","Okay so i need help with pendrive","USB issues","Pendrive issues","pendrive is not detected"],
#      "responses": ["First things to check are:\n1) Does the device work in a different USB port on the machine?\n2) Are other devices recognised in that port?\n3) Does the device work on another user’s machine?\n If you have tried these troubleshooting methods and still no luck, then your IT support help-desk can proceed with some more in-depth troubleshooting."],
#      "context": [""]
#     },
#     {"tag": "Slow Internet",
#      "patterns": ["My internet is really slow!","slow internet","Cannot connect to Internet","Internet is not fast","My Wi-Fi keeps dropping"],
#      "responses": ["If you're connecting wirelessly, then the location may be the problem. The signal is not necessarily strong in all corners of the building. Similarly, you could just be too far away. If this is not the issue, then spyware or viruses are a likely cause."],
#      "context": [""]
#     }
#     
# ]
# }

#import the dataset
with open('content.json') as content:
  data1 = json.load(content)

#getting all the data to list
tags = []
inputs = []
responses = {}
for intent in data1['intents']:
  responses [intent['tag']]=intent['responses']
  for lines in intent['patterns']: 
    inputs.append(lines)
    tags.append(intent['tag'])

#converting to dataframe
data = pd.DataFrame({"inputs":inputs ,"tags": tags})

data

#Data-Preprocessing
#Removing punctuations
import string
data['inputs'] = data['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['inputs'] = data['inputs'].apply(lambda wrd:''.join(wrd))
data

#tockenize the data
from tensorflow.keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['inputs'])
train = tokenizer.texts_to_sequences(data['inputs'])
#apply padding
from tensorflow.keras.preprocessing.sequence import pad_sequences
x_train = pad_sequences(train)
#encoding the outputs
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_train = le.fit_transform(data['tags'])

input_shape = x_train.shape[1]
print(input_shape)

#define vocabulary
vocabulary= len(tokenizer.word_index)
print("number of unique words : ", vocabulary)
output_length= le.classes_.shape[0]
print("output length: ", output_length)

#Neural Network : creating a model
i = Input(shape=(input_shape,))
x = Embedding(vocabulary+1 , 10) (i)
x = LSTM(10, return_sequences=True)(x)
x = Flatten()(x)
x = Dense(output_length,activation="softmax")(x)
model = Model(i,x)

#compiling the model
model.compile(loss="sparse_categorical_crossentropy", optimizer='adam',metrics=['accuracy'])

#training the model
train = model.fit(x_train,y_train,epochs=200)

#plotting model accuracy
plt.plot(train.history['accuracy'],label='training set accuracy')
plt.plot(train.history['loss'],label='training set loss')
plt.legend

import random


while True:
  texts_p = []
  prediction_input = input('You : ')
  
  #removing punctuation and converting to lowercase
  prediction_input = [letters.lower() for letters in prediction_input if letters not in string.punctuation ]
  prediction_input = ''.join(prediction_input)
  texts_p.append(prediction_input)

  #tokenizing and padding
  prediction_input = tokenizer.texts_to_sequences(texts_p)
  prediction_input = np.array(prediction_input).reshape(-1)
  prediction_input = pad_sequences([prediction_input], input_shape)

  #getting output from model
  output = model.predict(prediction_input)
  output = output.argmax()

  #finding the right tag andpredicting
  response_tag = le.inverse_transform([output])[0]
  print("Groot : ", random.choice(responses[response_tag]))
  if response_tag =="goodbye":
    break

"""DEPLOY MODEL TO HUGGINGFACE"""

!pip freeze > requirements.txt

!pipreqs .  --force

"""# New section"""