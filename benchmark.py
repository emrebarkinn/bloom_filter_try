from memory_usage import memory_usage
from bloomFilter import BloomFilter
from countingBloomFilter import CountingBloomFilter
from scalableBloomFilter import ScalableBloomFilter
import time


def main():
    input_size = 10000
    fp_rate = 0.1

    count_size = 4

    bloom_filter = BloomFilter(input_size, fp_rate)
    start_time = time.time()
    for i in range(0, input_size):
        bloom_filter.add(str(i))
    end_time = time.time()
    avg_add_time = (end_time - start_time) / input_size

    start_time = time.time()
    fp_count = 0
    for i in range(input_size, input_size * 2):
        if str(i) in bloom_filter:
            fp_count += 1
    end_time = time.time()
    avg_lookup_time = (end_time - start_time) / input_size

    print("Expected false positive rate for all calculations is :" + str(fp_rate))
    print()
    print("For Standard Bloom Filter : \nFalse positive count:" + str(fp_count) + "  in " + str(
        input_size) + " try. " + str(
        (fp_count / input_size)) + " rate of false positive")
    print("Avg lookup time :" + str('{:.20f}'.format(avg_lookup_time)) + "  Avg add time:" + str(
        '{:.20f}'.format(avg_add_time)))
    print("Memory usage in bytes :" + str(
        memory_usage.get_obj_size(bloom_filter) + bloom_filter.bit_array.buffer_info()[4]))

    counting_bloom_filter = CountingBloomFilter(input_size, fp_rate, count_size=count_size)

    start_time = time.time()
    for i in range(0, input_size):
        counting_bloom_filter.add(str(i))
    end_time = time.time()
    avg_add_time = (end_time - start_time) / input_size

    start_time = time.time()
    fp_count = 0
    for i in range(input_size, input_size * 2):
        if str(i) in counting_bloom_filter:
            fp_count += 1

    end_time = time.time()
    avg_lookup_time = (end_time - start_time) / input_size
    for i in range(0, input_size):
        if not str(i) in counting_bloom_filter:
            print(str(i))
    print()
    print("For counting filter :\nFalse positive count:" + str(fp_count) + "  in " + str(input_size) + " try. " + str(
        (fp_count / input_size)) + " rate of false positive")
    print("Avg lookup time :" + str('{:.20f}'.format(avg_lookup_time)) + "  Avg add time:" + str(
        '{:.20f}'.format(avg_add_time)))
    print("Memory usage in bytes :" + str(
        memory_usage.get_obj_size(counting_bloom_filter) ))

    scalable_bloom_filter = ScalableBloomFilter(fp_prob=fp_rate, growth=ScalableBloomFilter.SMALL_GROWTH)

    start_time = time.time()
    for i in range(0, input_size):
        scalable_bloom_filter.add(str(i))

    end_time = time.time()
    avg_add_time = (end_time - start_time) / input_size

    start_time = time.time()
    fp_count = 0
    for i in range(input_size, input_size * 2):
        if str(i) in scalable_bloom_filter:
            fp_count += 1

    end_time = time.time()
    avg_lookup_time = (end_time - start_time) / input_size
    print()
    print("For scalable filter :\nFalse positive count:" + str(fp_count) + "  in " + str(input_size) + " try. " + str(
        (fp_count / input_size)) + " rate of false positive")
    print("Avg lookup time :" + str('{:.20f}'.format(avg_lookup_time)) + "  Avg add time:" + str(
        '{:.20f}'.format(avg_add_time)))
    temp = 0
    for i in scalable_bloom_filter.bloom_filters:
        temp += i.bit_array.buffer_info()[4]
    print("Memory usage in bytes :" + str(memory_usage.get_obj_size(scalable_bloom_filter) + temp))

    c_scalable_bloom_filter = ScalableBloomFilter(fp_prob=fp_rate, growth=ScalableBloomFilter.SMALL_GROWTH,
                                                  countable=True, count_size=count_size)

    start_time = time.time()
    for i in range(0, input_size):
        c_scalable_bloom_filter.add(str(i))
    end_time = time.time()
    avg_add_time = (end_time - start_time) / input_size

    start_time = time.time()
    fp_count = 0
    for i in range(input_size, input_size * 2):
        if str(i) in c_scalable_bloom_filter:
            fp_count += 1

    end_time = time.time()
    avg_lookup_time = (end_time - start_time) / input_size
    print()
    print("For counting scalable filter :\nFalse positive count:" + str(fp_count) + "  in " + str(
        input_size) + " try. " + str(
        (fp_count / input_size)) + " rate of false positive")
    print("Avg lookup time :" + str('{:.20f}'.format(avg_lookup_time)) + "  Avg add time:" + str(
        '{:.20f}'.format(avg_add_time)))
    temp = 0

    print("Memory usage in bytes :" + str(memory_usage.get_obj_size(c_scalable_bloom_filter) + temp))

    size_sum = 0
    filled_bit_count = 0
    max_count = 0
    for a in c_scalable_bloom_filter.bloom_filters:
        for i in range(0, len(a)):
            if counting_bloom_filter.get_bit_value(i) > 0:
                size_sum += counting_bloom_filter.get_bit_value(i)
                filled_bit_count += 1
                if max_count < counting_bloom_filter.get_bit_value(i):
                    max_count = counting_bloom_filter.get_bit_value(i)

    avg_size = size_sum / filled_bit_count
    print("For counting filter -------- avg count:" + str(avg_size))
    print("For counting filter-------- max count:" + str(max_count))

    hasmap = {}
    start_time = time.time()
    for i in range(0, input_size):
        hasmap[str(i)] = i
    end_time = time.time()
    avg_add_time = (end_time - start_time) / input_size

    start_time = time.time()
    for i in range(input_size, input_size * 2):
        if str(i) in hasmap:
            pass
    end_time = time.time()
    avg_lookup_time = (end_time - start_time) / input_size
    print()
    print("For Hashmap ")
    print("Avg lookup time :" + str('{:.20f}'.format(avg_lookup_time)) + "  Avg add time:" + str(
        '{:.20f}'.format(avg_add_time)))
    print("Memory usage in bytes :" + str(memory_usage.get_obj_size(hasmap)))

    py_list = []
    start_time = time.time()
    for i in range(0, input_size):
        py_list.append(str(i))
    end_time = time.time()
    avg_add_time = (end_time - start_time) / input_size

    start_time = time.time()
    for i in range(input_size, input_size * 2):
        if str(i) in py_list:
            pass
    end_time = time.time()
    avg_lookup_time = (end_time - start_time) / input_size
    print()
    print("For List ")
    print("Avg lookup time :" + str('{:.20f}'.format(avg_lookup_time)) + "  Avg add time:" + str(
        '{:.20f}'.format(avg_add_time)))
    print("Memory usage in bytes :" + str(memory_usage.get_obj_size(py_list)))

    temp = 0
    for i in c_scalable_bloom_filter.bloom_filters:
        temp += memory_usage.get_obj_size(i)
    print("aaa" + str(memory_usage.get_obj_size(c_scalable_bloom_filter.bloom_filters)))
    print("xxx" + str(temp))


if __name__ == "__main__":
    main()
