# The title of each of your projects
# The date for each project
# The version for each project
# The summary for each project (the most recent commit message for that assignment)
# A listing of each file in the project with
# Its size
# The type of the file: is one of code, test, image, documentation, resource, etc (feel free to add as many types as you wish).
# The path is the path to your files in SVN.
# The file itself loaded in an iframe only on demand
# Each version of each file in the project
# The number is the revision number for that commit
# The author is the netid of the committer
# The info is the commit message for that revision
# The date is the date of that commit
import xml.etree.ElementTree as ET
import re
from sets import Set

#parse bot the svn_list.xml and svn_log.xml
def parse_svn():
    #list of dictionaries holding information about each entry
    svn_list = []

    tree = ET.parse('svn_list.xml')
    root = tree.getroot()
    #Parsing for svn_list.xml
    for child in root.findall('list'):
        Assignment = ""
        #For each entry we will iterate through see if its an assignment or file path and store all its informations
        for entry in child.findall('entry'):
            entry_dict = {}
            #Checking with Regex to get assignment name
            if re.match("Assignment...$" , entry.find('name').text) is not None:
                entry_dict["assignment"] = entry.find('name').text
                Assignment = entry.find('name').text
            #one case where we named it differently
            elif re.match("assignment.$" , entry.find('name').text) is not None:
                entry_dict["assignment"] = entry.find('name').text
                Assignment = entry.find('name').text
            else:
                entry_dict["belongs"] = Assignment
                entry_dict["filepath"] = entry.find('name').text
            #For each commit in entry itreate through getting the kind,filename,file path
            for commit in entry.findall('commit'):
                entry_dict["kind"] =entry.get('kind')
                if entry.get('kind') == "file":
                    name = entry.find('name').text
                    name = name.split('/')[-1]
                    entry_dict["filename"] = name
                    filetype = name.split('.')[-1]
                    entry_dict["filetype"] = filetype
                if entry.find('size') != None:
                    entry_dict["size"] = entry.find('size').text
                entry_dict["author"] = commit.find('author').text
                entry_dict["date"] = commit.find('date').text

                #Get date information and put it in proper format
                date = commit.find('date').text
                date = date.split('T')
                date_time = date[1].split('Z')
                date_time = date_time[0].split(':')
                date_sub = date[0].split('-')
                year = date_sub[0]
                month = date_sub[1]
                day = date_sub[2]
                hour = date_time[0]
                minute = date_time[1]
                second = date_time[2]
                entry_dict["year"] = year
                entry_dict["month"] = month
                entry_dict["day"] = day
                entry_dict["hour"] = hour
                entry_dict["minute"] = minute
                entry_dict["second"] = second

                entry_dict["revision"] = commit.get('revision')
            svn_list.append(entry_dict)

    tree_log = ET.parse('svn_log.xml')
    root_log = tree_log.getroot()
    #list of dictionaries holding information about each entry
    svn_log = []


    #Parsing for svn_log.xml
    for child in root_log.findall('logentry'):
        Assignment = ""

        entry_dict = {}
        date_low = 0
        time_low = 0

        for paths in child.findall('paths'):
           entry_dict["path"] = []
           #Go through all paths for a log entry
           for path in paths.findall('path'):
               assign = path.text.split('/')
               entry_dict["path"].append(path.text)

               if len(assign) > 3:
                   if re.match("Assignment...$" , assign[2]) is not None or re.match("assignment.$" , assign[2]) is not None:

                       entry_dict["assignment"] = assign[2]
           entry_dict["date"] = child.find('date').text
           #Some python splicing to get day,year,month HH:MM:SS format
           #LOOK for python date string object convertor
           date = child.find('date').text
           date = date.split('T')
           date_time = date[1].split('Z')
           date_time = date_time[0].split(':')
           date_sub = date[0].split('-')
           year = date_sub[0]
           month = date_sub[1]
           day = date_sub[2]
           hour = date_time[0]
           minute = date_time[1]
           second = date_time[2]
           time = ('').join(date_time)
           date = ('').join(date_sub[1:3])
           #Storing all revision for current entry
           entry_dict["revision"] = child.get('revision')
           entry_dict["author"] = child.find('author').text
           entry_dict["year"] = year
           entry_dict["month"] = month
           entry_dict["day"] = day
           entry_dict["hour"] = hour
           entry_dict["minute"] = minute
           entry_dict["second"] = second
           entry_dict["message"] = child.find('msg').text
           date_low = date

           svn_log.append(entry_dict)



    return (svn_list,svn_log)
svn_list = parse_svn()
