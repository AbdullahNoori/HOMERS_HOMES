from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')

client = MongoClient(host=f'{host}?retryWrites=false')
db = client.Store
homes = db.homes
    
app = Flask(__name__)
@app.route("/")
def index():
    all_homes = homes.find()
    print(all_homes)
    return render_template('home.html', homes=all_homes)
    # return render_template('home.html', homes=homes.find())

@app.route("/homes/new")
def home_new():
    # create new homes to sell
    return render_template("home_new.html")


@app.route('/homes', methods=['POST'])
def homes_upload():
    # upload new home
    home = {
        "title": request.form.get("title"),
        "image": request.form.get("image"),
        "price": request.form.get("price"),
    }
    home_id = homes.insert_one(home).inserted_id
    return redirect(url_for("home_show", home_id=home_id))

@app.route("/homes/<home_id>")
def home_show(home_id):
    # show home information
    home = homes.find_one({"_id": ObjectId(home_id)})
    return render_template("home_show.html", home=home)

@app.route("/homes/<home_id>/edit")
def home_edit(home_id):
    # show edit form
    home = homes.find_one({"_id" : ObjectId(home_id)})
    return render_template("home_edit.html", home=home)

@app.route("/homes/<home_id>", methods=["POST"])
def home_update(home_id):
    updated_home = {
        "title": request.form.get("title"),
        "image": request.form.get("image"),
        "price": request.form.get("price"),
    }
    homes.update_one({"_id": ObjectId(home_id)},{ "$set": updated_home})
    return redirect(url_for("home_show", home_id=home_id))

@app.route("/home/<home_id>/delete", methods=["POST"])
def home_delete(home_id):
    homes.delete_one({"_id": ObjectId(home_id)})
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))