from flask import Flask, request, jsonify
from model import db, HomeVideo
from flasgger import Swagger
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HomeVideo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

swagger = Swagger(app)

with app.app_context():
    db.create_all()

# 1. Post (api/HomeVideo)
@app.route('/api/HomeVideo', methods=['POST'])
def create_hv():
    """
       Добавление нового видео
       ---
       tags:
         - HomeVideo
       parameters:
         - in: body
           name: Добавление видео
           required: true
           schema:
             type: object
             required:
               - name
               - category
               - year
               - director
             properties:
               name:
                 type: string
                 description: Название видео
               category:
                 type: string
                 description: Категория видео
               year:
                 type: integer
                 description: Год выпуска
               director:
                 type: string
                 description: Режисёр видео
       responses:
         201:
           description: Видео успешно добавлено
         400:
           description: Некорректный запрос
       """
    if not request.json:
        return jsonify({'error': 'Некорректный запрос'}), 400

    data = request.json
    new_hv = HomeVideo(name=data['name'], category=data['category'],
                       year=data['year'], director=data['director'])
    db.session.add(new_hv)
    db.session.commit()
    return jsonify({'id': new_hv.id}), 201

# 2. Get (все) (api/HomeVideo)
@app.route('/api/HomeVideo', methods=['GET'])
def get_all_hw():
    """
        Просмотр всех видео
        ---
        tags:
          - HomeVideo
        responses:
          200:
            description: Список всех видео
        """
    hws = HomeVideo.query.all()
    return jsonify([{
        'id': hw.id,
        'name': hw.name,
        'category': hw.category,
        'year': hw.year,
        'director': hw.director
    } for hw in hws])

# 3. Get (конкретная) (api/HomeVideo/<id>)
@app.route('/api/HomeVideo/<int:id>', methods=['GET'])
def get_hw(id):
    """
            Просмотр видео по номеру ID
            ---
            tags:
              - HomeVideo
            parameters:
              - in: path
                name: id
                required: true
                type: integer
            responses:
              200:
                description: Информация о видео
              404:
                description: Видео не найдено
            """
    hw = HomeVideo.query.get(id)
    if not hw:
        return jsonify({'error': 'Видео не найдено'}), 404
    return jsonify({
        'id': hw.id,
        'name': hw.name,
        'category': hw.category,
        'year': hw.year,
        'director': hw.director
    })

# 4. Put (api/HomeVideo/<id>)
@app.route('/api/HomeVideo/<int:id>', methods=['PUT'])
def update_hw(id):
    """
        Обновление информации о видео
        ---
        tags:
          - HomeVideo
        parameters:
          - in: path
            name: id
            required: true
            type: integer
          - in: body
            name: Информация о видео
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: Название видео
                category:
                  type: string
                  description: Категория видео
                year:
                  type: integer
                  description: Год выпуска
                director:
                  type: string
                  description: Режисёр видео
        responses:
          200:
            description: Видеотека обновлена
          404:
            description: Видео не найдено
        """
    hw = HomeVideo.query.get(id)
    if not hw:
        return jsonify({'error': 'Видео не найдено'}), 404
    if not request.json:
        return jsonify({'error': 'Некорректный запрос'}), 400


    hw.name = request.json.get('name', hw.name)
    hw.category = request.json.get('category', hw.category)
    hw.year = request.json.get('year', hw.year)
    hw.director = request.json.get('director', hw.director)
    db.session.commit()
    return jsonify({'message': 'Видеотека обновлена'})

# 5. Delete (api/HomeVideo/<id>)
@app.route('/api/HomeVideo/<int:id>', methods=['DELETE'])
def delete_hw(id):
    """
       Удаление видео по номеру ID
       ---
       tags:
         - HomeVideo
       parameters:
         - in: path
           name: id
           required: true
           type: integer
       responses:
         200:
           description: Видео удалено
         404:
           description: Видео не найдено
       """
    hw = HomeVideo.query.get(id)
    if not hw:
        return jsonify({'error': 'Видео не найдено'}), 404

    db.session.delete(hw)
    db.session.commit()
    return jsonify({'message': 'Видео удалено'})
#if __name__ == 'main':
#  app.run(debug=True)
admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(ModelView(HomeVideo, db.session))

if __name__ == '__main__':
    #app.run('127.0.0.1', port=8050, debug=True)
    app.run(debug=True)