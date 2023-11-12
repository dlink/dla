import re
from decimal import Decimal

'''Functions for displaying and storing dimension figures
   all dimensions are stored in the database as Decimals in inches
   Three units of measure (uom) are supported for converting
   from and two display format: in, ft, and mix
'''

SIZE_RANGE_MINS = {
    'Small': 0,
    'Medium': 1800,
    'Large': 8000,
}

class DimensionsError(Exception): pass

def display_dimensions(dec_length, dec_width, dec_height, uom=None):
    '''Given decimal values in inches for l, w, h and a uom
       return a human readable dimension string in one of these
       formats based on uom:
         in:  6 x 6-1/2 x 13 in
         ft:  2 x 2 x 2 ft      (whole numbers only)
         mix: 6'2" x 3'1" x 1'9"

       for 2-D works length is None
         in: 13 x 13 in
    '''
    # if no uom passed in, determine best format
    max_d = 0
    only_ints = True
    for d in dec_length, dec_width, dec_height:
        if(d):
            max_d = max(max_d, d)
            if d % 1 != 0:
                only_ints = False
    if max_d <= 24:
        uom = 'in'
    #elif only_ints:
    #    uom = 'ft'
    else:
        uom = 'mix'

    str = ''
    if dec_length:
        str += \
            f"{dec_to_std(dec_length, uom)} x "
    str += \
        f"{dec_to_std(dec_width , uom)} x " \
        f"{dec_to_std(dec_height, uom)}"
    if uom in ('in', 'ft'):
        str = f'{str} {uom}.'
    return str

def storage_dimensions(std_number, uom):
    '''Given a standard number as string and a uom
       Return a list of l, w, and h as decimals suitable for storing
       in the database.
    '''
    std_number2 = std_number.replace(f'{uom}.', '')
    std_l, std_w, std_h = std_number2.split(' x ')
    return [std_to_dec(std_l, uom),
            std_to_dec(std_w, uom),
            std_to_dec(std_h, uom)]

def std_to_dec(std_number, uom='in'):
    '''Convert US Standard measurement and a uom return it as a Decimal
       value in inches. Three cases:
          1. in:  6-1/4 -> 6.25
          2. ft:  6     -> 72
          3. mix: 6' 0" -> 72
             mix: 6' 2" -> 72.1667
    '''
    if uom == 'in':
        return round(Decimal(std_number\
                             .replace('-1/4', '.25') \
                             .replace('-1/2', '.50') \
                             .replace('-3/4', '.75')), 2)
    elif uom == 'ft':
        return round(Decimal(std_number)*12,4)

    elif uom == 'mix':
        # match: n'[m"]
        pattern = r'(\d+)\'(?:\s*(\d+)\s*"?)?'
        match = re.search(pattern, std_number)
        if match:
            feet = int(match.group(1)) * 12
            inches = 0
            if match.group(2):
                inches = int(match.group(2))
            return round(Decimal(feet + inches/12), 4)
        else:
            raise DimensionsError(
                f"Unrecognized stardard measurement: '{std_number}'")
    else:
        raise DimensionsError(
            f"Unrecognized uom: dec_to_std('{std_number}', '{uom}')")

def dec_to_std(dec_number, uom='in'):
    '''Convert Decimal to US Standard measurement, given uom
       Three cases
         1. 1.25 in   -> 1-1/4 in.
         2. 6 ft      -> 6 ft.
         3. 6.1667 ft -> 6' 2"
    '''
    if uom == 'in':
        return str(round(dec_number, 2))\
            .replace('.00', '')\
            .replace('.25', '-1/4')\
            .replace('.50', '-1/2')\
            .replace('.75', '-3/4')

    elif uom == 'ft':
        return str(dec_number // 12)

    elif uom == 'mix':
        dec_int= round(dec_number, 0)
        #inches = round((dec_number-dec_int) * 12, 0)
        feet = dec_int//12
        inches = dec_int-(feet*12)
        if inches:
            return f'{feet}\'{inches}"'
        else:
            return f'{feet}\''
    else:
        raise DimensionsError(
            f"Unrecognized uom: dec_to_std('{round(dec_number, 4)}', '{uom}')")

def getSizeRange(area):
    if not area:
        return None
    if area >= SIZE_RANGE_MINS['Large']:
        return 'Large'
    elif area >= SIZE_RANGE_MINS['Medium']:
        return 'Medium'
    else:
        return 'Small'

#if __name__ == '__main__':
    #print(storage_dimensions('6\'2" x 3\'1" x 1\'9"', 'mix'))
    #print(display_dimensions(20.0,20.00, 72.00))
    #print(display_dimensions(72.17,36.08, 12.75))
