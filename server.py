from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('test.db', check_same_thread=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        with conn:
            books_db = conn.cursor()
            books_db.execute('''select * from Books''')
            books = books_db.fetchall()

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
            books_db = conn.cursor()
            books_db.execute('''insert into Books(Title, Author) values (?, ?)''', values)

        return jsonify(True)


@app.route('/book/<book_id>', methods=['GET'])
def get_book_by_id(book_id):
    if request.method == 'GET':
        with conn:
            books_db = conn.cursor()
            books_db.execute('''select * from Books where Id = ?''', book_id)

            book = books_db.fetchone()

            book_dict = {
                "id": book[0],
                "title": book[1],
                "author": book[2]
            }

        return jsonify(book=book_dict)

if __name__ == '__main__':
    app.run(debug=True)
