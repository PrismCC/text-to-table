def construct_from_split_and_newline(table, split, newline):
    if table[0] != split:
        return []
    res = []
    tmp_row = []
    content = ""
    skip = False
    for element in table[1:]:
        if element == split:
            if skip:
                skip = False
                continue
            tmp_row.append(content)
            content = ""
        elif element == newline:
            res.append(tmp_row)
            skip = True
            tmp_row = []
        else:
            if content != "":
                content += ' '
            content += element
    res.append(tmp_row)
    return res

def convert_text_to_list(text):
    split = '|'
    newline = '<NEWLINE>'
    if text == "":
        return []

    teams_head_index = text.find('Team:')
    players_head_index = text.find('Player:')
    if teams_head_index == -1 or players_head_index == -1:
        return []

    teams_text = text[teams_head_index+5:players_head_index]
    players_text = text[players_head_index+8:]
    teams_table = teams_text.split()
    players_table = players_text.split()
    teams_table.pop(0)
    players_table.pop(0)
    if teams_head_index < players_head_index:
        teams_table.pop(-1)
    else:
        players_table.pop(-1)

    teams_res = construct_from_split_and_newline(teams_table, split, newline)
    players_res = construct_from_split_and_newline(players_table, split, newline)
    teams_res[0][0] = "Teams"
    players_res[0][0] = "Players"
    return (teams_res, players_res)

class Table:
    def __init__(self, text):
        self.teams_data, self.players_data = convert_text_to_list(text)

    def __str__(self):
        res = ""
        for row in self.teams_data:
            for column in row:
                res += column + ' | '
            res = res[:-2] + '\n'
        for row in self.players_data:
            for column in row:
                res += column + ' | '
            res = res[:-2] + '\n'
        return res

    def get_teams_table(self):
        return self.teams_data

    def get_players_table(self):
        return self.players_data
