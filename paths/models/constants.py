CONTAINER_OPTIONS = (
    ('20DC', '20DC'),
    ('40HC', '40HC'),
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


ACCEPTABLE_AGENTS = ['WOSUN']

SEA_POINTS = {
    'НАХОДКА': {
        'VOSTOCHNY (VRANGEL BAY)': ['VRANGEL BAY', 'VOSTOCHNY', 'VRANGEL', 'VOSTOCHNY (VRANGEL BAY)'],
        'NAKHODKA': ['NAKHODKA'],
        'ASTAFYEVA': ['ASTAFYEVA'],
        'PPK-1': ['PPK-1']
    },
    'ВЛАДИВОСТОK': {
        'PACIFIC LOGISTIC': ['PL', 'VLADIVOSTOK (PL)', 'PACIFIC LOGISTIC'],
        'VLADIVOSTOK COMMERCIAL PORT': ['VLADIVOSTOK COMMERCIAL', 'VLADIVOSTOK COMMERCIAL PORT'],
        'VLADIVOSTOK (VMPP)': ['VLADIVOSTOK (VMPP)', 'VMPP'],
        'VLADIVOSTOK FISH PORT': ['FISH PORT', 'VLADIVOSTOK FISH PORT']
    },
}

CARRIERS = ['NECOLINE', 'TFL', 'LOGOPER', 'MSC', 'EUROSIB']

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
    'SHANGHAI',
    'QINGDAO',
    'TIANJIN',
    'NINGBO',
    'DALIAN',
    'XIAMEN',
    'NANSHA',
    'YANTIAN',
    'SHEKOU',
    'BUSAN'
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
    'ТОЛЬЯТТИ',
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

    'КУНЦЕВО 2',
    'КРЕСТЫ',
    'ТУЧКОВО',
    

]



# RR_NO_CITY = {
#     'Екатеринбург-товарный': 'Екатеринбург',
#     'Ростов-товарный': 'Ростов',
#     'Пенза-2': 'Пенза',
#     'Челябинск-грузовой': 'Челябинск',
#     'Люблино-сортировочный': 'Люблино'
# }