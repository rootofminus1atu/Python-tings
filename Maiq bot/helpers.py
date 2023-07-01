import inflect
p = inflect.engine()

def pretty_date(date):
    return date.strftime(f"{p.ordinal(date.strftime('%d'))} %B %Y")