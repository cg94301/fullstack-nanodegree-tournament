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
       wins integer,
       losses integer,
       id serial primary key
);

-- create table to track match outcomes
CREATE TABLE matches (
       winner integer,
       loser integer,
       match serial primary key
);

-- create a view to ease ranking
CREATE VIEW scores AS SELECT id,wins AS score from players;
