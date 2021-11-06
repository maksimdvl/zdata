from natasha import *
from natasha.markup import (
    show_markup_notebook as show_markup,
    format_json, show_json
)

First_example="""обращение товарища Петрова в адрес организации Московский Буллчник по улице Фрунзе, д12, о том что я уходя домой с работы подскользнулся у дома номер 8 не далеко от своего места жительства по улице Чураева, д. 1"""

example = """(08.11.1957 года рождения, уроженца Ростовской области,
г.Шахты, зарегистрированного по адресу: Ростовская область, г. Шахты,
ул. Гагарина, д.45, кв. 264, СНИЛС xxx-xxx-xx-xx, ИНН xxxxxxxxxxxx)"""

extractors = [
    NamesExtractor(),
    AddressExtractor(),
    DatesExtractor(),
    MoneyExtractor()
]


spans = []
facts = []
for extractor in extractors:
    matches = extractor(example)
    spans.extend(_.span for _ in matches)
    facts.extend(_.fact.as_json for _ in matches)


print(facts)


from yargy import or_,and_, rule, Parser
from yargy.predicates import caseless, normalized, dictionary
from yargy.predicates import gte, lte


def Get_SNILS(text):
    Section_SNILS_1 = and_(
        gte(0),
        lte(999)
    )
    Section_SNILS_2 = and_(
        gte(1000000000),
        lte(9999999999)
    )


    SNILS = or_(
        rule(
        Section_SNILS_1,
        '-',
        Section_SNILS_1,
        '-',
        Section_SNILS_1,
        '-',
        Section_SNILS_1),
        rule(
        'СНИЛС',
        Section_SNILS_1,
        '-',
        Section_SNILS_1,
        '-',
        Section_SNILS_1,
        '-',
        Section_SNILS_1),
        rule(
        Section_SNILS_2
        )

    )
    parser = Parser(SNILS)
    result = []
    for match in parser.findall(text):
        # print(match.span, [_.value for _ in match.tokens])
        result.append([_.value for _ in match.tokens])
    return result

text = '''
8 января 2014 года, 15 июня 2001 г.,
31 февраля 2018 СНИЛС 9992243611'''

print(Get_SNILS(text))

def Return_Passport(text):
    Section_Pasport_serial = and_(
        gte(0000),
        lte(9999)
    )
    Section_Pasport_Nomer = and_(
        gte(000000),
        lte(999999)
    )
    Pasport = or_(
        rule(
            'серия',
            Section_Pasport_serial,
            'номер',
            Section_Pasport_Nomer
        ),
        rule(
            "Паспорт",
            Section_Pasport_serial,
            Section_Pasport_Nomer
        ),
        rule(
            "паспорт",
            Section_Pasport_serial,
            Section_Pasport_Nomer
        ),
        rule(
            "РФ",
            Section_Pasport_serial,
            Section_Pasport_Nomer
        ),
        rule(
            'серия',
            Section_Pasport_serial,
            Section_Pasport_Nomer
        ),
        rule(
            Section_Pasport_serial,
            'номер',
            Section_Pasport_Nomer
        ),
    )
    parser = Parser(Pasport)
    result = []
    for match in parser.findall(text):
        #print(match.span, [_.value for _ in match.tokens])
        result.append([_.value for _ in match.tokens])
    return result

def Return_Phone(text):
    Section_Phone_plus_7 = and_(
        gte(70000000000),
        lte(79999999999)
    )
    Section_Phone_Sot = and_(
        gte(80000000000),
        lte(89999999999)
    )
    Phone = or_(
        rule(
        Section_Phone_Sot,
        ),
        rule(
        Section_Phone_plus_7,
        )
    )
    parser = Parser(Phone)
    result=[]
    for match in parser.findall(text):
        print(match.span, [_.value for _ in match.tokens])
        result.append([_.value for _ in match.tokens])
    return result


text = '''
8 января 2014 года, 15 июня 2001 г.,
31 февраля 2018 СНИЛС 999-222-33-11 ИНН 123456789101 Паспорт серия 1234 номер 212223 тел. 89648335821  +74952285701'''
#for match in parser.findall(text):
    #print(match.span, [_.value for _ in match.tokens])


print (Return_Phone(text))