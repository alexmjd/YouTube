import os, logging, ffmpeg
from flask_restful import Resource, reqparse
from flask import make_response, request
from flask_jsonpify import jsonify

logging.getLogger().setLevel(logging.INFO)

            

# Lancement de la conversion
#checkDefinition(height)

class Encoding(Resource):
    def calculDef(self, file):

        # parser = reqparse.RequestParser()
        # parser.add_argument('file', type = str, help = "input file")
        # args = parser.parse_args()
        # input_file = args['file']

        #inputFileName = 'video'
        #input_file = inputFileName+'.mp4'
        logging.info("\nCHECKING ENCODER == FILE  :: {}\n".format(file))

        return 1
        input_file = file
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
    

    def checkDefinition(self, height, input_file):
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

    def get(self):
        logging.info("\n\nWE ARE IN THE GET METHOD\n\n")
        parser = reqparse.RequestParser()
        #parser.add_argument('arg', type = int, help = "donnée de test")
        parser.add_argument('file', type = str, help = "file path")
        args = parser.parse_args()

        #response = args

        #response = request.form['file']
        #r = response.json

        logging.info("\n\n LOGGING GET :: \n RESPONSE (arg) :: {}\n".format(args['file']))
        #logging.info("\n\n LOGGING GET :: \n RESPONSE :: {}\n".format(response))
        #logging.info("\n\n LOGGING POST :: \n STATUS :: {}\n REASON :: {}\n".format(response.status_code, response.reason))

        return make_response(jsonify({'Message':'Ok', 'Method': 'GET'}))

    def post(self):
        logging.info("DATA HAS BEEN RECEIVED :: \n\n")

        parser = reqparse.RequestParser()
        #parser.add_argument('arg', type = int, help = "donnée de test")
        parser.add_argument('file', type = str, help = "file path")
        args = parser.parse_args()
        
        # This is another method to do same thing (data are for test)
        #response = request.form['arg']
        #retour = response * 2

        logging.info("\n\n///// LAUNCHING CONVERSION /////\n\n")

        completePath = args['file']
        logging.info("\n RESPONSE :: {} \n\n".format(completePath))
        path = completePath.split('/')[0]
        logging.info("\n PATH :: {} \n\n".format(path))
        file = completePath.split('/')[-1]
        logging.info("\n FILE :: {} \n\n".format(file))
        
        probe = ffmpeg.probe(file)

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

        logging.info("\n\nPRINTING :: WIDTH {}\t HEIGHT {}\n\n".format(width, height))
        
        logging.info("\n\n///// START CONVERSION /////\n\n")
    
        startIndex = 0

        #Récupère l'index de départ par rapport à la vidéo input
        for i in range(len(definition)):
            if definition[i] == height:
                startIndex = i
                break

        logging.info("\nTEMPORISATION ET STARTINDEX ::{}\n".format(startIndex))
        #Lance les copies de vidéos dans les résolutions plus basse        
        for value in range(startIndex+1, len(ratio)):
            logging.info("\nTEMPORISATION 1\n")
            quotient = ratio[value]
            logging.info("\nTEMPORISATION 2\n")
            outputName = str(definition[value])+'p'

            logging.info("\nTEMPORISATION 3\n")
            newWidth = 4 * quotient if definition[value] == 480 or definition[value] == 240 else 16 * quotient
            newHeight = 3 * quotient if definition[value] == 480 or definition[value] == 240 else 9 * quotient

            logging.info("\nTEMPORISATION 4\n")
            
            if width != 0 and height != 0:
                #logging.info("\nTest index :: {}\t printing definition :: {}\t and value :: {}\n".format(startIndex, definition[startIndex], value))
                os.system("ffmpeg -i {} -vf scale={}:{} -hide_banner {}.mp4".format(file, newWidth, newHeight, path+outputName))
            logging.info("\nTEMPORISATION 5\n\n")

        logging.info("\n\n///// ENDING CONVERSION /////\n\n")
        return make_response(jsonify({'message': 'ok', 'value': args['file']}))


        logging.info("\n\n LOGGING POST :: \n RESPONSE :: {}\n".format(completePath))
        #logging.info("\n\n LOGGING POST :: \n STATUS :: {}\n REASON :: {}\n".format(responsePost.status_code, responsePost.reason))

        if request.method == 'POST':
            logging.info("\n\nWE PASS THE ROUTE, NOW WE ARE IN THE POST METHOD\n\n")
            #logging.info("\n\n PINRINTG ::: {}\n\n".format(request.json['input_file']))
            #t_id = request.json['input_file']
        return "POST IS OK"
        return make_response(jsonify({'message': ' OK', 'Method': 'POST'}))