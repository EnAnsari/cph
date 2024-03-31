def tester(input_sample, output_sample):
    result = True
    items_in = input_sample.split()
    items_in = [item.strip() for item in items_in]
    items_out = output_sample.split()
    items_out = [item.strip() for item in items_out]

    return result