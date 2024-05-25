import sqlite3
import os
import yaml
import json

class Email_Parsing:

    def __init__(self):
        # opening the constants file
        with open("constants.yaml","r") as data:
            self.constants = yaml.full_load(data.read())
        # opening the rules files
        with open("rules.json","r") as rules:
            self.rules = json.loads(json.dumps(rules.read()))
    
    def search(self):
        print(self.rules)
        return True

    def forming_conditions(self,predicate,condition):
        if predicate == "ALL":
            pass
        else:
            pass
        return True
    
    def applying_filter(self):
        return True


Email_Parsing().search()