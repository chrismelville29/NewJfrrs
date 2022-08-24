import json


class League:
    def __init__(self, conference, name):
        self.conference = json.loads(open('data/conferences/'+conference,'r').read())
        self.athletes = self.conference['athletes']
        for athlete in self.athletes:
            athlete['manager'] = 'Nobody'
        self.name = name
        self.managers = {}
        self.weeks = []
        self.events = ['800','1000','Mile','3000','5000']
        self.test()

    def __str__(self):
        return_string = 'Name of league is ' + self.name +'.\nHere are the managers:'
        for name, manager in self.managers.items():
            return_string += '\n'+name+' has the following athletes: '
            for athlete in manager.get_athletes():
                return_string += '\n'+athlete['name']
        return return_string

    def add_manager(self, name):
        self.managers[name] = Manager(name)

        print('creating manager '+name)

    def get_json():
        return {'name':self.name,
        'managers':self.managers,
        'weeks':self.weeks}

    def test(self):
        self.add_manager('Jerry')
        self.add_manager('Jerome')
        self.add_manager('Jerald')
        self.add_manager('Jeronimo')
        self.add_manager('Jersson')
        self.add_manager('Jeremy')
        self.managers['Jerry'].add_athlete(self.athletes[49])
        self.managers['Jerry'].add_athlete(self.athletes[222])
        self.managers['Jerry'].add_athlete(self.athletes[179])
        self.managers['Jerome'].add_athlete(self.athletes[164])
        self.managers['Jerome'].add_athlete(self.athletes[134])
        self.managers['Jerome'].add_athlete(self.athletes[122])
        self.managers['Jerald'].add_athlete(self.athletes[130])
        self.managers['Jerald'].add_athlete(self.athletes[94])
        self.managers['Jerald'].add_athlete(self.athletes[92])
        self.managers['Jeronimo'].add_athlete(self.athletes[93])
        self.managers['Jeronimo'].add_athlete(self.athletes[82])
        self.managers['Jeronimo'].add_athlete(self.athletes[91])
        self.managers['Jersson'].add_athlete(self.athletes[404])
        self.managers['Jersson'].add_athlete(self.athletes[419])
        self.managers['Jersson'].add_athlete(self.athletes[366])
        self.managers['Jeremy'].add_athlete(self.athletes[344])
        self.managers['Jeremy'].add_athlete(self.athletes[334])
        self.managers['Jeremy'].add_athlete(self.athletes[262])
        test_week = Week('26 2022',self.managers,self.events)
        print(test_week)



class Manager:
    def __init__(self, name):
        self.name = name
        self.athletes = []

    def __str__(self):
        to_string = 'Hi my name is '+self.name+' and here are my athletes:'
        for athlete in self.athletes:
            to_string+='\nAthlete name: '+athlete['name']
        return to_string

    def get_name(self):
        return self.name

    def get_athletes(self):
        return self.athletes

    def add_athlete(self, athlete):
        self.athletes.append(athlete)
        athlete['manager'] = self.name

    def is_in_week(self, start_date, test_date):
        start_day = int(start_date.split()[0])
        test_day = int(test_date.split()[0])
        start_year = start_date.split()[1]
        test_year = test_date.split()[1]
        return test_day >= start_day and test_day-7 < start_day and start_year == test_year

    def get_week_races(self, start_day):
        races = []
        for athlete in self.athletes:
            for meet in athlete['meets']:
                if not self.is_in_week(start_day,meet['num_date']):
                    continue
                for race in meet['races']:
                    races.append({'manager':self.name,
                    'athlete':athlete['name'],
                    'distance':race['distance'],
                    'time':race['time'],
                    'meet':meet['name'],
                    'date':meet['date'],
                    'score':0})
        return races


class Week:
    def __init__(self, start_day, managers, events):
        self.start_day = start_day
        self.managers = managers
        self.races = self.sort_races(events)
        self.score_races()


    def __str__(self):
        to_string = 'week starting on day '+self.start_day+'\n'
        for event, races in self.races.items():
            to_string+='The races in the following event: '+event+'. There are '+str(len(races))+' races.\n'
            for race in races:
                to_string+=race['manager']+' is manager for '+race['athlete']+"'s " +str(race['time'])+' which scored '+str(race['score'])+' points. \n'
        return to_string

    def sort_races(self, events):
        races = {}
        for event in events:
            races[event] = []
        for name, manager in self.managers.items():
            for race in manager.get_week_races(self.start_day):
                if race['distance'] in events:
                    races[race['distance']].append(race)
        for event in races:
            races[event].sort(key = lambda race: (race['time'],race['date']))
        return races

    def score_races(self):
        values = [7,4,2,1]
        for event in self.races.values():
            scorers = min(len(values),len(event))
            for i in range(scorers):
                event[i]['score'] = values[i]





def test():
    the_league = League('1408_m', 'The League')
    print(the_league)

test()
