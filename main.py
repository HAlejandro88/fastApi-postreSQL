import databases
import sqlalchemy

from fastapi import FastAPI, Request

DATABASE_URL = "postgresql://postgres:mysecretpassword@some-postgres:5432/mydatabase"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

# middlewares

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.get("/books")
async def find_all_books():
    query = books.select()
    return await database.fetch_all(query) # this function return a Dicctionary List, automaticaly retun a json 


@app.post("/books")
async def create_book(request: Request):
    data = await request.json()
    query = books.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}
