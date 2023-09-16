from decimal import Decimal

def std_to_dec(std_number):
    '''Convert US Standard measurement to Decimal: 1-1/4 -> 1.25'''
    return round(Decimal(std_number\
                         .replace('-1/4', '.25') \
                         .replace('-1/2', '.50') \
                         .replace('-3/4', '.75')), 2)

def dec_to_std(dec_number):
    '''Convert Decimal to Us Standard measurement: 1.25 -> 1-14'''
    return str(round(dec_number, 2))\
        .replace('.00', '')\
        .replace('.25', '-1/4')\
        .replace('.50', '-1/2')\
        .replace('.75', '-3/4')
