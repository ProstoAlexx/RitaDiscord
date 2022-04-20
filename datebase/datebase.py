import sqlite3
from sqlite3 import dbapi2

class datebase:
    
    user = "default"
    guild = "default"
    search1 = "default"
    search2 = "default"
    search3 = "default"
    search4 = "default"
    
    def start( self ):
        global sql, db
        
        db = sqlite3.connect( 'datebase/base.db' )
        sql = db.cursor()
        sql.execute( '''CREATE TABLE IF NOT EXIST database (
            guilt INT,
            user INT,
            warn INT
        )''' )
        db.commit()
        
    def warn( self ):
        sql.execute( f"SELECT guilt FROM datebase WHERE guilt = '{ self.guilt }'")
        if sql.fetchone() is None:
            sql.execute( f"INSERT INTO datebase VALUES (?,?,?,?)", ( self.guilt, self.user, 1 ) )
            db.commit()
        else:
            sql.execute( f"SELECT user FROM datebase WHERE guild = '{ self.guild }' AND user = '{self.user}'" )
            if sql.fetchone() is None:
                sql.execute( f"INSERT INTO datebase VALUES (?,?,?,?)", ( self.guild, self.user, 1 ) )
                db.commit
            else:
                for i in sql.execute( f"SELECT warn FROM datebase WHERE guild = '{ self.guild }' AND user = '{ self.user }'" ):
                    newWarn = i[0] + 1
                sql.execute( f"UPDATE datebase SET warn = '{ newWarn }' WHERE guild = '{ self.guild } AND user = '{ self.user }''" )
                db.commit()
                
        def search( self ):
            self.search1 = ""
            self.search2 = ""
            self.search3 = ""
            for i in sql.execute( "SELECT guild FROM datebase" ):
                self.search1 += f"\n{ i[0] }"
            for i in sql.execute( "SELECT user FROM datebase" ):
                self.search2 += f"\n{ i[0] }"
            for i in sql.execute( "SELECT warn FROM datebase" ):
                self.search3 += f"\n{ i[0] }"