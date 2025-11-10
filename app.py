from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # Reads from .env file

app = Flask(__name__)

# Using SQLite for student simplicity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rockbands-mm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'SECRET'

db = SQLAlchemy(app)

# ==========================
# DATABASE MODELS
# ==========================


class Bands(db.Model):
    BandID = db.Column(db.Integer, primary_key=True)
    BandName = db.Column(db.String(80), nullable=False)
    FormedYear = db.Column(db.Integer)
    HomeLocation = db.Column(db.String(80))
    # Relationship: One band has many members + albums
    # members = db.relationship('Members', backref='band', lazy=True)
    memberships = db.relationship('Memberships', backref='band', lazy=True)
    collaborations = db.relationship('Collaborations', backref='band', lazy=True)


class Members(db.Model):
    MemberID = db.Column(db.Integer, primary_key=True)
    # BandID = db.Column(db.Integer, db.ForeignKey('bands.BandID'), nullable=False)
    MemberName = db.Column(db.String(80), nullable=False)
    MainPosition = db.Column(db.String(80))
    memberships = db.relationship('Memberships', backref='member', lazy=True)


class Memberships(db.Model):
    MembershipID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey(
        'bands.BandID'), nullable=False)
    MemberID = db.Column(db.Integer, db.ForeignKey(
        'members.MemberID'), nullable=False)
    StartYear = db.Column(db.Integer)
    EndYear = db.Column(db.Integer)  # NULL if still active
    Role = db.Column(db.Text)

class Collaborations(db.Model):
    CollaborationsID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey(
        'bands.BandID'), nullable=False)
    AlbumID = db.Column(db.Integer, db.ForeignKey(
        'albums.AlbumID'), nullable=False)
    CollabYear = db.Column(db.Integer)  


class Albums(db.Model):
    AlbumID = db.Column(db.Integer, primary_key=True)
    AlbumTitle = db.Column(db.String(80), nullable=False)
    ReleaseYear = db.Column(db.Integer)
    collaborations = db.relationship('Collaborations', backref='album', lazy=True)


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
    bands = Bands.query.all()  # Students see querying with relationships
    if request.method == 'POST':
        new_member = Members(
            MemberName=request.form['membername'],
            MainPosition=request.form['mainposition']
            # BandID=request.form['bandid']
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
            ReleaseYear=request.form['releaseyear'],
        )
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
    # Shows real database relationship querying
    band = Bands.query.get_or_404(id)
    return render_template('display_by_band.html', bands=[band])


@app.route('/memberships/add', methods=['GET', 'POST'])
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

@app.route('/collaborations/add', methods=['GET', 'POST'])
def add_collaboration():
    bands = Bands.query.all()
    albums = Albums.query.all()
    if request.method == 'POST':
        collaboration = Collaborations(
            BandID=request.form.get('bandid'),
            AlbumID=request.form.get('albumid'),
            CollabYear=request.form.get('collabyear') or None,
        )
        db.session.add(collaboration)
        db.session.commit()
        flash('Collaboration assigned', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('add_collaboration.html', bands=bands, albums=albums)



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
        flash('Membership updates', 'success')
        return redirect(url_for('view_by_band'))

    return render_template('add_membership.html', membership=membership, bands=bands, members=members)

@app.route('/collaborations/edit/<int:id>', methods=['GET', 'POST'])
def edit_collaborations(id):
    collaboration = Collaborations.query.get_or_404(id)
    bands = Bands.query.all()
    albums = Albums.query.all()
    if request.method == 'POST':
        collaboration.BandID = request.form.get('bandid')
        collaboration.AlbumID = request.form.get('albumid')
        collaboration.Collab = request.form.get('year')
        db.session.commit()
        flash('Collaboration updates', 'success')
        return redirect(url_for('view_by_band'))

    return render_template('add_collaboration.html', collaboration=collaboration, bands=bands, albums=albums)

@app.route('/memberships/delete/<int:id>')
def delete_membership(id):
    membership = Memberships.query.get_or_404(id)
    db.session.delete(membership)
    db.session.commit()
    flash('Membership removed', 'success')
    return redirect(url_for('view_by_band'))

@app.route('/collaborations/delete/<int:id>')
def delete_collaborations(id):
    collaboration = Collaborations.query.get_or_404(id)
    db.session.delete(collaboration)
    db.session.commit()
    flash('Collaboration removed', 'success')
    return redirect(url_for('view_by_band'))


# Create DB if not exists
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
