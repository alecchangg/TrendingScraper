from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from datetime import date
import mysql.connector

hw = ""
with open("hw.config") as file:
    hw = file.read()

app = Flask(__name__)
api = Api(app)



stagingIn = reqparse.RequestParser()
stagingIn.add_argument("name", type=str, help="Name of the video is required", required=True)
stagingIn.add_argument("views", type=str, help="Views of the video is required", required=True)
stagingIn.add_argument("likes", type=str, help="Likes of the video is required", required=True)
stagingIn.add_argument("channel", type=str, help="Channel of the video is required", required=True)
stagingIn.add_argument("subscribers", type=str, help="Channel Subscribers are required", required=True)

stagingOut = reqparse.RequestParser()
stagingOut.add_argument("name", type=str, help="Name of the video is required", required=True)
stagingOut.add_argument("views", type=int, help="Views of the video is required", required=True)
stagingOut.add_argument("likes", type=int, help="Likes of the video is required", required=True)
stagingOut.add_argument("channel", type=str, help="Channel of the video is required", required=True)
stagingOut.add_argument("subscribers", type=int, help="Channel Subscribers are required", required=True)

staging_fields = {
    'data': fields.List(fields.List(fields.String))
}

class Staging(Resource):
    @marshal_with(staging_fields)
    def get(self, io):
        db, mycursor = self.connect()
        if io == "in":
            mycursor.execute("SELECT * FROM StagingAreaIn")
        elif io == "out":
            mycursor.execute("SELECT * FROM StagingAreaOut")
        rows = []
        for x in mycursor:
            row = []
            for i in x:
                i = str(i)
                row.append(i)
            rows.append(row)
        jsonData = {}
        jsonData["data"] = rows
        return jsonData, 200

    @marshal_with(staging_fields)
    def put(self, io):
        db, mycursor = self.connect()
        args = stagingIn.parse_args()
        if io == "in":
            args = stagingIn.parse_args()
            mycursor.execute("INSERT INTO StagingAreaIn (name, views, likes, channel, subscribers) VALUES(%s,%s,%s,%s,%s)", (args['name'], args['views'], args['likes'], args['channel'], args['subscribers']))
        elif io == "out":
            args = stagingOut.parse_args()
            mycursor.execute("INSERT INTO StagingAreaOut (name, views, likes, channel, subscribers) VALUES(%s,%s,%s,%s,%s)", (args['name'], args['views'], args['likes'], args['channel'], args['subscribers']))
        db.commit()
        return '', 201

    def connect(self):
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = hw,
            database = "staging"
        )
        mycursor = db.cursor()
        return db, mycursor



dim_channel = reqparse.RequestParser()
dim_channel.add_argument("key", type=int)
dim_channel.add_argument("name", type=str)
dim_channel.add_argument("subscribers", type=int)

dim_date = reqparse.RequestParser()
dim_date.add_argument("key", type=int)
dim_date.add_argument("date", type=str)

dim_video = reqparse.RequestParser()
dim_video.add_argument("key", type=int)
dim_video.add_argument("name", type=str)
dim_video.add_argument("views", type=int)
dim_video.add_argument("likes", type=int)
dim_video.add_argument("channel", type=int)
dim_video.add_argument("trending_start_date", type=int)
dim_video.add_argument("trending_end_date", type=int)

fact_current_trending = reqparse.RequestParser()
fact_current_trending.add_argument("video", type=int)
fact_current_trending.add_argument("channel", type=int)
fact_current_trending.add_argument("date", type=int)

class Warehouse(Resource):
    def get(self, location):
        db, mycursor = self.connect()
        rows = []
        if location == "channel":
            args = dim_channel.parse_args()
            mycursor.execute("SELECT * FROM dim_channel WHERE name = %s", [args['name']])
            for x in mycursor:
                row = []
                for i in x:
                    row.append(i)
                rows.append(row)
        elif location == "date":
            args = dim_date.parse_args()
            mycursor.execute("SELECT * FROM dim_date WHERE date = %s", [args['date']])
            for x in mycursor:
                row = []
                for i in x:
                    row.append(i)
                row[1] = row[1].strftime("%Y-%m-%d")
                rows.append(row)
        elif location == "video":
            args = dim_video.parse_args()
            mycursor.execute("SELECT * FROM dim_video WHERE name = %s", [args['name']])
            for x in mycursor:
                row = []
                for i in x:
                    row.append(i)
                rows.append(row)
        jsonData = {}
        jsonData['data'] = rows
        return jsonData, 200

    def put(self, location):
        db, mycursor = self.connect()
        if location == "channel":
            args = dim_channel.parse_args()
            mycursor.execute("INSERT INTO dim_channel (name, subscribers) VALUES(%s,%s)", (args['name'], args['subscribers']))
        elif location == "date":
            args = dim_date.parse_args()
            mycursor.execute("INSERT INTO dim_date (date) VALUES(%s)", [args['date']])
        elif location == "video":
            args = dim_video.parse_args()
            mycursor.execute("INSERT INTO dim_video (name, views, likes, channel, trending_start_date, trending_end_date) VALUES(%s,%s,%s,%s,%s,%s)", (args['name'], args['views'], args['likes'], args['channel'], args['trending_start_date'], args['trending_end_date']))
        elif location == "trending":
            args = fact_current_trending.parse_args()
            mycursor.execute("INSERT INTO fact_current_trending (video, channel, date) VALUES(%s,%s,%s)", (args['video'], args['channel'], args['date']))
        db.commit()
        return '', 201

    def patch(self, location):
        db, mycursor = self.connect()
        if location == "channel":
            args = dim_channel.parse_args()
            mycursor.execute("UPDATE dim_channel SET subscribers = %s WHERE channel_key = %s", (args['subscribers'], args['key']))
        elif location == "video":
            args = dim_video.parse_args()
            mycursor.execute("UPDATE dim_video SET views = %s, likes = %s, trending_end_date = %s WHERE video_key = %s", (args['views'], args['likes'], args['trending_end_date'], args['key']))
        db.commit()
        return '', 200

    def delete(self, location):
        db, mycursor = self.connect()
        if location == "trending":
            mycursor.execute("DELETE FROM fact_current_trending WHERE trending_rank < 1000")
            mycursor.execute("ALTER TABLE fact_current_trending AUTO_INCREMENT = 1")
        return '', 204

    def connect(self):
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = hw,
            database = "warehouse"
        )
        mycursor = db.cursor()
        return db, mycursor


api.add_resource(Staging, "/staging/<string:io>/")
api.add_resource(Warehouse, "/warehouse/<string:location>/")

if __name__ == "__main__":
    app.run(debug=True)