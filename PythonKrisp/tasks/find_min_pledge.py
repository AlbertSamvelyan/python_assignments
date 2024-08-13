def find_min_pledge(pledge_list):
    pledge_list_sorted = sorted(pledge_list)
    i, j = 0, len(pledge_list_sorted) - 1

    if pledge_list_sorted[j] < 0:
        return 1

    while i < j:
        if pledge_list_sorted[i] < 0:
            i += 1
        elif (pledge_list_sorted[i + 1] - pledge_list_sorted[i]) > 1:
            return pledge_list_sorted[i] + 1
        else:
            i += 1
    return pledge_list_sorted[i] + 1
        
res = find_min_pledge([-1, -3])
print(res)
#assert find_min_pledge([1, 3, 6, 4, 1, 2]) == 5
#assert find_min_pledge([1, 2, 3]) == 4
#assert find_min_pledge([-1, -3]) == 1