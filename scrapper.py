#!/usr/bin/env python3
# coding=utf-8

import requests
from urlparse import urljoin
from bs4 import BeautifulSoup as bs

URL = 'http://www.sports-reference.com/olympics/'


def compose_url(season, year=None, sport=None):
    if year and sport:
        return urljoin(URL, season + '/' + year + '/' + sport)
    elif year:
        return urljoin(URL, season + '/' + year)
    else:
        return urljoin(URL, season)


def html_from(url):
    return bs(requests.get(url).text, "lxml")


class Medal:

    def __init__(self, metal, winner, country):
        self.metal = metal
        self.winner = winner
        self.country = country

    @classmethod
    def from_cell(cls, cell, metal):
        return None if len(cell.contents) == 0 else cls(
            winner=cell.find_all('a', href=True)[0].find(text=True),
            country=cell.findAll('img')[0].get('title'),
            metal=metal,
        )

    def __repr__(self):
        return "{} ({}) from {}".format(self.winner, self.metal, self.country)


class Event:

    def __init__(self, name, gold=None, silver=None, bronze=None):
        self.name = name
        self.gold = gold
        self.silver = silver
        self.bronze = bronze

    @property
    def medals(self):
        return filter(None, [self.gold, self.silver, self.bronze])

    @classmethod
    def from_row(cls, row):
        cells = row.findAll("td")
        return cls(
            name=cells[0].find(text=True),
            gold=Medal.from_cell(cells[1], 'Gold'),
            silver=Medal.from_cell(cells[2], 'Silver'),
            bronze=Medal.from_cell(cells[3], 'Bronze'),
        )

    def __repr__(self):
        return """Event: {}
        {}
        {}
        {}
        """.format(self.name, self.gold, self.silver, self.bronze)


class Sport:

    def __init__(self, olympic, name, identifier):
        self.olympic = olympic
        self.name = name
        self.identifier = identifier

    @property
    def events(self):
        html = html_from(compose_url(self.olympic.season,
                                     self.olympic.year,
                                     self.identifier))
        table = html.find('table', attrs={'id': 'medals'})
        for row in table.find('tbody').find_all('tr'):
            yield Event.from_row(row)

    @classmethod
    def from_row(cls, row, olympic):
        cells = row.findAll("td")
        a = cells[0].find_all('a', href=True)[0]
        return cls(
            name=a.find(text=True),
            identifier=a['href'].split('/')[-2],
            olympic=olympic,
        )

    def __repr__(self):
        return "{} ({}) ({})".format(
            self.name, self.identifier, self.olympic.year)


class Olympic:

    def __init__(self, season, year, city, country, countries, participants,
                 men, women, sports, events):

        self.season = season
        self.year = year
        self.city = city
        self.country = country
        self.countries = countries
        self.participants = participants
        self.men = men
        self.women = women
        self.events = events
        self.sport_count = sports

    @property
    def sports(self):
        html = html_from(compose_url(self.season, self.year))
        table = html.find('table', attrs={'id': 'sports'})
        for row in table.find_all('tr'):
            yield Sport.from_row(row, self)

    @classmethod
    def from_row(cls, row, season):
        cells = row.findAll("td")
        return cls(
            season=season,
            year=cells[0].find(text=True),
            city=cells[1].find(text=True),
            country=cells[2].find(text=True),
            countries=cells[3].find(text=True),
            participants=cells[4].find(text=True),
            men=cells[5].find(text=True),
            women=cells[6].find(text=True),
            sports=cells[7].find(text=True),
            events=cells[8].find(text=True),
        )

    @classmethod
    def load_all(cls, season):
        html = html_from(compose_url(season))
        table = html.find('table', attrs={'id': season.capitalize()})
        for row in table.find('tbody').find_all('tr'):
            yield cls.from_row(row, season)

    def __repr__(self):
        return "{} - {}, {}".format(self.year, self.country, self.city)
