'''
    scraper.py
    Christopher Melville aka Spectacles aka Miacjeff aka clb

    Scrapes TFRRS for assorted information.
    The data is structured in roughly the following structure:

                        Conference
                        /     |
                       /      |
                     Teams    |
                        \     |
                         \    |
                        Athletes
                        /  |    \
                       /   |     \
                    Meets  Prs  RelevantPRs

    Meets is a list of dictionaries with the following fields:
    date, name (of meet not athlete therein), races (a list of dictionaries with fields distance and time)

    Prs is a list of {distance, time} dictionaries

    relevant Prs is a dictionary with fields {800,1500,5000}

    write_conference(id, sex) method writes giantass json object to file conferences/id_sex

'''

from bs4 import BeautifulSoup
import re
import requests
import sys
import csv
import json

athletenumber = 0

def get_text_tags(url, tag, text):
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'lxml')
    return soup.find_all(tag, string=text)

def get_attr_tags(url, tag, attributes):
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'lxml')
    return soup.find_all(tag, attrs=attributes)

#just the most used version of get_attr_tagss
def get_link_tags(url, link_type):
    return get_attr_tags(url, 'a', {'href':re.compile('tfrrs.org/'+link_type+'/')})


class Conference:
    def __init__(self, id, sex):
        self.id = id
        self.url = 'https://www.tfrrs.org/leagues/'+self.id+'.html'
        self.sex = sex
        self.name = self.find_name()
        print('creating conference...  '+self.name)
        self.athletes = self.create_athletes()

    def find_name(self):
        conference_tag = get_attr_tags(self.url, 'h3', {'class':'panel-title'})[0]
        return conference_tag.text

    def create_athletes(self):
        team_tags = get_link_tags(self.url, 'teams')
        athletes = []
        for team in team_tags:
            id = team['href'].split('/')[-1]
            if id.split('_')[2] != self.sex:
                continue
            name = team.text
            for athlete in Team(id, name).get_athletes():
                athletes.append(athlete)
        return athletes

    def get_json(self):
        return {'name':self.name,
        'id':self.id+'_'+self.sex,
        'athletes':self.athletes}


class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        print('creating team: '+name)
        self.athletes = self.create_athletes()
        print('created team: '+name)

    def create_athletes(self):
        roster_tag = get_text_tags('https://www.tfrrs.org/teams/'+self.id, 'h3', 'ROSTER')[0]
        roster = roster_tag.next_sibling.next_sibling.contents[3].contents
        roster_length = len(roster)
        athletes = []
        for i in range(1, roster_length, 2):
            link_tag = roster[i].contents[1].contents[1]
            try:
                athletes.append(Athlete(link_tag['href'], link_tag.text, self.name).get_json())
            except:
                pass
        return athletes

    def get_athletes(self):
        return self.athletes

class Athlete:
    def __init__(self, url, name, team):
        self.url = 'https://tfrrs.org'+url
        self.name = self.straighten_name(name)
        global athletenumber
        print(self.name+" "+str(athletenumber))
        athletenumber+=1
        self.team = team
        self.meets = self.create_meets()
        self.prs = self.create_prs()
        self.relevant_prs = self.create_relevant_prs(self.prs)

    def straighten_name(self, name):
        name_list = name.split(', ')
        return name_list[1].strip()+' '+name_list[0].strip()

    def regularize_date(self, date):
        months = {'Jan':0,'Feb':31,'Mar':59,'Apr':90,'May':120,'Jun':151,
        'Jul':181,'Aug':212,'Sep':243,'Oct':263,'Nov':294,'Dec':324}
        splith = date.split()
        return str(months[splith[0]]+int(splith[1][:-1].split('-')[0]))+' '+splith[-1]

    def regularize_time(self, time):
        mins_seconds = time.split(':')
        if(len(mins_seconds) == 1):
            return round(float(mins_seconds[0]),2)
        return round(60*float(mins_seconds[0])+float(mins_seconds[1]),2)


    def create_meets(self):
        meets = []
        meets_tags = get_attr_tags(self.url, 'div', {'id':'meet-results'})[0].contents
        meets_length = len(meets_tags)
        for i in range(3, meets_length, 2):
            meet_header_tag = meets_tags[i].contents[1].contents[1]
            meets.append(self.create_meet(meet_header_tag))
        return meets


        
        

    def create_meet(self, table_head_tag):
        meet_tag = table_head_tag.contents[1].contents[1].contents[1]
        name = meet_tag.text
        date = meet_tag.next_sibling.next_sibling.text.split(';')[-1].strip()
        meet = {'name':name,
        'date':date,
        'num_date':self.regularize_date(date),
        'races':[]}
        race_tag = table_head_tag
        while True:
            try:
                race_tag = race_tag.next_sibling.next_sibling
                meet['races'].append(self.create_race(race_tag))
            except:
                break
        return meet

    def create_race(self, row_tag):
        distance_tag = row_tag.contents[1]
        distance = distance_tag.text.strip()
        time_tag = distance_tag.next_sibling.next_sibling.contents[1]
        time = time_tag.text.strip()
        return {'distance':distance,
        'time':self.regularize_time(time)}


    '''Most of these prs will never get used, but this still should exist for whenever
    I want to switch up which races make the relevant_prs cut
    '''
    def create_prs(self):
        table_tag_contents = get_attr_tags(self.url, 'div', {'class':'col-lg-8'})[0].contents[1].contents
        table_length = len(table_tag_contents)
        prs = []
        for i in range(1, table_length, 2):
            row_tag_contents = table_tag_contents[i].contents
            for j in range(2):
                distance_tag = row_tag_contents[8*j+3]
                pr = self.create_pr(distance_tag)
                if pr == None:
                    #if self.name == "Josh Meier":
                        #print("Uh oh")
                    break
                prs.append(pr)
        return prs

    def create_pr(self, distance_tag):
        distance = distance_tag.text.strip().replace('\n','').replace(' ','')
        try:
            time_tag = distance_tag.next_sibling.next_sibling.contents[1]
            #if self.name == "Josh Meier" and distance == "200":
              #  print(time_tag)
            time = time_tag.contents[1].text.strip()
            return {'distance':distance,
            'time':self.regularize_time(time)}
        except:
            #if self.name == "Josh Meier":
                #print(str(distance_tag))
                #print("That was jms distance tag")
            return None

    def create_relevant_prs(self, prs):
        relevant_distances = ['800','1000','1500','MILE','3000','3000S','5000','10,000']
        relevant_prs = {}
        for relevant_distance in relevant_distances:
            relevant_prs[relevant_distance] = 100000
        for pr in prs:
            if pr['distance'] in relevant_distances:
                relevant_prs[pr['distance']] = pr['time']
        return relevant_prs

    def get_json(self):
        return {'name':self.name,
        'team':self.team,
        'relevant_prs':self.relevant_prs,
        'meets':self.meets}

def write_conference(id, sex):
    with open('data/conferences/'+id+'_'+sex, 'w') as file:
        file.write(json.dumps(Conference(id, sex).get_json()))


write_conference('1408','m')
#write_conference('1408','f')
