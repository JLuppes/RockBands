from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # Reads from .env file

app = Flask(__name__)

# Using SQLite for student simplicity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rockbands_manytomany.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# DATABASE MODELS
# ==========================

# Association table for many-to-many
band_album = db.Table('band_album',
    db.Column('BandID', db.Integer, db.ForeignKey('bands.BandID'), primary_key=True),
    db.Column('AlbumID', db.Integer, db.ForeignKey('albums.AlbumID'), primary_key=True)
)

class Bands(db.Model):
    BandID = db.Column(db.Integer, primary_key=True)
    BandName = db.Column(db.String(80), nullable=False)
    FormedYear = db.Column(db.Integer)
    HomeLocation = db.Column(db.String(80))
    members = db.relationship('Members', backref='band', lazy=True)
    albums = db.relationship('Albums', secondary=band_album, backref=db.backref('bands', lazy=True), lazy=True)

class Members(db.Model):
    MemberID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey('bands.BandID'), nullable=False)
    MemberName = db.Column(db.String(80), nullable=False)
    MainPosition = db.Column(db.String(80))

class Albums(db.Model):
    AlbumID = db.Column(db.Integer, primary_key=True)
    AlbumTitle = db.Column(db.String(80), nullable=False)
    ReleaseYear = db.Column(db.Integer)

# ==========================
# ROUTES
# ==========================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bands/add', methods=['GET', 'POST'])
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

@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    bands = Bands.query.all()
    if request.method == 'POST':
        new_member = Members(
            MemberName=request.form['membername'],
            MainPosition=request.form['mainposition'],
            BandID=request.form['bandid']
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_member.html', bands=bands)

@app.route('/albums/add', methods=['GET', 'POST'])
def add_album():
    bands = Bands.query.all()
    if request.method == 'POST':
        new_album = Albums(
            AlbumTitle=request.form['albumtitle'],
            ReleaseYear=request.form['releaseyear']
        )
        selected_band_ids = request.form.getlist('bandids')
        for band_id in selected_band_ids:
            band = Bands.query.get(band_id)
            if band:
                new_album.bands.append(band)
        
        db.session.add(new_album)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_album.html', bands=bands)

@app.route('/bands/view')
def view_by_band():
    bands = Bands.query.all()
    return render_template('display_by_band.html', bands=bands)

@app.route('/bands/view/<int:id>')
def view_band(id):
    band = Bands.query.get_or_404(id)
    return render_template('display_by_band.html', bands=[band])

@app.route('/albums/view')
def view_albums():
    albums = Albums.query.all()
    return render_template('display_albums.html', albums=albums)

@app.route('/albums/view/<int:id>')
def view_album(id):
    album = Albums.query.get_or_404(id)
    return render_template('display_albums.html', albums=[album])

@app.route('/members/view')
def view_members():
    members = Members.query.all()
    return render_template('display_members.html', members=members)

@app.route('/members/view/<int:id>')
def view_member(id):
    member = Members.query.get_or_404(id)
    return render_template('display_members.html', members=[member])

@app.route('/bands/search')
def search_bands():
    query = request.args.get('q', '')
    if query:
        bands = Bands.query.filter(Bands.BandName.ilike(f'%{query}%')).all()
    else:
        bands = Bands.query.all()
    return render_template('display_by_band.html', bands=bands, search_query=query)

# Create DB if not exists
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
