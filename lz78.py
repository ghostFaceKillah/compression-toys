import ipdb
import struct

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

    # print "Size of dict at the end of compression = {}".format(len(d))

    resu = bytearray()
    for x, y in output_stream:
        resu += struct.pack('H', x)
        resu += struct.pack('H', y)

    return resu


def lz78_decompress(input_bytes):
    d = ['']

    output_string = ''

    input_stream = []

    for idx in xrange(len(input_bytes) / 4):
        x, y = struct.unpack('HH', input_bytes[4 * idx: 4 * (idx + 1)])
        # print idx
        # print x, y
        y = str(unichr(y))
        input_stream.append((x, y))

    for idx, symbol in input_stream:
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


def run_on_file(in_name, out_name, compress):
    with open(in_name, 'rb') as f:
        in_bytes = bytearray(f.read())

    f = lz78_compress if compress else lz78_decompress

    out_bytes = bytearray(f(in_bytes))

    with open(out_name, 'wb') as f:
        f.write(out_bytes)


if __name__ == "__main__":
    # run_test()
    run_on_file('test.txt', 'one.txt', True)
    run_on_file('one.txt', 'two.txt', compress=False)
