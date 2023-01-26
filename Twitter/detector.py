import json
import requests
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
import numpy as np
import re as re
import string
#texto
import nltk
from  tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from Twitter.gender_det  import Gender_det
class Detector:

    def __init__(self,weights, person, text, tokenizer) -> None:
        '''
        Constructor del objeto
        params:
        weights: String, ruta a la carpeta donde estan los weights
        person: String, ruta donde esta guardado el modelo para persona
        text: String, ruta donde esta guardado el modelo para texto

        '''
        #modelo para detectar personas en las fotos
        #Cambiar las rutas del modelo donde estan guardados los modelos
        self.es_persona = load_model(person)
        self.model_text_rute = text
        self.model_gender_rute = weights
        self.tokenizer_rute = tokenizer
        self.tokenizer = ""
        with open(self.tokenizer_rute) as f:
            data = json.load(f)
            self.tokenizer = tokenizer_from_json(data)
        nltk.download('stopwords')

    def detectar_nombre(self, name):
        '''
        Pregunta a una api si el nombre dado es de hombre:1 o mujer:0 
        params:
        name: String nombre a investigar
        '''
        s = name.split()
        count = 0
        for n in s:
            content = requests.get(f"https://api.genderize.io/?name={n}").text
            gender =  json.loads(content)['gender']
            count += 1 if gender == 'male' else 0
        
        return  1 if count/len(s) >= 0.5 else 0

    def detectar_persona(self, foto):
        '''
        Detecta si en la foto hay personas o no
        params:
        foto: Dirreccion de la foto
        return: 0 si es persona 1 si no es
        '''
        img = foto
        if type(foto) == str:
            img = load_img(foto)
            img = img.resize((73,73))
        img = np.array(img)
        img = np.array([img])
        r = self.es_persona.predict(img)
        #print(r[0][0])
        return 1 if r[0][0] > 0.8 else 0

    def detectar_genero_foto(self, foto):
        '''
        Detecta el genero de la persona en la foto, suponiendo que solo hay personas
         params:
        foto: Dirreccion de la foto
        return: 0 si es Mujer  1 si es Hombre
        '''
        #print(predict_gender(foto))
        dect = Gender_det(self.model_gender_rute)
        r = -1
        try:
            r =  0 if "Female" == dect.predict_gender(foto)[0] else 1
        except:
            r = -1
        return r

    def detectar_texto(self, text):
        '''
        Detecta el genero mediante la descripcion de la persona
        params:
        text: texto en español
        '''
        predict_text = Pre_text(self.tokenizer,self.model_text_rute)
        return predict_text.predict_gender(text)
     
    def detectar_genero(self, data, verbose = True):
        
        genero_foto = -1
        nombre = self.detectar_nombre(data["name"])
        es_persona = self.detectar_persona(data['image'])
        if es_persona:
            genero_foto = self.detectar_genero_foto(data['image'])
        texto = self.detectar_texto(data['description'])
        if verbose:
            print('Nombre: {}'.format(nombre))
            print('Genero por foto: {}'.format(genero_foto))
            print('Genero por descripcion: {}'.format(texto))
        if genero_foto == -1:
            total = (nombre + texto)/2 if texto != -1 else nombre
            return 1 if total >= 0.5 else 0
        elif texto != -1 :
            total = (nombre + genero_foto + texto)/3  
            return 1 if total >= 0.65 else 0
        else:
            total = (nombre + genero_foto)/2
            return 1 if total >= 0.5 else 0



class Pre_text:
    '''
    Clasee para separar el preprosesamiento del texto y predecir el genero dado el texto en Español
    '''
    def __init__(self, tokenizer,model_rute) -> None:
        '''
        Params: 
        model_rute: String donde esta guardado el modelo para texto.
        tokenizer: Objeto 
        '''
        self.tokenizer = tokenizer
        self.model_text = load_model(model_rute)
        self.stop = set(stopwords.words("spanish"))

    def remove_URL(self,text):
        '''
        Remueve texto del tipo https www y asi
        Params: texto, String
        '''
        url = re.compile(r"https?://\S+|www\.\S+")
        return url.sub(r"", text)

    
    def remove_punct(self, text):
        '''
        Remueve puntuacion den los textos
        Params: texto, String
        '''
        translator = str.maketrans("", "", string.punctuation)
        return text.translate(translator)
     

    def remove_stopwords(self,text):
        '''
        Quita las palabras [como, con, cuando,desde] etc.
        Params: texto, String
        '''
        filtered_words = [word.lower() for word in text.split() if word.lower() not in self.stop]
        return " ".join(filtered_words)

    def remove_garbage(self, text):
        '''
        Quita las ulr, puntuacion y stopword en el texto dado.
        Params: texto, String
        '''
        t = self.remove_URL(text)
        t = self.remove_punct(t)
        t = self.remove_stopwords(t)
        return t
 
    def predict_gender(self, text):
        '''
        Predice el genero con el texto que se da
        Params: texto, String
        '''
        texto = self.remove_garbage(text)
        if texto == '':
            return -1

        texto_secuencia = self.tokenizer.texts_to_sequences([texto])

        # Max number of words in a sequence
        texto_padded = pad_sequences(texto_secuencia, maxlen=20, padding="post", truncating="post")
        predictions = 1 if (self.model_text.predict(texto_padded))[0] > 0.5 else 0 
        
        return predictions