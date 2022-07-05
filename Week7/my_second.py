#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, tour_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def city_number_to_distance(city1, city2, cities):
    return distance(cities[city1], cities[city2])

# def solve(cities):
#     N = len(cities)

#     dist = [[0] * N for i in range(N)]
#     for i in range(N):
#         for j in range(i, N):
#             dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

#     current_city = 0
#     unvisited_cities = set(range(1, N))
#     tour = [current_city]

#     while unvisited_cities:
#         next_city = min(unvisited_cities,
#                         key=lambda city: dist[current_city][city])
#         unvisited_cities.remove(next_city)
#         tour.append(next_city)
#         current_city = next_city
#     return tour

def get_better_tour_sa(tour, cities):#交差をなくす
    for i in range(len(tour)):
        for j in range(i+1, len(tour)+1):
            prev = city_number_to_distance(tour[i], tour[(i+1)%len(tour)], cities) + city_number_to_distance(tour[j%len(tour)], tour[j-1], cities)
            new = city_number_to_distance(tour[j%len(tour)], tour[(i+1)%len(tour)], cities) + city_number_to_distance(tour[i], tour[j-1], cities)
            cost = new - prev
            if cost < 0:
                tour[i+1:j] = tour[j-1:i:-1]
    return tour

def one_or_opt(tour, cities):#1つの点を辺の途中に挿入するかどうか
    N = len(tour)
    for i in range(N):
        for j in range(N):
            prev = city_number_to_distance(tour[i-1], tour[i], cities) + city_number_to_distance(tour[i], tour[(i+1)%N], cities) + city_number_to_distance(tour[j], tour[(j+1)%N], cities)
            new = city_number_to_distance(tour[i-1], tour[(i+1)%N], cities) + city_number_to_distance(tour[j], tour[i], cities) + city_number_to_distance(tour[i], tour[(j+1)%N], cities)
            if prev > new:
                if i < j:
                    a = tour.pop(i)
                    tour.insert(j, a)
                elif j < i:
                    #tour = tour[:j+1] + tour[i:i+1] + tour[j+1:i] + tour[i+1:]
                    a = tour.pop(i)
                    tour.insert(j+1, a)
    return tour

def two_or_opt(tour, cities):#2点をまとめて別の場所に挿入
    N = len(tour)
    for i in range(N-1):
        for j in range(N):
            prev = city_number_to_distance(tour[i-1], tour[i], cities) + city_number_to_distance(tour[(i+1)%N], tour[(i+2)%N], cities) + city_number_to_distance(tour[j], tour[(j+1)%N], cities)
            new = city_number_to_distance(tour[i-1], tour[(i+2)%N], cities) + city_number_to_distance(tour[j], tour[i], cities) + city_number_to_distance(tour[(i+1)%N], tour[(j+1)%N], cities)
            if prev > new:
                if i < j:
                    a = tour.pop(i)
                    b = tour.pop(i)
                    tour.insert(j-1, b)
                    tour.insert(j-1, a)
                elif j < i:
                    a = tour.pop(i)
                    b = tour.pop(i)
                    tour.insert(j+1, b)
                    tour.insert(j+1, a)
            else:
                # prev = city_number_to_distance(tour[i-1], tour[i], cities) + city_number_to_distance(tour[(i+1)%N], tour[(i+2)%N], cities) + city_number_to_distance(tour[j], tour[(j+1)%N], cities)
                new = city_number_to_distance(tour[i-1], tour[(i+2)%N], cities) + city_number_to_distance(tour[j], tour[(i+1)%N], cities) + city_number_to_distance(tour[i], tour[(j+1)%N], cities)
                if prev > new:
                    if i < (j-2)%N:
                        a = tour.pop(i)#i
                        b = tour.pop(i)#i+1
                        tour.insert(j-1, a)
                        tour.insert(j-1, b)
                    elif j < (i-1)%N:
                        a = tour.pop(i)
                        b = tour.pop(i)
                        tour.insert(j+1, a)
                        tour.insert(j+1, b)
    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 2
    cities = read_input(sys.argv[1])
    tour = tour_input(sys.argv[2])
    for i in range(5):
      tour = get_better_tour_sa(tour, cities)
      tour = one_or_opt(tour, cities)
      tour = two_or_opt(tour, cities)
    
    print_tour(tour)