import sqlite3
from random import shuffle

def insert_player(player_id, username): #+
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    sql = f"INSERT INTO players (player_id, username) VALUES ('{player_id}', '{username}')"
    cur.execute(sql)

    con.commit()
    con.close()
def players_amount():#+
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    sql = f'SELECT * FROM players'
    cur.execute(sql)
    res=cur.fetchall()
    con.commit()
    con.close()
    return len(res)
# print(players_amount())

def get_mafia():#+
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    sql = f"SELECT username FROM players where role = 'mafia'"
    cur.execute(sql)

    data=cur.fetchall()
    names = ''
    for row in data:
        name = row[0]
        names+=name +'\n'
    con.close()
    return names

def get_playeridrole():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT player_id, role FROM players"
    cur.execute(sql)
    data=cur.fetchall()
    
    con.close()
    return data

def get_name():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT username FROM players"
    cur.execute(sql)
    a=cur.fetchall()
    data = [row[0] for row in a]
    return data

def steall(player_id,username):
    con = sqlite3.connect("db1.db")
    cur = con.cursor()

    sql = f"INSERT INTO id (idtg, username) VALUES ('{player_id}', '{username}')"
    cur.execute(sql)

    con.commit()
    con.close()
# print(get_playeridrole())
def get_alive():
    con = sqlite3.connect("db.db")
    cur=con.cursor()
    sql=f'SELECT username FROM players where dead = 0'
    cur.execute(sql)
    a=cur.fetchall()
    data = [row[0] for row in a]
    return data

def set_roles(count):#+
    roles = ['citizen']*(count-1)
    roles.append('doctor')
    mafia = int(count*0.3)
    for i in range(mafia):
        roles[i]='mafia'
    shuffle(roles)

    con = sqlite3.connect("db.db")
    cur=con.cursor()
    sq = f'SELECT player_id FROM players'
    cur.execute(sq)
    data = cur.fetchall()
    
    for role,player_id in zip(roles,data):
        sql=f"UPDATE players SET role ='{role}' WHERE player_id = {player_id[0]}"    
        cur.execute(sql)
    con.commit()    
    con.close()

def vote(type,username,player_id):
    con = sqlite3.connect("db.db")
    cur=con.cursor()
    sql=f'SELECT username FROM players WHERE player_id = {player_id} and dead = 0 and voted=0'
    cur.execute(sql)
    data = cur.fetchone()
    if data:
        sql = f"UPDATE players SET voted=1 WHERE player_id = {player_id}"
        cur.execute(sql)
        sql1 = f"UPDATE players SET {type}={type}+1 WHERE username = '{username}'"
        cur.execute(sql1)
        con.commit()
        return True
    con.close()
    return False
# print(vote('citizen_vote', 'макасин',5182614316))
def mafia_kill():
    con = sqlite3.connect("db.db")
    cur=con.cursor()

    cur.execute(f'SELECT MAX(mafia_vote) FROM players')
    mafvote = cur.fetchone()[0]

    cur.execute(f"SELECT COUNT(*) FROM players WHERE dead=0 and role='mafia'")
    alive_mafia=cur.fetchone()[0]

    username_killed='никого'
    if mafvote==alive_mafia:
        cur.execute(f"SELECT username FROM players WHERE mafia_vote = {mafvote}")
        username_killed=cur.fetchone()[0]

        cur.execute(f"UPDATE players SET maf_dead=1, dead=1 WHERE username = '{username_killed}'")
    con.commit()
    con.close()
    return username_killed

def citizen_kill():
    con = sqlite3.connect("db.db")
    cur=con.cursor()

    cur.execute(f'SELECT MAX(citizen_vote) FROM players')
    citvote = cur.fetchone()[0]

    cur.execute(f"SELECT COUNT(*) FROM players WHERE dead =0 and citizen_vote = '{citvote}'")
    alive_cit=cur.fetchone()[0]

    username_killed='никого'
    if alive_cit==1:
        cur.execute(f"SELECT username FROM players WHERE citizen_vote = {citvote}")
        username_killed=cur.fetchone()[0]

        cur.execute(f"UPDATE players SET dead=1 WHERE username = '{username_killed}'")
    con.commit()
    con.close()
    return username_killed

def check_winner():
    con = sqlite3.connect("db.db")
    cur=con.cursor()

    cur.execute(f'SELECT COUNT(*) FROM players WHERE dead = 0 and role != "mafia"')
    citalive = cur.fetchone()[0]
    cur.execute(f'SELECT COUNT(*) FROM players WHERE dead = 0 and role = "mafia"')
    mafalive = cur.fetchone()[0]
    if mafalive >= citalive:
        return 'maf'
    elif mafalive <= 0:
        return 'cit'
    else:
        return 'рано еще'


def clear(dead=False):
    con = sqlite3.connect("db.db")
    cur=con.cursor()
    sql = f"UPDATE players SET citizen_vote=0, mafia_vote=0, voted=0, doctor_vote=0, maf_dead=0"
    if dead:
        sql+=', dead=0, d_voted=0'
    cur.execute(sql)
    con.commit()
    con.close()

def get_doctor():
    con = sqlite3.connect("db.db")
    cur=con.cursor()
    sql = f"SELECT username FROM players WHERE role='doctor'"
    cur.execute(sql)
    doc = cur.fetchone()[0]
    con.commit()
    con.close()
    return doc

def get_dead():
    con = sqlite3.connect("db.db")
    cur=con.cursor()
    sql = f"SELECT username FROM players WHERE dead=1"
    cur.execute(sql)
    dead = cur.fetchall()
    data = [row[0] for row in dead]
    con.commit()
    con.close()
    return data

# def heal(username):
#     con = sqlite3.connect("db.db")
#     cur=con.cursor()
#     cur.execute(f'SELECT username FROM players WHERE maf_dead=1')
#     dead = cur.fetchall()
#     data = [row[0] for row in dead]
#     if username in data:
#         cur.execute(f"UPDATE players SET dead=0, maf_dead=0 WHERE username = '{username}'")
#     con.commit()
#     con.close()

def heal(username,player_id):
    con = sqlite3.connect("db.db")
    cur=con.cursor()
    sql=f'SELECT username FROM players WHERE player_id = {player_id} and dead = 0 and d_voted=0'
    cur.execute(sql)
    data = cur.fetchone()[0]
    if data:
        sql = f"UPDATE players SET d_voted=1 WHERE player_id = {player_id}"
        cur.execute(sql)
        sql1 = f"UPDATE players SET doctor_vote=1 WHERE username = '{username}'"
        cur.execute(sql1)
        sql2=f'SELECT username FROM players WHERE maf_dead = 1'
        cur.execute(sql2)
        con.commit()
        data2 = cur.fetchall()
        if data2:
            cur.execute(f'SELECT username FROM players WHERE maf_dead=1')
            dead = cur.fetchall()
            data = [row[0] for row in dead]
            if username in data:
                cur.execute(f"UPDATE players SET dead=0, maf_dead=0, mafia_vote=0 WHERE username = '{username}'")
                con.commit()
    con.close()


def d_voted_mimo(player_id):
    con = sqlite3.connect("db.db")
    cur=con.cursor()
    sql = f"UPDATE players SET d_voted=1 WHERE player_id = {player_id}"
    cur.execute(sql)
    con.commit()
    con.close()
