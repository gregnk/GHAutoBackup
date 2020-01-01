'''
GHAutoBackup v1.0.0 (2019-12-31)
https://github.com/gregnk/GHAutoBackup
By Gregory Karastergios

Description: A script which automatically backs up a bunch of git repositories
Requirements: git cli, python 3.7+
Usage: py GHAutoBackup.py [-debug]
Copyright:
(c) 2019 Gregory Karastergios

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

'''
Links.txt format

    <Type> <Link> 

Types:
    Repo: Single git repo (can be on any site)
    User: Github user
    Org:  Github organization

Example:
    Repo http://github.com/SomeGHUser/SomeRepo
    Repo http://git.somewebsite.com/SomeRepo
    User http://github.com/SomeGHUser
    Org http://github.com/SomeGHOrg
'''

#!/usr/bin/python3

import os
import sys
import json
import urllib.request

def backupRepo(repo):
    # Allow git output if specified
    if (len(sys.argv) > 1):
        debug = "" if (sys.argv[1] == "-debug") else " >nul 2>&1"
    else:
        debug = " >nul 2>&1"

    # Clone the repo
    os.system("git clone %s%s" % (repo, debug))

    # Update the repo
    os.chdir(os.path.basename(repo))
    os.system("git pull %s%s" % (repo, debug))
    os.chdir("..")

    print("Done: %s" % repo)

def cloneGithubRepoList(jsonString):
    # Get each repo link from the Json
    for object in json.loads(jsonString):
        print("Repo: %s" % object["html_url"])
        backupRepo(object["html_url"])

def filterGithubLink(link):
    name = ""

    # Remove the url part
    if (link[:18] == "http://github.com/"):
        name = link[18:len(link)]
    elif (link[:19] == "https://github.com/"):
        name = link[19:len(link)]

    # Remove any leading foreward slash
    if (name[len(name) - 1:len(name)] != "/"):
        name = name[:len(name)]
    else:
        name = name[:len(name) - 1]

    return name

def checkGithubLink(link):
    if (link[:18] == "http://github.com/"):
        return True
    elif (link[:19] == "https://github.com/"):
        return True

    return False

print("GHAutoBackup")
print("(c) 2019 Gregory Karastergios")
print("")

# Open the link list and format each line into an array
with open("Links.txt") as file:
    lines = file.read().splitlines() 

# Create backup dir if it doesn't already exist
if (os.path.isdir("Backup") == False):
    os.mkdir("Backup")

# Go into that dir
os.chdir("Backup")

# Go though each link
for line in lines:
    # Project (Single repo)
    if (line[:4] == "Repo"):
        link = line[5:len(line)]
        print("Repo: %s" % link)
        
        # Create the user folder if on Github
        if (checkGithubLink(link) == True):
            folderName = "_GHUser_%s" % filterGithubLink(link).split("/")[0]
            if (os.path.isdir(folderName) == False):
                os.mkdir(folderName)
            os.chdir(folderName)

            backupRepo(link)

            os.chdir("..")
        else:
            backupRepo(link)

    # User (All repos)
    elif (line[:4] == "User"):
        link = line[5:len(line)]
        print("User: %s" % link)

        name = filterGithubLink(link)
        folderName = "_GHUser_%s" % name;
        ghApiLink = "https://api.github.com/users/%s/repos?per_page=1000" % name

        if (os.path.isdir(folderName) == False):
            os.mkdir(folderName)
        os.chdir(folderName)

        cloneGithubRepoList(urllib.request.urlopen(ghApiLink).read())

        os.chdir("..")
        print("Done: %s" % link)
        
    # Organization (All repos)
    elif (line[:3] == "Org"):
        link = line[4:len(line)]
        print("Org: %s" % link)

        name = filterGithubLink(link)
        folderName = "_GHOrg_%s" % name;
        ghApiLink = "https://api.github.com/orgs/%s/repos?per_page=1000" % name

        if (os.path.isdir(folderName) == False):
            os.mkdir(folderName)
        os.chdir(folderName)

        cloneGithubRepoList(urllib.request.urlopen(ghApiLink).read())

        os.chdir("..")
        print("Done: %s" % link)

# Display done message
print("=============")
print("Done")