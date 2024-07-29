# -*- coding: utf-8 -*-
"""
@Time: 2024/6/17 上午2:29
@Auth: Bacchos
@File: db_utils.py
@IDE: PyCharm
@Motto: ABC(Always Be Coding)
"""

from fastapi import HTTPException
import mysql.connector
from mysql.connector import errorcode


def db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="chatapi",
            password="Ljw20110804",
            database="chatbot",
            ssl_disabled=True
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise HTTPException(status_code=400, detail="Access denied. Please check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise HTTPException(status_code=400, detail="Database does not exist.")
        else:
            raise HTTPException(status_code=500, detail=str(err))


def get_system_instruction(bot_name):
    connection = db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT instruction FROM system_instruction WHERE bot_name = %s"
    cursor.execute(query, (bot_name,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result['instruction']
    else:
        return None


def store_conversation(bot_name, role, parts):
    connection = db_connection()
    cursor = connection.cursor()

    table_mapping = {
        "BTC": "btc_convo",
        "ETH": "eth_convo",
        "SOL": "sol_convo",
        "PEPE": "pepe_convo",
        "DOGE": "doge_convo",
    }
    table_name = table_mapping.get(bot_name)
    if not table_name:
        raise ValueError(f"Invalid bot_name: {bot_name}")
    query = f"INSERT INTO {table_name} (bot_name, role, parts) VALUES (%s, %s, %s)"
    cursor.execute(query, (bot_name, role, parts))

    connection.commit()
    cursor.close()
    connection.close()
