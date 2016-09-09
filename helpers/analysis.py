from fp_growth import find_frequent_itemsets

def ship_log_analyzer(log_array, customer):
    array = []
    with open("shipping_analysis.csv") as file:
        for line in file:
            array.append(line.strip('\n').split(','))
    items = find_frequent_itemsets(array, 50)
    items = [item for item in items if customer in item]
    for item in items:
        print(item)
    out_array = log_array[:]
    for log_item in log_array:
        refs = log_item[1].pop(2) + ' ' + log_item[1].pop(1)
        refs = refs.split(' ')
        log_item[1] += refs
        print("Item: ", log_item[1])
        distance = 0
        for item in items:
            #print(item)
            #print(len(set(log_item[1]).intersection(item)))
            if len(set(log_item[1]).intersection(item)) > distance:
                distance = len(set(log_item[1]).intersection(item))
                print("Rule: ", item, " | Intersect: ",
                      len(set(log_item[1]).intersection(item)),
                      " | New Distance: ", distance)
        if distance < 3:
            out_array.remove(log_item)
    print(out_array)
    return out_array
