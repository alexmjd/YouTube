import os, logging, ffmpeg
from flask_restful import Resource
from flask_jsonpify import jsonify


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
        print("X :: {} \t Y :: {} \n".format(key, value))
        if key == "width":
            width = value
        if key == "height":
            height = value
            
print("Width : {} \t Height: {}\n".format(width, height))

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

    def get(self, input_var):
        return input_file
        #string = "get method is reached + input :: " + str(input_var)
        return string