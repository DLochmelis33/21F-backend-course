from graphene import *
from starlette.graphql import GraphQLApp
from fastapi import FastAPI
import datetime

app = FastAPI()


users = {
    0: {
        "nickname": "admin",
        "winrate": 1.0,
        "register_date": datetime.date(1970, 1, 1),
        "friends": []
    },
    1: {
        "nickname": "vasya",
        "winrate": 0.4,
        "register_date": datetime.date(2021, 10, 3),
        "friends": [2]
    },
    2: {
        "nickname": "katya",
        "winrate": 0.6,
        "register_date": datetime.date(2021, 10, 3),
        "friends": [1]
    }
}


class User(ObjectType):
    id = Field(Int)
    nickname = NonNull(String)
    winrate = Field(Float)
    register_date = Field(Date)
    friends = List(ID)


class GqlQuery(ObjectType):
    user = Field(User, user_id=Int())
    status = String()

    def resolve_user(root, info, user_id):
        userdata = users[user_id]
        return User(
            id=user_id,
            nickname=userdata["nickname"],
            winrate=userdata["winrate"],
            register_date=userdata["register_date"],
            friends=userdata["friends"]
        )

    def resolve_status(root, info):
        return String("ok")


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.add_route("/gql/", GraphQLApp(schema=Schema(query=GqlQuery)))
