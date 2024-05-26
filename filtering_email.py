import sqlite3
import os
import yaml
import json

class Email_Parsing:

    def __init__(self):
        # opening the constants file
        with open("constants.yaml","r") as data:
            self.constants = yaml.full_load(data.read())
        # opening the rules files and validating for the corrent format
        with open("rules.json","r") as rules:
            self.rules = json.loads(rules.read())
        for rules in self.rules.keys():
            for criteria in self.rules.get(rules).get("criteria"):
                if criteria.get("predicate") in ["Greater than","Less than"] and not criteria.get("value").isdigit():
                    raise TypeError("Criteria is not matched")
                else:
                    pass


    def search(self,predicate,condition):
        conditions = self.forming_conditions(predicate,condition)
        # forming sqlite3 connections
        sql_connection = sqlite3.connect("DB/email_db")
        sql_cursor = sql_connection.cursor()
        # getting the 
        mail_data = sql_cursor.execute(f"select message_id from inbox where {conditions}")
        mail_data = [dict(zip(map(lambda x : x[0],mail_data.description),i)) for i in mail_data.fetchall()]
        sql_connection.close()
        return mail_data

    def forming_conditions(self,predicate,condition):
        """
            Forming the sql condtion based on the filter conditions.
        """
        concat_conditions = []
        for cond in condition:
            temp_cond = []
            temp_cond.append(f"{self.constants['Fields_References'][cond['field_name']]} \
                            {self.constants['CONDITION_SYMBOL'][cond['predicate']]} \
                            '%{cond['value']}%'") if self.constants['CONDITION_SYMBOL'][cond['predicate']] == 'like' \
                            else temp_cond.append(f"'{cond['value']}'")    
            concat_conditions.append(" ".join(temp_cond))
        if predicate == "All":
            return " and ".join(concat_conditions)
        else:
            return " or ".join(concat_conditions)
    
    def applying_filter(self):
        num_rules = self.rules.keys()
        for rules in num_rules:
            filtered_mail = self.search(self.rules.get(rules).get("predicates"),self.rules.get(rules).get("criteria"))
            # filtered message id by applied rules
            print(filtered_mail)
        return True


Email_Parsing().applying_filter()