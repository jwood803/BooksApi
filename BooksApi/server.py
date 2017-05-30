from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('test.db', check_same_thread=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        with conn:
            booksDb = conn.cursor()
            booksDb.execute('''select * from Books''')
            books = booksDb.fetchall()

        book_list = []
        for book in books:
            book_dict = {
                "id": book[0],
                "title": book[1],
                "author": book[2]
            }

            book_list.append(book_dict)

        return jsonify(books=book_list)
    elif request.method == 'POST':
        values = (request.form['title'], request.form['author'])

        with conn:
            booksDb = conn.cursor()
            booksDb.execute('''insert into books(Title, Author) values (?, ?)''', values)

        return jsonify(True)

@app.route('/book/<id>', methods=['GET'])
def get_book_by_id(id):
    if request.method == 'GET':
        with conn:
            booksDb = conn.cursor()
            booksDb.execute('''select * from Books where Id = ?''', (id))

            book = booksDb.fetchone()

            book_dict = {
                "id": book[0],
                "title": book[1],
                "author": book[2]
            }

        return jsonify(book=book_dict)

if __name__ == '__main__':
    app.run(debug=True)