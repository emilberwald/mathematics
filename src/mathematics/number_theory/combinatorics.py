def integer_partitions(number_of_elements,total_sum):
    if number_of_elements == 1:
        yield (total_sum,)
    else:
        for i in range(0,total_sum + 1):
            for j in integer_partitions(number_of_elements - 1,total_sum - i):
                yield (i,) + j
