import pandas as pd
import matplotlib.pyplot as plt

# Read circuit and race data
df = pd.read_csv('/kaggle/input/motogp-circuits/circuit_data.csv', usecols=['Name', 'Right Corners','Left Corners'])
df['Direction'] = ['Clockwise' if r > l else 'Anticlockwise' for r, l in zip(df['Right Corners'], df['Left Corners'])]
df1 = df[['Name','Direction']]
df2 = pd.read_csv('/kaggle/input/moto-gp-world-championship19492022/grand-prix-race-winners.csv')

# Merge circuit direction with race data
merged_df = pd.merge(df1, df2, left_on='Name', right_on='Circuit')
merged_df = merged_df[['Circuit','Direction','Class','Rider','Season']]

# Select Rider and active seasons
selected_rider = "Valentino Rossi"
df_active_seasons = pd.read_csv('/kaggle/input/motogp-riders-active-years-per-category/active_years_per_category.csv')
selected_rider_row = df_active_seasons[df_active_seasons['rider_name'] == selected_rider].index[0]

def get_active_years(column_name):
    years = df_active_seasons.loc[selected_rider_row, column_name]
    if pd.isna(years):
        return []
    return [int(year.strip()) for year in years.split(',') if year.strip()]

# Get active seasons for each class
active_seasons = {
    '50cc': get_active_years('50cc'),
    '80cc': get_active_years('80cc'),
    '125cc': get_active_years('125cc'),
    '250cc': get_active_years('250cc'),
    '350cc': get_active_years('350cc'),
    'MotoE™': get_active_years('MotoE'),
    'Moto3™': get_active_years('Moto3'),
    'Moto2™': get_active_years('Moto2'),
    'MotoGP™': get_active_years('MotoGP')
}

# Initialize counters
total_races = {class_name: {
    'clockwise': 0, 'anticlockwise': 0,
    'rider_count_clockwise': 0, 'rider_count_anticlockwise': 0
} for class_name in active_seasons}

# Calculate totals
for class_name, seasons in active_seasons.items():
    df_class = merged_df[merged_df['Season'].isin(seasons)]
    total_races[class_name]['clockwise'] = len(df_class[(df_class['Class'] == class_name) & (df_class['Direction'] == 'Clockwise')])
    total_races[class_name]['anticlockwise'] = len(df_class[(df_class['Class'] == class_name) & (df_class['Direction'] == 'Anticlockwise')])
    total_races[class_name]['rider_count_clockwise'] = len(df_class[(df_class['Class'] == class_name) & (df_class['Direction'] == 'Clockwise') & (df_class['Rider'] == selected_rider)])
    total_races[class_name]['rider_count_anticlockwise'] = len(df_class[(df_class['Class'] == class_name) & (df_class['Direction'] == 'Anticlockwise') & (df_class['Rider'] == selected_rider)])

# Global totals
total_races_clockwise = sum(v['clockwise'] for v in total_races.values())
total_races_anticlockwise = sum(v['anticlockwise'] for v in total_races.values())
total_races_count = total_races_clockwise + total_races_anticlockwise
total_rider_wins_clockwise = sum(v['rider_count_clockwise'] for v in total_races.values())
total_rider_wins_anticlockwise = sum(v['rider_count_anticlockwise'] for v in total_races.values())

# Basic stats
print(f"Total number of races: {total_races_count}")
print(f"Total number of races at clockwise circuits: {total_races_clockwise}")
print(f"Total number of races at anticlockwise circuits: {total_races_anticlockwise}")
print(f"Total number of wins at clockwise circuits: {total_rider_wins_clockwise}")
print(f"Total number of wins at anticlockwise circuits: {total_rider_wins_anticlockwise}")

percentage_clockwise_circuits = round(total_races_clockwise / total_races_count * 100, 2)
percentage_anticlockwise_circuits = round(total_races_anticlockwise / total_races_count * 100, 2)
print(f"Percentage of races at clockwise circuits: {percentage_clockwise_circuits}%")
print(f"Percentage of races at anticlockwise circuits: {percentage_anticlockwise_circuits}%")

# Rider win percentages
winning_percentage_clockwise = round(total_rider_wins_clockwise / total_races_clockwise * 100,2)
winning_percentage_anticlockwise = round(total_rider_wins_anticlockwise / total_races_anticlockwise * 100,2)

# New: Overall win rate by direction (all riders)
overall_win_ratio_clockwise = round(total_rider_wins_clockwise / total_races_count * 100, 2)
overall_win_ratio_anticlockwise = round(total_rider_wins_anticlockwise / total_races_count * 100, 2)

print(f"{selected_rider}'s overall win rate: {round((total_rider_wins_clockwise + total_rider_wins_anticlockwise) / total_races_count * 100, 2)}%")
print(f"{selected_rider}'s win % at clockwise: {winning_percentage_clockwise}%")
print(f"{selected_rider}'s win % at anticlockwise: {winning_percentage_anticlockwise}%")

# Plotting winning percentage per direction
plt.figure(figsize=(6,5))
winning_percentages = [winning_percentage_clockwise, winning_percentage_anticlockwise]
circuits = ['Clockwise', 'Anticlockwise']
plt.bar(circuits, winning_percentages, color=['#1f77b4', '#ff7f0e'])

# Add data labels
for i in range(len(winning_percentages)):
    plt.text(i, winning_percentages[i], f"{winning_percentages[i]}%", ha='center', va='bottom')

plt.title(f'{selected_rider} Winning Percentages per Circuit Direction')
plt.xlabel('Circuit Direction')
plt.ylabel('Winning Percentage')
plt.tight_layout()
plt.show()

# New: Bar Chart of Wins by Class and Direction
classes = []
cw_wins = []
acw_wins = []

for class_name in total_races:
    cw = total_races[class_name]['rider_count_clockwise']
    acw = total_races[class_name]['rider_count_anticlockwise']
    if cw + acw > 0:  # Only include if he has wins in that class
        classes.append(class_name)
        cw_wins.append(cw)
        acw_wins.append(acw)

# Plot stacked bar chart
plt.figure(figsize=(10,6))
bar1 = plt.bar(classes, cw_wins, label='Clockwise')
bar2 = plt.bar(classes, acw_wins, bottom=cw_wins, label='Anticlockwise')

# Add labels
for i in range(len(classes)):
    total = cw_wins[i] + acw_wins[i]
    plt.text(i, total + 0.5, str(total), ha='center', va='bottom')

plt.title(f'{selected_rider} Wins by Class and Circuit Direction')
plt.xlabel('Racing Class')
plt.ylabel('Number of Wins')
plt.legend()
plt.tight_layout()
plt.show()
