from flask import Flask, jsonify, request
from models import Meme, db, User, Image
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template, redirect, url_for, flash, request
from functools import wraps
from flask_login import login_required
from flask import flash
from flask_login import current_user
from helpers import token_required


site = Blueprint("site", __name__, template_folder="../site/site_templates")

@site.route ('/getimages', methods=['GET'])
@token_required
def getimages(current_user_token):
    images = Image.query.all()
    response = jsonify([image.serialize() for image in images])
    print (current_user)
    return response


@site.route('/addnewmeme', methods=['POST'])
@token_required
def addnewmeme(current_user_token):
    print(current_user)
    new_meme = Meme(
        meme_name =request.json['meme_name'],
        meme_caption =request.json['meme_caption'],
        img_id=request.json['img_id'],
    )
    db.session.add(new_meme)
    db.session.commit()

    return jsonify({ "message": "Meme added successfully" }), 200

@site.route('/deletememe', methods=['DELETE'])
@token_required
def deletememe(current_user_token):
    meme = Meme.query.filter_by(meme_id=request.json['meme_id']).first()
    if not meme:
        return jsonify({ "message": "No meme found!" }), 404
    db.session.delete(meme)
    db.session.commit()
    return jsonify({ "message": "Meme deleted successfully" }), 200

@site.route('/updatememe', methods=['PUT'])
@token_required
def updatememe(current_user_token):
    meme = Meme.query.filter_by(meme_id=request.json['meme_id']).first()
    if not meme:
        return jsonify({ "message": "No meme found!" }), 404
    meme.meme_name = request.json['meme_name']
    meme.meme_caption = request.json['meme_caption']
    meme.img_id = request.json['img_id']
    db.session.commit()
    return jsonify({ "message": "Meme updated successfully" }), 200


@site.route('/getmeme', methods=['GET'])
@token_required
def getmeme(current_user_token):
    memes = Meme.query.all()
    response = jsonify([meme.serialize() for meme in memes])
    return response



@site.route('/profile')
@login_required
def profile():
    user = current_user
    print(current_user.id)
    return render_template('profile.html', user=user)

