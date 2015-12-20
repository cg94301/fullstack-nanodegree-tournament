-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

-- create table to keep track of register players and their scores
CREATE TABLE players (
       name text,
       id serial primary key
);

-- create table to track match outcomes
-- add foreign key to make sure only valid IDs are inserted
CREATE TABLE matches (
       winner integer REFERENCES players(id),
       loser integer REFERENCES players(id),
       match serial primary key
);

-- create view of win and loss counts to ease ranking
-- use left join to make sure that players with no match show up too
CREATE VIEW wincount AS SELECT id,count(winner) AS wcount FROM players LEFT JOIN matches ON id = winner GROUP BY players.id;
CREATE VIEW losscount AS SELECT id,count(loser) AS lcount FROM players LEFT JOIN matches ON id = loser GROUP BY players.id;
