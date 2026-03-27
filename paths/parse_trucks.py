from .models import ACCEPTABLE_LOCAL_HUBS, ACCEPTABLE_INNER_RR


def parse_truck_sheet(df):
    sheet_errors = []
    city = None

    for row in df.itertuples(index=False):
        gtd_20, gtd_40, vtt_20, vtt_40 = None, None, None, None

        if row[0] != row[0] and not city: # В первой колонке nan и город не был ранее распознан
            continue
        if row[1] != row[1]: # В колонке ЖД терминала nan
            continue
        
        if isinstance(row[0], str):
            city = row[0].strip().upper()
            if city not in ACCEPTABLE_LOCAL_HUBS:
                sheet_errors.append(f'Автовывоз: неопознанный город: {city}')
                city = None
        
        if isinstance(row[1], str):
            rr_terminal = row[1].strip().upper()
            if rr_terminal not in ACCEPTABLE_INNER_RR:
                if rr_terminal == 'Орехово - Зуево'.strip().upper():
                    print(rr_terminal)
                sheet_errors.append(f'Автовывоз: неопознанный ЖД терминал: {rr_terminal}')
                continue

        if isinstance(row[2], int):
            gtd_20 = row[2]
        else:
            sheet_errors.append(f'Непонятный формат цены на ГТД {row[2]}')
            continue

        if isinstance(row[3], int):
            gtd_40 = row[3]
        else:
            sheet_errors.append(f'Непонятный формат цены на ГТД {row[3]}')
            continue

        if isinstance(row[4], int):
            vtt_20 = row[4]
        else:
            sheet_errors.append(f'Непонятный формат цены на ВТТ {row[4]}')
            continue
    
        if isinstance(row[5], int):
            vtt_40 = row[5]
        else:
            sheet_errors.append(f'Непонятный формат цены на ВТТ {row[5]}')
            continue
        
        if not gtd_20 and not gtd_40 and not vtt_20 and not vtt_40:
            continue


    return sheet_errors