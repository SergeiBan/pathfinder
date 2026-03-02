from datetime import date
from django.db.models import F


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
    applicable_rates = None
    applicable_rates = SeaRate.objects.filter(
        sea_start_terminal=sea_start_terminal, container=container
        ).distinct()
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


def get_line_mm_rates(line_rates, InnerRRRate, end_terminals, container, end_city):
    sea_to_rr = []
    sea_rr_truck = []

    # Получаем все ЖД ставки из всех морских терминалов прибытия во все ЖД терминалы города доставки
    rr_rates = InnerRRRate.objects.filter(
        end_terminal__in=end_terminals,
        container=container
    ).distinct().annotate(truck=F('end_terminal__city__local_truck__price'))
    
    # Все морские ставки линии сочетаем со всеми ЖД ставками по критериям: город и линия
    for sea_rate in line_rates:
            for rr_rate in rr_rates:
                if (
                      sea_rate.sea_end_terminal.local_hub_city == rr_rate.start_terminal.city
                      and sea_rate.sea_line == rr_rate.line
                ):
                    sea_to_rr.append([sea_rate, rr_rate])
    

    # 3. Если нужен автовывоз в другой город
    if end_city.ingoing_truck_rates.exists():
        remote_truck_rates = end_city.ingoing_truck_rates.all()
        all_rr_rates = InnerRRRate.objects.all() # Все ЖД линии России

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
    

def get_agent_mm_rates(agent_rates, InnerRRRate, end_terminals, container, end_city):
    sea_to_rr = []
    sea_rr_truck = []

    # Получаем все ЖД ставки из всех морских терминалов прибытия во все ЖД терминалы города доставки
    rr_rates = InnerRRRate.objects.filter(
            end_terminal__in=end_terminals,
            container=container,
            line__isnull=True
        ).distinct().annotate(truck=F('end_terminal__city__local_truck__price'))
    
    for sea_rate in agent_rates:
            for rr_rate in rr_rates:
                if sea_rate.sea_end_terminal.local_hub_city == rr_rate.start_terminal.city:
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

    POL = sea_start[0]
    if len(sea_start) > 2:
        drop_off = ' '.join(sea_start[1:])
    else:
        drop_off = sea_start[1]
    return POL, drop_off
