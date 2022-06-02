import re


PATTERN_PARENTHESIS = re.compile(r'[-a-zA-ZÀ-ÖØ-öø-ÿ|0-9]*\([-a-zA-ZÀ-ÖØ-öø-ÿ|\W|0-9]*\)[-a-zA-ZÀ-ÖØ-öø-ÿ|0-9]*', re.UNICODE)

PATTERN_DATE = r'(\d+)([a-zA-Z]*)(\d+)'

PATTERN_ORCID = r'(.*)(\d{4}-\d{4}-\d{4}-\d{3}[\d|X|x])(.*)'

# https://www.crossref.org/blog/dois-and-matching-regular-expressions/ (accessed on 2021/08/31)
PATTERNS_DOI = [re.compile(pd) for pd in [
    r'10.\d{4,9}/[-._;()/:A-Z0-9]+$',
    r'10.1002/[^\s]+$',
    r'10.\d{4}/\d+-\d+X?(\d+)\d+<[\d\w]+:[\d\w]*>\d+.\d+.\w+;\d$',
    r'10.1207/[\w\d]+\&\d+_\d+$',
    r'10.\d{4,9}/[-._;()/:a-zA-Z0-9]*']
]

# https://en.wikipedia.org/wiki/International_Standard_Serial_Number (accessed on 2021/08/31)
PATTERN_ISSN_WITHOUT_HYPHEN = re.compile(r'^[0-9]{4}[0-9]{3}[0-9xX]$')
PATTERN_ISSN_WITH_HYPHEN = re.compile(r'^[0-9]{4}-[0-9]{3}[0-9xX]$')

PATTERN_PAGE_RANGE = r'(\d*)[-|_|:|;|,|.](\d*)'

JOURNAL_TITLE_SPECIAL_CHARS = {
    '@',
    '&'
}

JOURNAL_TITLE_SPECIAL_WORDS = {
    'impresso',
    'print',
    'impreso',
    'online',
    'eletronico',
    'electronico',
    'cdrom'
}

PUNCTUATION_TO_REMOVE_FROM_TITLE_VISUALIZATION = {
    ',',
    '.',
    ';',
    ':',
    ' '
}

PUNCTUATION_TO_KEEP_IN_PERSONS_NAME_VISUALIZATION = {
    ','
}

TEXT_MONTH_TO_NUMERIC_MONTH = {
    'janeiro':'01',
    'jan':'01',
    'enero':'01',
    'january':'01',
    'fevereiro':'02',
    'fev':'02',
    'febrero':'02',
    'february':'02',
    'feb':'02',
    'março':'03',
    'mar':'03',
    'marzo':'03',
    'march':'03',
    'abril':'04',
    'abr':'04',
    'april':'04',
    'apr':'04',
    'maio':'05',
    'mai':'05',
    'mayo':'05',
    'may':'05',
    'junho':'06',
    'jun':'06',
    'junio':'06',
    'june':'06',
    'julho':'07',
    'jul':'07',
    'julio':'07',
    'july':'07',
    'agosto':'08',
    'ago':'08',
    'august':'08',
    'aug':'08',
    'setembro':'09',
    'set':'09',
    'septiembre':'09',
    'sept':'09',
    'september':'09',
    'sep': '09',
    'outubro':'10',
    'out':'10',
    'octubre':'10',
    'oct':'10',
    'october':'10',
    'novembro':'11',
    'nov':'11',
    'noviembre':'11',
    'november':'11',
    'dezembro':'12',
    'dez':'12',
    'diciembre':'12',
    'dic':'12',
    'december':'12',
    'dec':'12',
}

DATE_SEPARATORS = {
    '/',
    '.',
    ' ',
    '-'
}

PUNCTUATION_TO_DEFINE_PAGE_RANGE = {
    '-',
    '_',
    ':',
    ';',
    ',',
    '.'
}
