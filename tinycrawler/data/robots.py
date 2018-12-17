from tinycrawler.expirables import ExpirableRobotFileParser


class Robots:
    def __init__(self, **kwargs):
        """Creates a structure to hold parsed robots txts.
            follow_robot_txt:bool, whetever to follow robots txt in the first place.
            follow_robot_txt_black_list:List[Domain], list of domains to not follow robots txts. Overrides follow_robot_txt value, if provided.
            follow_robot_txt_white_list:List[Domain], list of domains to follow robots txts. Overrides follow_robot_txt value, if provided.
        """
