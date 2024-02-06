from flask import Flask, jsonify, request
from models import Meme, db, User, Image
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from functools import wraps
from helpers import verify_firebase_token
import firebase_admin
from firebase_admin import auth


site = Blueprint("site", __name__, template_folder="../site/site_templates")


@site.route('/addnewmeme', methods=['POST'])
@verify_firebase_token
def addnewmeme():
    print(request.json)
    new_meme = Meme(
        meme_caption =request.json['caption'],
        img_id=request.json['img_id'],
    )
    db.session.add(new_meme)
    db.session.commit()

    return jsonify({ "message": "Meme added successfully" }), 200

@site.route('/deletememe', methods=['DELETE'])
@verify_firebase_token
def deletememe():
    meme_id = request.args.get('meme_id')
    meme = Meme.query.filter_by(meme_id = meme_id).first()
    if not meme:
        return jsonify({ "message": "No meme found!" }), 404
    db.session.delete(meme)
    db.session.commit()
    return jsonify({ "message": "Meme deleted successfully" }), 200

@site.route('/updatememe', methods=['PUT'])
@verify_firebase_token
def updatememe():
    meme = Meme.query.filter_by(meme_id=request.json['meme_id']).first()
    if not meme:
        return jsonify({ "message": "No meme found!" }), 404
    meme.meme_caption = request.json['meme_caption']
    db.session.commit()
    meme = Meme.query.filter_by(meme_id=request.json['meme_id']).first()
    return jsonify( meme.serialize() ), 200

@site.route('/getmeme', methods=['GET'])
def getmeme():
    memes = Meme.query.all()
    response = jsonify([meme.serialize() for meme in memes])
    return response

@site.route('/getimage', methods=['POST'])
def getimage():
    img_id = request.json.get('img_id')
    image = Image.query.filter_by(id=img_id).first()
    print(image.img_url)

    if image is None:
        return jsonify({ "message": "No meme found!" }), 404

    return jsonify({ "img_url": image.img_url }), 200



