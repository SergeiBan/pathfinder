CONTAINER_OPTIONS = (
    ('20DC', '20DC'),
    ('H0HC', '40HC'),
)

ACCEPTABLE_LOCAL_CITIES = [
    'Владивосток', 'Находка', 'Москва', 'Санкт-Петербург',
    'Новосибирск', 'Екатеринбург', 'Красноярск',
    'Ростов', 'Тольятти', 'Нижний Новгород', 'Пенза',
    'Казань', 'Челябинск', 'Самара', 'Иркутск', 'Нижнекамск',
    'Минск', 'Омск', 'Пермь', 'Ульяновск', 'Ростов-на-Дону',
    
]

ACCEPTABLE_LOCAL_HUBS = [
    'ВЛАДИВОСТОК', 'НАХОДКА', 'МОСКВА', 'САНКТ-ПЕТЕРБУРГ',
    'НОВОСИБИРСК', 'ЕКАТЕРИНБУРГ', 'КРАСНОЯРСК',
    'РОСТОВ', 'ТОЛЬЯТТИ', 'НИЖНИЙ НОВГОРОД', 'ПЕНЗА',
    'КАЗАНЬ', 'ЧЕЛЯБИНСК', 'САМАРА', 'ИРКУТСК', 'НИЖНЕКАМСК',
    'МИНСК', 'ОМСК', 'ПЕРМЬ', 'УЛЬЯНОВСК', 'РОСТОВ-НА-ДОНУ',
    'ЛЮБЛИНО'
]


SEA_POINTS = {
    'Nakhodka': {
        'VOSTOCHNY (VRANGEL BAY)': ['VRANGEL BAY', 'VOSTOCHNY', 'VRANGEL']
    },
    'VLADIVOSTOK': {
        'PACIFIC LOGISTIC': ['PL', 'VLADIVOSTOK (PL)'],
        'VLADIVOSTOK COMMERCIAL PORT': ['VLADIVOSTOK COMMERCIAL'],
        'VLADIVOSTOK (VMPP)': ['VLADIVOSTOK (VMPP)']
    }
    
}

CORRECT_PODS = {
    'Vostochny (VRANGEL BAY)': ['VRANGEL BAY', 'VOSTOCHNY', 'VRANGEL'],
    'Pacific Logistic': ['PL', 'VLADIVOSTOK (PL)'],
    'Vladivostok Commercial Port': ['VLADIVOSTOK COMMERCIAL'],
    'Vladivostok (VMPP)': ['VLADIVOSTOK (VMPP)']
}


PORTS = {
    'Vladivostok': [
        'Vladivostok Commercial Port', 'Vladivostok Commercial',
        'Fish Port', 'Vladivostok Fish Port', 'Vladivostok (VMPP)', 'VMPP', 'Vladivostok (PL)',
        'Pacific Logistic', 'Pacific Logistics',
    ],
    'Nakhodka': [
        'VRANGEL BAY', 'Vostochny', 'Vostochny (VRANGEL BAY)',
        'VRANGEL', 'Nakhodka', 'PPK-1', 'Astafyeva'
    ]

}

ACCEPTABLE_POLS = [
    'Shanghai',
    'Qingdao',
    'Tianjin',
    'Ningbo',
    'Dalian',
    'Xiamen',
    'Nansha',
    'Yantian',
    'Shekou',
    'Busan'
]

ACCEPTABLE_INNER_RR = [
    'ЭЛЕКТРОУГЛИ',
    'СЕЛЯТИНО',
    'КУПАВНА',
    'МИХНЕВО',
    'ЗАНЕВСКИЙ ПОСТ',
    'КЛЕЩИХА',
    'ЕКАТЕРИНБУРГ-ТОВАРНЫЙ',
    'БАЗАИХА',
    'РОСТОВ-ТОВАРНЫЙ',
    # ТОЛЬЯТТИ нет терминала
    'КОСТАРИХА',
    'ПЕНЗА-2',
    'ЛАГЕРНАЯ',
    'ЧЕЛЯБИНСК-ГРУЗОВОЙ',
    'СИЛИКАТНАЯ',
    'БЕЛЫЙ РАСТ',
    'ЧЕХОВ',
    'ХОВРИНО',
    'НОВОСИБИРСК-ВОСТОЧНЫЙ',
    'КОЛЬЦОВО',
    'АВТОВО',
    'ФИНЛЯНДСКИЙ',
    'РОСТОВ-ЗАПАДНЫЙ',
    'БЕЗЫМЯНКА',
    'ТИХОРЕЦКАЯ',
    'ФОРМАЧЕВО',
    'ИРКУТСК-СОРТИРОВОЧНЫЙ',
    'КРУГЛОЕ ПОЛЕ',
    'КОЛЯДИЧИ',
    'ВОРСИНО',
    'СЕЛЯТИНО',
    'РАМЕНСКОЕ',
    'ШУШАРЫ',
    'ЛЮБЕРЦЫ',
    'ЛЮБЛИНО-СОРТИРОВОЧНЫЙ',
    'ЗВЕЗДА',
    'АППАРАТНАЯ',
    'ИНЯ-ВОСТОЧНЫЙ',
    'ЧИК',
    'ЧЕМСКИЙ',
    'ОРЕХОВО-ЗУЕВО',

]


RR_NO_CITY = {
    'Екатеринбург-товарный': 'Екатеринбург',
    'Ростов-товарный': 'Ростов',
    'Пенза-2': 'Пенза',
    'Челябинск-грузовой': 'Челябинск',
    'Люблино-сортировочный': 'Люблино'
}