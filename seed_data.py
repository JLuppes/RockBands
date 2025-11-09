from app import app, db, Bands, Members, Albums

def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        sleep_token = Bands(BandName='Sleep Token', FormedYear=2016, HomeLocation='London, UK')
        loathe = Bands(BandName='Loathe', FormedYear=2014, HomeLocation='Liverpool, UK')
        currents = Bands(BandName='Currents', FormedYear=2011, HomeLocation='Connecticut, USA')
        shadow_of_intent = Bands(BandName='Shadow of Intent', FormedYear=2013, HomeLocation='Connecticut, USA')
        fit_for_autopsy = Bands(BandName='Fit for an Autopsy', FormedYear=2008, HomeLocation='New Jersey, USA')
        end = Bands(BandName='End', FormedYear=2017, HomeLocation='Brooklyn, USA')
        better_lovers = Bands(BandName='Better Lovers', FormedYear=2023, HomeLocation='USA')
        
        db.session.add_all([sleep_token, loathe, currents, shadow_of_intent, fit_for_autopsy, end, better_lovers])
        db.session.commit()
        
        # Sleep Token members
        db.session.add(Members(BandID=sleep_token.BandID, MemberName='Vessel', MainPosition='Vocals'))
        db.session.add(Members(BandID=sleep_token.BandID, MemberName='II', MainPosition='Drums'))
        db.session.add(Members(BandID=sleep_token.BandID, MemberName='III', MainPosition='Bass'))
        db.session.add(Members(BandID=sleep_token.BandID, MemberName='IV', MainPosition='Guitar'))
        
        # Loathe members
        db.session.add(Members(BandID=loathe.BandID, MemberName='Kadeem France', MainPosition='Vocals'))
        db.session.add(Members(BandID=loathe.BandID, MemberName='Erik Bickerstaffe', MainPosition='Guitar/Vocals'))
        db.session.add(Members(BandID=loathe.BandID, MemberName='Connor Sweeney', MainPosition='Guitar'))
        db.session.add(Members(BandID=loathe.BandID, MemberName='Feisal El-Khazragi', MainPosition='Bass'))
        db.session.add(Members(BandID=loathe.BandID, MemberName='Sean Radcliffe', MainPosition='Drums'))
        
        # Currents members
        db.session.add(Members(BandID=currents.BandID, MemberName='Brian Wille', MainPosition='Vocals'))
        db.session.add(Members(BandID=currents.BandID, MemberName='Chris Wiseman', MainPosition='Guitar'))
        db.session.add(Members(BandID=currents.BandID, MemberName='Ryan Castaldi', MainPosition='Bass'))
        db.session.add(Members(BandID=currents.BandID, MemberName='Matt Young', MainPosition='Drums'))
        
        # Shadow of Intent
        db.session.add(Members(BandID=shadow_of_intent.BandID, MemberName='Ben Duerr', MainPosition='Vocals'))
        db.session.add(Members(BandID=shadow_of_intent.BandID, MemberName='Chris Wiseman', MainPosition='Guitar'))
        db.session.add(Members(BandID=shadow_of_intent.BandID, MemberName='Andrew Monias', MainPosition='Bass'))
        
        # Fit for an Autopsy
        db.session.add(Members(BandID=fit_for_autopsy.BandID, MemberName='Joe Badolato', MainPosition='Vocals'))
        db.session.add(Members(BandID=fit_for_autopsy.BandID, MemberName='Will Putney', MainPosition='Guitar'))
        db.session.add(Members(BandID=fit_for_autopsy.BandID, MemberName='Pat Sheridan', MainPosition='Guitar'))
        db.session.add(Members(BandID=fit_for_autopsy.BandID, MemberName='Peter Spinazola', MainPosition='Bass'))
        db.session.add(Members(BandID=fit_for_autopsy.BandID, MemberName='Josean Orta', MainPosition='Drums'))
        
        # End
        db.session.add(Members(BandID=end.BandID, MemberName='Brendan Murphy', MainPosition='Vocals'))
        db.session.add(Members(BandID=end.BandID, MemberName='Will Putney', MainPosition='Guitar'))
        db.session.add(Members(BandID=end.BandID, MemberName='Gregory Thomas', MainPosition='Drums'))
        
        # Better Lovers
        db.session.add(Members(BandID=better_lovers.BandID, MemberName='Greg Puciato', MainPosition='Vocals'))
        db.session.add(Members(BandID=better_lovers.BandID, MemberName='Jordan Buckley', MainPosition='Guitar'))
        db.session.add(Members(BandID=better_lovers.BandID, MemberName='Clayton Stevens', MainPosition='Bass'))
        db.session.add(Members(BandID=better_lovers.BandID, MemberName='Stephen Micciche', MainPosition='Drums'))
        
        db.session.commit()
        
        # Sleep Token albums
        st_album1 = Albums(AlbumTitle='Sundowning', ReleaseYear=2019)
        st_album1.bands.append(sleep_token)
        db.session.add(st_album1)
        
        st_album2 = Albums(AlbumTitle='This Place Will Become Your Tomb', ReleaseYear=2021)
        st_album2.bands.append(sleep_token)
        db.session.add(st_album2)
        
        st_album3 = Albums(AlbumTitle='Take Me Back to Eden', ReleaseYear=2023)
        st_album3.bands.append(sleep_token)
        db.session.add(st_album3)
        
        # Loathe albums
        loathe_album1 = Albums(AlbumTitle='I Let It In and It Took Everything', ReleaseYear=2020)
        loathe_album1.bands.append(loathe)
        db.session.add(loathe_album1)
        
        loathe_album2 = Albums(AlbumTitle='The Cold Sun', ReleaseYear=2017)
        loathe_album2.bands.append(loathe)
        db.session.add(loathe_album2)
        
        # Currents albums
        currents_album1 = Albums(AlbumTitle='The Way It Ends', ReleaseYear=2020)
        currents_album1.bands.append(currents)
        db.session.add(currents_album1)
        
        currents_album2 = Albums(AlbumTitle='The Place I Feel Safest', ReleaseYear=2017)
        currents_album2.bands.append(currents)
        db.session.add(currents_album2)
        
        # Shadow of Intent
        soi_album1 = Albums(AlbumTitle='Melancholy', ReleaseYear=2019)
        soi_album1.bands.append(shadow_of_intent)
        db.session.add(soi_album1)
        
        soi_album2 = Albums(AlbumTitle='Elegy', ReleaseYear=2022)
        soi_album2.bands.append(shadow_of_intent)
        db.session.add(soi_album2)
        
        # Fit for an Autopsy
        ffaa_album1 = Albums(AlbumTitle='The Sea of Tragic Beasts', ReleaseYear=2019)
        ffaa_album1.bands.append(fit_for_autopsy)
        db.session.add(ffaa_album1)
        
        ffaa_album2 = Albums(AlbumTitle='Oh What the Future Holds', ReleaseYear=2022)
        ffaa_album2.bands.append(fit_for_autopsy)
        db.session.add(ffaa_album2)
        
        # End
        end_album = Albums(AlbumTitle='Splinters from an Ever-Changing Face', ReleaseYear=2020)
        end_album.bands.append(end)
        db.session.add(end_album)
        
        # Better Lovers
        bl_album = Albums(AlbumTitle='God Made Me An Animal', ReleaseYear=2024)
        bl_album.bands.append(better_lovers)
        db.session.add(bl_album)
        
        # Collaboration albums
        collab1 = Albums(AlbumTitle='Cross-Genre Collaboration', ReleaseYear=2024)
        collab1.bands.append(sleep_token)
        collab1.bands.append(loathe)
        db.session.add(collab1)
        
        collab2 = Albums(AlbumTitle='Metalcore United', ReleaseYear=2023)
        collab2.bands.append(currents)
        collab2.bands.append(shadow_of_intent)
        collab2.bands.append(fit_for_autopsy)
        db.session.add(collab2)
        
        db.session.commit()
        
        print("Database seeded successfully!")
        print(f"Added {Bands.query.count()} bands")
        print(f"Added {Members.query.count()} members")
        print(f"Added {Albums.query.count()} albums")

if __name__ == '__main__':
    seed_database()
