import praw
import easygui
import sys
import pprint
import csv
import os
from shorttext.utils import standard_text_preprocessor_1


def manualsortsubs(listofsubs):
    preprocessor1 = standard_text_preprocessor_1()
    choices = ["nothing", "askedbefore", "premisewrong"] #TODO: decide on choices
    title = "Choose category"
    classdict = {"nothing": [], "askedbefore": [], "premisewrong": []}
    for sub in listofsubs:
        choice = easygui.buttonbox(sub, title, choices)
        if choice is None:
            sys.exit(0)
        else:
            classdict[choice].append(preprocessor1(sub))
    return classdict


def write_to_csv(sorted_dict):
    with open('dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=",", lineterminator='\n')
        for key, value in sorted_dict.items():
            for subitem in value:
                writer.writerow([key, subitem])


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
    clientid = "secret"
    clientsecret = "secret"
    pwd = "secret"
    useragent = "testscript by /u/elibeforebot"
    usern = "elibeforebot"
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
                unsortedsubs.append(rethread.title + " " + rethread.selftext)
                already_done.add(rethread.id)
        classdict = manualsortsubs(unsortedsubs)
        write_to_csv(classdict)
        return classdict


def main():
    classdict = get_submissions(25)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(classdict)


if __name__ == "__main__":
    main()
