from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import mysql.connector

hw = ""
with open("hw.config") as file:
    hw = file.read()

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = hw,
    database = "staging"
)

mycursor = db.cursor()

app = Flask(__name__)
api = Api(app)


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=str, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=str, help="Likes of the video is required", required=True)
video_put_args.add_argument("channel", type=str, help="Channel of the video is required", required=True)
video_put_args.add_argument("subscribers", type=str, help="Channel Subscribers are required", required=True)

video_get_args = reqparse.RequestParser()



resource_fields = {
    'data': fields.List(fields.List(fields.String))
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self):
        #args = video_get_args.parse_args()

        mycursor.execute("SELECT * FROM StagingArea")
        
        rows = []

        for x in mycursor:
            row = []
            for i in x:
                i = str(i)
                row.append(i)
            rows.append(row)

        jsonData = {}
        jsonData["data"] = rows
        print(jsonData)

        return jsonData, 200

    @marshal_with(resource_fields)
    def put(self):
        args = video_put_args.parse_args()
        
        mycursor.execute("INSERT INTO StagingArea (name, views, likes, channel, subscribers) VALUES(%s,%s,%s,%s,%s)", (args['name'], args['views'], args['likes'], args['channel'], args['subscribers']))
        
        db.commit()
        return '', 201

    @marshal_with(resource_fields)
    def patch(self):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video not found...")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return result

    def delete(self):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video not found...")

        db.session.delete(result)
        db.session.commit()

        return '', 204

api.add_resource(Video, "/video/")

if __name__ == "__main__":
    app.run(debug=True)