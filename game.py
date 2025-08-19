import random
import json

class Game:
    def __init__(self):
        self.num_player = 0
        self.card_list = []
        self.reveal_card_list = []
        self.confirm_number = 0
        self.reveal_number = 0
        self.player_dict = {}
        self.discussion_time = False
        self.result_time = False
        with open("topics.json", "r", encoding="utf-8") as f:
            self.topics = json.load(f)
        self.topic = random.sample(self.topics, 1)[0]
        
    def prepare_game_start(self, num_player, uids):
        self.num_player = num_player
        self.card_list = random.sample(list(range(1, 101)), num_player)
        for uid in uids:
            self.player_dict[uid] = {"confirm": False, "reveal": False}

    def return_card_number(self, slot_id):
        return self.card_list[slot_id]
    
    def return_discussion_time(self):
        return self.discussion_time
    
    def return_topic(self):
        return self.topic
    
    def return_confirm_number(self):
        return self.confirm_number
        
    def return_reveal_card_list(self):
        # return [name for name, player in self.player_dict.items() if player["reveal"]]
        return self.reveal_card_list
    
    def update_confirm_number_and_jedge_all_confirmed(self, uid):
        self.player_dict[uid]["confirm"] = True
        self.confirm_number = sum(player["confirm"] for player in self.player_dict.values())
        if self.confirm_number >= self.num_player:
            self.discussion_time = True
            return self.confirm_number, self.discussion_time
        else:
            self.discussion_time = False
            return self.confirm_number, self.discussion_time
        
    def update_reveal_card_list_and_jedge_all_revealed(self, uid):
        if self.player_dict[uid]["reveal"]:
            if self.reveal_number >= self.num_player:
                self.result_time = True
            else:
                self.result_time = False
            return False, self.result_time
        else:
            self.player_dict[uid]["reveal"] = True
            self.reveal_card_list.append(uid)
            self.reveal_number = sum(player["reveal"] for player in self.player_dict.values())
            if self.reveal_number >= self.num_player:
                self.result_time = True
            else:
                self.result_time = False
            return True, self.result_time
        
    def finish_game(self, slot_list, card_list):
        sorted_card_list = sorted(card_list)
        d = {}
        d["card_number"] = card_list
        d["slot_number"] = [x + 1 for x in slot_list]
        wrong_list = []
        for i in range(len(card_list)):
            if sorted_card_list[i] == card_list[i]:
                wrong_list.append(False)
            else:
                wrong_list.append(True)
        d["wrong"] = wrong_list
        return d

        
    