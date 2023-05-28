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
def pie_draw():
    pie_num = 5
    player_points = np.random.randint(5, 30, pie_num)
    pie_color = random.sample(colors, pie_num)
    pie_explode = (0.05, 0.05, 0.05, 0.05, 0.05)
    plt.pie(x=player_points, labels=random.sample(player_name, pie_num), colors=pie_color, radius=1, shadow=False,
            explode=pie_explode, autopct='%3.1f%%')
    plt.title('Contribution of each team member')
    plt.savefig('./picture/pie', dpi=600, bbox_inches='tight')
    plt.show()


# 绘制雷达图
def radar_draw():
    radar_num = 5
    single_data = np.random.randint(5, 20, radar_num)
    radar_label = np.array(['Scores', 'Rebounds', 'Assists', 'Steals', 'Stability'])
    angle = np.linspace(0, np.pi * 2, radar_num, endpoint=False)
    single_data = np.concatenate((single_data, [single_data[0]]))
    radar_label = np.concatenate((radar_label, [radar_label[0]]))
    angle = np.concatenate((angle, [angle[0]]))
    single_color = random.choice(colors)
    ax = plt.subplot(111, polar=True)
    ax.plot(angle, single_data, 'o-', linewidth=0.8, color=single_color, alpha=0.4)
    ax.fill(angle, single_data, alpha=0.15, color=single_color)
    ax.set_thetagrids(angle * 180 / np.pi, labels=radar_label)
    ax.set_theta_zero_location('N')
    ax.set_rlim(0, 25)
    ax.set_title("Single player's data")
    plt.legend(['player X'], loc='best')
    plt.savefig('./picture/radar', dpi=600, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    pie_draw()
    radar_draw()
