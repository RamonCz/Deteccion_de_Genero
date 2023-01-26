# Deteccion_de_Genero
En este proyecto se obtienen los datos del perfil de las cuenta de twitter que especifiquemos y con ellas hacer una prediccion de genero con un 73% de efectividad.

Usando tecnologias como Redes neuronales convolucionales, apis que detectan genero por nombre y Redes Neuronales Recurrentes. 

## Jupyters
- Analisis_Datos, Se ve un analisis de los datos y como fueron disminuyendo conforme avenzabamos
- main, Es como una guia para identificar el genero solo por su screen_name.
- /jupyters, Encontraras jupyters en los cuales muestran como hice cada modelo.

## librerias
Version de python =  3.9.16 

Installar las siguientes librerias 

- tweepy = 4.12.1
- configparser
- tensorflow = 2.10.0
- pandas 
- opencv-python = 4.6.0
- Pillow
- nltk
- [Modelos a descargar](https://drive.google.com/drive/folders/1A7A3GLHy5RZHcIMg10JTLR_YiFqT7dtI?usp=share_link).

Si quieres hacer una prueba usa main.ipynb, los demas jupyter notebook son una ventana a a ver como hice cada modelo o como limpie los datos que obtube de Twitter

## Como detectar el genero?
- Descargar los modelos, la carpeta weights y los modelos:  modelo_text.h5, modelo_vgg98.h5 y tokenizer.json
 
Todos los modelos estan en el siguiente link [Modelos a descargar](https://drive.google.com/drive/folders/1A7A3GLHy5RZHcIMg10JTLR_YiFqT7dtI?usp=share_link).
- Configurar las llaves de acceso para la API  de twitter, seguir el archivo conf.ini 
- Seguir los pasos que estan en main.ipynb 

Aqui solo tienen que cambiar las rutas de accesso a las llaves y modelos.

My_Twitter.py se usa para obtener los datos de Twitter

Detector.py se usa para usar los modelos y predecir el genero

## Que redes Nueronales se usan?
### Red neuronal convolucional
Para el modelo vgg98.h5 que detecta si hay una persona en la foto se uso este tipo de Red. Aqui una breve descripcion [Red neuronal convolucional](https://www.iebschool.com/blog/redes-neuronales-convolucionales-big-data/). En espesifico se uso una red ya pre entrenada llamada  VGG16, enternado con la base de datos imaginet. Claro adaptada a nuestras necesidades. Codigo el cual muestra mas o menos como los hice esta en person_neural.ipynb


Por otro lado se uso deteccion de objetos para ubicar las caras de las personas en las fotos asi como para predicir el genero. [Deteccion de cara](https://en.wikipedia.org/wiki/Face_detection). Codigo el cual esta en gender_cv2.ipynb o en gender_det.py para usarlo como objeto

### Red neuronale recurrente
Para el modelo text.h5 el cual predice el genero por medio de la descripcion del usuario. Aqui algunos datos de [Redes neuronales recurrentes](https://torres.ai/redes-neuronales-recurrentes/). Codigo el cual muestra mas o menos como los hice esta en text_class.ipynb


### Datos obtenidos
Todos los datos obtenidos son publicos, son de perfiles no tiene restricciones de visualizacion y se pueden acceder a ellos desde internet.

En el jupyternotebook Analisis_datos.ipynb bien un poco de explicacion acerca de los datos por cada .csv
- users.csv, Datos obtenidos de la API casi 21,000
- user_0bots.csv, Datos pero clasificando los usuarios si son bots o no. (Usando botometer) /21,000
- user_human_v1.csv, Datos de usuarios que en su foto se encontraron personas(usando vgg98)/ 4,500
- user_gender_0bots, Datos identificando personas en fotos y prediciendo el genero(usando, vgg98.h5 y text.h5)/ 1,000
- users_by_me.csv, Datos de gender_0bots pero clasificados por mi (a mano)\1,000