CONTAINER_OPTIONS = (
    ('20DC', '20DC'),
    ('H0HC', '40HC'),
)


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


RR_NO_CITY = {
    'Екатеринбург-товарный': ''
}