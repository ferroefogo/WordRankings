from sqlite3 import connect

conn = connect('ChatLogs.db')
c = conn.cursor()

c.execute("""CREATE TABLE ChatLogDeets(
    guild_id INTEGER NOT NULL DEFAULT '',
    user_id PRIMARY KEY,
    msg_content CHAR(1000) NOT NULL DEFAULT '',
    msg_created_at TIMESTAMP NOT NULL DEFAULT ''
) """)

conn.commit()