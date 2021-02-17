from bottle import run, view, static_file, get, post, request, response
import sqlite3
import uuid
import os


##############################
@get("/app.css")
def do():
    return static_file("app.css", root="css")

##############################


@get("/logo.png")
def do():
    return static_file("logo.png", root="images")

##############################


@get("/")
@view("index")
def do():
    db = sqlite3.connect("data/database.db")
    items = db.execute(
        "SELECT * FROM items ORDER BY RANDOM() LIMIT 21").fetchall()
    db.close()
    return dict(items=items)

##############################


@get("/items/<item_id>")
@view("item")
def do(item_id):
    db = sqlite3.connect("./data/database.db")
    item = db.execute("SELECT * FROM items WHERE item_id = ?",
                      (item_id,)).fetchone()
    print(item)
    db.close()
    return dict(item=item)

##############################


@get("/upload")
@view("upload")
def do():
    return

##############################


@post("/upload")
def do():
    # ALWAYS Validate before doing anything else
    if request.files.get("my_file") is None:
        response.status = 400  # request is incorrect
        return

    the_file = request.files.get("my_file")
    the_file_name, the_file_extension = os.path.splitext(the_file.filename)
    print(f"the_file_name: {the_file_name}")
    print(f"the_file_extension: {the_file_extension}")
    # print(dir(the_file))
    the_file_name = str(uuid.uuid4()).replace("-", "")
    the_file.save(f"./files/{the_file_name}{the_file_extension}")  # F string
    return "file saved"


##############################
run(host="127.0.0.1", port=8080, debug=True, reloader=True, server="paste")
