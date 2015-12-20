#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    pg = connect()
    c = pg.cursor()
    c.execute("DELETE FROM matches")
    pg.commit()
    pg.close()

def deletePlayers():
    """Remove all the player records from the database."""
    pg = connect()
    c = pg.cursor()
    c.execute("DELETE FROM players")
    pg.commit()
    pg.close()

def countPlayers():
    """Returns the number of players currently registered."""
    pg = connect()
    c = pg.cursor()
    c.execute("SELECT count(id) FROM players")
    count = c.fetchall()
    pg.close()
    return count[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).

    Returns:
      The ID of the just created player. 
    """
    pg = connect()
    c = pg.cursor()
    # Use RETURNING id to access the id of this last insert
    c.execute("INSERT INTO players VALUES (%s,%s,%s) RETURNING id", (name,0,0))
    pg.commit()
    id = c.fetchall()
    pg.close()
    return id[0][0]

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
    pg = connect()
    c = pg.cursor()
    c.execute("SELECT players.id,players.name,players.wins,players.wins+players.losses as matches from players,scores where players.id = scores.id order by scores.score desc;")
    scores = c.fetchall()
    pg.close()
    return scores

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pg = connect()
    c = pg.cursor()
    c.execute("INSERT INTO matches VALUES (%s,%s)", (winner, loser))
    c.execute("UPDATE players SET wins = wins + 1 WHERE id = %s", (winner,))
    c.execute("UPDATE players SET losses = losses + 1 WHERE id = %s", (loser,))
    pg.commit()
    pg.close()

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
