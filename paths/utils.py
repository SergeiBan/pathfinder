from datetime import date
from decimal import Decimal
from django.db.models import F, Q

from paths.models.rr import InnerRRRate
from paths.models.sea import SeaRate

from .models import (
    SeaStartTerminal, SeaLine, SeaETD, SeaEndTerminal, LocalHubCity,
    PORTS, ForeignAgent, SEA_POINTS, ACCEPTABLE_AGENTS, ACCEPTABLE_POLS, DROP_OFF_TRANSLATIONS
)
import sys, datetime, math


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


def find_all_seapaths(sea_start_terminal, container, SeaRate, etd_from=None, etd_to=None, end_city=None, pod=None):
    today = date.today()
    applicable_rates = None
    applicable_rates_no_etd = None
    applicable_rates_with_etd = None

    if container == '20DC':
        applicable_rates_no_etd = SeaRate.objects.select_related('sea_start_terminal', 'sea_line', 'sea_end_terminal').prefetch_related('etd').filter(
            sea_start_terminal=sea_start_terminal, etd__etd__isnull=True, rate_20__isnull=False, drop_off__in=[end_city]
            ).distinct()
        applicable_rates_with_etd = SeaRate.objects.select_related('sea_start_terminal', 'sea_line', 'sea_end_terminal').prefetch_related('etd').filter(
            sea_start_terminal=sea_start_terminal, etd__etd__isnull=False, rate_20__isnull=False, drop_off__in=[end_city]
            ).distinct()
    
    if container == '40HC':
        applicable_rates_no_etd = SeaRate.objects.select_related('sea_start_terminal', 'sea_line', 'sea_end_terminal').prefetch_related('etd').filter(
            sea_start_terminal=sea_start_terminal, etd__etd__isnull=True, rate_40__isnull=False, drop_off__in=[end_city]
            ).distinct()
        applicable_rates_with_etd = SeaRate.objects.select_related('sea_start_terminal', 'sea_line', 'sea_end_terminal').prefetch_related('etd').filter(
            sea_start_terminal=sea_start_terminal, etd__etd__isnull=False, rate_40__isnull=False, drop_off__in=[end_city]
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
    
    result_rates = None
    if applicable_rates_no_etd and applicable_rates_with_etd:
        result_rates = applicable_rates_no_etd | applicable_rates_with_etd
    else:
        result_rates = applicable_rates_no_etd or applicable_rates_with_etd

    if pod:
        result_rates = result_rates.filter(sea_end_terminal=pod)
    return result_rates


def get_inner_rr_rates(ar_cities, container, InnerRRRate, end_terminals, gross, is_agent_rate, is_vtt):
    # Получаем все ЖД ставки из всех морских терминалов прибытия во все ЖД терминалы города доставки
    if is_vtt and container == '20DC':
        field_name = 'vtt_20'
    elif not is_vtt and container == '20DC':
        field_name = 'gtd_20'
    elif is_vtt and container == '40HC':
        field_name = 'vtt_40'
    elif not is_vtt and container == '40HC':
        field_name = 'gtd_40'
    
    overweight = None
    if container == '20DC' and gross >= 18000:
        overweight = math.ceil(gross / 1000)
    elif container == '40HC' and gross >= 20000:
        overweight = math.ceil(gross / 1000)
    overweight = overweight * 2500

    lookup = {f"end_terminal__{field_name}__isnull": False}
    rr_rates = None
    if container == '20DC' and gross <= 24000:
        rr_rates = InnerRRRate.objects.select_related('start_terminal', 'line', 'end_terminal__city').filter(
            (Q(end_terminal__in=end_terminals) &
            Q(rate_20_24__isnull=False)),
            line__isnull=is_agent_rate,
            start_terminal__name__in=ar_cities, **lookup
        ).distinct().annotate(truck=F('end_terminal__city__local_truck'))


    elif container == '20DC':
        rr_rates = InnerRRRate.objects.select_related('start_terminal', 'line', 'end_terminal__city').filter(
            (Q(end_terminal__in=end_terminals) & Q(rate_20_28__isnull=False)), line__isnull=is_agent_rate,
            start_terminal__name__in=ar_cities, **lookup
        ).distinct().annotate(truck=F('end_terminal__city__local_truck'))

    if container == '40HC':
        rr_rates = InnerRRRate.objects.select_related('start_terminal', 'line', 'end_terminal__city').filter(
            (Q(end_terminal__in=end_terminals) &
            Q(rate_40__isnull=False)),
            line__isnull=is_agent_rate,
            start_terminal__name__in=ar_cities, **lookup
        ).distinct().annotate(truck=F('end_terminal__city__local_truck'))
    
    return rr_rates

def get_line_mm_rates(line_rates, InnerRRRate, end_terminals, container, end_city, gross, is_vtt):
    sea_to_rr = []
    sea_rr_truck = []
    sea_endnames = line_rates.values('sea_end_terminal__name')
    # Получаем все ЖД ставки из всех морских терминалов прибытия во все ЖД терминалы города доставки
    rr_rates = get_inner_rr_rates(sea_endnames, container, InnerRRRate, end_terminals, gross, is_agent_rate=False, is_vtt=is_vtt)
  
    # Все морские ставки линии сочетаем со всеми ЖД ставками по критериям: город и линия
    for sea_rate in line_rates:
        for rr_rate in rr_rates:
            if (
                sea_rate.sea_end_terminal.name == rr_rate.start_terminal.name
                and sea_rate.sea_line == rr_rate.line
            ):
                if not rr_rate.pol or rr_rate.pol == sea_rate.sea_start_terminal:
                    sea_to_rr.append([sea_rate, rr_rate])
    
    sea_rr_truck = None
  
    return (sea_to_rr, sea_rr_truck)
    

def get_agent_mm_rates(agent_rates, InnerRRRate, end_terminals, container, end_city, gross, is_vtt):
    sea_to_rr = []
    sea_rr_truck = []
    sea_endnames = agent_rates.values('sea_end_terminal__name')
    # Получаем все ЖД ставки из всех морских терминалов прибытия во все ЖД терминалы города доставки
    rr_rates = get_inner_rr_rates(sea_endnames, container, InnerRRRate, end_terminals, gross, is_agent_rate=True, is_vtt=is_vtt)
    
    for sea_rate in agent_rates:
            for rr_rate in rr_rates:
                if sea_rate.sea_end_terminal.name == rr_rate.start_terminal.name:
                    sea_to_rr.append([sea_rate, rr_rate])

    sea_rr_truck = None
    
    return (sea_to_rr, sea_rr_truck)

def get_pol(first_col, sheet_errors):
    
    sea_start = first_col.split('\n')
    
    POL = sea_start[0].strip().upper()
    if POL not in ACCEPTABLE_POLS:
        raise ValueError(f'Море: порт отправки неопознан: {POL}')

    drop_off_points = sea_start[1].strip().split('Drop off')[1]
    if '/' in drop_off_points:
        drop_off_points = [d.strip().upper() for d in drop_off_points.split('/')]
    else:
        drop_off_points = [drop_off_points.strip().upper()]

    obj, created = SeaStartTerminal.objects.get_or_create(
        name=POL,
        defaults={}
    )
    POL = obj or created

    drop_off_objs = []
    for d in drop_off_points:
        if d not in DROP_OFF_TRANSLATIONS:
            sheet_errors.append(f'Море: неопознанный город drop off: {d}')
            continue
        d_city = DROP_OFF_TRANSLATIONS[d]
        d_city_obj, is_created = LocalHubCity.objects.get_or_create(name=d_city, defaults={})
        drop_off_objs.append(d_city_obj)

    return POL, drop_off_objs


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
    'Jun': 6,
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


def sort_sea_rr(rates: list[SeaRate, InnerRRRate], container: str, gross: Decimal, is_vtt: bool, with_guard: bool):
    annotated_rates = []
    for rate in rates:
        total = 0
        sea_price, rr_price = 0, 0
        
        if container == '20DC':
            sea_price = rate[0].rate_20

            if gross <= 24000:
                rr_price = rate[1].rate_20_24
            else:
                rr_price = rate[1].rate_20_28

            if is_vtt:
                station = rate[1].end_terminal.vtt_20
            else:
                station = rate[1].end_terminal.gtd_20
        
        if container == '40HC':
            sea_price = rate[0].rate_40
            rr_price = rate[1].rate_40
            if is_vtt:
                station = rate[1].end_terminal.vtt_40
            else:
                station = rate[1].end_terminal.gtd_40
        

        rr_price += rate[1].thc

        guard = None
        if with_guard:
            if container == '20DC' and rate[1].guard_20 is not None:
                guard = rate[1].guard_20
            if container == '40HC' and rate[1].guard_40 is not None:
                guard = rate[1].guard_40
        if not guard: # Убрать, когда в FOR заполним охрану до конца
            guard = 0
        
        sea_price = sea_price + (sea_price * rate[0].conversion)
        total = total + sea_price + rr_price + station + guard
        annotated_rates.append({
            'sea_rate': rate[0], 'sea_price': sea_price, 'etds': rate[0].get_etds(), 'carrier': rate[0].sea_line,
            'rr_rate': rate[1], 'rr_price': rr_price, 'station': station,
            'local_truck': rate[1].truck, 'total': total, 'guard': guard
        })
        

    sorted_rates = sorted(annotated_rates, key=lambda x: x['total'])
    return sorted_rates


def sort_everything(agent_rates, line_rates):
    united_rates = agent_rates + line_rates
    sorted_rates = sorted(united_rates, key=lambda x: x['total'])
    return sorted_rates