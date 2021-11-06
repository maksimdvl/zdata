
from yargy import or_,and_, rule, Parser
from yargy.predicates import gte, lte


def Get_SNILS_spans(text):
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
        result.append(match.span)
    return result


def Get_Passport_spans(text):
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
        result.append(match.span)
    return result

def Get_Phone_spans(text):
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
        result.append(match.span)
    return result




def Get_All_spans(text):
    spans = []
    Phone_spans=Get_Phone_spans(text)
    Snils_spans=Get_SNILS_spans(text)
    Pasport_spans=Get_Passport_spans(text)
    for i in Phone_spans:
        spans.append(i)
    for i in Snils_spans:
        spans.append(i)
    for i in Pasport_spans:
        spans.append(i)
    return spans




