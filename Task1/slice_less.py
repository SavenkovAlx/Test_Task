def slice_less(my_list, lesser):
    return sorted(filter(lambda i: i > lesser, my_list), reverse=True)
