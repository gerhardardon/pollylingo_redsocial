import json, boto3, base64, io

json_file_path = '../../../credentials.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)



ACCESS_KEY = json_data['rekognition']['access_key']
SECRET_KEY = json_data['rekognition']['secret_key']


def compare_faces(source_image, target_image):


    client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)
    
    try:
        response = client.compare_faces(SimilarityThreshold = 90
                                        ,SourceImage={'Bytes': source_image},
                                        TargetImage={'Bytes': target_image})
        
        if response['FaceMatches'][0]['Similarity']:
            similarity_percent = response['FaceMatches'][0]['Similarity']
            print("similarity",similarity_percent)
            return ({"type": "ok", "message":"Login con Exito"}) if similarity_percent > 90 else {"type": "error", "message": "No se ha podido verificar la identidad"}

    except :
        return {"type": "error", "message": "No se ha podido verificar la identidad"}
    

def get_profile_picture_information(source_image):

    client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)
    
    try:
        response = client.detect_faces(Image={'Bytes': source_image}, Attributes=['AGE_RANGE','BEARD','EMOTIONS','EYEGLASSES','GENDER'
    ])
        age_range = f"Edad: {response['FaceDetails'][0]['AgeRange']['Low']} a {response['FaceDetails'][0]['AgeRange']['High']} años"

        # Find strongest emotion based on confidence
        emotions = response['FaceDetails'][0]['Emotions']
        strongest_emotion = max(emotions, key=lambda x: x['Confidence'])['Type']

        result = {
            "AgeRange": age_range,
            "StrongestEmotion": translate_to_spanish(strongest_emotion),
            "Gender": translate_to_spanish(response['FaceDetails'][0]['Gender']['Value']),
            "Eyeglasses": response['FaceDetails'][0]['Eyeglasses']['Value'],
            "Beard": response['FaceDetails'][0]['Beard']['Value']
        }

        return result

    except :
        return {"type": "error", "message": "No se ha podido verificar la identidad"}
    


def get_animal_info(source_image):

    client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)
    
    try:
        response = client.detect_labels(Image={'Bytes': source_image}, MaxLabels=10, MinConfidence=90)
        labels = response['Labels']
        # Muestra los objetos detectados en la imagen
        print("Objetos detectados:")
        for label in response['Labels']:
            #print(f"  - {label['Name']} (Confianza: {label['Confidence']})")

            if label['Name'] == 'Dog':
                print(f" PERRO - {label['Name']} (Confianza: {label['Confidence']})")
                return {"type": "ok", "message": "perro"}
            elif label['Name'] == 'Shark':
                print(f" TIBURON - {label['Name']} (Confianza: {label['Confidence']})")
                return {"type": "ok", "message": "tiburon"}
            elif label['Name'] == 'Cat':
                print(f" GATO - {label['Name']} (Confianza: {label['Confidence']})")
                return {"type": "ok", "message": "gato"}
            elif label['Name'] == 'Cow':
                print(f" VACA - {label['Name']} (Confianza: {label['Confidence']})")
                return {"type": "ok", "message": "vaca"}
            elif label['Name'] == 'Horse':
                print(f" CABALLO - {label['Name']} (Confianza: {label['Confidence']})")
                return {"type": "ok", "message": "caballo"}
            elif label['Name'] == 'Bear':
                print(f" OSO - {label['Name']} (Confianza: {label['Confidence']})")
                return {"type": "ok", "message": "oso"}
            elif label['Name'] == 'Elephant':
                print(f" ELEFANTE - {label['Name']} (Confianza: {label['Confidence']})")
                return {"type": "ok", "message": "elefante"}
            
    except :
        return {"type": "error", "message": "No se ha podido verificar la identidad"}
    
def detect_text(source_image):

    client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)
    
    try:
        response = client.detect_text(Image={'Bytes': source_image})
        detected_text = ""
        for text in response['TextDetections']:
            detected_text += text['DetectedText'] + " "
        return detected_text

    except :
        return {"type": "error", "message": "No se pudo extraer texto de la imagen"}



def translate_to_spanish(word):
    if word == "HAPPY":
        return "Expresión de felicidad"
    elif word == "SAD":
        return "Expresión de tristeza"
    elif word == "ANGRY":
        return "Expresión de enojo"
    elif word == "CONFUSED":
        return "Expresión de confusión"
    elif word == "DISGUSTED":
        return "Expresión de asco"
    elif word == "SURPRISED":
        return "Expresión de sorpresa"
    elif word == "CALM":
        return "Expresión neutra"
    elif word == "Male":
        return "Masculino"
    elif word == "Female":
        return "Femenino"