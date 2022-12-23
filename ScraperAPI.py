from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
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
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = hw,
            database = "staging"
        )
        mycursor = db.cursor()

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

        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = hw,
            database = "staging"
        )
        mycursor = db.cursor()

        args = stagingIn.parse_args()
        if location == "staging" and io == "in":
            args = stagingIn.parse_args()
            mycursor.execute("INSERT INTO StagingAreaIn (name, views, likes, channel, subscribers) VALUES(%s,%s,%s,%s,%s)", (args['name'], args['views'], args['likes'], args['channel'], args['subscribers']))
        elif location == "staging" and io == "out":
            args = stagingOut.parse_args()
            mycursor.execute("INSERT INTO StagingAreaOut (name, views, likes, channel, subscribers) VALUES(%s,%s,%s,%s,%s)", (args['name'], args['views'], args['likes'], args['channel'], args['subscribers']))

        db.commit()
        return '', 201

    @marshal_with(staging_fields)
    def patch(self):
        pass

    def delete(self):
        return '', 204



dim_channel = reqparse.RequestParser()
dim_channel.add_argument("name", type=str, help="Channel requires a name", required=True)
dim_channel.add_argument("subscribers", type=int, help="Channel requires subscribers", required=True)

class Warehouse(Resource):
    def get(self, location):
        return {'data': "fake data"}

    def put(self, location):
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = hw,
            database = "warehouse"
        )
        mycursor = db.cursor()

        if location == "channel":
            args = dim_channel.parse_args()
            mycursor.execute("INSERT INTO dim_channel (name, subscribers) VALUES(%s,%s)", (args['name'], args['subscribers']))

        db.commit()
        return '', 201



api.add_resource(Staging, "/staging/<string:io>/")
api.add_resource(Warehouse, "/warehouse/<string:location>/")

if __name__ == "__main__":
    app.run(debug=True)