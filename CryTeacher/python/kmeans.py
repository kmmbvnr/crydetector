#!/opt/pypy/bin/pypy
# -*- coding: utf-8; mode: django -*-
import os
import sys
import random
from glob import glob
from itertools import izip


PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')


def read_all_logs():
    result = {}
    for filename in glob("%s/*.txt" % LOGS_DIR):
        with open(filename) as filehandle:
            result[filename] = []
            for line in filehandle:
                result[filename].append(eval(line[34:])[:128])
    return result


def logs_iterator(logs):
    for content in logs.itervalues():
        for row in content:
            yield row

def raw_logs(logs):
    result = []
    for row in logs_iterator(logs):
        result.append(row)
    return result


def find_closest_centroids(data, centroids):    
    result = []
    error = 0
    for row in data:
        min_centroid, min_length = -1, sys.maxint
        for pos in range(len(centroids)):
            length = sum((r-c)**2 for r,c in izip(row, centroids[pos]))
            if length < min_length:
                min_centroid = pos
                min_length = length
        result.append(min_centroid)
        error += min_length
    return result, error


def compute_means(data, idx, count):
    counts = [0.] * count
    centroids = [[0]*len(data[0]) for _ in range(count)]
    for row, cpos in izip(data, idx):
        counts[cpos] += 1
        for pos in range(len(row)):
            centroids[cpos][pos] += row[pos]

    for cpos in range(count):
        for pos in range(len(data[0])):
            centroids[cpos][pos] /= counts[cpos]

    return centroids


def kmeans(data, count=2, iterations=10):
    centroids = random.sample(data, count)

    for _ in range(iterations):
        idx, error = find_closest_centroids(data, centroids)
        centroids = compute_means(data, idx, count)
    return centroids, idx, error


print "Reading data... ",
logs = read_all_logs()
data = raw_logs(logs)
random.shuffle(data)
print "Done."

def select_cluster_count():
    """
    2, 14729243.8236, 439.968220339, 0.332628611698 ;
    3, 13250748.6465, 406.877293578, 0.30725863284 ;
    4, 12337656.9637, 342.303155007, 0.256871035941 ;
    5, 11766481.6898, 245.015384615, 0.160324171952 ;
    6, 11442216.8301, 243.181818182, 0.158914728682 ;
    7, 11065847.5602, 235.671201814, 0.155391120507 ;
    8, 10803030.8082, 210.426470588, 0.143763213531 ;
    9, 10579679.5685, 209.074812968, 0.141296687808 ;
    10, 10447796.8507, 169.558404558, 0.123678646934 ;
    11, 10303579.0753, 182.743362832, 0.119450317125 ;
    12, 10183409.9668, 172.811764706, 0.119802677942 ;
    13, 10101993.0356, 182.019553073, 0.126145172657 ;
    14, 9943968.93319, 150.694630872, 0.105003523608 ;
    15, 9862252.00339, 160.176119403, 0.118040873855 ;
    16, 9781849.26519, 143.547038328, 0.101127554616 ;
    17, 9744460.41156, 152.62541806, 0.105355884426 ;
    18, 9622590.37691, 134.414814815, 0.0951374207188 ;
    19, 9562832.23588, 163.139318885, 0.113812544045 ;
    20, 9500426.28536, 147.277027027, 0.104298801973 ;
    21, 9476903.41264, 122.268595041, 0.0852713178295 ;
    22, 9383122.65363, 147.335640138, 0.101832276251 ;
    23, 9365251.16538, 133.244444444, 0.0951374207188 ;
    """
    for count in range(2, 24):
        centroids, idx, error = kmeans(data, count=count, iterations=100)

        sums = [sum(c) for c in centroids]
        mins = sums[:]
        mins.sort()    
        min_centroid = sums.index(mins[0])
        noise_points = 1.0*sum([c == min_centroid for c in idx])/len(data)
    
        print "%s, %s, %s, %s ;" % (count, error, mins[0], noise_points)



def print_selected_centroids_filter():
    """
    cry9.txt     0.33
    nocry11.txt  0.06
    nocry5.txt   0.0
    nocry3.txt   0.16
    cry7.txt     0.62
    cry15.txt    0.61
    nocry1.txt   0.0
    nocry15.txt  1.0
    nocry4.txt   0.3
    nocry7.txt   0.13
    cry12.txt    0.24
    cry2.txt     0.5
    cry1.txt     0.56
    cry3.txt     0.45
    nocry9.txt   0.96
    cry6.txt     0.22
    nocry10.txt  0.13
    nocry6.txt   0.10
    nocry17.txt  0.01
    nocry14.txt  0.0
    cry10.txt    0.25
    nocry13.txt  0.0
    cry5.txt     0.3
    nocry12.txt  0.0
    nocry8.txt   0.0
    cry11.txt    0.21

    Selected centroid:
    [ 13.89, 10.68, 8.49, 6.49, 5.58, 5.07, 4.96, 5.39,
      6.71, 7.3, 7.66, 8.02, 7.79, 7.25, 6.44, 6.3,
      6.02, 5.71, 5.4, 5.12, 4.69, 4.3, 4.48, 3.88,
      3.53, 3.67, 3.32, 3.0, 3.15, 3.44, 4.31, 4.67,
      3.63, 3.04, 2.66, 2.45, 2.36, 2.37, 2.02, 1.91,
      1.69, 1.86, 1.68, 1.5, 1.41, 1.5, 1.66, 1.54,
      1.69, 1.4, 1.32, 1.43, 1.34, 1.4, 1.31, 1.11,
      1.21, 1.44, 1.4, 1.49, 1.56, 1.37, 1.19, 1.35,
      1.42, 1.52, 1.52, 1.46, 1.16, 1.42, 1.41, 1.38,
      1.43, 1.18, 1.38, 1.45, 1.36, 1.44, 1.82, 2.91,
      2.44, 1.61, 1.42, 1.19, 1.2, 1.08, 1.08, 1.04,
      1.07, 0.94, 1.04, 0.88, 0.88, 0.96, 0.91, 0.87,
      0.88, 0.82, 0.9, 0.99, 0.93, 0.91, 0.88, 0.95,
      0.83, 0.95, 0.91, 1.07, 1.17, 1.3, 1.11, 1.06,
      0.89, 1.08, 1.08, 1.08, 1.05, 1.04, 1.15, 1.1,
      1.02, 1.08, 1.14, 0.99, 0.96, 0.81, 0.8, 0.97 ]

    Or, if rounded

    [ 13.0, 8.0, 5.0, 4.0, 3.0, 2.0, 2.0, 2.0,
      3.0, 4.0, 4.0, 5.0, 5.0, 5.0, 4.0, 4.0,
      4.0, 3.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0,
      3.0, 3.0, 3.0, 2.0, 3.0, 3.0, 4.0, 5.0,
      3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
      2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0,
      2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 4.0,
      3.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 ]
    
    """
    centroids, idx, error = kmeans(data, count=5, iterations=100)
    sums = [sum(c) for c in centroids]
    mins = sums[:]
    mins.sort()    
    min_centroid = sums.index(mins[0])

    for pos in range(len(centroids)):
        centroids[pos] = [round(x) for x in centroids[pos]]

    for filename, rows in logs.iteritems():
        idx, error = find_closest_centroids(rows, centroids)
        noise_points = 1.0*sum([c == min_centroid for c in idx])/len(rows)
        print filename, error, round(noise_points, 2)

    print "Selected centroid:"
    print [round(x,0) for x in centroids[min_centroid]]


def classify_with_noice_centroid():
    centroids, idx, error = kmeans(data, count=5, iterations=100)
    sums = [sum(c) for c in centroids]
    mins = sums[:]
    mins.sort()    
    min_centroid = sums.index(mins[0])

    output = os.path.join(PROJECT_ROOT, 'matlab', 'data.txt')
    with open(output, 'w') as output_file:
        for filename, rows in logs.iteritems():
            if 'nocry' in filename:
                for row in rows:
                    output_file.write("%s, 0, 0\n" % ",".join(str(r) for r in row))
            else:
                idx, error = find_closest_centroids(rows, centroids)
                for pos in range(len(rows)):
                    if idx[pos] == min_centroid:
                        output_file.write("%s, 0, 1\n" % ",".join(str(r) for r in rows[pos]))
                    else:
                        output_file.write("%s, 1, 1\n" % ",".join(str(r) for r in rows[pos]))


# print_selected_centroids_filter()
classify_with_noice_centroid()
