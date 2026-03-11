from .models import CORRECT_PODS, RR_NO_CITY
from .models import SeaEndTerminal
from django.shortcuts import get_object_or_404
from decimal import Decimal


def get_correct_pod(english_pod):
    for k, v in CORRECT_PODS.items():
            if english_pod.upper() in v:
                return k
    return english_pod


def parse_for(df):
    
    carrier = None
    current_pod = None
    sheet_errors = []
    counter = 0
    for row in df.itertuples(index=False):
        rate_20ft_24t = None
        rate_20ft_28t = None
        rate_40ft = None
        pods = []
        rr_terminal = None
        rr_city = None

        if current_pod is None and row[0] != row[0]: # Это верхняя строчка
            continue
        if row[2] != row[2]: # Это пустая строчка
            continue

        if row[0] == row[0] and ':' not in row[0]:
            english_pod = row[0].split('\n')[1].strip()
            
        elif row[0] == row[0] and ':' in row[0]:
            english_pod = row[0].split('\n')[1].strip()

            if '/' in english_pod:
                raw_pods = english_pod.split('/')
                pods = [p.strip() for p in raw_pods]

            carrier = row[0].split(':')[0].strip()
        
        english_pod = get_correct_pod(english_pod)
        
        correct_pods = []
        if pods:
            for english_pod in pods:
                correct_pod = get_correct_pod(english_pod)
                correct_pods.append(correct_pod)
                terminal = get_object_or_404(SeaEndTerminal, name=correct_pod)
                city = terminal.local_hub_city
        
        # Теперь мы знаем, что это не первая строчка
        current_pod = correct_pods or english_pod
        
        # Берем ЖД терминал прибытия
        
        arrival = row[2].strip()
        if '(' in arrival:
            rr_terminal, rr_city = arrival.split('(')
            rr_terminal = rr_terminal.strip()
            rr_city = rr_city.replace(')', '').strip()
            
        elif arrival in RR_NO_CITY:
            rr_terminal = arrival
            rr_city = RR_NO_CITY[arrival]

        
        elif arrival not in RR_NO_CITY:
            rr_terminal = f'{arrival} любой ЖД терминал'
            rr_city = arrival
        
        
        # Теперь - цены на контейнеры
        if row[3] != '/':
            try:
                rate_20ft_24t = Decimal(row[3])
            except:
                raise sheet_errors.append(f'Цена на ЖД 20фт до 24т в неверном формате {row[3]} {type(row[3])}')
        
        if row[4] != '/':
            try:
                rate_20ft_28t = Decimal(row[4])
            except:
                sheet_errors.append(f'Цена на ЖД 20фт до 28т в неверном формате: {row[4]} {type(row[4])}')
        
        if row[5] != '/':
            try:
                rate_40ft = Decimal(row[5])
            except:
                sheet_errors.append(f'Цена на ЖД 40фт - не десятичное число {row[5]}, {type(row[5])}')

        # Терминальные расходы
        try:
            terminal_cost = Decimal(row[6])
            counter += 1
        except:
            return ValueError('Терминальные расходы в неверном формате')
        print(terminal_cost)
    print(counter)
    return sheet_errors
        

