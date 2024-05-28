from flask import Flask, request, jsonify
from flask_cors import CORS
from db_handler import create_comment, create_user, ask_user, get_user_albums_and_pictures, get_name, get_album_names,editInfo, editFile, uploadFile,  create_album, update_album_name, delete_pictures_by_album, get_profile_picure_path, user_exists, create_post, get_all_posts, get_comments
from s3_handler import upload_profile_picture_to_s3, add_s3_url, delete_pictures_from_paths, get_image_by_path
from rekognition_handler import compare_faces, get_animal_info, get_profile_picture_information, detect_text
from translate_handler import translate_text
import base64
from PIL import Image
from io import BytesIO
import boto3

app = Flask(__name__)

# Utilizando una variable de entorno para la clave secreta de JWT
CORS(app)
app.json.sort_keys = False

@app.route('/')
def default():
    return 'Hello world! from python'

@app.route('/extractText', methods=['POST'])
def extract_text():
    if 'file' in request.files:
        upload_file = request.files['file']
        image64 = base64.b64encode(upload_file.read()).decode('utf-8')
        buffered = BytesIO()
        image1 = Image.open(BytesIO(base64.b64decode(image64)))
        image1.save(buffered, format="PNG")
        image1_bytes = buffered.getvalue()
        response = detect_text(image1_bytes)
        return jsonify({"text": response})


@app.route('/auth/register', methods=['POST'])
def register():
    full_name = request.form.get('fullName')
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not (full_name and username and password):
        return jsonify({"type": "error", "message": "Faltan datos para el registro"}), 400
    
    profile_picture_path = 'Fotos_perfil/default.png'
    if 'profilePicture' in request.files:
        profile_picture = request.files['profilePicture']
        profile_picture_path = f'Fotos_perfil/{username}_{profile_picture.filename}'
    
    response = create_user(full_name, username, password, profile_picture_path)
    if response['type'] == 'ok':
        if 'profilePicture' in request.files and not upload_profile_picture_to_s3(profile_picture, profile_picture_path):
            return jsonify({"type": "warning", "message":"Advertencia (fallo al subir foto): usuario registrado sin foto, puede intentar subirla de nuevo en su perfil"})
    return jsonify(response)


@app.route('/translate', methods=['POST'])
def do_translate():
    text = request.json.get('text')
    source_language = request.json.get('sourceLanguage')
    target_language = request.json.get('targetLanguage')
    print (text, source_language, target_language)
    translated_text = translate_text(text, source_language, target_language)
    return jsonify({"translatedText": translated_text})

@app.route('/auth/login', methods=['POST'])
def login():
    
    username = request.form.get('username')
    password = request.form.get('password')

    if user_exists(username) == False:
        return jsonify({"type": "error", "message": f"El usuario '{username}' no existe"}), 401



    if 'profilePicture' in request.files:
        profile_picture = request.files['profilePicture']
        profile_picture.save("profile_picture.jpg")
        # Move the file pointer back to the start of the file
        profile_picture.seek(0)
        # convert profile picture to base64
        profile_picture_base64 = base64.b64encode(profile_picture.read()).decode('utf-8')

        # save profile picture to local machine

        original_profile_picture_path = get_profile_picure_path(username)
        if not original_profile_picture_path:
            return jsonify({"type": "error", "message": "No se encontró foto de perfil"}), 400
        original_profile_picture = get_image_by_path(original_profile_picture_path['picture_path'])
        # convert original_profile_picture to base64
        original_profile_picture_base64 = base64.b64encode(original_profile_picture.read()).decode('utf-8')
        buffered = BytesIO()
        image1 = Image.open(BytesIO(base64.b64decode(profile_picture_base64)))
        image1.save(buffered, format="JPEG")
        image1_bytes = buffered.getvalue()
        buffered2 = BytesIO()
        image2 = Image.open(BytesIO(base64.b64decode(original_profile_picture_base64)))
        image2.save(buffered2, format="JPEG")
        image2_bytes = buffered2.getvalue()

        response = compare_faces(image1_bytes,image2_bytes)
        print("response",response)
        return jsonify(response)



    else:
        print(username, password)
        # Tenemos que encriptar el password para ver si luego hace match 
        if not (username and password):
            return jsonify({"type": "error", "message": "Faltan datos para el login"}), 400

        response = ask_user(username, password)
        if response['type'] == 'ok':
            #access_token = create_access_token(identity=username)
            return jsonify({"type": "ok", "message":"Login con Exito"}), 200
        else:
            print(response) 
            return jsonify(response), 401
        


@app.route('/get/profile-picture-tags', methods=['POST'])
def get_profile_picture_tags():
    username = request.get_json().get('username')
    original_profile_picture_path = get_profile_picure_path(username)
    if not original_profile_picture_path:
        return jsonify({"type": "error", "message": "No se encontró foto de perfil"}), 400
    original_profile_picture = get_image_by_path(original_profile_picture_path['picture_path'])
    # convert original_profile_picture to base64
    original_profile_picture_base64 = base64.b64encode(original_profile_picture.read()).decode('utf-8')
    buffered = BytesIO()
    image1 = Image.open(BytesIO(base64.b64decode(original_profile_picture_base64)))
    image1.save(buffered, format="JPEG")
    image1_bytes = buffered.getvalue()
    response = get_profile_picture_information(image1_bytes)
    return jsonify(response)

@app.route('/get/image-album', methods=['POST'])
def get_image_album():
    if 'file' in request.files:
        upload_file = request.files['file']
        print(upload_file)

        # convert original_profile_picture to base64
        image64 = base64.b64encode(upload_file.read()).decode('utf-8')
        buffered = BytesIO()
        image1 = Image.open(BytesIO(base64.b64decode(image64)))
        image1.save(buffered, format="PNG")
        image1_bytes = buffered.getvalue()
        response = get_animal_info(image1_bytes)
        return jsonify(response)
    else:
        return jsonify({"type": "error", "message": "Upsi no se ha enviado la imagen"}), 400


@app.route('/get/albums', methods=['POST'])
def get_albums_and_pictures():
    data = request.get_json()
    username = data.get('username')
    json_without_urls = get_user_albums_and_pictures(username)
    json_with_urls = add_s3_url(json_without_urls, "practica1-g1-imagenes-b.s3.amazonaws.com")
    return jsonify(json_with_urls)


# TODO add to nodejs api
@app.route('/get/albums-names', methods=['POST'])
def get_albums_names():
    payload = request.get_json()
    username = payload.get('username')

    return jsonify(get_album_names(username))

@app.route('/create-album', methods=['POST'])
def create_albumm():
    payload = request.get_json()
    username = payload.get('username')
    album_name = payload.get('albumName')

    print(username, album_name)

    return jsonify(create_album(username, album_name))


@app.route('/update-album', methods=['POST'])
def update_album():
    payload = request.get_json()
    username = payload.get('username')
    new_album_name = payload.get('newAlbumName')
    old_album_name = payload.get('oldAlbumName')

    return jsonify(update_album_name(username, old_album_name, new_album_name))


@app.route('/delete-album', methods=['POST'])
def delete_album():
    payload = request.get_json()
    username = payload.get('username')
    album_name = payload.get('albumName')
    paths_to_delete = delete_pictures_by_album(username, album_name)
    if delete_pictures_from_paths(paths_to_delete):
        return jsonify({'type': 'ok', 'message': f'Álbum {album_name} eliminado con éxito'})
    
    return jsonify({'type': 'err', 'message': f'No se pudo eliminar álbum "{album_name}"'})




@app.route('/get/name', methods=['POST'])
def get_profile_name():
    payload = request.get_json()
    username = payload.get('username')
    user_name = get_name(username)
    return user_name

@app.route('/photos', methods=['GET'])
def list_photos():
    # Lógica para listar las fotos del usuario
    return jsonify({"message": "Listado de fotos"}), 200

@app.route('/edit-album/<albumid>', methods=['PUT'])
def edit_album(albumid):
    # Lógica para editar un álbum
    return jsonify({"message": "Álbum editado"}), 200


@app.route('/user/profile', methods=['PUT'])
def upload_profile_photo():
    username = request.form.get('username')
    newusername = request.form.get('newusername')
    fullname = request.form.get('fullname')
    password = request.form.get('password')

    response = ask_user(username, password)
    if response['type'] == 'ok':
        
        profile_picture_path = None
        if 'file' in request.files:
            profile_picture = request.files['file']
            profile_picture_path = f'Fotos_perfil/{username}_{profile_picture.filename}'

        # print("username: ", username, "newusername: ", newusername, "fullname: ", fullname, "password: ", password, "profile_picture_path: ", profile_picture_path)

        if profile_picture_path == None:
            print('no profile picture')
            response = editInfo(username, newusername, fullname, password)
            return jsonify(response)
        else:
            print(' profile picture sent')
            response = editInfo(username, newusername, fullname, password)
            print('edit response: ', response)
            editFile(newusername, profile_picture_path)
            upload_profile_picture_to_s3(profile_picture, profile_picture_path)
            return jsonify(response), 200
    else:
        return jsonify(response), 401

    

 

@app.route('/photos', methods=['POST'])
# JWT -> Autenticacion del metodo 
def upload_photo():
    username = request.form.get('username')
    album = request.form.get('album')
    name = request.form.get('name')
    description = request.form.get('description')
    
    upload_path = None
    if 'file' in request.files:
        upload_file = request.files['file']
        upload_path = f'Fotos_publicadas/{name}.png'
    
    # print("username: ", username, "album: ", album, "name: ", name, "upload_path: ", upload_path)
    if upload_path == None:
        return jsonify({"type" : "err", "message": "No se pudo subir foto, intente de nuevo mas tarde"}), 500
    else:
        uploadFile(username, album, upload_path, description)
        upload_profile_picture_to_s3(upload_file, upload_path)
        return jsonify({"type" : "ok", "message": "Foto subida con éxito"}), 200
    
## Endpoint para crear un post (nombre de usuario, nombre de album, contedio de tag, descripcion de post)    
@app.route('/add-post', methods=['POST'])
def add_post():
    print("entrando a add-post")
    username = request.form.get('username')
    album = request.form.get('album')
    tag = request.form.get('tag')
    postDescription = request.form.get('postDescription')
    fileName = request.form.get('fileName')
    #print(username, album, tag, postDescription)

    upload_path = None
    if 'file' in request.files:
        upload_file = request.files['file']
        ###cambiar al path de uso en s3
        upload_path = f'Fotos_publicadas/{fileName}.png'

    if upload_path == None:
        return jsonify({"type" : "err", "message": "No se pudo subir foto, intente de nuevo mas tarde"}), 500
    else:
        create_post(username, album, upload_path, tag, postDescription)
        return jsonify({"type" : "ok", "message": "Foto subida con éxito"}), 200

## devuelve un JSON con la info de todos los post
@app.route('/get-all-posts', methods=['GET'])
def get_posts():
    return get_all_posts()

## Endpoint para dejar un comentario en un post (id del post, descripcion del comentario) 
@app.route('/leave-comments', methods=['POST'])
def leave_comment():
    post_id = request.form.get('post_id')
    description = request.form.get('description')
    print(post_id, description)
    try:
        create_comment(description, post_id)
        return jsonify({"type": "ok", "message": "Comentario agregado con éxito"})
    except Exception as e:
        return jsonify({"type": "error", "message": e}), 500

##devuelve un json con los comentarios de un post (postId)
@app.route('/get-comments', methods=['GET'])
def get_comment():
    post_id = request.form.get('post_id')
    print(post_id)
    return get_comments(post_id)

@app.route('/get-current-profile-picture', methods=['POST'])
def get_current_pp():
    return get_profile_picure_path(request.get_json().get('username'))

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
