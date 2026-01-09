from flask import Flask, render_template, request, jsonify
from db import setup_db, insert_book, get_all_books, delete_book, update_book

from scrapers.bkm import bkm_scraper
from scrapers.dr import scrape_dr
from scrapers.kitapyurdu import scrape_kitapyurdu

app = Flask(__name__)
setup_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query")

    results = []

    # 1) BKM
    try:
        bkm = bkm_scraper(query)
        if bkm:
            results.append(bkm)
    except:
        pass

    # 2) DR
    try:
        dr = scrape_dr(query)
        if dr:
            results.append(dr)
    except:
        pass

    # 3) Kitapyurdu
    try:
        ky = scrape_kitapyurdu(query)
        if ky:
            results.append(ky)
    except:
        pass

    return jsonify(results)


@app.route("/add", methods=["POST"])
def add_book():
    book = request.json
    insert_book(book)
    return jsonify({"status": "ok"})


@app.route("/books")
def books():
    return jsonify(get_all_books())


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    delete_book(id)
    return jsonify({"status": "ok"})


@app.route("/update/<int:id>", methods=["PUT"])
def update(id):
    new_price = request.json.get("price")
    update_book(id, new_price)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
