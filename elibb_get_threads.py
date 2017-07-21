import praw
import easygui
import sys
import pprint
import csv
import os
import sqlite3
from shorttext.utils import standard_text_preprocessor_1
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


def manualsortsubs(listofsubs):
    preprocessor1 = standard_text_preprocessor_1()
    choices = ["nothing", "askedbefore", "premisewrong", "stupid", "selfanswered"]  # TODO: decide on choices
    title = "Choose category"
    classdict = {}
    for choice in choices:
        classdict[choice] = []
    for sub in listofsubs:
        choice = easygui.buttonbox(sub[0], title, choices)
        if choice is None:
            sys.exit(0)
        else:
            classdict[choice].append([preprocessor1(sub[0]), sub[1]])
    return classdict


def write_to_sqlite(sorted_dict):
    conn = sqlite3.connect('prepdata.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''create table if not exists submissions (submission text, category text, id text, likes integer)''')
    for key, value in sorted_dict.items():
        for subitem in value:
            # check if submission already exists
            cur.execute('''select * from submissions where id = ?''', [subitem[1]])
            res = cur.fetchall()
            print(res)
            if not res:
                cur.execute('''insert into submissions values (?,?,?,?)''', (subitem[0], key, subitem[1], 0))
    conn.commit()
    cur.close()
    conn.close()


def write_to_csv(sorted_dict):
    with open('dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=",", lineterminator='\n')
        for key, value in sorted_dict.items():
            for subitem in value:
                writer.writerow([key, subitem[0]])


def read_from_sqlite(fpath="prepdata.db"):
    classdict = {}
    conn = sqlite3.connect(fpath)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''select * from submissions''')
    res = cur.fetchall()
    for row in res:
        try:
            classdict[row["category"]].append(row["submission"])
        except KeyError:
            classdict[row["category"]] = [row["submission"]]

    pp = pprint.PrettyPrinter(indent=4)
    for row in res:
        pp.pprint(dict(row))
    pp.pprint(classdict)


def read_from_csv(fpath="dict.csv"):
    classdict = {}
    temprow = None
    with open(fpath, "r") as csv_file:
        reader = csv.reader(csv_file)
        print(dir(reader))
        for row in reader:
            temprow = list(row)
            try:
                if temprow[0] not in classdict:
                    classdict[temprow[0]] = []
                classdict[temprow[0]].append(temprow[1])
            except IndexError:
                print(row)

        return classdict


def get_subreddit(sreddit):
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read("reddit.cfg")
    clientid = config.get("reddit", "clientid")
    clientsecret = config.get("reddit", "clientsecret")
    pwd = config.get("reddit", "password")
    useragent = config.get("reddit", "useragent")
    usern = config.get("reddit", "user")
    reddit = praw.Reddit(client_id=clientid,
                         client_secret=clientsecret,
                         password=pwd,
                         user_agent=useragent,
                         username=usern)
    print(reddit.user.me())
    return reddit.subreddit(sreddit)


def get_submissions(sublimit=None):
    if os.path.isfile("dict.csv"):
        return read_from_csv("dict.csv")
    else:
        elisub = get_subreddit("explainlikeimfive")
        already_done = set()
        unsortedsubs = []
        for rethread in elisub.new(limit=sublimit):  # limit=None
            if rethread.id not in already_done:
                unsortedsubs.append([rethread.title + " " + rethread.selftext, rethread.id])
                already_done.add(rethread.id)
        classdict = manualsortsubs(unsortedsubs)
        # write_to_csv(classdict)
        write_to_sqlite(classdict)
        return classdict


def main():
    # conn = sqlite3.connect('prepdata.db')
    # conn.row_factory = sqlite3.Row
    # cur = conn.cursor()
    classdict = get_submissions(25)
    read_from_sqlite()
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(classdict)


if __name__ == "__main__":
    main()
