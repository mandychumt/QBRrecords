import csv
def read_csv_dict(filename):
    with open(filename, 'r') as file_handle:
        reader = csv.DictReader(file_handle, delimiter=",")
        csv_list = list(reader)
    return csv_list


class Game(object):
    def __init__ (self, action_plays, game_id, h_a, opponent, totalQBR, W_L, player_id): 
        #h_a means home or away
        #W_L means Win or Loss
        self.action_plays = int(action_plays)
        self.game_id = game_id
        self.h_a = h_a
        self.opponent = opponent
        self.totalQBR = float(totalQBR)
        self.W_L = W_L
        self.player_id = int(player_id)

class Player(object):
    def __init__ (self, player_id, first_name, last_name, team_name):
        self.player_id = int(player_id)
        self.first_name = first_name
        self.last_name = last_name
        self.team_name = team_name
        self.gamels = []
        
    def add_game (self, game):
        self.gamels.append(game)
        
    #get the game in a loss with the highest totalQBR from all games of a player
    def get_Lmax_game (self): 
        Lmax_game = None
        max_qbr = -1.0 #qbr in list is always larger than 0
        for game in self.gamels:
            if game.W_L == 'W':
                pass
            #only check for loss games
            elif max_qbr < game.totalQBR:
                max_qbr = game.totalQBR
                Lmax_game = game
        return Lmax_game
    
    #get the game in a win with the lowest totalQBR from all games of a player
    def get_Wmin_game (self):
        Wmin_game = None
        min_qbr = 100.0 #qbr in game is always less than 100
        for game in self.gamels:
            if game.W_L == 'L':
                pass
            #only check for win games
            elif min_qbr > game.totalQBR:
                min_qbr = game.totalQBR
                Wmin_game = game
        return Wmin_game
    
    #get the game with the highest action_plays from all games of a player
    def get_max_action_game (self):
        max_action_game = None
        max_action_plays = -1 #action in game is always non negative
        for game in self.gamels:
            if game.action_plays > max_action_plays:
                max_action_plays = game.action_plays
                max_action_game = game
        return max_action_game
    
    #get the average totalQBR of all games of a player
    def get_avg_totalQBR (self):
        sum_totalQBR = 0.0
        for game in self.gamels:
            sum_totalQBR += game.totalQBR
        avg = sum_totalQBR / len(self.gamels)
        return avg


#read csv files and construct player dictionary
#rows = list of dictionary, each dictionary represents a game
#each dictionary in rows: key=header value=data
rows = []
for i in range(2004,2018):
    file_name = str(i) + '.csv'
    rows.extend(read_csv_dict(file_name))

#now all files are represented by 'rows', next step is to construct a player dictionary 
player_d = {} #key = (firstname, lastname) tuple
for row in rows:
    first_name = row['first_name']
    last_name = row['last_name']
    game = Game(row['action_plays'], row['espn_game_id'], row['home_away'], row['opponent'], \
                row['total_QBR'], row['won_lost'], row['espn_player_id'])
    
    if (first_name, last_name) not in player_d:
        #create a new key for the player if it is not in player_d
        player_d[(first_name, last_name)] = Player(row['espn_player_id'], first_name, last_name, row['team_name'])
    
    player_d[(first_name, last_name)].add_game(game)    



#set the initials values of what are needed to be found
#totalQBR is in range 0 ~ 100
highest_QBR_loss = -1
highest_QBR_loss_game = None

lowest_QBR_win = 100
lowest_QBR_win_game = None

highest_action = -1 #action is always non negative in chart
highest_action_game = None

highest_avg_totalQBR = -1
highest_avg_totalQBR_player = None


for player in player_d.values():
    
    #find the game in a loss with the highest totalQBR
    Lmax_game = player.get_Lmax_game()
    if Lmax_game is None:
        pass
     #only check for loss games
    elif Lmax_game.totalQBR > highest_QBR_loss:
        highest_QBR_loss = Lmax_game.totalQBR
        highest_QBR_loss_game = Lmax_game
    
    #find the game in a win with the lowest totalQBR
    Wmin_game = player.get_Wmin_game()
    if Wmin_game is None:
        pass
     #only check for win games
    elif Wmin_game.totalQBR < lowest_QBR_win:
        lowest_QBR_win = Wmin_game.totalQBR
        lowest_QBR_win_game = Wmin_game
    
    #find the game with the highest action_plays
    action_game = player.get_max_action_game()
    if highest_action < action_game.action_plays:
        highest_action = action_game.action_plays
        highest_action_game = action_game
    
    #find the player with the highest average totalQBR
    avg_totalQBR = player.get_avg_totalQBR()
    if avg_totalQBR > highest_avg_totalQBR:
        highest_avg_totalQBR = avg_totalQBR
        highest_avg_totalQBR_player = player
        

print ("Player {} in game {} had the highest total_QBR in loss, value {}".format(highest_QBR_loss_game.player_id, \
                                    highest_QBR_loss_game.game_id, highest_QBR_loss_game.totalQBR))
print ("Player {} in game {} had the lowest total_QBR in win, value {}".format(lowest_QBR_win_game.player_id, \
                                    lowest_QBR_win_game.game_id, lowest_QBR_win_game.totalQBR))
print ("Player {} in game {} had the highest action_plays, value {}".format(highest_action_game.player_id, \
                                    highest_action_game.game_id, highest_action_game.action_plays))
print ("player {} had the highest average total_QBR, value {}".format(highest_avg_totalQBR_player.player_id, \
                                    highest_avg_totalQBR))