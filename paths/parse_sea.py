import datetime

from paths.models.constants import ACCEPTABLE_POLS
from paths.models.sea import SeaRate
from paths.utils import check_agent, get_carrier, get_container_prices, get_conversion, get_etd, get_pods, get_pol, make_dates


def parse_sea_sheet(sheet_name, df):
    sheet_errors = []
    POL, drop_off = None, None
                    
    for row in df.itertuples(index=False):

        if row[2] != row[2]: # Это пустая строчка
            continue

        # В первой колонке - порт отправки и дроп офф
        first_col = row[0]
        if isinstance(first_col, str):
            POL, drop_off = get_pol(first_col)

        # Прежде всего проверяем, что цена есть хотя бы на один тип контейнера
        rate_20 = get_container_prices(row[2])
        rate_40 = get_container_prices(row[3])
        if not rate_20 and not rate_40:
            continue

        # Во второй колонке - линия
        second_col = row[1]
        if isinstance(second_col, str):
            sea_line = get_carrier(second_col)
        
        # В колонке E (пятая) - морские терминалы прибытия
        POD_col = row[4]
        if isinstance(POD_col, str):
            pods = get_pods(POD_col)
        
        # В колонке F (седьмая) - ETD
        year = datetime.date.today().year
        etd_col = row[6]
        etds = get_etd(etd_col, year)

        # В десятой колонке - валидность
        validity_col = row[9]
        try:
            validity_date = make_dates([validity_col], year, sheet_errors)[0]
        except:
            continue

        # В колонке 12 - ставка конвертации
        conversion_rate = get_conversion(row[11])

        # В колонке 14 - агент или линия
        agent = row[13]
        is_agent = check_agent(agent)

        for pod in pods:

            sr = SeaRate(
                sea_line=sea_line,
                sea_start_terminal=POL,
                validity=validity_date,
                rate_20=rate_20,
                rate_40=rate_40,
                sea_end_terminal=pod,
                conversion=conversion_rate,
                agent=is_agent
            )
            sr.save()
            if etds:
                sr.etd.add(*etds)

    return sheet_errors