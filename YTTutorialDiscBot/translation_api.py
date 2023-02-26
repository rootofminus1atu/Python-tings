import requests
import os
from dotenv import load_dotenv
load_dotenv()

url = "https://translated-mymemory---translation-memory.p.rapidapi.com/get"

text = "the one piece is real"

querystring = {
    "langpair": "cu|bruh",
    "q": text,
    "mt": "1",
    "onlyprivate": "0",
    "de": "a@b.c"}
headers = {
    "X-RapidAPI-Key": os.getenv('translation_key'),
    "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com"}


response = requests.request("GET", url, headers=headers, params=querystring).json()

print(response['responseData']['translatedText'])
print(response)

# how a sample response looks like
dictt = {
    'responseData': {
        'translatedText': "you don't have",
        'match': 0.99},
    'quotaFinished': False,
    'mtLangSupported': None,
    'responseDetails': '',
    'responseStatus': 200,
    'responderId': None,
    'exception_code': None,
    'matches': [
        {
            'id': '684743592',
            'segment': 'du hast mich',
            'translation': "you don't have",
            'source': 'de-DE',
            'target': 'en-US',
            'quality': '100',
            'reference': None,
            'usage-count': 2,
            'subject': '',
            'created-by': 'MateCat',
            'last-updated-by': '',
            'create-date': '2022-01-19 20:15:12',
            'last-update-date': '2022-01-19 20:15:12',
            'match': 0.99
        },
        {
            'id': 0,
            'segment': 'du hast mich',
            'translation': "you've got me",
            'source': 'de-DE',
            'target': 'en-GB',
            'quality': 70,
            'reference': 'Machine Translation.',
            'usage-count': 2,
            'subject': False,
            'created-by': 'MT!',
            'last-updated-by': 'MT!',
            'create-date': '2023-01-07 02:04:37',
            'last-update-date': '2023-01-07 02:04:37',
            'match': 0.85,
            'model': 'neural'
        }
    ]
}
