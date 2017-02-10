def lz78_compress(input_string):
    d = {}
    d_counter = 1
    output_stream = []
    w = ''

    for K in input_string:
        if w + str(K) in d:
            w = w + str(K)
        else:
            output_stream.append((d[w] if w in d else 0, K))
            d[w + str(K)] = d_counter
            d_counter += 1
            w = ''

    if w != '':
        output_stream.append((d[w], 0))

    print "Size of dict at the end of compression = {}".format(len(d))
    return output_stream


def lz78_decompress(input_stream):
    d = ['']

    output_string = ''

    for idx, symbol in input_stream:
        symbol = str(unichr(symbol))
        output_string += d[idx]
        output_string += symbol
        d.append(d[idx] + symbol)

    return output_string[:-1]


def run_test():
    sample_in = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
    deserunt mollit anim id est laborum."""

    compressed = lz78_compress(bytearray(sample_in))
    decompressed = lz78_decompress(compressed)

    assert decompressed == sample_in
    print "Len of in: {}, len of compressed = {}, ratio = {:.2%}".format(
        len(sample_in), len(compressed), float(len(compressed)) / len(sample_in)
    )
