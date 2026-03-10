from .models import CORRECT_PODS, RR_NO_CITY
from .models import SeaEndTerminal
from django.shortcuts import get_object_or_404


def get_correct_pod(english_pod):
    for k, v in CORRECT_PODS.items():
            if english_pod.upper() in v:
                return k
    return english_pod


def parse_for(df):
    pods = []
    current_pod = None
    carrier = None
    rr_terminal = None
    rr_city = None

    for row in df.itertuples(index=False):

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
            print(rr_terminal, rr_city)
        
        


