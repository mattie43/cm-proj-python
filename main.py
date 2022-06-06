from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  views = db.Column(db.Integer, nullable=False)
  likes = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f"Video(name={name}, views={views}, likes={likes})"

resource_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'views': fields.Integer,
  'likes': fields.Integer,
}

class Video(Resource):
  @marshal_with(resource_fields)
  def get(self, video_id):
    result = VideoModel.query.filter_by(id=video_id).first()
    return result

  def post(self, video_id):
    data = request.get_json()
    newVid = VideoModel(id=video_id, name=data['name'], views=data['views'], likes=data['likes'])
    db.session.add(newVid)
    try:
      db.session.commit()
    except:
      return{'message':'failed'}
    return{'message':data}

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
  app.run(debug=True)