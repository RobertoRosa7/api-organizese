
# -*- coding: utf-8 -*-
import bs4
import requests
import re
import asyncio


async def get_status_code():
  URLS = ['https://kinsta.com/pt/blog/lista-codigos-status-http/']
  
  res = requests.get(URLS[0])
  res.raise_for_status()
  soup = bs4.BeautifulSoup(res.text, 'html.parser')
  elements = soup.select('ul li')
  data = await making_data(elements)

  return data


async def making_data(elements):
  data = []
  for el in range(len(elements)):
    text = elements[el].text.strip()
    text_match = re.compile(r"\d\d\d:(.*)", re.DOTALL)
    status_match = re.compile(r"\d\d\d", re.DOTALL)

    result = text_match.search(text)
    status_result = status_match.search(text)

    if result != None:
      data.append({
        'status': int(status_result.group()),
        'text': result.group()
      })

  return data


asyncio.run(get_status_code())