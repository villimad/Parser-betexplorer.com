import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *


class Pars:

    def __init__(self, sport, param):

        self.url = 'https://www.betexplorer.com/'
        self.sport = self.url + sport + '/'
        self.today = 'https://www.betexplorer.com/next/' + sport + '/'
        self.count_arr = []
        self.param = param
        pass

    def clear(self):
        self.sport = ''
        self.count_arr = []
        pass

    def liga(self):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76'}
        http_proxy = "http://1.0.0.112:80"

        res = requests.get(self.sport, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        poisk1 = soup.find('ul', class_='list-events js-upcoming js-upcoming-left').find_all('li')
        poisk2 = soup.find('ul', class_='list-events js-upcoming js-upcoming-right').find_all('li')
        poisk = poisk1 + poisk2
        count_arr = []
        for q in range(0, len(poisk)):
            try:
                name_count = poisk[q].find('div').find('strong')
                if name_count != None:
                    name_arr = []
                    name_arr.append(name_count.text)
                else:
                    continue
                liga_arr = poisk[q].find('ul').find_all('a', class_='list-events__item__title')
                liga_count_arr = []
                for i in range(0, len(liga_arr)):
                    try:
                        liga_name_url = []
                        liga_name = liga_arr[i].text
                        liga_url = liga_arr[i].get('href')
                        liga_url = 'https://www.betexplorer.com' + liga_url
                        liga_name_url.append(liga_name)
                        liga_name_url.append(liga_url)
                        liga_count_arr.append(liga_name_url)
                    except:
                        ggg = 1
                name_arr.append(liga_count_arr)
                count_arr.append(name_arr)

            except Exception as e:
                gg = 1
            pass

        self.count_arr = count_arr

        pass

    def match(self):

        def get_table(url):

            k = requests.get(url)

            sp = BeautifulSoup(k.text, 'html.parser')

            poi = sp.find('a', class_="wrap-section__header__link").get('onclick')

            poi = poi.split("'")[1]
            print(poi)

            # url запроса

            headers = {

                'Host': 'www.betexplorer.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                'Referer': url,
                'Cache-Control': 'max-age=0, no-cache'

            }

            url_get = 'https://www.betexplorer.com/gres/ajax/mutual-matches.php?par=' + str(poi)

            result = requests.get(url_get, headers=headers)

            return result.text

        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76'}

        f = open('table.csv', 'a', encoding='cp1251', newline='')

        k1 = 'Кол-во матчей сыгранных больше ' + str(self.param)
        k2 = 'Кол-во матчей сыгранных меньше ' + str(self.param)
        k3 = 'Кол-во мячей в играх где счет больше ' + str(self.param)


        data = {'Команда 1': ['Команда 1'], 'Команда 2': ['Команда 2'],
                'Общее кол-во матчей': ['Общее кол-во матчей'],
                'Общее кол-во мячей': ['Общее кол-во мячей'],
                'Общее кол-во побед 1 команды': ['Общее кол-во побед 1 команды'],
                'Общее кол-во ничьих': ['Общее кол-во ничьих'],
                'Общее кол-во побед 2 команды': ['Общее кол-во побед 2 команды'],
                str(k1): [str(k1)],
                str(k2): [str(k2)],
                str(k3): [str(k3)],

                'Кол-во матчей где в счете нет нуля': ['Кол-во матчей где в счете нет нуля'],
                'Кол-во мячей забитых командой 1': ['Кол-во мячей забитых командой 1'],
                'Кол-во мячей забитых командой 2': ['Кол-во мячей забитых командой 2'],
                '': ['']}

        df = pd.DataFrame(data)

        df.to_csv(f, sep=';', header=False, index=False)

        f.close()

        count_arr = self.count_arr

        p = len(count_arr[:])

        for q in range(0, p):

            try:
                print(count_arr[q][1])
                pc_a = len(count_arr[q][1])
                for i in range(0, pc_a):
                    url = count_arr[q][1][i][1]
                    res = requests.get(url, headers=headers1)
                    soup1 = BeautifulSoup(res.text, 'html.parser')
                    poisk = soup1.find('table').find_all('tr')[1:]
                    for q1 in range(0, len(poisk)):
                        #Формируется ссылка на матч
                        math_url = 'https://www.betexplorer.com' + poisk[q1].find('a').get('href')
                        math_name1 = poisk[q1].find('a').find_all('span')[0].text
                        math_name2 = poisk[q1].find('a').find_all('span')[1].text
                        date = poisk[q1].find_all('td', class_='h-text-right')[-1].text
                        print(date)

                        print(math_url)
                        print(math_name1)
                        print(math_name2)
                        # переменые общие
                        all_match = 0
                        all_boll = []
                        win_math_name1 = 0
                        win_math_name2 = 0
                        null_math = 0
                        more_param = 0
                        less_param = 0
                        # кол-во мячей в играх где счет больше param
                        more_boll_param = 0
                        # кол-во мячей в играх где счет меньше param
                        less_boll_param = 0
                        # кол-во матчей где в счете нет 0
                        null_boll_math = 0
                        # кол-во мячей забитых командой 1
                        all_boll_team1 = 0
                        # кол-во мячей забитых командой 2
                        all_boll_team2 = 0
                        soup2 = get_table(math_url)
                        soup2 = BeautifulSoup(soup2, 'html.parser')
                        try:
                            poisk3 = soup2.find_all('div', class_="box-overflow__in")[-1].find_all('tbody')
                            for q2 in range(0, len(poisk3)):
                                per = poisk3[q2].find_all('tr')[1:]

                                all_match = all_match + len(per)
                                for q3 in range(0, len(per)):
                                    team = []
                                    schet = []
                                    t = per[q3].find_all('td')
                                    team1 = t[0].text
                                    team2 = t[1].text
                                    team.append(team1)
                                    team.append(team2)
                                    s = t[2].text.split(':')

                                    try:
                                        s[0] = s[0].split(' ')[0]
                                    except:
                                        s[0] = s[0]
                                    try:

                                        s[1] = s[1].split(' ')

                                        if len(s[1]) > 1:
                                            s[1] = s[1][0]
                                            if s[1] <= s[0]:
                                                s[0] = s[1]
                                            else:
                                                s[1] = s[0]
                                        else:
                                            s[1] = s[1][0]

                                    except:
                                        s[1] = s[1]

                                    schet.append(int(s[0]))
                                    schet.append(int(s[1]))

                                    if (schet[0] + schet[1]) > self.param:
                                        more_param += 1
                                        more_boll_param = more_boll_param + schet[0] + schet[1]
                                    if (schet[0] + schet[1]) < self.param:
                                        less_param += 1
                                        less_boll_param = less_boll_param + schet[0] + schet[1]
                                    if schet[0] != 0 and schet[1] != 0:
                                        null_boll_math += 1
                                    try:
                                        ind1 = team.index(math_name1)
                                    except:
                                        math_name1 = math_name1.split(' (')[0]
                                        ind1 = team.index(math_name1)
                                    try:
                                        ind2 = team.index(math_name2)
                                    except:
                                        math_name2 = math_name2.split(' (')[0]
                                        ind2 = team.index(math_name2)

                                    all_boll_team1 = all_boll_team1 + int(s[ind1])
                                    all_boll_team2 = all_boll_team2 + int(s[ind2])
                                    if schet[ind1] > schet[ind2]:
                                        win_math_name1 = win_math_name1 + 1
                                    if schet[ind1] < schet[ind2]:
                                        win_math_name2 = win_math_name2 + 1
                                    if schet[ind1] == schet[ind2]:
                                        null_math = null_math + 1
                                    all_boll = all_boll + schet

                                    pass

                                pass

                            # [print(table[q3]) for q3 in range(0, len(table))]

                        except Exception as e:
                            print(e)

                        print('Команда 1')
                        print(math_name1)
                        print('Команда 2')
                        print(math_name2)
                        print('Общее кол-во матчей')
                        print(all_match)

                        try:
                            all_boll = sum(all_boll)
                        except:
                            all_boll = 0

                        print('Общее кол-во мячей')
                        print(all_boll)
                        print('Общее кол-во побед 1 команды')
                        print(win_math_name1)
                        print('Ничьих')
                        print(null_math)
                        print('Общее кол-во побед 2 команды')
                        print(win_math_name2)
                        print('Кол-во матчей сыгранных больше param')
                        print(more_param)
                        print('Кол-во матчей сыгранных меньше param')
                        print(less_param)
                        print('Кол-во мячей в играх где счет больше param')
                        print(more_boll_param)

                        print('Кол-во матчей где в играх нет 0')
                        print(null_boll_math)

                        try:
                            print('Начало записи')
                            f = open('table.csv', 'a', encoding='cp1251', newline='')
                            data = {'Команда 1': [str(math_name1)], 'Команда 2': [str(math_name2)],
                                    'Общее кол-во матчей': [str(all_match)],
                                    'Общее кол-во мячей': [str(all_boll)],
                                    'Общее кол-во побед 1 команды': [str(win_math_name1)],
                                    'Общее кол-во ничьих': [str(null_math)],
                                    'Общее кол-во побед 2 команды': [str(win_math_name2)],
                                    'Кол-во матчей сыгранных больше ' + str(
                                        self.param): [str(more_param)],
                                    'Кол-во матчей сыгранных меньше ' + str(
                                        self.param): [str(less_param)],
                                    'Кол-во мячей в играх где счет больше ' + str(
                                        self.param): [str(more_boll_param)],

                                    'Кол-во матчей где в счете нет нуля': [str(null_boll_math)],
                                    'Кол-во мячей забитых командой 1': [str(all_boll_team1)],
                                    'Кол-во мячей забитых командой 2': [str(all_boll_team2)],
                                    '': ['']
                                    }

                            df = pd.DataFrame(data)

                            df.to_csv(f, sep=';', header=False, index=False)

                            f.close()

                            print('Конец записи')

                        except Exception as e:
                            print(e)

                        ggg = 1
                        # *******************************************

                        # *******************************************
                        pass

                    pass
                    print('Конец лиги')
            except Exception as e:
                print(e)
        print('***************Конец парсинга******************')

    def match_today(self):
        def get_table(url):

            k = requests.get(url)

            sp = BeautifulSoup(k.text, 'html.parser')

            poi = sp.find('a', class_="wrap-section__header__link").get('onclick')

            poi = poi.split("'")[1]
            print(poi)

            # url запроса

            headers = {

                'Host': 'www.betexplorer.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                'Referer': url,
                'Cache-Control': 'max-age=0, no-cache'

            }

            url_get = 'https://www.betexplorer.com/gres/ajax/mutual-matches.php?par=' + str(poi)

            result = requests.get(url_get, headers=headers)

            return result.text

        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76'}

        f = open('table.csv', 'a', encoding='cp1251', newline='')

        k1 = 'Кол-во матчей сыгранных больше ' + str(self.param)
        k2 = 'Кол-во матчей сыгранных меньше ' + str(self.param)
        k3 = 'Кол-во мячей в играх где счет больше ' + str(self.param)

        data = {'Команда 1': ['Команда 1'], 'Команда 2': ['Команда 2'],
                'Общее кол-во матчей': ['Общее кол-во матчей'],
                'Общее кол-во мячей': ['Общее кол-во мячей'],
                'Общее кол-во побед 1 команды': ['Общее кол-во побед 1 команды'],
                'Общее кол-во ничьих': ['Общее кол-во ничьих'],
                'Общее кол-во побед 2 команды': ['Общее кол-во побед 2 команды'],
                str(k1): [str(k1)],
                str(k2): [str(k2)],
                str(k3): [str(k3)],

                'Кол-во матчей где в счете нет нуля': ['Кол-во матчей где в счете нет нуля'],
                'Кол-во мячей забитых командой 1': ['Кол-во мячей забитых командой 1'],
                'Кол-во мячей забитых командой 2': ['Кол-во мячей забитых командой 2'],
                '': ['']}

        df = pd.DataFrame(data)

        df.to_csv(f, sep=';', header=False, index=False)

        f.close()

        url = self.today

        spisok = requests.get(url, headers=headers1)

        soup = BeautifulSoup(spisok.text, 'html.parser')

        poisk = []

        poisk1 = soup.find_all(attrs={'data-def':'1'})

        for q in range(0, len(poisk1)):
            try:
                k = poisk1[q].find_all(class_='table-main__tt')
                poisk = poisk + k
            except:
                continue

        for q in range(0, len(poisk)):

            math_url = 'https://www.betexplorer.com' + str(poisk[q].find('a').get('href'))
            print(poisk[q].find_all('span'))
            math_name1 = poisk[q].find_all('span')[1].text

            math_name2 = poisk[q].find_all('span')[2].text

            print(math_url)
            print(math_name1)
            print(math_name2)
            # переменые общие
            all_match = 0
            all_boll = []
            win_math_name1 = 0
            win_math_name2 = 0
            null_math = 0
            more_param = 0
            less_param = 0
            # кол-во мячей в играх где счет больше param
            more_boll_param = 0
            # кол-во мячей в играх где счет меньше param
            less_boll_param = 0
            # кол-во матчей где в счете нет 0
            null_boll_math = 0
            # кол-во мячей забитых командой 1
            all_boll_team1 = 0
            # кол-во мячей забитых командой 2
            all_boll_team2 = 0
            soup2 = get_table(math_url)
            soup2 = BeautifulSoup(soup2, 'html.parser')
            try:
                poisk3 = soup2.find_all('div', class_="box-overflow__in")[-1].find_all('tbody')
                for q2 in range(0, len(poisk3)):
                    per = poisk3[q2].find_all('tr')[1:]

                    all_match = all_match + len(per)
                    for q3 in range(0, len(per)):
                        team = []
                        schet = []
                        t = per[q3].find_all('td')
                        team1 = t[0].text
                        team2 = t[1].text
                        team.append(team1)
                        team.append(team2)
                        s = t[2].text.split(':')

                        try:
                            s[0] = s[0].split(' ')[0]
                        except:
                            s[0] = s[0]
                        try:

                            s[1] = s[1].split(' ')

                            if len(s[1]) > 1:
                                s[1] = s[1][0]
                                if s[1] <= s[0]:
                                    s[0] = s[1]
                                else:
                                    s[1] = s[0]
                            else:
                                s[1] = s[1][0]

                        except:
                            s[1] = s[1]

                        schet.append(int(s[0]))
                        schet.append(int(s[1]))

                        if (schet[0] + schet[1]) > self.param:
                            more_param += 1
                            more_boll_param = more_boll_param + schet[0] + schet[1]
                        if (schet[0] + schet[1]) < self.param:
                            less_param += 1
                            less_boll_param = less_boll_param + schet[0] + schet[1]
                        if schet[0] != 0 and schet[1] != 0:
                            null_boll_math += 1
                        try:
                            ind1 = team.index(math_name1)
                        except:
                            math_name1 = math_name1.split(' (')[0]
                            ind1 = team.index(math_name1)
                        try:
                            ind2 = team.index(math_name2)
                        except:
                            math_name2 = math_name2.split(' (')[0]
                            ind2 = team.index(math_name2)

                        all_boll_team1 = all_boll_team1 + int(s[ind1])
                        all_boll_team2 = all_boll_team2 + int(s[ind2])
                        if schet[ind1] > schet[ind2]:
                            win_math_name1 = win_math_name1 + 1
                        if schet[ind1] < schet[ind2]:
                            win_math_name2 = win_math_name2 + 1
                        if schet[ind1] == schet[ind2]:
                            null_math = null_math + 1
                        all_boll = all_boll + schet

                        pass

                    pass

                # [print(table[q3]) for q3 in range(0, len(table))]

            except Exception as e:
                print(e)

            print('Команда 1')
            print(math_name1)
            print('Команда 2')
            print(math_name2)
            print('Общее кол-во матчей')
            print(all_match)

            try:
                all_boll = sum(all_boll)
            except:
                all_boll = 0

            print('Общее кол-во мячей')
            print(all_boll)
            print('Общее кол-во побед 1 команды')
            print(win_math_name1)
            print('Ничьих')
            print(null_math)
            print('Общее кол-во побед 2 команды')
            print(win_math_name2)
            print('Кол-во матчей сыгранных больше param')
            print(more_param)
            print('Кол-во матчей сыгранных меньше param')
            print(less_param)
            print('Кол-во мячей в играх где счет больше param')
            print(more_boll_param)

            print('Кол-во матчей где в играх нет 0')
            print(null_boll_math)

            try:
                print('Начало записи')
                f = open('table.csv', 'a', encoding='cp1251', newline='')
                data = {'Команда 1': [str(math_name1)], 'Команда 2': [str(math_name2)],
                        'Общее кол-во матчей': [str(all_match)],
                        'Общее кол-во мячей': [str(all_boll)],
                        'Общее кол-во побед 1 команды': [str(win_math_name1)],
                        'Общее кол-во ничьих': [str(null_math)],
                        'Общее кол-во побед 2 команды': [str(win_math_name2)],
                        'Кол-во матчей сыгранных больше ' + str(
                            self.param): [str(more_param)],
                        'Кол-во матчей сыгранных меньше ' + str(
                            self.param): [str(less_param)],
                        'Кол-во мячей в играх где счет больше ' + str(
                            self.param): [str(more_boll_param)],

                        'Кол-во матчей где в счете нет нуля': [str(null_boll_math)],
                        'Кол-во мячей забитых командой 1': [str(all_boll_team1)],
                        'Кол-во мячей забитых командой 2': [str(all_boll_team2)],
                        '': ['']
                        }

                df = pd.DataFrame(data)

                df.to_csv(f, sep=';', header=False, index=False)

                f.close()

                print('Конец записи')

            except Exception as e:
                print(e)

            ggg = 1

        print('***********Конец парсинга*************')
        pass


def clicked():
    value = txt.get()
    value2 = float(txt2.get())
    value3 = selected.get()
    print(value3)
    if value3 == 1:
        a = Pars(value, value2)
        a.match_today()
    else:
        if value3 == 2:
            a = Pars(value, value2)
            a.liga()
            a.match()
    window.quit()


window = Tk()

window.title("Парсинг betexplorer")
window.geometry('400x70')
selected = IntVar()
selected.set(1)
lbl = Label(window, text="Введите раздел")
lbl.grid(column=0, row=0, sticky="w")
lbl2 = Label(window, text="Введите параметр")
lbl2.grid(column=0, row=1, sticky="w")
txt = Entry(window, width=10)
txt.grid(column=1, row=0)
txt.insert(0, 'hockey')
txt2 = Entry(window, width=10)
txt2.grid(column=1, row=1)
txt2.insert(0, 2.5)
btn = Button(window, text="Начать парсинг", command=clicked)
btn.grid(column=3, row=1, sticky='w')
rad1 = Radiobutton(window, text='Парсить сегодня', value='1', variable=selected)
rad1.grid(column=2, row=0, sticky='w')
rad2 = Radiobutton(window, text='Парсить все', value='2',variable=selected)
rad2.grid(column=2, row=1, sticky='w')

window.mainloop()
