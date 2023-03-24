from sgp4.api import jday
from sgp4.api import Satrec
from sgp4.api import SatrecArray
import json
from api_calls import todays_prefix, check_for_today
import numpy
import datetime
from matplotlib import pyplot


def get_tle_list():
    output = []
    star_out = []
    local_copy_address = todays_prefix() + '.json'
    with open('./api_archive/'+local_copy_address, 'r') as json_blob:
        todays_data = json.load( json_blob)
    for sat in todays_data:
        if outdated(sat):
            continue
        if 'STARLINK' in sat['OBJECT_NAME']:
            star_out.append([
                sat["TLE_LINE1"],
                sat["TLE_LINE2"],
                ])
            continue
        output.append([
            sat["TLE_LINE1"],
            sat["TLE_LINE2"],
            ])
    return output+star_out

def outdated(sat_data):
    epoch_string = sat_data['EPOCH']
    epoch_date = datetime.datetime.strptime(epoch_string, '%Y-%m-%dT%H:%M:%S.%f')
    today = datetime.datetime.today()
    
    if today-epoch_date > datetime.timedelta(days=2):
        print(sat_data['OBJECT_NAME'], 'is out of date', epoch_string)
        print(today, epoch_date, today-epoch_date)
        return True
    return False

def generate_time_stamps():
    today = datetime.date.today()
    today_julian, fraction = jday(today.year, today.month, today.day, 0, 0, 0)
    print(today_julian, fraction)
    jd = numpy.ones(1440)*today_julian
    fr = numpy.linspace(0, 1, num=1440)+fraction
    print(jd[:3])
    print(fr[:3])
    return jd, fr

def find_close_approach(tracks, concerned):
    min_values = []
    for candidate in tracks:
        delta = candidate-concerned
        delta = delta*delta
        delta = delta.sum(axis=1)
        delta = delta**0.5
        # print(delta[:3], min(delta))
        closest = min(delta)
        if  closest == 0:
            # print('got a 0')
            continue
        if numpy.isnan(closest ):
            print('nanny detected')
            continue
        min_values.append(closest)
        # break
    return min(min_values)

def generate_close_approach_matrix(tracks):
    num_total = len(tracks)
    matrix = numpy.zeros((num_total, num_total))
    for ind1, subject in enumerate(tracks):
        for ind2, concerned in enumerate(tracks):
            if ind2 <= ind1:
                continue
            delta = concerned-subject
            delta = delta*delta
            delta = delta.sum(axis=1)
            delta = delta**0.5
            closest = min(delta)
            matrix[ind1][ind2] = closest
            matrix[ind2][ind1] = closest
    return matrix

def second_min(iterable):
    lowest = 10**9
    lowest2 = 10**9-1
    for element in iterable:
        if element < lowest:
            lowest2 = lowest
            lowest = element
            continue
        if element < lowest2:
            lowest2 = element
            continue
    return lowest2

def generate_bar_chart(distances):
    x_vals = numpy.linspace(distances[0], distances[-1], num=10)
    heights = numpy.zeros(10)

    # print(distances[:5])
    # print(x_vals)
    # print(distances[-5:])

    for index, threshold in enumerate(x_vals):
        if index==0:
            continue
        for loc, distance in enumerate(distances):
            if distance < threshold and distance >= x_vals[index-1]:
                # print(loc, distance, threshold)
                heights[index-1]+=1
    heights[-2]+=1

    print(heights, sum(heights), len(distances))
    figure, subplots = pyplot.subplots(1)
    subplots.set_xlabel('kilometers', fontsize=16)
    subplots.set_ylabel('satellites', fontsize=16)
    subplots.set_title(
        'Number of Close Approaches for 200 Satellites', fontsize=16)
    # bar_labels = list(x_vals)
    bar_labels = [' ']*10
    bar_labels[0] = '<%.0f km'%x_vals[1]
    print(bar_labels)
    bar_objects = subplots.bar(
        x_vals, heights, 
        width=4.0, align='edge',
        # {'label':bar_labels}
        # bottom=bar_labels
        )
    subplots.bar_label(bar_objects, bar_labels)
    pyplot.savefig(
        './bar_chart_archive/'+'collision_anxiety_'+todays_prefix()+'.png'
        )
    pyplot.savefig(
        '../docs/images/today.png'
        )

def generate_heat_map(dist_matrix):
    pyplot.clf()
    pyplot.imshow(dist_matrix, cmap='hot', interpolation='nearest')
    pyplot.savefig(
        './heat_map_archive/'+'neighborhood_'+todays_prefix()+'.png'
        )

def main():
    todays_sats = get_tle_list()
    day_vals, fraction_vals = generate_time_stamps()

    sat_objects = [Satrec.twoline2rv(sat[0], sat[1]) for sat in todays_sats]
    sat_array = SatrecArray(sat_objects)
    errors, radii, velocitys = sat_array.sgp4(day_vals, fraction_vals)

    close_approaches = []
    # for index, track in enumerate(radii):
    #     if sum(errors[index]) > 0:
    #         print(index, todays_sats[index])
    #         continue
    #     close_approaches.append(find_close_approach(radii, track))
    close_approach_matrix = generate_close_approach_matrix(radii)
    # close_approahes = [sorted(close_approaches)]
    close_approaches = [second_min(row) for row in close_approach_matrix]
    close_approaches.sort()
    generate_bar_chart(close_approaches)
    generate_heat_map(close_approach_matrix)

    # print(errors[:3])

if __name__ == '__main__':
    main()

'''

'''