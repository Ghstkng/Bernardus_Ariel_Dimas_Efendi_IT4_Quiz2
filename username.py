import mysql.connector as mysql
from mysql.connector import Error
import sqlalchemy
from urllib.parse import quote_plus as urlquote
import matplotlib.pyplot as plt
import pandas as pd
import os

class SysManagement:
    def _init_(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def create_db(self, db_name):
        conn = mysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password
        )
        try:
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("CREATE DATABASE {}".format(db_name))
        except Error as e:
            print("Error while connecting to MySQL", e)

    def create_table(self, db_name, table_name, df):
        conn = mysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password
        )
        try:
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("USE {}".format(db_name))
                cursor.execute("CREATE TABLE {}".format(table_name))
        except Error as e:
            print("Error while connecting to MySQL", e)
        for i, row in df.iterrows():
            var = "INSERT INTO {} VALUES {}".format(
                table_name.split(' ', 1)[0], tuple(row))
            cursor.execute(var)
            print('Record inserted')
            conn.commit()

    def load_data(self, db_name, table_name):
        conn = mysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password
        )
        try:
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM {}.{}".format(db_name, table_name))
                result = cursor.fetchall()
                return result
        except Error as e:
            print("Error while connecting to MySQL", e)

    def import_csv(self, path):
        return pd.read_csv(path, index_col=False, delimiter=',')

system = SysManagement()
system.host = 'localhost'
system.port = '3306'
system.user = 'root'
system.password = ''

username_df = system.import_csv('username.csv')
system.create_table('username (Username VARCHAR(255),Identifier VARCHAR(255), First_Name VARCHAR(255), Last_Name VARCHAR(255))', usename_df)
print(system.load_data('username'))
    
