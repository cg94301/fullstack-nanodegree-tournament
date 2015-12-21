#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

class DB:
    def __init__(self, db_con_str="dbname=tournament"):
        """
        Creates a database connection with the connection string provided
        :param str db_con_str: Contains the database connection string, with a default value when no argument is passed to the parameter
        """
        self.conn = psycopg2.connect(db_con_str)

    def cursor(self):
        """
        Returns the current cursor of the database
        """
        return self.conn.cursor()

    def execute(self, sql_query_string, sql_sub, and_close=False):
        """
        Executes SQL queries
        :param str sql_query_string: Contain the query string to be executed
        :param tuple sql_sub: Contains any string subsitutions
        :param bool and_close: If true, closes the database connection after executing and commiting the SQL Query
        """
        cursor = self.cursor()
        cursor.execute(sql_query_string, sql_sub)
        if and_close:
            self.conn.commit()
            self.close()
        return (self.conn, cursor if not and_close else None)

    def close(self):
        """
        Closes the current database connection
        """
        return self.conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    DB().execute("DELETE FROM matches", None, True)

def deletePlayers():
    """Remove all the player records from the database."""
    DB().execute("DELETE FROM players", None, True)

def countPlayers():
    """Returns the number of players currently registered."""
    (db,c) = DB().execute("SELECT count(*) FROM players", None)
    cursor = c.fetchone()
    db.close()
    return cursor[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).

    Returns:
      The ID of the just created player.
    """
    (db,c) = DB().execute("INSERT INTO players VALUES (%s) RETURNING id", (name,))
    db.commit()
    id = c.fetchone()
    db.close()
    return id[0]

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    (db,c) = DB().execute("SELECT players.id,name,wcount,wcount+lcount from players,wincount,losscount where players.id = wincount.id and players.id = losscount.id order by wcount desc;", None)
    scores = c.fetchall()
    db.close()
    return scores

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB().execute("INSERT INTO matches VALUES (%s,%s)", (winner, loser), True)

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    # extract id and name from standings
    idnames = [ (x[0],x[1]) for x in standings]
    # zip into pairs
    pairs = zip(idnames[::2] , idnames[1::2])
    # combine tuple of tuples into flat tuple
    pairings = [ x[0] + x[1] for x in pairs]
    return pairings
