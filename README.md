# Udacity Fullstack Nanodegree P2 Tournament Results
---
### Description

This project implements a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament. It has two parts: defining the database schema (SQL table definitions) in tournament.sql, and writing code that will use it to track a Swiss tournament in tournament.py.

### How to Start

Test proper implementation by running some select tests against the DB:

```
    host$> git clone https://github.com/cg94301/fullstack-nanodegree-vm.git
    host$> cd fullstack-nanodegree-vm/vagrant
    host$> vagrant up
    host$> vagrant ssh
    vagrant@vagrant-ubuntu-trusty-32$> cd /vagrant/tournament
    vagrant@vagrant-ubuntu-trusty-32$> psql
    vagrant=> \i tournament.sql
    tournament=> \q
    vagrant@vagrant-ubuntu-trusty-32$> python tournament_test.py
```

Running the tests will result in the following output if successful:

```
    1. Old matches can be deleted.
    2. Player records can be deleted.
    3. After deleting, countPlayers() returns zero.
    4. After registering a player, countPlayers() returns 1.
    5. Players can be registered and deleted.
    6. Newly registered players appear in the standings with no matches.
    7. After a match, players have updated standings.
    8. After one match, players with one win are paired.
    Success!  All tests pass!

```
Exit the project:

```
    vagrant@vagrant-ubuntu-trusty-32$> exit
    host$> vagrant halt
```