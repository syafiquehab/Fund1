#!/usr/bin/env python3
# coding=utf-8

from scrapper import Olympic
import pandas as pd

__author__ = ['Patricio Lopez', 'Francesca Lucchini']


def olimpic_to_dic(element):
    return {
        'year': element.year,
        'city': element.city,
        'country': element.country,
        'participants': element.participants,
        'men': element.men,
        'women': element.women,
        'sport': element.sport_count,
        'events': element.events
    }


if __name__ == '__main__':
    olimpics = Olympic.load_all(season='summer')
    data_olimpics = [olimpic_to_dic(o) for o in olimpics]
    t1 = pd.DataFrame(data_olimpics)
    t1.to_csv('olimpics.csv', encoding='utf-8')

    olimpics = Olympic.load_all(season='summer')
    full_data = []
    for olimpic in olimpics:
        for sport in olimpic.sports:
            for event in sport.events:
                for medal in event.medals:
                    full_data.append({
                        'year': olimpic.year,
                        'sport': sport.name,
                        'event': event.name,
                        'medal': medal.metal,
                        'winner': medal.winner,
                    })

    t2 = pd.DataFrame(full_data)
    t2.to_csv('full_data.csv', encoding='utf-8')
