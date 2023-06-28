import csv
import random

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.dpi'] = 200
plt.rcParams['font.family'] = 'Consolas'

# 颜色库
colors = ['#FF817D', '#FFCDD5', '#FFCAA1', '#FFEFA0', '#CBEF96', '#BAFFF8', '#C5E4FF', '#DDC2FF', '#F8D3FF']
team_color = colors[1:8]


# 从csv中读取数据为列表
def csv_to_list(csv_file):
    data = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)
    return data


# 绘制饼图
def pie_draw(data, label, title):
    pie_explode = (0.05,) * len(data)
    plt.pie(x=data, labels=label, colors=team_color, radius=1, shadow=False,
            explode=pie_explode, autopct='%3.1f%%')
    plt.title(title)
    plt.savefig('output/' + title, dpi=600, bbox_inches='tight')
    plt.show()


def barh_draw(data, label, color, title):
    ax = plt.axes()
    ax.barh(label, data, color=color)
    ax.set_title(title)
    ax.set_xlabel("Ability points")
    ax.set_ylabel("Player")
    ax.grid(axis='x')
    ax.set_xlim(80, 140)
    plt.savefig('output/' + title, dpi=600, bbox_inches='tight')
    plt.show()


# 绘制雷达图
def radar_draw( data, label, player):
    angle = np.linspace(0, np.pi * 2, 5, endpoint=False)
    radar_data = np.concatenate((data, [data[0]]))
    radar_label = np.concatenate((label, [label[0]]))
    angle = np.concatenate((angle, [angle[0]]))
    single_color = random.choice(colors)
    ax = plt.subplot(111, polar=True)
    ax.plot(angle, radar_data, 'o-', linewidth=0.8, color=single_color, alpha=0.8)
    ax.fill(angle, radar_data, alpha=0.15, color=single_color)
    ax.set_thetagrids(angle * 180 / np.pi, labels=radar_label)
    ax.set_theta_zero_location('N')
    ax.set_rlim(0, 100)
    title = 'Data of ' + player
    ax.set_title(title)
    plt.legend([player], loc='best')
    plt.savefig('output/' + title, dpi=600, bbox_inches='tight')
    plt.show()


def team():
    team_data = csv_to_list(r"output\teams.csv")
    team_name = []
    team_winner = []
    team_points = []
    for i in team_data:
        team_name.append(i[0])
        team_winner.append(i[1])
        team_points.append(i[2])

    team_winner = list(map(float, team_winner))
    team_points = list(map(float, team_points))
    # 第四队和第六队补正
    team_winner[3] *= 1.2
    team_winner[5] *= 1.2
    team_points[3] *= 1.2
    team_points[5] *= 1.2

    pie_draw(team_winner, team_name, "winner_pie")
    pie_draw(team_points, team_name, "points_pie")


def top_players():
    players_data = csv_to_list(r"output\top-nine player.csv")
    player_name = []
    player_points = []
    player_team = []
    team_name = ["Hawks", "Magic", "Nets", "Wizards", "Trail Blaze", "Grizzlies", "Knicks"]
    for i in players_data:
        player_name.append(i[0])
        player_points.append(int(i[1]))
        player_team.append(i[2])
    player_color = [colors[team_name.index(i) + 1] for i in player_team]
    barh_draw(player_points[::-1], player_name[::-1], player_color[::-1], "top-nine player")


def single_player():
    single_players = ["Brook Lopez", "Nikola Vucevic", "Al Horford"]
    for player in single_players:
        player_data = csv_to_list("output/" + player + ".csv")
        records = scores = assists = rebounds = steals = 0
        points = []
        for record in player_data:
            records += 1
            scores += int(record[0])
            assists += int(record[1])
            rebounds += int(record[2])
            steals += int(record[3])
            points.append(scores * 3 + assists + rebounds + steals)
        data = [(scores / records ) * 4, (assists / records + 1) * 16, (rebounds / records) * 7.5,
                (steals / records + 1) * 40, 5000 / np.var(np.array(points)) * 100]
        print(player, data)
        label=['Scores', 'Rebounds', 'Assists', 'Steals', 'Stability']
        radar_draw(data,label, player)



def main():
    # radar_num = 5
    # radar_data = np.random.randint(5, 20, radar_num)
    # radar_label = np.array(['Scores', 'Rebounds', 'Assists', 'Steals', 'Stability'])
    # radar_draw(radar_num, radar_label, radar_data, 'Player X')
    single_player()


if __name__ == '__main__':
    main()
