import os, logging, ffmpeg
from flask_restful import Resource, reqparse
from flask import make_response, request
from flask_jsonpify import jsonify

logging.getLogger().setLevel(logging.INFO)

inputFileName = 'video'
input_file = inputFileName+'.mp4'
probe = ffmpeg.probe(input_file)
outputName = ''

definition = [1080, 720, 480, 360, 240]
ratio = [120, 80, 160, 40, 80]

# Récupération des infos de la videeo originale pour les opérations
width = 0
height = 0

for metadata in probe['streams']:
    for (key, value) in metadata.items():
        #print("X :: {} \t Y :: {} \n".format(key, value))
        if key == "width":
            width = value
        if key == "height":
            height = value
            
#print("Width : {} \t Height: {}\n".format(width, height))

# Lancement de la conversion
#checkDefinition(height)

class Encoding(Resource):

    def getFileName(self, filePath):
        """
        Split les infos du filePath avec les '/'
        prendre la dernière occurence (fileName)
        """
        logging.info("File :: {}".format(filePath))
        return "file name ok"

    def conversion(input_file, width, height, outputName):
        if width != 0 and height != 0:
            os.system("ffmpeg -i {} -vf scale={}:{} -hide_banner {}.mp4".format(input_file, width, height, inputFileName+outputName))
    

    def checkDefinition(self, height):
        startIndex = 0

        #Récupère l'index de départ par rapport à la vidéo input
        for i in range(len(definition)):
            if definition[i] == height:
                startIndex = i
                break

        #Lance les copies de vidéos dans les résolutions plus basse        
        for value in range(startIndex-1, len(ratio)):
            quotient = ratio[value]
            outputName = str(definition[value])+'p'

            newWidth = 4 * quotient if definition[value] == 480 or definition[value] == 240 else 16 * quotient
            newHeight = 3 * quotient if definition[value] == 480 or definition[value] == 240 else 9 * quotient

            conversion(input_file, newWidth, newHeight, outputName)

    def testRoute(self):
        return "routing ok"

    def get(self):
        logging.info("\n\nWE ARE IN THE GET METHOD\n\n")
        parser = reqparse.RequestParser()
        parser.add_argument('arg', type = int, help = "donnée de test")
        args = parser.parse_args()



        response = request.form['arg']
        #r = response.json

        logging.info("\n\n LOGGING GET :: \n RESPONSE :: {}\n".format(response))
        logging.info("\n\n LOGGING GET :: \n RESPONSE (arg) :: {}\n".format(args['arg']))
        #logging.info("\n\n LOGGING POST :: \n STATUS :: {}\n REASON :: {}\n".format(response.status_code, response.reason))

        return "yes"
        return input_file
        #string = "get method is reached + input :: " + str(input_var)
        return string

    def post(self):
        logging.info("DATA HAS BEEN RECEIVED :: \n\n")

        
        response = request.form['arg']

        retour = response * 2

        return make_response(jsonify({'message': 'ok', 'value': retour}))


        logging.info("\n\n LOGGING POST :: \n RESPONSE :: {}\n".format(response))
        #logging.info("\n\n LOGGING POST :: \n STATUS :: {}\n REASON :: {}\n".format(responsePost.status_code, responsePost.reason))

        if request.method == 'POST':
            logging.info("\n\nWE PASS THE ROUTE, NOW WE ARE IN THE POST METHOD\n\n")
            #logging.info("\n\n PINRINTG ::: {}\n\n".format(request.json['input_file']))
            #t_id = request.json['input_file']
        return "POST IS OK"
        return make_response(jsonify({'message': ' OK'}))