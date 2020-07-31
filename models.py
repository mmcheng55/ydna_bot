from peewee import *

db = SqliteDatabase("main.db")


class RolesCanBeAdded(Model):
    name = CharField()
    id_ = IntegerField()

    class Meta:
        database = db


class VotingForRoles(Model):
    user_id = IntegerField()
    role_id = IntegerField()
    msg_id = IntegerField()

    class Meta:
        database = db


class CommandRecords(Model):
    user_id = IntegerField()
    command = CharField()
    command_type = CharField()
    action = CharField()
    time = DateTimeField()

    class Meta:
        database = db


# class UserFlask(Model):
#     username = CharField()
#     password = CharField()


db.connect()
db.create_tables([RolesCanBeAdded, VotingForRoles, CommandRecords])


def find_query(model: Model, conditions):
    try:
        return model.get(conditions)
    except DoesNotExist:
        return None