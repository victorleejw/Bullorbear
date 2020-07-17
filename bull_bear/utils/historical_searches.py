'''
---Historical Searches Theory---
Return 5 ramdom link that timestamp within 24 hours
If link that timestamp within 24 hours < 5, remaining will be random link that over 24 hours
If no link that timestamp within 24 hours, all will be random link that over 24 hours
Save link (this action put at last to prevent same link appear at historical search results)
'''

from pandas import read_csv, to_datetime
from datetime import datetime, timedelta
from random import sample

# Previous criteria: data science module return True
def main(link):

    LINK_COUNT = 5

    link_data_df = read_csv('./bull_bear/utils/historical_searches_data.csv')
    link_data_df['timestamp'] = to_datetime(link_data_df['timestamp']) # Change timestamp column datatype to timestamp

    # Get 5 link which had been searched within 24 hours
    hours_24 = timedelta(hours=24)
    within_24_hours = link_data_df['timestamp'] > (datetime.now() - hours_24)
    searches_df = link_data_df.loc[within_24_hours]
    searches_list = searches_df['link'].values.tolist()
    searches_list_count = len(searches_list)
    if searches_list_count >= LINK_COUNT:
        random_index_list = sample(range(searches_list_count), LINK_COUNT) # 5 random index without duplicate(index)
        random_searches_link = [searches_list[index] for index in random_index_list]

    else: # Not enough 5 search link within 24 hours
        over_24_hours = link_data_df['timestamp'] < (datetime.now() - hours_24)
        searches_over_24hours_df = link_data_df.loc[over_24_hours]
        searches_over_24hours_list = searches_over_24hours_df['link'].values.tolist()
        searches_over_24hours_list_count = len(searches_over_24hours_list)
        
        if searches_list_count != 0: # less than 5 link within 24 hours but not 0 link
            random_searches_link = searches_list
            random_index_list = sample(range(searches_over_24hours_list_count), LINK_COUNT - searches_list_count)
            random_searches_link_remaining = [searches_over_24hours_list[index] for index in random_index_list]
            random_searches_link = random_searches_link + random_searches_link_remaining # Make it 5 search link

        else: # no link within 24 hours
            random_index_list = sample(range(searches_over_24hours_list_count), LINK_COUNT)
            random_searches_link = [searches_over_24hours_list[index] for index in random_index_list]

    # Save search history
    timestamp = datetime.now()
    link_data_df = link_data_df.append({'link': link, 'timestamp': timestamp}, ignore_index=True)
    link_data_df.to_csv('./bull_bear/utils/historical_searches_data.csv', index=False)

    return random_searches_link # 5 link in list
