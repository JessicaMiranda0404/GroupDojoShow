from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Show:
    db_name = "group_dojoshows"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO shows (title,description,user_id) VALUES(%(title)s,%(description)s,%(user_id)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.db_name).query_db(query)
        shows = []
        for row in results:
            shows.append( cls(row))
        return shows

    @classmethod
    def update(cls,data):
        query = "UPDATE shows SET title = %(title)s, description = %(description)s,updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 2:
            flash("Title must be at least 2 characters","show")
            is_valid= False
        if len(show['description']) < 3:
            flash("Description must be at least 3 characters","show")
            is_valid= False
        return is_valid