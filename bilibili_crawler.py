"""
# Author: Richard Lu
# Project name: Bilibili Crawler
# Date Started: April 2020
# Contact: admin@richardlu.ca
# Repo: https://github.com/Sprit-Fun/Bilibili_Crawler
# Total Time used: 3 hours
# Last Updated: 2022/01/03
# Version: 1.01
"""

# This program can crawl Bilibili comments into a local file.
# Run the program with any Python interpreter to crawl comments.
# Special Thanks: https://blog.csdn.net/qq_44861455

import requests
import json
from time import sleep


print("Welcome to Bilibili Crawler V1.01 optimized by Richard Lu.")
print("Special thanks to aka.")

headers = {
    'User-Agent': 'XXX'
}

# BV Number.
bv = input('Please input the BV Number found directly on Bilibili (Format '
           'BV16f4y147Uz): ')
# Comment pages, 1 by default.
pn = 1
# 0 to sort by time, 2 to sort by most popular.
sort = int(input("Type 0 to crawl by time sorted, type 2 to crawl by most "
                 "popular comments sorted: "))

# BV and OID conversion algorithm.
judge = 0
table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


def dec(x: str):  # Input BV Number outputs OID
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58 ** i
    return (r - add) ^ xor


def enc(x: str):  # Input OID outputs BV Number.
    x = (x ^ xor) + add
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x // 58 ** i % 58]
    return ''.join(r)


# BV to OID
oid = dec(bv)
file_name = input("Which file name to save to, or create a new file if not "
                  "exist: ")
fp = open(file_name, "w", encoding="UTF-8")
i = 1

while True:
    url = f'https://api.bilibili.com/x/v2/reply?pn={pn}&type=1&oid=' \
          f'{oid}&sort={sort}'
    response = requests.get(url, headers=headers)
    a = json.loads(response.text)
    if pn == 1:
        count = a['data']['page']['count']
        size = a['data']['page']['size']
        page = count // size + 1
        print(str(page) + " pages in total, expected time to crawl: " +
              str(page * 1.5) + " seconds.")
    for b in a['data']['replies']:
        judge = 0
        str1 = ''
        str_list = list(b['content']['message'])
        for x in range(len(str_list)):
            if str_list[x] == '[':
                judge = 1
            if judge != 1:
                str1 = str1 + str_list[x]
            if str_list[x] == ']':
                judge = 0
        fp.write(str(i) + '、' + str1 + '\n' + '-' * 10 + '\n')
        i = i + 1
    if pn != page:
        pn += 1
    else:
        fp.close()
        break

print("All comments have been successfully crawled, please check the local "
      "file for crawled comments.")
print("Thanks for using the program.")
