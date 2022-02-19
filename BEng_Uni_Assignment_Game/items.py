class Items():
    #New Class that allows items to be created

    def __init__(self):
        self.items = {}

    def add_new_item(self, item, description):
        self.items[item] = description

    def get_item_exists(self, item):
        if item in self.items:
            return True
        else:
            return False

    def get_item_description(self, item):
        if item in self.items:
            return self.items[item]
        else:
            return None