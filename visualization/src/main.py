import random

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.dpi'] = 200
plt.rcParams['font.family'] = 'Consolas'

# 颜色库
colors = ['#FF817D', '#FFCDD5', '#FFCAA1', '#FFEFA0', '#CBEF96', '#BAFFF8', '#C5E4FF', '#DDC2FF', '#F8D3FF']
# 球员名
player_name = ['Aka', 'Bob', 'Chris', 'Daniel', 'Evan', 'Frank', 'George']


# 绘制饼图
def pie_draw(num, points, team):
    pie_color = random.sample(colors, num)
    pie_explode = (0.05, 0.05, 0.05, 0.05, 0.05)
    plt.pie(x=points, labels=random.sample(player_name, num), colors=pie_color, radius=1, shadow=False,
            explode=pie_explode, autopct='%3.1f%%')
    title = "Data of " + team
    plt.title(title)
    plt.savefig('./picture/' + title, dpi=600, bbox_inches='tight')
    plt.show()


# 绘制雷达图
def radar_draw(num, label, data, player):
    angle = np.linspace(0, np.pi * 2, num, endpoint=False)
    radar_data = np.concatenate((data, [data[0]]))
    radar_label = np.concatenate((label, [label[0]]))
    angle = np.concatenate((angle, [angle[0]]))
    single_color = random.choice(colors)
    ax = plt.subplot(111, polar=True)
    ax.plot(angle, radar_data, 'o-', linewidth=0.8, color=single_color, alpha=0.4)
    ax.fill(angle, radar_data, alpha=0.15, color=single_color)
    ax.set_thetagrids(angle * 180 / np.pi, labels=radar_label)
    ax.set_theta_zero_location('N')
    ax.set_rlim(0, 25)
    title = 'Data of ' + player
    ax.set_title(title)
    plt.legend([player], loc='best')
    plt.savefig('./picture/' + title, dpi=600, bbox_inches='tight')
    plt.show()


def main():
    pie_num = 5
    pie_player_points = np.random.randint(5, 30, pie_num)
    pie_draw(pie_num, pie_player_points, 'Team A')

    radar_num = 5
    radar_data = np.random.randint(5, 20, radar_num)
    radar_label = np.array(['Scores', 'Rebounds', 'Assists', 'Steals', 'Stability'])
    radar_draw(radar_num, radar_label, radar_data, 'Player X')


if __name__ == '__main__':
    main()
