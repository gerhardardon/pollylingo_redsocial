import boto3, json, mimetypes

json_file_path = '../../../credentials.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)



ACCESS_KEY = json_data['s3']['access_key']
SECRET_KEY = json_data['s3']['secret_key']



s3 = boto3.client('s3', aws_access_key_id= ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


def upload_profile_picture_to_s3(profile_picture, profile_picture_path):
    content_type, _ = mimetypes.guess_type(profile_picture_path)
    
    try:
        s3.upload_fileobj(profile_picture, 'practica1-g1-imagenes-b', profile_picture_path, ExtraArgs={'ContentType': content_type})
        return True
    except Exception as e:
        print(e)
        return False
    
def add_s3_url(json_data, bucket_path):
    for album, pictures in json_data["albums"].items():
        for picture in pictures:
            picture_path = picture["picture_path"]
            s3_url = f"https://{bucket_path}/{picture_path}"
            picture["url"] = s3_url
    return json_data

def delete_pictures_from_paths(paths):
    try:
        for path in paths:
            s3.delete_object(Bucket='practica1-g1-imagenes-b', Key=path)
        return True
    except Exception as e:
        print(e)
        return False


def get_image_by_path(path):
    # get the image from s3
    try:
        response = s3.get_object(Bucket='practica1-g1-imagenes-b', Key=path)
        image_data = response['Body']
        return image_data
    except Exception as e:
        print(e)
        return None
