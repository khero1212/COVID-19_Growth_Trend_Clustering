
import csv
from scipy.spatial import distance
import math
import numpy as np
from scipy.spatial.distance import pdist,squareform


def load_data(filepath):
    time_series = []
    
    with open(filepath, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "Long" in row:
                row.pop("Long")
            if "Lat" in row:
                row.pop("Lat")
            time_series.append(dict(row))
    
    return time_series

def calculate_x_y(time_series):
    value_list = list(time_series.values())
    del value_list[0]
    del value_list[0]
    value_list = list(map(lambda x: int(x),value_list))
    n = len(value_list)
    x, y, ten_index, hundred_index = 0,0,0,0
    
    
    if value_list[n-1] <= 0:
        x = math.nan
        y = math.nan
        return (x,y)
    
    for i in range(n):
        if value_list[i] <= (value_list[n-1]/10) and i == n-1:
            ten_index = i
            break
        elif value_list[i] <= (value_list[n-1]/10) and value_list[i+1] > (value_list[n-1]/10):
            ten_index = i
            break
    
    x = n - 1 - ten_index
            
    for j in range(n):
        if value_list[j] <= (value_list[n-1]/100) and j == n-1:
            hundred_index = j
            break
        elif value_list[j] <= (value_list[n-1]/100) and value_list[j+1] > (value_list[n-1]/100):
            hundred_index = j
            break    
    
    if hundred_index == 0 and value_list[n-1]/100 < value_list[hundred_index]:
        y = math.nan
    else:
        y = ten_index - hundred_index
        
    return (x,y)


def min_dist(cluster_one, cluster_two):
    final_dist = math.inf
    
    for point_one in cluster_one:
        for point_two in cluster_two:
            euc_dist = distance.euclidean(point_one, point_two)
            if euc_dist <= final_dist:
                final_dist = euc_dist
    
    return final_dist

def cluster_dist(feature1, feature2, distance_array):
    dist = float('inf')
    for x in feature1:
        for y in feature2:

            if x != y and distance_array[x][y] < dist:
                dist = distance_array[x][y]
    return dist


def min_clusters(dataset, temp_dict, distance_array):
    min_dist = float('inf')
    cluster_one = None
    cluster_two = None
    for cluster1 in temp_dict:
        for cluster2 in temp_dict:
            if cluster1 != cluster2:
                d = cluster_dist(temp_dict[cluster1], temp_dict[cluster2], distance_array)
                if d < min_dist:
                    min_dist = d
                    cluster_one = cluster1
                    cluster_two = cluster2
                elif min_dist == d:
                    if cluster1 < cluster_one:
                        cluster_one = cluster1
                        cluster_two = cluster2
                    elif cluster1 == cluster_one:
                        if cluster2 < cluster_two:
                            cluster_two = cluster2
    return cluster_one, cluster_two, min_dist


def hac(dataset):
    new_dataset = []
    for x in range(len(dataset)):
         if not(math.isnan(dataset[x][0])) and not(math.isnan(dataset[x][1])):
                   new_dataset.append(dataset[x]) 
    dataset = new_dataset
    m = len(dataset)
    final = np.zeros((m - 1, 4))
    temp_dict = {}
    for i in range(m):
        temp_dict[i] = np.array([i])
    distance_matrix = squareform(pdist(dataset))
    for i in range(m - 1):
        (cluster_one, cluster_two, minimum) = min_clusters(dataset, temp_dict, distance_matrix)
        final[i, 0] = cluster_one
        final[i, 1] = cluster_two
        final[i, 2] = minimum
        final[i, 3] = len(temp_dict[cluster_one]) + len(temp_dict[cluster_two])
        temp_dict[m + i] = np.concatenate([temp_dict.pop(cluster_one), temp_dict.pop(cluster_two)])
    return final