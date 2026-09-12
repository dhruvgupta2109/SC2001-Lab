'''
SC2001 LAB-1:
1. Gupta Dhruv
2. ADD YOUR NAME
3. ADD YOUR NAME
'''

import random
import time

# 1. insertion sort 
def insertion_sort(L, left, right, counter):
    for i in range(left + 1, right + 1):
        key = L[i]
        j = i - 1
        while j >= left:
            counter[0] += 1  
            if L[j] > key:
                L[j + 1] = L[j]
                j -= 1
            else:
                break
        L[j + 1] = key
    return L


# 3. og merge sort (baseline)
def original_merge_sort(L, left, right, counter):
    if left < right:
        mid = (left + right) // 2
        original_merge_sort(L, left, mid, counter)
        original_merge_sort(L, mid + 1, right, counter)
        merge(L, left, mid, right, counter)
    return L


# 4. hybrod sort (merge sort + insertion sort switch at threshold S)
def hybrid_sort(L, left, right, S, counter):
    size = right - left + 1
    if size <= S:
        insertion_sort(L, left, right, counter)
    else:
        mid = (left + right) // 2
        hybrid_sort(L, left, mid, S, counter)
        hybrid_sort(L, mid + 1, right, S, counter)
        merge(L, left, mid, right, counter)
    return L


# 2. merge (helper func for both merge sort versions)
def merge(L, left, mid, right, counter):
    left_part = L[left:mid + 1]
    right_part = L[mid + 1:right + 1]

    i = 0     
    j = 0   
    k = left    

    while i < len(left_part) and j < len(right_part):
        counter[0] += 1  
        if left_part[i] <= right_part[j]:
            L[k] = left_part[i]
            i += 1
        else:
            L[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        L[k] = left_part[i]
        i += 1
        k += 1
    while j < len(right_part):
        L[k] = right_part[j]
        j += 1
        k += 1


# 5. random data generator
def generate_random_Lay(n, max_value=1000000):
    return [random.randint(1, max_value) for i in range(n)]

# 6. demo
S = 10       
n= 10000

data = generate_random_Lay(n)
data_for_hybrid = data.copy()
data_for_original = data.copy()

#hybrid sort
comparisons_hybrid = [0]
start = time.process_time()
hybrid_sort(data_for_hybrid, 0, n - 1, S, comparisons_hybrid)
time_hybrid = time.process_time() - start

#merge sort
comparisons_original = [0]
start = time.process_time()
original_merge_sort(data_for_original, 0, n - 1, comparisons_original)
time_original = time.process_time() - start

# confirm
assert data_for_hybrid == sorted(data), "Hybrid sort incorrect"
assert data_for_original == sorted(data), "Merge sort incorrect"

print(f"Array size: {n:,}   S = {S}")
print(f"Hybrid sort : comparisons: {comparisons_hybrid[0]:,}   time: {time_hybrid:.4f}s")
print(f"Merge sort  : comparisons: {comparisons_original[0]:,}   time: {time_original:.4f}s")