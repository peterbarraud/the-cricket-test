from libs.dataclasses import VenueInfo
from csv import DictReader

def get_venue_info(venue_data,teams_dict):
    venue_info : VenueInfo = VenueInfo(venue_data['id'],venue_data['name'],venue_data['city'])
    venue_info.Country = list({i:j for i,j in teams_dict.items() if j == venue_data['country']})[0]
    return venue_info
    
def get_venuecsv_dict():
    teams_dict : dict = dict()
    with open('data/venues.csv') as f:
        for row in DictReader(f,delimiter='|'):
            teams_dict[int(row['id'])] = VenueInfo(row['id'],row['name'],row['city'],row['country'])
    return teams_dict
