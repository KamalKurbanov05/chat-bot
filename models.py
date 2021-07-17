
from pony.orm import Database, Required, Json, db_session, select, commit

from settings import DB_CONFIG

db = Database()

db.bind(**DB_CONFIG)


class UserState(db.Entity):
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


class UserData(db.Entity):
    departure_city = Required(str)
    data_departure = Required(str)
    arrival_city = Required(str)
    sites = Required(str)
    name = Required(str)
    number = Required(str, unique=True)


db.generate_mapping(create_tables=True)

