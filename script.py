from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy 



app = Flask(__name__) 
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False;
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:123456@localhost/myfirstDB'
app.debug = True
db = SQLAlchemy(app)

class books(db.Model):
    __tablename__ = 'books_1'
    bookTitle = db.Column(db.String(100),primary_key = True)
    bookAuthor = db.Column(db.String(100), nullable=False)

    def __init__(self,bookTitle,bookAuthor):
        self.bookTitle = bookTitle
        self.bookAuthor = bookAuthor

# for retreving the data
@app.route('/book', methods = ['GET'])
def gbooks():
    allbooks = books.query.all()
    output = []
    for book in allbooks:
        current = {}
        current['bookTitle'] = book.bookTitle
        current['bookAuthor'] = book.bookAuthor
        output.append(current)
    return jsonify(output)


#for posting new data
@app.route('/book',methods=['POST'])
def pbooks():
    bookTitle = request.form["bookTitle"]
    bookAuthor = request.form["bookAuthor"]
    entry = books(bookTitle,bookAuthor)
    db.session.add(entry)
    db.session.commit()
    return "posted sussessfully"



#for deleting the particular book
@app.route('/book/<bookTitle>', methods=['DELETE'])
def dbooks(bookTitle):
   book = books.query.get(bookTitle)
   db.session.delete(book)
   db.session.commit()
   return "deleted successfully"


#for updating
@app.route('/book/<string:bookTitle>', methods=['PUT'])
def ubooks(bookTitle):
    bookData = request.get_json()
    currbook = bookData['bookTitle']
    book = books.query.filter_by(bookTitle = currbook)
    db.session.commit()
    return jsonify(bookData)




if __name__ == '__main__':
    app.run()