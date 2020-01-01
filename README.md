# GHAutoBackup
A script which automatically backs up a bunch of git repositories

## Requirements
* Git CLI
* Python 3.7+

## Usage
	py GHAutoBackup.py [-debug]

The program will archive all of the links listed in `Links.txt` (See below)

## Links.txt Format

    <Type> <Link>

### Types

    Repo: Single git repo (can be on any site)
    User: Github user
    Org:  Github organization

### Example
    Repo http://github.com/SomeGHUser/SomeRepo
    Repo http://git.somewebsite.com/SomeRepo
    User http://github.com/SomeGHUser
    Org http://github.com/SomeGHOrg
	
## Copyright
(c) 2019 Gregory Karastergios

This program is distributed under the ISC License. See LICENSE.md for more details.