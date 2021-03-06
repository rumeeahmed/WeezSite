from flask import render_template
from flask.views import MethodView
from models.weezbase import WeezBase


class Awards(MethodView):
    """
    Object that serves the Awards page.
    """

    def get(self) -> str:
        """
        Handle the get request made to this route. Return the details of all awards in the Firebase database.
        :return: a HTML template.
        """
        self._initialise_database()
        awards_data = self._count_awards()
        return render_template('awards.html', awards_data=awards_data, session_count=self.session_count)

    def _initialise_database(self) -> None:
        """
        Initialise the database and retrieve the data to be processed and then passed into the Awards template.
        :return: None
        """
        weezbase = WeezBase()
        player_data = weezbase.db.collection('players').get()
        self.players = [player.to_dict() for player in player_data]

        self.data = []
        documents = weezbase.db.collection('awards').stream()

        self.session_count = 0
        for doc in documents:
            # Use the document ID to get the fields inside the document.
            awards = weezbase.db.collection('awards').document(doc.id).get().to_dict()
            self.data.append(awards)
            self.session_count += 1

    def _process_awards_data(self) -> dict:
        """
        Process the raw data retrieved from firebase and add the count of the awards together for the awards.
        :return: a dictionary containing a dictionary for each player and the count of the awards received.
        """
        data = {}
        for player in self.players:
            player_dict = {
                'bullet_bitch': 0,
                'gummy_bear': 0,
                'head_master': 0,
                'lethal_killer': 0,
                'least_lethal_killer': 0,
                'medic': 0,
                'pussio': 0,
                'tank': 0,
                'team_demolisher': 0,
                'team_hater': 0,
                'team_lover': 0,
                'top_assister': 0,
                'big_spender': 0,
                'hungry_bitch': 0,
                'weary_traveller': 0,
            }

            # Iterate over the award dicts in the list
            for award in self.data:
                # Iterate ove the keys in the dicts
                for key in award.keys():
                    # If the award key contains players name then add 1 to the value associated award key in player_dict
                    if award[key] == player['player']:
                        player_dict[key] += 1

            data[player['player']] = player_dict
        return data

    def _count_awards(self) -> dict:
        """
        Get the processed player awards data and then add them up.
        :return: a dictionary containing all the added up data for the players.
        """
        awards_data = self._process_awards_data()
        awards_dict = {
            'bullet_bitch': [0, 'Bullet Bitch', 'The player that received the most damage.', ''],
            'gummy_bear': [0, 'Gummy Bear', 'The player that takes the least damage taken per death.', ''],
            'head_master': [0, 'Headmaster', 'The player with the most headshots.', ''],
            'lethal_killer': [0, 'Lethal Killer', 'The player that has the least amount of damage per kill.', ''],
            'least_lethal_killer': [
                0, 'Least Lethal Killer', 'The player that has the most amount of damage per kill.', ''
            ],
            'medic': [0, 'Medic', 'The player with the most revives.', ''],
            'pussio': [0, 'Pussio', 'The Pussio!', ''],
            'tank': [0, 'Tank', 'The player that takes the most damage per death.', ''],
            'team_demolisher': [0, 'Team Demolisher', 'The player with the most team wipes', ''],
            'team_hater': [0, 'Team Hater', 'The player with the lowest score.', ''],
            'team_lover': [0, 'Team Lover', 'The player with the highest score.', ''],
            'top_assister': [0, 'Top Assister', 'The player with the most assists.', ''],
            'big_spender': [0, 'Big Spender', 'The player that bought the most items from the shop.', ''],
            'hungry_bitch': [0, 'Hungry Bitch', 'The player that opened the most crates.', ''],
            'weary_traveller': [0, 'Wearey Traveller', 'The player that covered the most distance.', ''],
        }

        # Iterate over the player name and its dictionary value in the awards_data dict.
        for player_key, awards in awards_data.items():
            # Iterate over the award key and its value
            for award_key, award_value in awards.items():
                # If the value associated with the award is greater than the one in the awards dict add that value and
                # its key to corresponding key in the awards dict.
                if awards_data[player_key][award_key] > awards_dict[award_key][0]:
                    awards_dict[award_key][0] = award_value
                    awards_dict[award_key][3] = player_key
        return awards_dict
