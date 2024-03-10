import psycopg
import sys
from flask import Flask, jsonify, g 

lista_com_inic = [
        "CREATE SCHEMA IF NOT EXISTS books;",
        "DROP TABLE IF EXISTS books.Book;",
        "DROP TABLE IF EXISTS books.Writer;",
        """CREATE TABLE IF NOT EXISTS books.Writer (
            id SERIAL PRIMARY KEY, 
            name TEXT NOT NULL);""",
        """CREATE TABLE IF NOT EXISTS books.Book(
            id SERIAL PRIMARY KEY,
            author_id int,
            name TEXT NOT NULL,
            CONSTRAINT fk_writer
                FOREIGN KEY(author_id) 
                REFERENCES books.Writer(id)
            );""",
           "INSERT INTO books.Writer (name) Values ('Yates, John');",
           "INSERT INTO books.Writer (name) Values ('Egan, Greg');",
           "INSERT INTO books.Writer (name) Values ('Watts, Peter');",
           "with author_id as (select id from books.Writer where name = 'Watts, Peter') insert into books.Book (author_id, name) SELECT id as author_id, 'Blindsight' FROM author_id;",
           "with author_id as (select id from books.Writer where name = 'Watts, Peter') insert into books.Book (author_id, name) SELECT id as author_id, 'Echopraxia' FROM author_id;",
           "with author_id as (select id from books.Writer where name = 'Yates, John') insert into books.Book (author_id, name) SELECT id as author_id, 'The Mind Illuminated' FROM author_id;",
           "with author_id as (select id from books.Writer where name = 'Yates, John') insert into books.Book (author_id, name) SELECT id as author_id, 'Enlightenment' FROM author_id;",
        ]


if (len(sys.argv) > 1) and (sys.argv[1] == "init"):
    conexion = psycopg.connect(
        dbname="prueba",
        user="uno",
        password="8.B(P8pDQeMH!",
        host="localhost",
        port="5432"
    )
    cursor = conexion.cursor()
    for cmd in lista_com_inic:
        print(cmd)
        cursor.execute(cmd)
    conexion.commit()
    conexion.close()
    cursor.close()

app = Flask(__name__)

@app.before_request
def before_request():
    conexion = psycopg.connect(
        dbname="prueba",
        user="uno",
        password="8.B(P8pDQeMH!",
        host="localhost",
        port="5432"
    )
    g.con = conexion

@app.after_request
def after_request(response):
    if g.con is not None:
        print('Closing db connection!')
        g.con.close()
    return response

@app.route('/')
def get_authors():
    cursor = g.con.cursor()
    q_result = cursor.execute("SELECT * FROM books.Writer;").fetchall()
    print(type(q_result))
    cursor.close()
    return jsonify({'authors' : q_result})

@app.route('/old_writers/<a_id>')
def get_books_of_author(a_id):
    cursor = g.con.cursor()
    query = """WITH writer AS
    (SELECT id as a_id, name as author_name from books.Writer where id = """ + a_id + """ limit 1)
    SELECT a_id, author_name, id, name from writer LEFT JOIN books.Book ON author_id=a_id;
    """
    q_result = cursor.execute(query).fetchall()
    if not q_result:
        cursor.close()
        return jsonify({'id' : a_id, 'name' : 'None', "books": []})
    else:
        books = []
        for rec in q_result:
            books.append([rec[2], rec[3]])
        cursor.close()
        return jsonify({'id' : q_result[0][0], 'name' : q_result[0][1], 'books' : books})

@app.route('/writers/<a_id>')
def get_books_of_author_by_id(a_id):
    cursor = g.con.cursor()
    query = """WITH writer AS
    (SELECT id as a_id, name as author_name from books.Writer where id = """ + a_id + """)
    SELECT a_id as id, MIN(author_name) as name, JSONB_AGG(jsonb_build_object('id', books.Book.id, 'name', books.Book.name)) as books from writer LEFT JOIN books.Book ON author_id=a_id group by a_id;
    """
    q_result = cursor.execute(query).fetchall()
    if not q_result:
        cursor.close()
        return jsonify({'id' : a_id, 'name' : 'None', "books": []})
    else:
        cursor.close()
        return jsonify({'id' : a_id, 'name' : q_result[0][1], 'books' : q_result[0][2]})




if __name__ == '__main__':
    app.run(debug=True)
