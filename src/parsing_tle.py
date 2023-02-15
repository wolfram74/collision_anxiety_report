# https://pypi.org/project/sgp4/
from sgp4.api import jday
from sgp4.api import Satrec

# https://en.wikipedia.org/wiki/Two-line_element_set
demo_tle = '''0 ONEWEB-0716
1 55177U 23004AP  23018.75001157 -.00057913  00000-0 -58498-2 0  9997
2 55177  86.5133 282.0024 0012666 183.9121  98.4018 14.91413721  1427
'''

def parse_tle_set(tle_set):

    pass

def to_radius(cartesian):
    return (sum([el**2 for el in cartesian]))**.5

def print_distance(body):
    low = 6962
    high = 6985.2
    average = (low+high)/2
    last = 1
    for i in range(180):
        julian_date, fraction = jday(2023, 1, 18, 18, i ,0)
        error, position, velocity = body.sgp4(julian_date, fraction)
        displace = to_radius(position)-average
        if last*displace < 0:
            print(i, last, displace)
        last = displace
        # print( "%03d, %02.3f" % (i, displace) )

def main():
    lines = demo_tle.split('\n')
    print(lines)
    julian_date, fraction = jday(2023, 1, 18, 18, 0 ,0)
    print(julian_date, fraction)
    oneweb = Satrec.twoline2rv(lines[1], lines[2])
    error, position, velocity = oneweb.sgp4(julian_date, fraction)
    print(error)
    print(position, to_radius(position))
    print(velocity)
    
    # print_distance(oneweb)

if __name__ == '__main__':
    main()

'''

'''