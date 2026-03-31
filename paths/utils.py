from datetime import date
from django.db.models import F, Q

from .models import (
    SeaStartTerminal, SeaLine, SeaETD, SeaEndTerminal, LocalHubCity,
    PORTS, ForeignAgent, SEA_POINTS, ACCEPTABLE_AGENTS, ACCEPTABLE_POLS
)
import sys, datetime


def find_seapath(sea_start_terminal, sea_end_terminal, container, SeaRate, etd_from=None, etd_to=None):
    applicable_rates = None
    applicable_rates = SeaRate.objects.filter(
        sea_start_terminal=sea_start_terminal, sea_end_terminal=sea_end_terminal, container=container
        )
    if applicable_rates:
        today = date.today()

        if etd_from is None and etd_to is None:
            applicable_rates = applicable_rates.filter(etd__etd__gt=today).distinct()
        
        elif etd_from is None and etd_to is not None:
            applicable_rates = applicable_rates.filter(etd__etd__gt=today, etd__etd__lte=etd_to).distinct()

        elif etd_from is not None and etd_to is None:
            applicable_rates = applicable_rates.filter(etd__etd__gte=etd_from).distinct()

        elif etd_from is not None and etd_to is not None:
            applicable_rates = applicable_rates.filter(etd__etd__gte=etd_from, etd__etd__lte=etd_to).distinct()

    return applicable_rates


def find_all_seapaths(sea_start_terminal, container, SeaRate, etd_from=None, etd_to=None):
    today = date.today()
    applicable_rates = None
    applicable_rates_no_etd = None
    applicable_rates_with_etd = None

    if container == '20DC':
        applicable_rates_no_etd = SeaRate.objects.filter(
            sea_start_terminal=sea_start_terminal, etd__etd__isnull=True, rate_20__isnull=False
            ).distinct()
        applicable_rates_with_etd = SeaRate.objects.filter(
            sea_start_terminal=sea_start_terminal, etd__etd__isnull=False, rate_20__isnull=False
            ).distinct()
    
    if container == '40HC':
        applicable_rates_no_etd = SeaRate.objects.filter(
            sea_start_terminal=sea_start_terminal, etd__etd__isnull=True, rate_40__isnull=False
            ).distinct()
        applicable_rates_with_etd = SeaRate.objects.filter(
            sea_start_terminal=sea_start_terminal, etd__etd__isnull=False, rate_40__isnull=False
            ).distinct()
    
    if applicable_rates_no_etd:
        applicable_rates_no_etd = applicable_rates_no_etd.filter(validity__gt=today).distinct()

    if applicable_rates_with_etd:

        if etd_from is None and etd_to is None:
            applicable_rates_with_etd = applicable_rates_with_etd.filter(etd__etd__gt=today).distinct()
        
        elif etd_from is None and etd_to is not None:
            applicable_rates_with_etd = applicable_rates_with_etd.filter(etd__etd__gt=today, etd__etd__lte=etd_to).distinct()

        elif etd_from is not None and etd_to is None:
            applicable_rates_with_etd = applicable_rates_with_etd.filter(etd__etd__gte=etd_from).distinct()

        elif etd_from is not None and etd_to is not None:
            applicable_rates_with_etd = applicable_rates_with_etd.filter(etd__etd__gte=etd_from, etd__etd__lte=etd_to).distinct()
    
    if applicable_rates_no_etd and applicable_rates_with_etd:
        return applicable_rates_no_etd | applicable_rates_with_etd
    return applicable_rates_no_etd or applicable_rates_with_etd


def get_inner_rr_rates(ar_cities, container, InnerRRRate, end_terminals, gross, is_agent_rate):
    # Получаем все ЖД ставки из всех морских терминалов прибытия во все ЖД терминалы города доставки
    
    rr_rates = None
    if container == '20DC' and gross <= 24000:
        rr_rates = InnerRRRate.objects.filter(
            (Q(end_terminal__in=end_terminals) &
            Q(rate_20_24__isnull=False)),
            line__isnull=is_agent_rate,
            start_terminal__name__in=ar_cities
        ).distinct().annotate(truck=F('end_terminal__city__local_truck'))


    elif container == '20DC':
        rr_rates = InnerRRRate.objects.filter(
            (Q(end_terminal__in=end_terminals) & Q(rate_20_28__isnull=False)), line__isnull=is_agent_rate
        ).distinct().annotate(truck=F('end_terminal__city__local_truck'))

    if container == '40HC':
        rr_rates = InnerRRRate.objects.filter(
            (Q(end_terminal__in=end_terminals) &
            Q(rate_40__isnull=False)),
            line__isnull=is_agent_rate
        ).distinct().annotate(truck=F('end_terminal__city__local_truck'))
    
    return rr_rates

def get_line_mm_rates(line_rates, InnerRRRate, end_terminals, container, end_city, gross):
    sea_to_rr = []
    sea_rr_truck = []
    sea_endnames = line_rates.values('sea_end_terminal__name')
    # Получаем все ЖД ставки из всех морских терминалов прибытия во все ЖД терминалы города доставки
    rr_rates = get_inner_rr_rates(sea_endnames, container, InnerRRRate, end_terminals, gross, is_agent_rate=False)
  
    # Все морские ставки линии сочетаем со всеми ЖД ставками по критериям: город и линия
    for sea_rate in line_rates:
        for rr_rate in rr_rates:
            if (
                sea_rate.sea_end_terminal.name == rr_rate.start_terminal.name
                and sea_rate.sea_line == rr_rate.line
            ):
                if not rr_rate.pol or rr_rate.pol == sea_rate.sea_start_terminal:
                    sea_to_rr.append([sea_rate, rr_rate])
    
    # Если нужен автовывоз в другой город
    if end_city.ingoing_truck_rates.exists():
        remote_truck_rates = end_city.ingoing_truck_rates.all()
        all_rr_rates = InnerRRRate.objects.all() # Все ЖД ставки внутри России

        # Сопоставляем ставки ЖД и автовывоза по критерию - город
        rr_plus_truck_rates = []
        for remote_truck in remote_truck_rates:
            for rr_rate in all_rr_rates:
                if rr_rate.end_terminal.city == remote_truck.start_city:
                    rr_plus_truck_rates.append([rr_rate, remote_truck])
    
        # Сопоставляем морские ставки и ЖД ставки по городу, получим путь море - ЖД - автовывоз
        for sea_rate in line_rates:
            for rr_truck in rr_plus_truck_rates:
                if (
                    sea_rate.sea_end_terminal.local_hub_city == rr_truck[0].start_terminal.city
                    and sea_rate.sea_line == rr_truck[0].line
                ):
                    sea_rr_truck.append([sea_rate, rr_truck[0], rr_truck[1]])
    return (sea_to_rr, sea_rr_truck)
    

def get_agent_mm_rates(agent_rates, InnerRRRate, end_terminals, container, end_city, gross):
    sea_to_rr = []
    sea_rr_truck = []
    sea_endnames = agent_rates.values('sea_end_terminal__name')
    # Получаем все ЖД ставки из всех морских терминалов прибытия во все ЖД терминалы города доставки
    rr_rates = get_inner_rr_rates(sea_endnames, container, InnerRRRate, end_terminals, gross, is_agent_rate=True)
    
    for sea_rate in agent_rates:
            for rr_rate in rr_rates:
                if sea_rate.sea_end_terminal.name == rr_rate.start_terminal.name:
                    sea_to_rr.append([sea_rate, rr_rate])

    # Если возможен автовывоз из другого города
    if end_city.ingoing_truck_rates.exists():
        remote_truck_rates = end_city.ingoing_truck_rates.all()
        all_rr_rates = InnerRRRate.objects.filter(line__isnull=True)

        # Сопоставляем ставки ЖД и автовывоза по критерию - город
        rr_plus_truck_rates = []
        for remote_truck in remote_truck_rates:
            for rr_rate in all_rr_rates:
                if rr_rate.end_terminal.city == remote_truck.start_city:
                    rr_plus_truck_rates.append([rr_rate, remote_truck])

        # Сопоставляем морские ставки и ЖД ставки по городу, получим путь море - ЖД - автовывоз
        for sea_rate in agent_rates:
            for rr_truck in rr_plus_truck_rates:
                if sea_rate.sea_end_terminal.local_hub_city == rr_truck[0].start_terminal.city:
                    sea_rr_truck.append([sea_rate, rr_truck[0], rr_truck[1]])

    return (sea_to_rr, sea_rr_truck)

def get_pol(first_col):
    
    sea_start = first_col.split('\n')
    # Добавить проверку по списку
    POL = sea_start[0].strip().upper()
    if POL not in ACCEPTABLE_POLS:
        raise ValueError(f'Море: порт отправки неопознан: {POL}')

    if len(sea_start) > 2:
        drop_off = ' '.join(sea_start[1:]).strip()
    else:
        drop_off = sea_start[1].strip()

    obj, created = SeaStartTerminal.objects.get_or_create(
        name=POL,
        defaults={}
    )
    POL = obj or created
    return POL, drop_off


def get_carrier(second_col):
    carrier = second_col.strip().upper()
    obj, created = SeaLine.objects.get_or_create(
        name=carrier,
        defaults={}
    )
    carrier = obj or created
    return carrier


def get_pods(pod_col):
    sheet_errors = []
    pods = None
    if '&' in pod_col:
        pod_col = pod_col.split('&')
        pods = [p.strip().upper() for p in pod_col]    
    elif '/' in pod_col:
        pod_col = pod_col.split('/')
        pods = [p.strip().upper() for p in pod_col]
    else:
        pods = [pod_col.strip().upper()]

    result_pods = []
    for p in pods:
        is_found = False
        for city, ports in SEA_POINTS.items():
            for correct, arbitrary in ports.items():
                if p in arbitrary:
                    result_pods.append([correct, city])
                    is_found = True
        if not is_found:
            sheet_errors.append(f'Морской терминал {p} не распознан')
        
    
    created_pods = []
    for p in result_pods:
        city_obj, created_city = LocalHubCity.objects.get_or_create(name=p[1], defaults={})
        city = city_obj or created_city
        
        pod_obj, created_pod = SeaEndTerminal.objects.get_or_create(
            name=p[0],
        defaults={'local_hub_city': city}
        )
        created_pods.append(pod_obj or created_pod)

    return created_pods


MONTHS = {
    'Feb': 2,
    'Mar': 3,
    'март': 3,
    'Apr': 4,
    'May': 5,
}


def make_dates(wierd_dates, year, sheet_errors=None):

    new_dates = []
    for wierd_date in wierd_dates:
        if isinstance(wierd_date, datetime.date):
            new_dates.append(wierd_date)
            continue

        if '-' in wierd_date:
            wierd_date = wierd_date.split('-')
        elif '.' in wierd_date:
            wierd_date = wierd_date.split('.')
        if 'NSH' in wierd_date[0]:
            wierd_date[0] = wierd_date[0][3:]

        try:
            day = int(wierd_date[0].strip())
        except:
            sheet_errors.append(f'Дата в неизвестном формате: {wierd_date[0]}')
            raise ValueError(f'Дата в неизвестном формате: {wierd_date[0]}')
        
        month = MONTHS[wierd_date[1].strip()]
        new_date = datetime.date(year, month, day)
        new_dates.append(new_date)

    return new_dates


def get_etd(etd_col, year):

    if etd_col != etd_col:
        return None
    
    etds = None
    if isinstance(etd_col, str):
        if '/' in etd_col:
            return None
        
        if '&' in etd_col:
            etd_col = etd_col.split('&')
            etds = [e.strip() for e in etd_col] 
        else:
            etds = [etd_col.strip()]
        
        new_dates = make_dates(etds, year)
        new_etds = []

        for new_date in new_dates:
            obj, created = SeaETD.objects.get_or_create(
                etd=new_date,
            )
            new_etds.append(obj or created)
            
    return new_etds


def get_container_prices(col_price):
    if col_price != col_price:
        return None

    if (isinstance(col_price, int)):
        return col_price
    
    if not (isinstance(col_price, str)):
        sys.exit('the price is of unknown type')

    if '/' in col_price or 'SPACE' in col_price or 'NO' in col_price:
        return None
    
    col_price = col_price.replace(' ', '')
    if '$' in col_price:
        col_price = col_price[1:]
    
    return int(col_price)


def get_conversion(col_conversion):
    if (isinstance(col_conversion, float)):
        return col_conversion
    else:
        raise ValueError(f'Ставка конвертации не десятичное число {col_conversion}')
        

def check_agent(agent):
    if (isinstance(agent, str)):
        agent = agent.upper()
        if agent in ACCEPTABLE_AGENTS:
            obj, created = ForeignAgent.objects.get_or_create(
                title=agent, defaults={}
            )
            return obj or created
    return None
