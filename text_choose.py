# 从文件中挑选段落
def choose_text(filename, teams):
    # 打开文件并读取内容
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # 将文本分割成段落
    paragraphs = text.split('\n')
    vs_info = []
    result = []

    # 遍历每个段落
    for para in paragraphs:
        first_sentence = para.split('.')[0]
        two = []
        for team in teams:
            if team in first_sentence:
                two += [team]
        if len(two) == 2:
            # 选择在同时出现在teams中两两对决的比赛
            a_vs_b = two[0] + '-' + two[1]
            if not a_vs_b in vs_info:
                vs_info.append(two[0] + '-' + two[1])
                result.append(para)

    return vs_info, result


if __name__ == '__main__':
    # 选择队伍
    teams = ['Atlanta Hawks', 'Orlando Magic', 'Washington Wizards', 'Brooklyn Nets', 'New York Knicks',
             'Portland Trail Blazers', 'Memphis Grizzlies']
    check, result_list = choose_text('rotowire.txt', teams)
    print(len(check))
    # 比赛对决双方概览
    check.sort()
    for i in check:
        print(i)
    with open('text_chosen.txt', 'w', encoding='utf-8') as f:
        for i in result_list:
            f.write(i + '\n\n')
