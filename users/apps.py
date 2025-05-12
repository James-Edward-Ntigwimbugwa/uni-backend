from django.apps import AppConfig

# @app.route('/',methods=[GET])
# def index():
#     return jsonify({"message": "Hello World"}),


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
