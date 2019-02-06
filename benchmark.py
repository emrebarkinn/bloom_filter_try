from memory_usage import memory_usage
from bloomFilter import BloomFilter
from countingBloomFilter import CountingBloomFilter
from scalableBloomFilter import ScalableBloomFilter


def main():
    input_size = 100000
    bloom_filter = BloomFilter(input_size, 0.01)

    for i in range(0, input_size):
        bloom_filter.add(str(i))

    fp_count = 0
    for i in range(input_size, input_size * 2):
        if str(i) in bloom_filter:
            fp_count += 1

    print("Expected false positive rate for all calculations is : 0.01")
    print("For Standard Bloom Filter : \nFalse positive count:" + str(fp_count) + "  in " + str(input_size) + " try. " + str(
        (fp_count / input_size)) + " rate of false positive")

    counting_bloom_filter = CountingBloomFilter(input_size, 0.01)

    for i in range(0, input_size):
        counting_bloom_filter.add(str(i))

    fp_count = 0
    for i in range(input_size, input_size * 2):
        if str(i) in counting_bloom_filter:
            fp_count += 1

    print("For counting filter :\nFalse positive count:" + str(fp_count) + "  in " + str(input_size) + " try. " + str(
        (fp_count / input_size)) + " rate of false positive")

    scalable_bloom_filter = ScalableBloomFilter(fp_prob=0.01, growth=ScalableBloomFilter.LARGE_GROWTH)

    for i in range(0, input_size):
        scalable_bloom_filter.add(str(i))

    fp_count = 0
    for i in range(input_size, input_size * 2):
        if str(i) in scalable_bloom_filter:
            fp_count += 1

    print("For scalable filter :\nFalse positive count:" + str(fp_count) + "  in " + str(input_size) + " try. " + str(
        (fp_count / input_size)) + " rate of false positive")

    c_scalable_bloom_filter = ScalableBloomFilter(fp_prob=0.01, growth=ScalableBloomFilter.LARGE_GROWTH,countable=True)

    for i in range(0, input_size):
        c_scalable_bloom_filter.add(str(i))

    fp_count = 0
    for i in range(input_size, input_size * 2):
        if str(i) in c_scalable_bloom_filter:
            fp_count += 1

    print("For counting scalable filter :\nFalse positive count:" + str(fp_count) + "  in " + str(input_size) + " try. " + str(
        (fp_count / input_size)) + " rate of false positive")

    size_sum = 0
    filled_bit_count = 0
    max_count = 0
    for i in range(0, counting_bloom_filter.size):
        if counting_bloom_filter.check_bit(i):
            size_sum += counting_bloom_filter.get_bit_value(i)
            filled_bit_count += 1
            if max_count < counting_bloom_filter.get_bit_value(i):
                max_count = counting_bloom_filter.get_bit_value(i)

    avg_size = size_sum/filled_bit_count
    print("For counting filter -------- avg count:" + str(avg_size))
    print("For counting filter-------- max count:" + str(max_count))
    hasmap = {}

    print("aaa")
    for i in range(0,input_size):
        hasmap[str(i)]=i
    print("aaa")


if __name__ == "__main__":
    main()
