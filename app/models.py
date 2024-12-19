from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class League(db.Model):
    __tablename__ = 'leagues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    tier = db.Column(db.String(50), nullable=False)

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'), nullable=False)
    budget = db.Column(db.Numeric(15, 2), nullable=False, default=0)
    league = db.relationship('League', backref=db.backref('teams', lazy=True))
    events = db.relationship('Event', back_populates='team', lazy='dynamic')
class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=False)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(2), nullable=False)
    height = db.Column(db.Numeric(5, 2), nullable=False)
    weight = db.Column(db.Numeric(5, 2), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    birth_date = db.Column(db.Date, nullable=False)
    market_value = db.Column(db.Numeric(15, 2), nullable=False, default=0)
    
    # Relation avec Team
    team = db.relationship('Team', backref=db.backref('players', lazy=True))
    
    # Relation avec Event
    events = db.relationship('Event', back_populates='player', lazy='dynamic')
    
    # Relation avec PlayerEvent (backref défini dans PlayerEvent)
    player_events = db.relationship('PlayerEvent', back_populates='player', lazy='dynamic')

class PlayerStat(db.Model):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    games_played = db.Column(db.Integer, nullable=False, default=0)
    ppg = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    apg = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    rpg = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    minutes_played = db.Column(db.Integer, nullable=False, default=0)
    fgm = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    fga = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    fg_pct = db.Column(db.Numeric(5, 3), nullable=False, default=0)
    threepm = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    threepa = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    three_pct = db.Column(db.Numeric(5, 3), nullable=False, default=0)
    ftm = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    fta = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    ft_pct = db.Column(db.Numeric(5, 3), nullable=False, default=0)
    steals = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    blocks = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    turnovers = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    player = db.relationship('Player', backref=db.backref('stats', lazy=True))
    season = db.relationship('Season', backref=db.backref('player_stats', lazy=True))

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    home_score = db.Column(db.Integer, nullable=False, default=0)
    away_score = db.Column(db.Integer, nullable=False, default=0)
    season = db.relationship('Season', backref=db.backref('games', lazy=True))
    home_team = db.relationship('Team', foreign_keys=[home_team_id])
    away_team = db.relationship('Team', foreign_keys=[away_team_id])

class GameStat(db.Model):
    __tablename__ = 'game_stats'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    rebounds = db.Column(db.Integer, nullable=False, default=0)
    assists = db.Column(db.Integer, nullable=False, default=0)
    minutes_played = db.Column(db.Integer, nullable=False, default=0)
    fgm = db.Column(db.Integer, nullable=False, default=0)
    fga = db.Column(db.Integer, nullable=False, default=0)
    threepm = db.Column(db.Integer, nullable=False, default=0)
    threepa = db.Column(db.Integer, nullable=False, default=0)
    ftm = db.Column(db.Integer, nullable=False, default=0)
    fta = db.Column(db.Integer, nullable=False, default=0)
    steals = db.Column(db.Integer, nullable=False, default=0)
    blocks = db.Column(db.Integer, nullable=False, default=0)
    turnovers = db.Column(db.Integer, nullable=False, default=0)
    game = db.relationship('Game', backref=db.backref('game_stats', lazy=True))
    player = db.relationship('Player', backref=db.backref('game_stats', lazy=True))

class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    team = db.relationship('Team', backref=db.backref('user_profiles', lazy=True))

class Transfer(db.Model):
    __tablename__ = 'transfers'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    from_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    to_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    transfer_fee = db.Column(db.Numeric(15, 2), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    player = db.relationship('Player', backref=db.backref('transfers', lazy=True))
    from_team = db.relationship('Team', foreign_keys=[from_team_id])
    to_team = db.relationship('Team', foreign_keys=[to_team_id])

class TeamSeason(db.Model):
    __tablename__ = 'team_season'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    budget_remaining = db.Column(db.Numeric(15, 2), default=0)
    team = db.relationship('Team', backref=db.backref('team_seasons', lazy=True))
    season = db.relationship('Season', backref=db.backref('team_seasons', lazy=True))

class PlayerEvent(db.Model):
    __tablename__ = 'player_events'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    event_type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    
    # Relation avec Player
    player = db.relationship('Player', backref=db.backref('events_log', lazy='dynamic'))
    
    # Relation avec Season
    season = db.relationship('Season', backref=db.backref('player_events', lazy='dynamic'))

class Finance(db.Model):
    __tablename__ = 'finances'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    revenue = db.Column(db.Numeric(15, 2), default=0)
    expenses = db.Column(db.Numeric(15, 2), default=0)

    team = db.relationship('Team', backref='finances')
    season = db.relationship('Season', backref='finances')

    def __repr__(self):
        return f"<Finance id={self.id}, team_id={self.team_id}, season_id={self.season_id}, revenue={self.revenue}, expenses={self.expenses}>"


class PlayerPosition(db.Model):
    __tablename__ = 'player_positions'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    position = db.Column(db.String(2), nullable=False)

    player = db.relationship('Player', backref='positions')

    def __repr__(self):
        return f"<PlayerPosition id={self.id}, player_id={self.player_id}, position={self.position}>"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    player = db.relationship('Player', back_populates='events')
    team = db.relationship('Team', back_populates='events')

class SeasonGoal(db.Model):
    __tablename__ = 'season_goals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    goal_text = db.Column(db.Text, nullable=False)
