import pandas as pd
from fuzzywuzzy import process

def select_players(player_csv_file, goalie_csv_file, season):
    # Read the CSV files
    df_players = pd.read_csv(player_csv_file)
    df_goalies = pd.read_csv(goalie_csv_file)
    df_players = df_players[df_players['RK'] != 'Rk']
    df_goalies = df_goalies[df_goalies['RK'] != 'Rk']
    df_players['SCORING_GP'] = pd.to_numeric(df_players['SCORING_GP'])
    df_goalies['GOALIE_STATS_GP'] = pd.to_numeric(df_goalies['GOALIE_STATS_GP'])

    # Filter out rookies
    df_players = df_players[df_players.groupby('PLAYER')['SEASON'].transform('min') != season]
    df_goalies = df_goalies[df_goalies.groupby('PLAYER')['SEASON'].transform('min') != season]

    # Filter the data for the given season
    df_players = df_players[df_players['SEASON'] == season]
    df_goalies = df_goalies[df_goalies['SEASON'] == season]

    # Define the positions for forwards and defensive players
    forwards = ['F', 'LW', 'RW', 'W', 'C']
    defensive = ['D']

    # Filter the data for forwards and defensive players
    df_forwards = df_players[df_players['POS'].isin(forwards)]
    df_defensive = df_players[df_players['POS'].isin(defensive)]

    # Sort the players by the number of games played and select the top ones for each team
    df_forwards = df_forwards.groupby('TM').apply(lambda x: x.nlargest(12, 'SCORING_GP')).reset_index(drop=True)
    df_defensive = df_defensive.groupby('TM').apply(lambda x: x.nlargest(6, 'SCORING_GP')).reset_index(drop=True)

    # If there are less than 12 forwards or 6 defensive players for a team, select additional players
    for team in df_players['TM'].unique():
        total_players = len(df_forwards[df_forwards['TM'] == team]) + len(df_defensive[df_defensive['TM'] == team])
        if total_players < 18:
            remaining_players = df_players[(df_players['TM'] == team) & (~df_players['PLAYER'].isin(df_forwards['PLAYER'])) & (~df_players['PLAYER'].isin(df_defensive['PLAYER']))]
            remaining_players = remaining_players.nlargest(18 - total_players, 'SCORING_GP')
            df_forwards = pd.concat([df_forwards, remaining_players[remaining_players['POS'].isin(forwards)]])
            df_defensive = pd.concat([df_defensive, remaining_players[remaining_players['POS'].isin(defensive)]])

    # Select the top 2 goalies for each team
    df_goalies = df_goalies.groupby('TM').apply(lambda x: x.nlargest(2, 'GOALIE_STATS_GP')).reset_index(drop=True)

    # Define the team names
    team_names = {
        'COL': 'team_colorado', 
        'DAL': 'team_dallas', 
        'ARI': 'team_coyotes', 
        'NSH': 'team_predators', 
        'STL': 'team_blues', 
        'MIN': 'team_wild', 
        'WPG': 'team_jets', 
        'CHI': 'team_blackhawks', 
        'VEG': 'team_knights', 
        'VAN': 'team_canucks', 
        'LAK': 'team_kings', 
        'CGY': 'team_flames', 
        'EDM': 'team_oilers', 
        'SEA': 'team_kraken', 
        'ANA': 'team_ducks', 
        'SJS': 'team_sharks', 
        'BOS': 'team_bruins', 
        'DET': 'team_wings', 
        'MTL': 'team_canadiens', 
        'TOR': 'team_leafs', 
        'OTT': 'team_senators', 
        'TBL': 'team_lightning', 
        'FLA': 'team_panthers', 
        'BUF': 'team_sabres', 
        'PHI': 'team_flyers', 
        'CBJ': 'team_jackets', 
        'NYR': 'team_rangers', 
        'CAR': 'team_hurricanes', 
        'NJD': 'team_devils', 
        'NYI': 'team_islanders', 
        'PIT': 'team_penguins', 
        'WSH': 'team_capitals'
    }
    # Create the output file
    with open(f'roster_{season}.txt', 'w', encoding='utf-8') as f:
        for team in df_players['TM'].unique():
            if team == 'TOT':
                continue
            # Find the most similar team name
            team_name = team_names[team]

            # Get the players for the team
            team_players = df_forwards[df_forwards['TM'] == team]['PLAYER'].tolist() + df_defensive[df_defensive['TM'] == team]['PLAYER'].tolist()

            # Write the team and players to the file
            f.write(f"{team_name}_{season}={team_players}\n")

            # Write the team and goalies to the file
            f.write(f"{team_name}_goalies_{season}={df_goalies[df_goalies['TM'] == team]['PLAYER'].tolist()}\n")

# Use the function
select_players('player_proj\skaters_1996_2023.csv', 'player_proj\goalies_1996_2023.csv', 2019)
select_players('player_proj\skaters_1996_2023.csv', 'player_proj\goalies_1996_2023.csv', 2022)
