from .models import (
    InnerRRRate, InnerRRTerminal, SeaEndTerminal,
    LocalHubCity, ACCEPTABLE_INNER_RR, ACCEPTABLE_LOCAL_HUBS, SEA_POINTS, CARRIERS,
    ACCEPTABLE_POLS, SeaStartTerminal, SeaLine
)
from django.shortcuts import get_object_or_404
from decimal import Decimal


def get_correct_pod(english_pod, sheet_errors):
    for city, ports in SEA_POINTS.items():
        for correct, arbitrary in ports.items():
            if english_pod in arbitrary:
                return correct, city
    sheet_errors.append(f'Морской терминал {english_pod} не найден')


def get_carrier(carrier):
    for c in CARRIERS:
        if c == carrier:
            return c
    raise ValueError(f'Линия {carrier} не найден')


def get_guard_price(cell, sheet_errors):
        guard_price = None
        if cell == '/':
            return guard_price
        
        if isinstance(cell, str) and '₽' in cell:
            price = cell.split(',')[0].replace(' ', '')
            try:
                guard_price = Decimal(price)
            except:
                sheet_errors.append(f'Цена на охрану ЖД - в неизвестном формате: {cell}')

        else:
            try:
                guard_price = Decimal(cell)
            except:
                sheet_errors.append(f'Цена на охрану ЖД - в неизвестном формате {cell}')
        
        return guard_price


def parse_for(df):
    InnerRRTerminal.objects.all().delete()
    
    carrier = None
    current_pods = None
    correct_pods = []
    sheet_errors = []
    for row in df.itertuples(index=False):
        rate_20ft_24t = None
        rate_20ft_28t = None
        rate_40ft = None
        guard_20ft = None
        guard_40ft = None
        validity = None
        updated_at = None
        is_by_wagon = False
        pods = []
        rr_end_terminal_name = None
        rr_end_city_name = None
        terminal_cost = None
        pol_obj, pol_created = None, None
        carrier_obj, carrier_created = None, None

        if current_pods is None and row[0] != row[0]: # Это верхняя строчка
            continue
        if row[2] != row[2]: # Это пустая строчка
            continue

        # Морские порты без линии, только один порт
        if row[0] == row[0] and ':' not in row[0]:
            english_pod = row[0].split('\n')[1].strip().upper()
            english_pod, city = get_correct_pod(english_pod, sheet_errors)
            english_pod = [english_pod]
            
        # Морские порты с линией
        elif row[0] == row[0] and ':' in row[0]:
            english_pod = row[0].split('\n')[1].strip().upper() # Порт
            carrier = row[0].split('\n')[0].strip().upper().replace(':', '') # Линия
            if carrier not in CARRIERS:
                sheet_errors.append(f'Линия {carrier} неизвестна')
                continue
            carrier_obj, carrier_created = SeaLine.objects.get_or_create(name=carrier, defaults={})
            
            # Портов может быть несколько
            if '/' in english_pod:
                raw_pods = english_pod.split('/')
                pods = [p.strip() for p in raw_pods]
                correct_pods = []
                for p in pods:
                    correct_pod, city = get_correct_pod(p, sheet_errors)
                    correct_pods.append(correct_pod)
            else:
                english_pod, city = get_correct_pod(english_pod, sheet_errors)
                english_pod = [english_pod]

        current_pods = correct_pods or english_pod

        # Проверяем, указан ли порт отправки, для особо строгих линейщиков
        if isinstance(row[1], str):
            possible_pol = row[1].strip().upper()
            if possible_pol not in ACCEPTABLE_POLS:
                sheet_errors.append(f'Неизвестный POL в ЖД ставке: {possible_pol}')
                continue
            pol_obj, pol_created = SeaStartTerminal.objects.get_or_create(name=possible_pol, defaults={})
        
        # Берем ЖД терминал прибытия
        arrival = row[2].strip().upper()
        if '*' in arrival:
            is_by_wagon = True
            arrival = arrival.replace('*', '')
        if '(' in arrival: # Строчка включает ЖД терминал и город
            rr_end_terminal_name, rr_end_city_name = arrival.split('(')
            rr_end_terminal_name = rr_end_terminal_name.strip()
            rr_end_city_name = rr_end_city_name.replace(')', '').strip()

            if rr_end_terminal_name not in ACCEPTABLE_INNER_RR:
                sheet_errors.append(f'Неизвестный ЖД терминал прибытия: {rr_end_terminal_name}')
                continue
        else: # Если в строчке - только город, а ЖД терминал не указан
            rr_end_terminal_name = f'любой ЖД терминал {arrival}'
            rr_end_city_name = arrival
        
        # Проверяем, что ЖД город прибытия допустимый. Иначе нужно его исправить/добавить
        if rr_end_city_name not in ACCEPTABLE_LOCAL_HUBS:
                sheet_errors.append(f'Неизвестный город ЖД терминала прибытия: {rr_end_city_name}')
                continue
        
        
        # Теперь - цены на контейнеры
        if row[3] != '/':
            try:
                rate_20ft_24t = Decimal(row[3])
            except:
                sheet_errors.append(f'Цена на ЖД 20фт до 24т в неверном формате {row[3]} {type(row[3])}')
        
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
        if not (row[3] or row[4] or row[5]):
            continue

        # Терминальные расходы
        try:
            terminal_cost = Decimal(row[6])
        except:
            sheet_errors.append(f'Терминальные расходы в неверном формате: {row[6]}')
            continue
        
        # Охрана
        guard_20ft = get_guard_price(row[7], sheet_errors)
        guard_40ft = get_guard_price(row[8], sheet_errors)

        # Валидность
        try:
            validity = row[9].date()
        except:
            sheet_errors.append(f'FOR Валидность - нераспознан формат: {row[9]}')
            continue

        # Дата обновления
        try:
            updated_at = row[10].date()
        except:
            sheet_errors.append(f'FOR Дата обновления - нераспознан формат: {row[10]}')
            continue

        # Создаем ЖД терминал
        for pod in current_pods:

            # Получаем морской терминал и город
            terminal = get_object_or_404(SeaEndTerminal, name=pod)
            city = terminal.local_hub_city

            # Создаем ЖД терминал отправки - он назван, как морской
            rr_start_terminal, created_start_terminal = InnerRRTerminal.objects.get_or_create(
                name=pod,
                defaults={'city': city}
            )

            # Конечный ЖД терминал
            rr_end_city, created_end_city = LocalHubCity.objects.get_or_create(
                name=rr_end_city_name,
                defaults={}
            )
            rr_end_terminal, created_end_terminal = InnerRRTerminal.objects.get_or_create(
                name=rr_end_terminal_name,
                defaults={'city': rr_end_city or created_end_city}
            )

            new_rate = InnerRRRate.objects.create(
                start_terminal=rr_start_terminal or created_start_terminal,
                end_terminal=rr_end_terminal or created_end_terminal,
                rate_20_24=rate_20ft_24t or None,
                rate_20_28=rate_20ft_28t or None,
                rate_40=rate_40ft or None,
                line=carrier_obj or carrier_created,
                is_by_wagon=is_by_wagon,
                thc=terminal_cost,
                pol=pol_obj or pol_created
            )


    return sheet_errors




