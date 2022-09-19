import json
import uuid
from database import db
from flask_restful import Resource, reqparse
from flask import Response,jsonify
from typing import Dict
from return_error import return_error


todo_put_args = reqparse.RequestParser()
# All the arguments are needed to input
todo_put_args.add_argument("title", type=str, required=True)
todo_put_args.add_argument("description", type=str, required=True)


todo_update_args = reqparse.RequestParser()
# All the arguments are needed to update
todo_update_args.add_argument("title", type=str, default='')
todo_update_args.add_argument("description", type=str, default='')




class todo(Resource):

    def get(self, todoID: str = None) -> Dict:
        status_code = 0
        count = 0
        db_data = {}

        # return the list of todo objets in db
        if not todoID:
            todo_db_data = db.TODO_Collection.find({}, {"_id": False})
            if todo_db_data:
                status_code = 200
                for data in todo_db_data:
                    count += 1
                    db_data[count] = data
            else:
                return {}

        # return only todo objets for the id in db
        else:
            todo_db_data = db.TODO_Collection.find_one({"id": todoID,}, {"_id": False})
            if not todo_db_data:
                return return_error(status=404)
            else:
                status_code = 200
                db_data = todo_db_data
        byte_format = json.dumps(db_data)
        return Response(byte_format, status=status_code, mimetype='application/json')

    def put(self) -> Dict:

        status_code = 0
        # extract the arguments passed for put operation
        args = todo_put_args.parse_args()

        # Use uuid module to create an id as per the specification
        id  = str(uuid.uuid4())
        args["id"] = id

        # insert the updated dataset in mongodb collection
        try:
            status_code = 200
            response = db.TODO_Collection.insert_one(args)
            byte_format = json.dumps({"Status":"Insert operation Successfull!"})
            return Response(byte_format, status=status_code, mimetype='application/json')
        except Exception as E:
            status_code = 503
            print(e)
            return return_error(status=status_code)

    def patch(self, todoID: str = None) -> Dict:
        status_code = 0
        if not todoID:
            status_code = 400
            return return_error(status=status_code)
        else:
            # Parse the update args from request
            args = todo_update_args.parse_args()

            # delete the empty keys if they exist
            empty_keys = [key for key, value in args.items() if not value]
            for key in empty_keys:
                del args[key]
            if not args:
                # In case of empty argument body in a request
                status_code = 400
                return return_error(status=status_code)
            else:
                # Check if the id exist or not in the db
                todo_db_data = db.TODO_Collection.find_one({"id": todoID}, {"_id": False})
                if not todo_db_data:
                    status_code = 400
                    return return_error(status=status_code)
                else:
                    status_code = 200
                    # Update the data in mongodb collection
                    response =  db.TODO_Collection.find_one_and_update({"id": todoID}, {"$set": args})
                    byte_format = json.dumps({"Status": "Update operation Successfull!"})
                    return Response(byte_format, status=status_code, mimetype='application/json')

    def delete(self, todoID: str = None):
        # Some repeating code here, could be made into a smaller module to reduce the redundancy, but as a small project, can be kept for now
        status_code = 0
        if not todoID:
            status_code = 400
            return return_error(status=status_code)
        else:
            todo_db_data = db.TODO_Collection.find_one({"id": todoID}, {"_id": False})
            if not todo_db_data:
                status_code = 400
                return return_error(status=status_code)
            else:
                status_code = 200
                # Update the data in mongodb collection
                response = db.TODO_Collection.delete_one({"id": todoID})
                byte_format = json.dumps({"Status": "Delete operation Successfull!"})
                return Response(byte_format, status=status_code, mimetype='application/json')













