from flask import Flask,jsonify,request,send_file
import MySQLdb
import traceback

app=Flask(__name__)
imagePath='images/{}'
imageUrl= 'https://kevin97333.pythonanywhere.com/image/{}'
@app.route('/')
def index():
    return '<h1>Server running</h1>'

#GETS

@app.route('/videos', methods=['GET'])
def search_videos():
    try:
        concept_id = request.args.get('concept_id')
        conexion = MySQLdb.connect('Database URL',
                                            'Database User',
                                            'Database Password',
                                            'Database Schema')
        cursor=conexion.cursor()
        sql = """SELECT video_id FROM has_video WHERE concept_id='{0}';""".format(concept_id)
        cursor.execute(sql)
        datos = cursor.fetchall()
        videos = []
        for fila in datos:
            video = { 'id': fila[0] }
            videos.append(video)
        cursor.close()
        conexion.close()
        return jsonify({'videos': videos}),200
    except Exception as ex:
        cursor.close()
        conexion.close()
        traceback.print_exc()
        return jsonify({'mensaje': "Bad request"}),400
@app.route('/concepts', methods=['GET'])
def get_concepts():
    try:
        conexion = MySQLdb.connect('Database URL',
                                            'Database User',
                                            'Database Password',
                                            'Database Schema')
        cursor=conexion.cursor()
        sql = """SELECT id,title,authors,category,main_image,location,description FROM concept;"""
        cursor.execute(sql)
        datos = cursor.fetchall()
        concepts = []
        for fila in datos:
            image = { 'url': imageUrl.format(fila[4]) }
            if fila[5]!= "":
                concept = {'id': fila[0], 'title': fila[1], 'authors': fila[2], 'category': fila[3], 'image': image, 'location': fila[5], 'description': fila[6] }
            else:
                concept = {'id': fila[0], 'title': fila[1], 'authors': fila[2], 'category': fila[3], 'image': image, 'description': fila[6] }
            concepts.append({'concept': concept})
        cursor.close()
        conexion.close()
        return jsonify({'concepts': concepts}),200
    except Exception as ex:
        cursor.close()
        conexion.close()
        traceback.print_exc()
        return jsonify({'mensaje': "Bad request"}), 400
@app.route('/image/<name>', methods=['GET'])
def get_image(name):
    image = imagePath.format(name)
    return send_file(image, mimetype="image/png")


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(host='0.0.0.0',port=5000)
