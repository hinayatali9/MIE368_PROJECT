# %%
import pandas as pd
import time

# %%
player_stats=pd.read_html('https://www.hockey-reference.com/leagues/NHL_2007_skaters.html')
new_df=pd.DataFrame(player_stats[0])

if isinstance(new_df.columns, pd.MultiIndex):
    # Replace the top header with the subheader
    new_df.columns = new_df.columns.get_level_values(1)

new_df=new_df.reset_index(drop=True)
new_df

# %%
start_year = 2023
all_df_skaters=pd.DataFrame()
all_df_goalies=pd.DataFrame()

print(start_year)

url_skaters=f'https://www.hockey-reference.com/leagues/NHL_{start_year}_skaters.html'
url_goalies=f'https://www.hockey-reference.com/leagues/NHL_{start_year}_goalies.html'
df_skaters = pd.read_html(url_skaters)
df_goalies = pd.read_html(url_goalies)
df_skaters_cleaned=pd.DataFrame(df_skaters[0])
df_goalies_cleaned=pd.DataFrame(df_goalies[0])
if isinstance(df_skaters_cleaned.columns, pd.MultiIndex):
    df_skaters_cleaned.columns = df_skaters_cleaned.columns.get_level_values(1)
if isinstance(df_goalies_cleaned.columns, pd.MultiIndex):
    df_goalies_cleaned.columns = df_goalies_cleaned.columns.get_level_values(1)
df_skaters_cleaned=df_skaters_cleaned.drop_duplicates(['Rk'], keep='first')
df_goalies_cleaned=df_goalies_cleaned.drop_duplicates(['Rk'], keep='first')
df_skaters_cleaned['SEASON']=start_year
df_goalies_cleaned['SEASON']=start_year
all_df_skaters = pd.concat([all_df_skaters, df_skaters_cleaned], axis=0, ignore_index=True)
all_df_goalies = pd.concat([all_df_goalies, df_goalies_cleaned], axis=0, ignore_index=True)
all_df_skaters.to_csv("skaters_1996_2023.csv")
all_df_goalies.to_csv("goalies_1996_2023.csv")

start_year -= 1
years = list(range(1996, start_year + 1))
years.reverse()
years.remove(2005) # lockout season, no data
time.sleep(10)

for year in years:
    url_skaters=f'https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html'
    url_goalies=f'https://www.hockey-reference.com/leagues/NHL_{year}_goalies.html'
    print(year)
    df_skaters = pd.read_html(url_skaters)
    df_goalies = pd.read_html(url_goalies)
    df_skaters_cleaned=pd.DataFrame(df_skaters[0])
    df_goalies_cleaned=pd.DataFrame(df_goalies[0])
    if isinstance(df_skaters_cleaned.columns, pd.MultiIndex):
        df_skaters_cleaned.columns = df_skaters_cleaned.columns.get_level_values(1)
    if isinstance(df_goalies_cleaned.columns, pd.MultiIndex):
        df_goalies_cleaned.columns = df_goalies_cleaned.columns.get_level_values(1)
    df_skaters_cleaned=df_skaters_cleaned.drop_duplicates(['Rk'], keep='first')
    df_goalies_cleaned=df_goalies_cleaned.drop_duplicates(['Rk'], keep='first')
    df_skaters_cleaned['SEASON']=year
    df_goalies_cleaned['SEASON']=year
    df_skaters_cleaned.to_csv("skaters_1996_2023.csv", index=False, header=False, mode='a')
    df_goalies_cleaned.to_csv("goalies_1996_2023.csv", index=False, header=False, mode='a')
    time.sleep(10)
