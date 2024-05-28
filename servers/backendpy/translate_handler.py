import boto3, json

json_file_path = '../../../credentials.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)



ACCESS_KEY = json_data['translate']['access_key']
SECRET_KEY = json_data['translate']['secret_key']

translate = boto3.client(service_name='translate', region_name='us-east-1', aws_access_key_id= ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


def translate_text(text, source_language, target_language):
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.get('TranslatedText')


# print(translate_text("Hello, how are you?", "en", "es"))