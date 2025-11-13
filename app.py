from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # Reads from .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Using SQLite for student simplicity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rockbands-mm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'SECRET'

db = SQLAlchemy(app)

# ==========================
# DATABASE MODELS
# ==========================
class Albums(db.Model):
    AlbumID = db.Column(db.Integer, primary_key=True)
    BandID = db.Column(db.Integer, db.ForeignKey('bands.BandID'), nullable=False)
    AlbumTitle = db.Column(db.String(80), nullable=False)
    ReleaseYear = db.Column(db.Integer)
    collaborations = db.relationship('Collaborations', backref='album', lazy=True)

class Bands(db.Model):
    BandID = db.Column(db.Integer, primary_key=True)
    BandName = db.Column(db.String(80), nullable=False)
    FormedYear = db.Column(db.Integer)
    HomeLocation = db.Column(db.String(80))
    memberships = db.relationship('Memberships', backref='band', lazy=True)
    albums = db.relationship('Albums', backref='band', lazy=True)
    collaborations = db.relationship('Collaborations', backref='collaborating_band', lazy=True)
    
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

class Collaborations(db.Model):
    CollaborationID=db.Column(db.Integer, primary_key=True)
    AlbumID=db.Column(db.Integer, db.ForeignKey('albums.AlbumID'), nullable=False)
    BandID=db.Column(db.Integer, db.ForeignKey('bands.BandID'), nullable=False)
    Role=db.Column(db.String(80))
    


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
def add_member(): # Students see querying with relationships
    if request.method == 'POST':
        new_member = Members(
            MemberName=request.form['membername'],
            MainPosition=request.form['mainposition']
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_member.html')

@app.route('/albums/add', methods=['GET', 'POST'])
def add_album():
    bands = Bands.query.all()
    if request.method == 'POST':
        new_album = Albums(
            AlbumTitle=request.form['albumtitle'],
            ReleaseYear=request.form['releaseyear'],
            BandID=request.form['bandid']
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
        
        membership.StartYear = request.form.get('startyear') or None
        membership.EndYear = request.form.get('endyear') or None
        db.session.commit()
        flash('Membership updated', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('edit_membership.html', membership=membership, bands=bands, members=members)

@app.route('/memberships/delete/<int:id>')
def delete_membership(id):
    membership = Memberships.query.get_or_404(id)
    db.session.delete(membership)
    db.session.commit()
    flash('Membership removed', 'success')
    return redirect(url_for('view_by_band'))






@app.route('/bands/edit/<int:id>', methods=['GET', 'POST'])
def edit_band(id):
    band = Bands.query.get_or_404(id)
    if request.method == 'POST':
        band.BandName = request.form['bandname']
        band.FormedYear = request.form['formedyear']
        band.HomeLocation = request.form['homelocation']
        db.session.commit()
        flash('Band updated', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('edit_band.html', band=band)

@app.route('/bands/delete/<int:id>')
def delete_band(id):
    band = Bands.query.get_or_404(id)
    db.session.delete(band)
    db.session.commit()
    flash('Band deleted', 'success')
    return redirect(url_for('view_by_band'))

@app.route('/members/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Members.query.get_or_404(id)
    if request.method == 'POST':
        member.MemberName = request.form['membername']
        member.MainPosition = request.form['mainposition']
        db.session.commit()
        flash('Member updated', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('edit_member.html', member=member)

@app.route('/members/delete/<int:id>')
def delete_member(id):
    member = Members.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted', 'success')
    return redirect(url_for('view_by_band'))

@app.route('/albums/edit/<int:id>', methods=['GET', 'POST'])
def edit_album(id):
    album = Albums.query.get_or_404(id)
    bands = Bands.query.all()
    if request.method == 'POST':
        album.AlbumTitle = request.form['albumtitle']
        album.ReleaseYear = request.form['releaseyear']
        album.BandID = request.form['bandid']
        db.session.commit()
        flash('Album updated', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('edit_album.html', album=album, bands=bands)

@app.route('/albums/delete/<int:id>')
def delete_album(id):
    album = Albums.query.get_or_404(id)
    db.session.delete(album)
    db.session.commit()
    flash('Album deleted', 'success')
    return redirect(url_for('view_by_band'))





@app.route('/collaborations/add', methods=['GET', 'POST'])
def add_collaboration():
    albums=Albums.query.all()
    bands=Bands.query.all()
    if request.method =='POST':
        collaborations=Collaborations(
            AlbumID=request.form.get('albumid'), 
            BandID=request.form.get('bandid'),
            Role=request.form.get('role')
        )
        db.session.add(collaborations)
        db.session.commit()
        flash('Collaboration Linked', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('add_collab.html', albums=albums, bands=bands)

@app.route('/collaborations/edit/<int:id>', methods=['GET', 'POST'])
def edit_collaboration(id):
    collaboration = Collaborations.query.get_or_404(id)
    albums=Albums.query.all()
    bands=Bands.query.all()
    if request.method == 'POST':
        collaboration.AlbumID = request.form.get('albumid')
        collaboration.BandID = request.form.get('bandid')
        collaboration.Role = request.form.get('role')
        db.session.commit()
        flash('Collaboration has been updated', 'success')
        return redirect(url_for('view_by_band'))
    return render_template('edit_collaboration.html', collaborations=collaborations, albums=albums, bands=bands)

@app.route('/collaborations/delete/<int:id>')
def delete_collaboration(id):
    collaboration = Collaborations.query.get_or_404(id)
    db.session.delete(collaboration)
    db.session.commit()
    flash('Collaboration deleted', 'success')
    return redirect(url_for('view_by_band'))


# Create DB if not exists
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
