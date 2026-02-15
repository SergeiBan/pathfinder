from datetime import date


def find_seapath(start_port, sea_end_terminal, container, SeaRate, etd_from=None, etd_to=None):
    applicable_rates = None
    applicable_rates = SeaRate.objects.filter(
        start_port=start_port, sea_end_terminal=sea_end_terminal, container=container
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


def find_inner_rrpath(sea_rates, InnerRRRate, rr_end_city=None, rr_end_terminal=None):
    print(sea_rates, rr_end_city, rr_end_terminal)
    all_end_ports = sea_rates.