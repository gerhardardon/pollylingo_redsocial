import json
import mysql.connector
from mysql.connector import errorcode
from encrpyt import md5_hash
import json
from flask import jsonify


json_file_path = '../../../credentials.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)



DB_HOST = json_data['rds']['host']
DB_PORT = json_data['rds']['port']
DB_NAME = json_data['rds']['database_name']
DB_USER = json_data['rds']['user']
DB_PASSWORD = json_data['rds']['password']

def create_user(full_name, username, password, profile_picture_path):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
                       (full_name, username, md5_hash(password)))
        
        cursor.execute("SET @user_id = LAST_INSERT_ID()")

        cursor.execute("INSERT INTO albums (name, user_id) VALUES ('profile_pictures', @user_id)")

        if profile_picture_path != "Fotos_perfil/default.png":

            cursor.execute("SET @album_id = LAST_INSERT_ID()")

            cursor.execute("INSERT INTO pictures (album_id, user_id, picture_path, is_current_profile_picture) VALUES (@album_id, @user_id, %s, TRUE)", (profile_picture_path,))


        connection.commit()
        return {"type": "ok", "message":f"Correcto: Usuario '{username}' registrado!"}

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            return {"type": "err", "message":f"Error: Nombre de usuario '{username}' ya existe."}
        else:
            return {"type": "err", "message":"Error: base de datos no esta funcionando correctamente"}

    finally:
        cursor.close()
        connection.close()

# Get Data For login 
def ask_user(username, password):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s AND password = %s",
                       (username, md5_hash(password)))
        result = cursor.fetchone()[0]

        if result == 1:
            return {"type": "ok", "message": f"Correcto: Usuario '{username}' autenticado!"}
        else:
            return {"type": "err", "message": "Error: Usuario o contraseña incorrectos."}

    except mysql.connector.Error as err:
        return {"type": "err", "message": "Error: base de datos no está funcionando correctamente"}

    finally:
        cursor.close()
        connection.close()


def user_exists(username):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s",
                       (username,))
        result = cursor.fetchone()[0]

        if result == 1:
            return True
        else:
            return False

    finally:
        cursor.close()
        connection.close()

def get_name(username):
    # Assuming DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD are defined elsewhere
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_result = cursor.fetchone()
        if user_result:
            user_id = user_result['id']

            cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
            name_result = cursor.fetchone()
            if name_result:
                complete_name = name_result['name']
            else:
                # Handle case where the user's name is not found
                return jsonify({'ok': False, 'message': 'User name not found'}), 404
        else:
            # Handle case where the user ID is not found
            return jsonify({'ok': False, 'message': 'User not found'}), 404
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'ok': False, 'message': 'An error occurred'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'ok': True, 'name': complete_name})

def get_user_albums_and_pictures(username):
    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        with connection.cursor(dictionary=True) as cursor:
            # Get user ID based on the username
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = cursor.fetchone()['id']

            # Get album names
            cursor.execute("SELECT name FROM albums WHERE user_id = %s", (user_id,))
            album_names = [album['name'] for album in cursor.fetchall()]

            # Get pictures for each album along with the current profile picture
            albums_info = {}
            for album_name in album_names:
                cursor.execute("""
                    SELECT p.picture_path, p.is_current_profile_picture, p.description
                    FROM pictures p
                    JOIN albums a ON p.album_id = a.album_id
                    WHERE a.user_id = %s AND a.name = %s
                """, (user_id, album_name))
                
                pictures_info = []
                for picture in cursor.fetchall():
                    picture_info = {
                        'picture_path': picture['picture_path'],
                        'is_current_profile_picture': picture['is_current_profile_picture'],
                        'description': picture['description']
                    }
                    pictures_info.append(picture_info)
                
                albums_info[album_name] = pictures_info

    finally:
        connection.close()

    # Create JSON object
    result = {'albums': albums_info}
    return result

def get_profile_picure_path(username):
    profile_picture_path = None
    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        with connection.cursor(dictionary=True) as cursor:
            # Get user ID based on the username
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = cursor.fetchone()['id']

            cursor.execute("SELECT album_id FROM albums WHERE user_id = %s AND name = 'profile_pictures'", (user_id,))
            album_id = cursor.fetchone()['album_id']

            cursor.execute("SELECT picture_path FROM pictures WHERE album_id = %s AND is_current_profile_picture = 1", (album_id,))
            profile_picture_path = cursor.fetchone()['picture_path']

    finally:
        connection.close()

    # Create JSON object
    result = {'picture_path': profile_picture_path}
    return result

def editInfo(username, newusername, fullname, passwordd):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute("UPDATE users SET name = %s WHERE username = %s ",
                       (fullname, username))
        cursor.execute("UPDATE users SET username = %s WHERE username = %s",
                       (newusername, username))
        connection.commit()

        return {"type": "ok", "message":f"Correcto: Información de usuario '{username}' modificada!", "newusername": newusername}

    except mysql.connector.Error as err:
        print(err)
        if err.errno == errorcode.ER_DUP_ENTRY:
            return {"type": "err", "message":f"Error: Nombre de usuario '{username}' ya existe."}
        else:
            return {"type": "err", "message":"Error: base de datos no esta funcionando correctamente"}

    finally:
        cursor.close()
        connection.close()

def editFile(newusername, profilePicturePath):
    try:
        connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )

        # Obtener el cursor
        cursor = connection.cursor()

        # Obtener el id del usuario
        cursor.execute('SELECT id FROM users WHERE username = %s', (newusername,))
        currentid = cursor.fetchone()[0]

        # Obtener el id del álbum
        cursor.execute('SELECT album_id FROM albums WHERE user_id = %s AND name = "profile_pictures"', (currentid,))
        currentalbum = cursor.fetchone()[0]

        # Actualizar el estado de las imágenes existentes
        cursor.execute('UPDATE pictures SET is_current_profile_picture = 0 WHERE user_id = %s', (currentid,))

        # Insertar la nueva imagen del perfil
        cursor.execute('INSERT INTO pictures (album_id, user_id, picture_path, is_current_profile_picture) VALUES (%s, %s, %s, 1)',
                       (currentalbum, currentid, profilePicturePath))

        # Confirmar los cambios en la base de datos
        connection.commit()

        print('foto actualizada con éxito')

    except mysql.connector.Error as err:
        print(f'Error al actualizar el perfil: {err}')

    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def uploadFile(username, album, picturePath, description):
    try:
        connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )

        # Obtener el cursor
        cursor = connection.cursor()

        # Obtener el id del usuario
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        currentid = cursor.fetchone()[0]

        # Obtener el id del álbum
        cursor.execute('SELECT album_id FROM albums WHERE user_id = %s AND name = %s', (currentid, album))
        if cursor.fetchone() == None:
            print("No existe el album: creando...")
            cursor.execute('INSERT INTO albums (name, user_id) VALUES (%s, %s)', (album, currentid))
            cursor.execute('SELECT album_id FROM albums WHERE user_id = %s AND name = %s', (currentid, album)) 
            currentalbum = cursor.fetchone()[0]
            cursor.execute('INSERT INTO pictures (album_id, user_id, picture_path, is_current_profile_picture, description) VALUES (%s, %s, %s, 0, %s)',(currentalbum, currentid, picturePath, description))

        else:
            print("Existe el album")  
            cursor.execute('SELECT album_id FROM albums WHERE user_id = %s AND name = %s', (currentid, album)) 
            currentalbum = cursor.fetchone()[0]
            cursor.execute('INSERT INTO pictures (album_id, user_id, picture_path, is_current_profile_picture, description) VALUES (%s, %s, %s, 0, %s)',(currentalbum, currentid, picturePath, description))

            


        # Actualizar el estado de las imágenes existentes
        #cursor.execute('UPDATE pictures SET is_current_profile_picture = 0 WHERE user_id = %s', (currentid,))

        # Insertar la nueva imagen del perfil
        #cursor.execute('INSERT INTO pictures (album_id, user_id, picture_path, is_current_profile_picture) VALUES (%s, %s, %s, 1)',
        #               (currentalbum, currentid, profilePicturePath))

        # Confirmar los cambios en la base de datos
        connection.commit()

        print('foto subida con éxito')

    except mysql.connector.Error as err:
        print(f'Error al subir: {err}')

    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
    
def get_album_names(username):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        query = """
        SELECT albums.album_id, albums.name as album_name
        FROM users
        JOIN albums ON users.id = albums.user_id
        WHERE users.username = %s
        """

        cursor.execute(query, (username,))
        result = cursor.fetchall()

        # Convert the result to a JSON object
        albums_json =  [{'album_id': album[0], 'album_name': album[1]} for album in result]

        connection.close()

        print(albums_json)

        return albums_json

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'type': 'err', 'message': 'An error occurred'}), 500
    
    finally:
        cursor.close()
        connection.close()

def create_post(username, album, picturePath, tag, postDescription):
    try:
        connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )

        # Obtener el cursor
        cursor = connection.cursor()

        # Obtener el id del usuario
        cursor.execute('SELECT id FROM user WHERE username = %s', (username,))
        currentid = cursor.fetchone()[0]
        print("-id user:",currentid)

        # Creamos el post
        cursor.execute('INSERT INTO post (description, user_id) VALUES (%s, %s)', (postDescription, currentid))
        cursor.execute('SELECT id FROM post WHERE user_id = %s AND description = %s', (currentid, postDescription))
        currentpost = cursor.fetchone()[0]
        print("-id post:",currentpost)

        # Verificamos si el album existe
        cursor.execute('SELECT id FROM album WHERE user_id = %s AND album_name = %s', (currentid, album))
        if cursor.fetchone() == None:
            print("No existe el album: creando...")
            # Creamos el album
            cursor.execute('INSERT INTO album (album_name, user_id) VALUES (%s, %s)', (album, currentid))
            cursor.execute('SELECT id FROM album WHERE user_id = %s AND album_name = %s', (currentid, album)) 
            currentalbum = cursor.fetchone()[0]
        else:
            print("Existe el album")
            cursor.execute('SELECT id FROM album WHERE user_id = %s AND album_name = %s', (currentid, album)) 
            currentalbum = cursor.fetchone()[0]
        print("-id album",currentalbum)
        
        # Insertamos la imagen
        cursor.execute('INSERT INTO picture (name, album_id, post_id) VALUES (%s, %s, %s)',(picturePath, currentalbum, currentpost))

        # Insertamos el tag (si es que existe)
        if tag != "":
            cursor.execute('INSERT INTO tag (tag_name, post_id) VALUES (%s, %s)',(tag, currentpost))
        connection.commit()
        print('post subido con éxito')
        

    except mysql.connector.Error as err:
        print(f'Error al subir: {err}')

    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def get_all_posts():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        query = """
        SELECT post.id, post.description, user.username, picture.name, tag.tag_name, album_name
        FROM post
        JOIN user ON post.user_id = user.id
        JOIN picture ON post.id = picture.post_id
        LEFT JOIN tag ON post.id = tag.post_id
        JOIN album ON picture.album_id = album.id
        """

        cursor.execute(query)
        result = cursor.fetchall()

        # Convert the result to a JSON object
        posts_json = [{'post_id': post[0], 'description': post[1], 'username': post[2], 'picture_name': post[3], 'tag_name': post[4], 'album_name': post[5]} for post in result]

        connection.close()

        print(posts_json)

        return posts_json

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'type': 'err', 'message': 'An error occurred'}), 500
    
    finally:
        cursor.close()
        connection.close()

def create_comment(comment, postId):
    try :
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        cursor.execute('INSERT INTO comment (description, post_id) VALUES (%s,%s)', (comment, postId))
        connection.commit()
        print('comentario subido con éxito')

    except mysql.connector.Error as err:
        print(f'Error al comentar: {err}')

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def get_comments(postId):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        query = """
        SELECT comment.id, comment.description
        FROM comment
        WHERE comment.post_id = %s
        """

        cursor.execute(query, (postId,))
        result = cursor.fetchall()

        # Convert the result to a JSON object
        comments_json = [{'comment_id': comment[0], 'description': comment[1]} for comment in result]

        connection.close()

        print(comments_json)

        return comments_json

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'type': 'err', 'message': 'An error occurred'}), 500
    
    finally:
        cursor.close()
        connection.close()

def create_album(username, album_name):
    connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()

        if user_id:
            user_id = user_id[0]  
 
            cursor.execute("INSERT INTO albums (name, user_id) VALUES (%s, %s)", (album_name, user_id))

            connection.commit()

            return {"type": "ok", "message": f"Album '{album_name}' creado con éxito!"}
        else:
            return {"type": "err", "message": "Usuario no encontrado"}

    except mysql.connector.Error as err:
        print(err)
        return {"type": "err", "message": "Error: base de datos no está funcionando correctamente"}

    finally:
        cursor.close()
        connection.close()

def update_album_name(username, old_album_name, new_album_name):

    try:
        connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
        cursor = connection.cursor()

        update_query = """
            UPDATE albums
            SET name = %s
            WHERE user_id = (
                SELECT id
                FROM users
                WHERE username = %s
            ) AND name = %s
        """

        cursor.execute(update_query, (new_album_name, username, old_album_name))
        return {"type": "ok", "message": f"Nombre de álbum '{old_album_name}' actualizado a '{new_album_name}' con éxito!"}
    except mysql.connector.Error as err:
        print(err)
        return {"type": "err", "message": "Error: base de datos no está funcionando correctamente"}

    finally:
        connection.commit()
        cursor.close()
        connection.close()

def delete_pictures_by_album(username, album_name):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
        cursor = connection.cursor()

        # Get user_id
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()

        if not user_id:
            return json.dumps({"error": "User not found"})

        # Get album_id
        cursor.execute("SELECT album_id FROM albums WHERE user_id = %s AND name = %s", (user_id[0], album_name))
        album_id = cursor.fetchone()

        if not album_id:
            return json.dumps({"error": "Album not found for the specified user"})

        # Get pictures to be deleted
        cursor.execute("SELECT * FROM pictures WHERE album_id = %s", (album_id[0],))
        deleted_pictures = cursor.fetchall()

        # Delete pictures
        cursor.execute("DELETE FROM pictures WHERE album_id = %s", (album_id[0],))

        cursor.execute("DELETE FROM albums WHERE album_id = %s", (album_id[0],))

        # Commit changes and close connection
        connection.commit()

        path_list = [tup[3] for tup in deleted_pictures]
        return path_list
    except mysql.connector.Error as err:
        print(err)
        return {"type": "err", "message": "Error: base de datos no está funcionando correctamente"}
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
    