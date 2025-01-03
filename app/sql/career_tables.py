def get_drop_tables_sql(username):
    """Retourne le SQL pour supprimer les tables existantes."""
    prefix = f"career_{username}_"
    return f"""
    DROP TABLE IF EXISTS {prefix}game_stats;
    DROP TABLE IF EXISTS {prefix}games;
    DROP TABLE IF EXISTS {prefix}player_stats;
    DROP TABLE IF EXISTS {prefix}player_positions;
    DROP TABLE IF EXISTS {prefix}transfers;
    DROP TABLE IF EXISTS {prefix}player_events;
    DROP TABLE IF EXISTS {prefix}events;
    DROP TABLE IF EXISTS {prefix}players;
    DROP TABLE IF EXISTS {prefix}team_season;
    DROP TABLE IF EXISTS {prefix}finances;
    DROP TABLE IF EXISTS {prefix}teams;
    DROP TABLE IF EXISTS {prefix}leagues;
    DROP TABLE IF EXISTS {prefix}seasons;
    """

def get_create_tables_sql(username):
    """Retourne le SQL pour créer les nouvelles tables."""
    prefix = f"career_{username}_"
    return f"""
    -- Leagues
    CREATE TABLE {prefix}leagues (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        tier VARCHAR(50) NOT NULL
    );

    -- Teams
    CREATE TABLE {prefix}teams (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        league_id INTEGER REFERENCES {prefix}leagues(id),
        budget NUMERIC(15, 2) NOT NULL DEFAULT 0,
        logo TEXT
    );

    -- Seasons
    CREATE TABLE {prefix}seasons (
        id SERIAL PRIMARY KEY,
        start_year INTEGER NOT NULL,
        end_year INTEGER NOT NULL
    );

    -- Players
    CREATE TABLE {prefix}players (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        position VARCHAR(2) NOT NULL,
        height NUMERIC(5, 2) NOT NULL,
        weight NUMERIC(5, 2) NOT NULL,
        team_id INTEGER REFERENCES {prefix}teams(id),
        birth_date DATE NOT NULL,
        market_value NUMERIC(15, 2) NOT NULL DEFAULT 0
    );

    -- Player Stats
    CREATE TABLE {prefix}player_stats (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES {prefix}players(id),
        season_id INTEGER REFERENCES {prefix}seasons(id),
        games_played INTEGER NOT NULL DEFAULT 0,
        ppg NUMERIC(5, 2) NOT NULL DEFAULT 0,
        apg NUMERIC(5, 2) NOT NULL DEFAULT 0,
        rpg NUMERIC(5, 2) NOT NULL DEFAULT 0,
        minutes_played INTEGER NOT NULL DEFAULT 0,
        fgm NUMERIC(5, 2) NOT NULL DEFAULT 0,
        fga NUMERIC(5, 2) NOT NULL DEFAULT 0,
        fg_pct NUMERIC(5, 3) NOT NULL DEFAULT 0,
        threepm NUMERIC(5, 2) NOT NULL DEFAULT 0,
        threepa NUMERIC(5, 2) NOT NULL DEFAULT 0,
        three_pct NUMERIC(5, 3) NOT NULL DEFAULT 0,
        ftm NUMERIC(5, 2) NOT NULL DEFAULT 0,
        fta NUMERIC(5, 2) NOT NULL DEFAULT 0,
        ft_pct NUMERIC(5, 3) NOT NULL DEFAULT 0,
        steals NUMERIC(5, 2) NOT NULL DEFAULT 0,
        blocks NUMERIC(5, 2) NOT NULL DEFAULT 0,
        turnovers NUMERIC(5, 2) NOT NULL DEFAULT 0
    );

    -- Games
    CREATE TABLE {prefix}games (
        id SERIAL PRIMARY KEY,
        season_id INTEGER REFERENCES {prefix}seasons(id),
        home_team_id INTEGER REFERENCES {prefix}teams(id),
        away_team_id INTEGER REFERENCES {prefix}teams(id),
        date TIMESTAMP NOT NULL,
        home_score INTEGER NOT NULL DEFAULT 0,
        away_score INTEGER NOT NULL DEFAULT 0
    );

    -- Game Stats
    CREATE TABLE {prefix}game_stats (
        id SERIAL PRIMARY KEY,
        game_id INTEGER REFERENCES {prefix}games(id),
        player_id INTEGER REFERENCES {prefix}players(id),
        points INTEGER NOT NULL DEFAULT 0,
        rebounds INTEGER NOT NULL DEFAULT 0,
        assists INTEGER NOT NULL DEFAULT 0,
        minutes_played INTEGER NOT NULL DEFAULT 0,
        fgm INTEGER NOT NULL DEFAULT 0,
        fga INTEGER NOT NULL DEFAULT 0,
        threepm INTEGER NOT NULL DEFAULT 0,
        threepa INTEGER NOT NULL DEFAULT 0,
        ftm INTEGER NOT NULL DEFAULT 0,
        fta INTEGER NOT NULL DEFAULT 0,
        steals INTEGER NOT NULL DEFAULT 0,
        blocks INTEGER NOT NULL DEFAULT 0,
        turnovers INTEGER NOT NULL DEFAULT 0
    );

    -- Transfers
    CREATE TABLE {prefix}transfers (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES {prefix}players(id),
        from_team_id INTEGER REFERENCES {prefix}teams(id),
        to_team_id INTEGER REFERENCES {prefix}teams(id),
        transfer_fee NUMERIC(15, 2) NOT NULL,
        date TIMESTAMP NOT NULL
    );

    -- Team Season
    CREATE TABLE {prefix}team_season (
        id SERIAL PRIMARY KEY,
        team_id INTEGER REFERENCES {prefix}teams(id),
        season_id INTEGER REFERENCES {prefix}seasons(id),
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        budget_remaining NUMERIC(15, 2) DEFAULT 0
    );

    -- Events
    CREATE TABLE {prefix}events (
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL,
        date TIMESTAMP NOT NULL,
        type VARCHAR(50) NOT NULL,
        player_id INTEGER REFERENCES {prefix}players(id),
        team_id INTEGER REFERENCES {prefix}teams(id),
        duration_days INTEGER,
        resolved BOOLEAN DEFAULT FALSE
    );

    -- Player Events
    CREATE TABLE {prefix}player_events (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES {prefix}players(id),
        season_id INTEGER REFERENCES {prefix}seasons(id),
        event_type VARCHAR(255) NOT NULL,
        description TEXT,
        date TIMESTAMP NOT NULL
    );

    -- Finances
    CREATE TABLE {prefix}finances (
        id SERIAL PRIMARY KEY,
        team_id INTEGER REFERENCES {prefix}teams(id),
        season_id INTEGER REFERENCES {prefix}seasons(id),
        revenue NUMERIC(15, 2) DEFAULT 0,
        expenses NUMERIC(15, 2) DEFAULT 0
    );

    -- Player Positions
    CREATE TABLE {prefix}player_positions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES {prefix}players(id),
        position VARCHAR(2) NOT NULL
    );

    -- Season Goals
    CREATE TABLE {prefix}season_goals (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        season_id INTEGER REFERENCES {prefix}seasons(id),
        goal_text TEXT NOT NULL,
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """