from PIL import Image
from urllib import request
from io import BytesIO
import requests
import tweepy
import configparser
import time
import pandas as pd

class My_Twitter:

  def __init__(self, keys) -> None:
    # read configs
    self.config = configparser.ConfigParser(interpolation=None)
    self.config.read(keys)
    
    if not(float(tweepy.__version__[:3]) >= 3.1 and float(tweepy.__version__[:3]) < 4):
      
      #Usando app-auth en ambos casos
      try:
        self.api_bearer = self.config['Twitter']['bearer_token']
        self.auth = tweepy.OAuth2BearerHandler(self.api_bearer)

        self.api = tweepy.API(self.auth)
        self.cliente = tweepy.Client(bearer_token= self.api_bearer)
        #bounding_box:[-119.7747642418,14.1509134215,-89.001337923,32.7744708416]"
      except AttributeError:
        print('Solo dispondras de la funcion es_bot(). \n De botometer')
    else:
      print('Solo dispondras de la funcion es_bot(). \n De botometer')


  def get_user_data(self, username):
    try:
      data = self.cliente.get_user(username  = username,user_fields=['description','profile_image_url'])
    except:
      return -1
    s = data.data['profile_image_url']
    fin = s[-3:] if 'jpeg' != s[-4:] else 'jpeg'
    todo = s[:-10] if 'jpeg' != s[-4:] else s[:-11]
    image_url = '{}bigger.{}'.format(todo,fin)
    image = self.loadImage(image_url)
    dict = {'description':data.data['description'],"image":image,'name':data.data['name']}
    return dict


  def loadImage(self,url):
    res = request.urlopen(url).read()
    Sample_Image = Image.open(BytesIO(res))
    return Sample_Image
    
  def download_Image(self, image_url,id,path):
    '''
    Descarga la imagen de la ulr con el id que se le indica cambiamos de formato a .png o gif
    image_url: url de la imagen
    id: nombre imagen
    path: direccion de la carpeta
    '''
    tipos = ['jpg','png','gif', 'descarga', False]
    des = False
    for i in range(0,5):
      
      image_url = image_url if des else '{}{}'.format(image_url[0:-3],tipos[i])
      response = requests.get(image_url, stream=True)
      
      if response.status_code == 200:
        fin = image_url[-3:] if 'jpeg' != image_url[-4:] else 'jpeg'
        file = open("{}\{}.{}".format(path,id,tipos[i]), "wb") if tipos[i] else open("{}\{}.{}".format(path,id,fin), "wb") 
        file.write(response.content)
        file.close()
        break
      if type(tipos[i]) == bool:
        print('error al descargar imagen :{}'.format(id))
        return id
      if 'descarga' == tipos[i]:
        data = self.cliente.get_user(id = id,user_fields=['profile_image_url'])
        s = data.data['profile_image_url']
        if s == 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png':
          return id
        fin = s[-3:] if 'jpeg' != s[-4:] else 'jpeg'
        todo = s[:-10] if 'jpeg' != s[-4:] else s[:-11]
        image_url = '{}bigger.{}'.format(todo,fin)
        des = True
        continue
    return 1 if des else 0


  def es_bot(self, id):
    '''
    Identifica si la cuenta esta manejada por un bot o no, solo se pueden 2000 peticiones al dia
    Nota!!!!!!!!!! Botometer solo sirve con tweepy 'tweepy >= 3.5.0,<4'
    Param: id account
    Return: 1 si es bot o 0 de lo contrario
    '''
    if not(float(tweepy.__version__[:3]) >= 3.1 and float(tweepy.__version__[:3]) < 4):
        print("La Version de tweepy no sirve para botometer.\n Usa la 3.10.0 \n Usa  'pip install botometer' y se desactualizaran las librerias de tweeepy, pero deberas actualizarlas si deseas usar otra funcion de la clase Twitter")
    else:
        from botometer import Botometer #importamos la liberia aqui para no tener errores al usar el archivo.py
        twitter_app_auth = {
                            'consumer_key': self.config['Twitter']['api_key'],
                            'consumer_secret': self.config['Twitter']['api_key_secrete'],
                            'access_token': self.config['Twitter']['access_token'],
                            'access_token_secret': self.config['Twitter']['access_token_secret']
                          }
        botometer_api_url = "https://botometer-pro.p.rapidapi.com"

        bom = Botometer(
                        wait_on_ratelimit = True,
                        botometer_api_url=botometer_api_url,
                        rapidapi_key = self.config['Twitter']['botometer_API'],
                        **twitter_app_auth)
        result = bom.check_account(id,)
        #print(result['cap']['universal'])
        return 1 if result['cap']['universal'] > 0.75 else 0

  def downloads_users(self, file):
    '''
    Descarga los usuarios de Mexico, buscando con las palabras clave "soy de X" donde X es un estado la republica mexicana,
    La descarga se hace en automatico repetando los requests que la API de twitter nos deja y el tiempo de espera.
    Si la ubicacion del usuario no esta disponible, la funcion supondra que es de mexico
    '''

    df = pd.read_csv(file)
    number , reqs_list = 0,0
    estados = [
    'Aguascalientes',
    'Baja California',
    'Baja California Sur',
    'Campeche',
    'Chiapas',
    'Chihuahua',
    'Coahuila de Zaragoza',
    'Colima',
    'Ciudad de México',
    'Durango',
    'Guanajuato',
    'Guerrero',
    'Hidalgo',
    'Jalisco',
    'Estado de Mexico',
    'Michoacan de Ocampo',
    'Morelos',
    'Nayarit',
    'Nuevo Leon',
    'Oaxaca',
    'Puebla',
    'Queretaro de Arteaga',
    'Quintana Roo',
    'San Luis Potosi',
    'Sinaloa',
    'Sonora',
    'Tabasco',
    'Tamaulipas',
    'Tlaxcala',
    'Veracruz de Ignacio de la Llave',
    'Yucatan',
    'Zacatecas',
    'Mexico'
  ]
    #frases = ["Soy de", 'Vivo en', 'viviendo en','resido en','alojo en']
    query = ""
    for frase in ["El estado"]:
      for estado in estados:
        page = 0
        print("Descargando usuarios con: '{} {}".format(frase,estado))
        query = estado#"{} {}".format(frase,estado)#"place_country: MX" #cambiar query para obtener mas usuarios

        mexico = ['méxico','mexico','mex','cdmx']
        while(True):
          #solo se pueden hacer 300 requests por 15 min.
          if reqs_list >= 899:
            reqs_list = 0
            print("Esperado por 15 min")
            time.sleep(960)
            break
          reqs_list += 1
          users = self.api.search_users(q=query,page= page)
          for user in users:
            if(not user.id in df['id'].values): #Verifico que el usuario no este ya guardado
              atributos = ['id', 'name','screen_name','location' , 'description']
              atributos_user = []
              for x in atributos:
                try:
                  atributos_user.append(user._json[x])
                except:
                  atributos_user.append('')

              #Si la localizacion no esta activada supondremos que viene mexico
              atributos_user[3] = 'mex' if (atributos_user[3] == '') else atributos_user[3].lower() 

              #con el if nos aseguramos que venga de algun estado o que simplemente tenga el pais
              if (any(mex in atributos_user[3] for mex in mexico) or any(mex.lower() in atributos_user[3] for mex in estados)):
                  #para mejorar la exploracion pondremos el estado en donde se encontro
                  atributos_user[3] = estado
                  #get img for 73x73 
                  u = user.profile_image_url.split("_")
                  u.pop()
                  u.append("bigger.jpg") ## add _bigger al request
                  s = '_'.join(u)
                  #bot = es_bot(int(user.id)) por si algun dia actualizan botometer
                  atributos_user.append(s)
                  df.loc[len(df.index)] = atributos_user#, bot]
                  number += 1
          if page == 51: #limite de paginas 
            break
          page += 1
        #Guardamos el dataFrame
    print("Se han descargado: {} nuevos usuarios".format(number)) 
    df.to_csv(file, index= False)
