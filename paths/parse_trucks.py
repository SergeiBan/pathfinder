from .models import ACCEPTABLE_LOCAL_HUBS, ACCEPTABLE_INNER_RR, InnerRRTerminal, LocalHubCity


def validate_price(price_cell):
    if price_cell != price_cell or price_cell == '/':
        return None
    
    if isinstance(price_cell, int):
        return price_cell
    else:
        raise ValueError('Автовывоз: цена в неверном формате')
        

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
                continue
        
        if isinstance(row[1], str):
            rr_terminal = row[1].strip().upper()
            if rr_terminal not in ACCEPTABLE_INNER_RR:
                sheet_errors.append(f'Автовывоз: неопознанный ЖД терминал: {rr_terminal}')
                continue

        if ((row[2] != row[2] or row[2] == '/') and
            (row[3] != row[3] or row[3] == '/') and
            (row[4] != row[4] or row[4] == '/') and
            (row[5] != row[5] or row[5] == '/')):
            continue
        
        try:
            gtd_20 = validate_price(row[2])
        except:
            sheet_errors.append(f'Автвовывоз: неизвестный формат цены на ГТД {row[2]}')
            continue
        
        try:
            gtd_40 = validate_price(row[3])
        except:
            sheet_errors.append(f'Автвовывоз: неизвестный формат цены на ГТД {row[3]}')
            continue
        
        try:
            vtt_20 = validate_price(row[4])
        except:
            sheet_errors.append(f'Автвовывоз: неизвестный формат цены на ВТТ {row[4]}')
            continue

        try:
            vtt_40 = validate_price(row[5])
        except:
            sheet_errors.append(f'Автвовывоз: неизвестный формат цены на ВТТ {row[5]}')
            continue

    
        city_obj, city_created = LocalHubCity.objects.get_or_create(name=city, defaults={})
        terminal = InnerRRTerminal.objects.filter(name=rr_terminal)
        if terminal:
            terminal = terminal.first()
            terminal.gtd_20 = gtd_20
            terminal.gtd_40 = gtd_40
            terminal.vtt_20 = vtt_20
            terminal.vtt_40 = vtt_40
            terminal.save()
        else:
            sheet_errors.append(f'Автовывоз: ЖД терминал не найден: {rr_terminal}')
            continue

    return sheet_errors