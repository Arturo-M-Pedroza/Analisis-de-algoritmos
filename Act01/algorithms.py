#libreries 
import tkinter as tk
import random as rd

def binarySearch(list, number):

    left = 0
    right = len(list) - 1

    while left <= right: # Binary search loop
        mid = (left + right) // 2

        if list[mid] == number:
            print(f"Binary Search Index: {mid}")
            return mid
        elif list[mid] < number:
            left = mid + 1
        else:
            right = mid - 1 

    return -1  # Number not found in the list

def linealSearch(list, number):

    for i in range(len(list)):
        if list[i] == number:
            print(f"Lineal Search Index: {i}")
            return i
    
    return -1 # Number not found in the list
    

def generateList(size):
    list = []
    for i in range(size):
        list.append(rd.randint(0, size))
        
    print("List generated:", list)

    return list
