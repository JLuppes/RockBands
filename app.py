import os
import random
import time
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import sys


# ==========================
# INIT
# ==========================
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rockband.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# DATABASE MODELS
# ==========================
class Bands(db.Model):
    BandID = db.Column(db.Integer, primary_key=True)
    BandName = db.Column(db.String(80), nullable=False)
    FormedYear = db.Column(db.Integer)
    HomeLocation = db.Column(db.String(80))
    memberships = db.relationship('Memberships', backref='band', lazy=True)
    albums = db.relationship('Albums', secondary='band_albums', back_populates='bands')

class Albums(db.Model):
    AlbumID = db.Column(db.Integer, primary_key=True)
    AlbumTitle = db.Column(db.String(80), nullable=False)
    ReleaseYear = db.Column(db.Integer)
    bands = db.relationship('Bands', secondary='band_albums', back_populates='albums')

class Members(db.Model):
    MemberID = db.Column(db.Integer, primary_key=True)
    MemberName = db.Column(db.String(80), nullable=False)
    MainPosition = db.Column(db.String(80))
    memberships = db.relationship('Memberships', backref='member', lazy=True)

class Memberships(db.Model):
    MembershipID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey('bands.BandID'), nullable=False)
    MemberID = db.Column(db.Integer, db.ForeignKey('members.MemberID'), nullable=False)
    StartYear = db.Column(db.Integer)
    EndYear = db.Column(db.Integer)
    Role = db.Column(db.Text)

class BandAlbums(db.Model):
    __tablename__ = 'band_albums'
    BandAlbumID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey('bands.BandID'), nullable=False)
    AlbumID = db.Column(db.Integer, db.ForeignKey('albums.AlbumID'), nullable=False)


# ==========================
# ROUTES - HOME
# ==========================
@app.route('/')
def index():
    return render_template('index.html')


# ==========================
# ROUTES - BANDS
# ==========================Arrrr
@app.route('/bands/add', methods=['GET', 'POST'])#+
def add_band():
    if request.method == 'POST':
        new_band = Bands(
            BandName=request.form['bandname'],
            FormedYear=request.form['formedyear'],
            HomeLocation=request.form['homelocation']
        )
        db.session.add(new_band)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_band.html')


@app.route('/bands/view')
def view_by_band():
    bands = Bands.query.all()
    return render_template('display_by_band.html', bands=bands)


@app.route('/bands/view/<int:id>')
def view_band(id):
    band = Bands.query.get_or_404(id)
    return render_template('display_by_band.html', bands=[band])


# ==========================
# ROUTES - MEMBERS
# ==========================
@app.route('/members/add', methods=['GET', 'POST']) #+
def add_member():
    bands = Bands.query.all()
    if request.method == 'POST':
        new_member = Members(
            MemberName=request.form['membername'],
            MainPosition=request.form['mainposition']
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_member.html', bands=bands)


# ==========================
# ROUTES - ALBUMS
# ==========================
@app.route('/albums/add', methods=['GET', 'POST'])#+
def add_album():
    bands = Bands.query.all()
    if request.method == 'POST':
        new_album = Albums(
            AlbumTitle=request.form['albumtitle'],
            ReleaseYear=request.form['releaseyear']
        )
        band_ids = request.form.getlist('bandids')
        for band_id in band_ids:
            band = Bands.query.get(band_id)
            if band:
                new_album.bands.append(band)
        db.session.add(new_album)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_album.html', bands=bands)


# ==========================
# ROUTES - MEMBERSHIPS
# ==========================
@app.route('/memberships/add', methods=['GET', 'POST'])#+
def add_membership():
    bands = Bands.query.all()
    members = Members.query.all()
    if request.method == 'POST':
        membership = Memberships(
            BandID=request.form.get('bandid'),
            MemberID=request.form.get('memberid'),
            Role=request.form.get('role'),
            StartYear=request.form.get('startyear') or None,
            EndYear=request.form.get('endyear') or None
        )
        db.session.add(membership)
        db.session.commit()
        flash('Membership assigned', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('add_membership.html', bands=bands, members=members)


@app.route('/memberships/edit/<int:id>', methods=['GET', 'POST'])
def edit_membership(id):
    membership = Memberships.query.get_or_404(id)
    bands = Bands.query.all()
    members = Members.query.all()
    if request.method == 'POST':
        membership.BandID = request.form.get('bandid')
        membership.MemberID = request.form.get('memberid')
        membership.Role = request.form.get('role')
        membership.StartYear = request.form.get('startyear') or None
        membership.EndYear = request.form.get('endyear') or None
        db.session.commit()
        flash('Membership updated', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('add_membership.html', membership=membership, bands=bands, members=members)


@app.route('/memberships/delete/<int:id>')
def delete_membership(id):
    membership = Memberships.query.get_or_404(id)
    db.session.delete(membership)
    db.session.commit()
    flash('Membership removed', 'success')
    return redirect(url_for('view_by_band'))


# ==========================
# THE DB
# ==========================wtf
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
