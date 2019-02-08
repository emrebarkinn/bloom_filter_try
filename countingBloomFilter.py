import math
import mmh3
import numpy as np
from bitarray import bitarray
from bitstring import BitArray


class CountingBloomFilter(object):

    def __init__(self, items_count, fp_prob, count_size=8):
        """
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        """
        self.count_size = count_size
        self.item_low_count = items_count
        # False posible probability in decimal
        self.fp_prob = fp_prob

        # Size of bit array to use
        self.size = self.get_size(items_count, fp_prob)

        # number of hash functions to use
        self.hash_count = self.get_hash_count(self.size, items_count)
        if self.hash_count == 0:
            self.hash_count = 1
        self.size += self.hash_count - (self.size % self.hash_count)

        # slice size
        self.slice_size = self.size // self.hash_count

        if self.count_size == 8:
            self.bit_array = bytearray(self.size)
        else:
            self.bit_array = bitarray(self.size*self.count_size)
            self.bit_array.setall(0)

        self.count = 0

    def set_value_bit(self, index, value):

        temp = bitarray(('{0:0' + str(self.count_size) + 'b}').format(value))
        if temp.length() == self.count_size:
            for i in range(self.count_size - 1, -1, -1):
                self.bit_array[index * self.count_size + i] = temp[i]

            # overflow on bit value

    def get_bit_value(self, index):

        if self.count_size == 8:
            return self.bit_array[index]

        value = 0
        for i in range(self.count_size - 1, 0, -1):
            if self.bit_array[index*self.count_size + i]:
                value += 2 ** (self.count_size - 1 - i)

        return value

    def check_bit(self, index):

        return self.get_bit_value(index) > 0

    def half_adder(self, bit_a, bit_b):
        return (bit_a ^ bit_b), bit_a and bit_b

    def full_adder(self, bit_a, bit_b, carry=0):
        sum1, carry1 = self.half_adder(bit_a, bit_b)
        sum2, carry2 = self.half_adder(sum1, carry)
        return sum2, carry1 or carry2

    def binary_bitarray_adder(self, value, index):
        bits_b = bitarray(('{0:0' + str(self.count_size) + 'b}').format(value))
        carry = False
        for i in range(self.count_size - 1, -1, -1):
            summ, carry = self.full_adder(self.bit_array[index*self.count_size + i], bits_b[i], carry)
            self.bit_array[index * self.count_size + i] = summ

        if carry:
            print("Overflow")
            self.binary_bitarray_sub(value, index)

    def binary_bitarray_sub(self,  value, index):
        carry = 1
        bits_b = bitarray(('{0:0' + str(self.count_size) + 'b}').format(value))
        bits_b = ~ bits_b

        for i in range(self.count_size - 1, -1, -1):
            summ, carry = self.full_adder(self.bit_array[index * self.count_size + i], bits_b[i], carry)
            self.bit_array[index * self.count_size + i] = summ

    def add(self, item):
        '''
        Add an item in the filter
        '''
        """
        if item in self:
            return False
        """
        if self.count > self.item_low_count:
            print("BloomFilter reached it's limit")
            return False

        start_point = 0
        for i in range(self.hash_count):
            # create digest for given item.
            # i work as seed to mmh3.hash() function
            # With different seed, digest created is different
            digest = mmh3.hash(item, i) % self.slice_size


            # set the bit True in int_array
            if self.count_size == 8:
                self.bit_array[start_point + digest] += 1
            else:
                self.binary_bitarray_adder(1, start_point + digest)
            start_point += self.slice_size
        self.count += 1
        return True

    def delete(self, item):

        if item in self:

            start_point = 0
            for i in range(self.hash_count):
                digest = mmh3.hash(item, i) % self.slice_size

                if self.count_size == 8:
                    self.bit_array[start_point + digest] -= 1
                else:
                    self.binary_bitarray_sub(1,start_point + digest)

                start_point += self.slice_size
            self.count -= 1
            return True
        return False

    def __contains__(self, item):
        '''
        Check for existence of an item in filter
        '''
        start_point = 0
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.slice_size
            if self.count_size == 8:
                if not self.bit_array[start_point + digest] > 0:
                    # if
                    return False
            else:
                if not self.check_bit(start_point + digest):
                    # if
                    return False
            start_point += self.slice_size
        return True

    def __len__(self):

        return self.count

    # TODO consider union and intersection operations can be useful and work correctly
    #  for counting and scalable bloom filters

    def copy(self):

        new_filter = CountingBloomFilter(self.item_low_count, self.fp_prob)
        new_filter.bit_array = self.bit_array.copy()
        return new_filter

    def union(self, other):

        if self.size != other.size:
            # or self.fp_prob != other.fp.prob :
            raise ValueError("Filters must have same size for union")

        new_filter = self.copy()
        for i in range(0, new_filter.size):
            new_filter.bit_array[i] += other.bit_array[i]
        return new_filter

    def intersection(self, other):

        if self.size != other.size:
            # or self.fp_prob != other.fp.prob :
            raise ValueError("Filters must have same size for union")

        new_filter = self.copy()
        for i in range(0, new_filter.size):
            new_filter.bit_array[i] = min(new_filter.bit_array[i], other.bit_array[i])
        return new_filter

    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersection(other)

    """
    def calculate_hashes(self, item):
        hashes = []
        start_point = 0
        for i in range(0, self.hash_count):
            hashes.append(start_point + (mmh3.hash(item, i) % self.slice_size))
            start_point += self.slice_size
        return hashes
    """

    @classmethod
    def get_size(self, n, p):
        """
        Return the size of bit array(m) to used using
        following formula
        m = -(n * lg(p)) / (lg(2)^2)
        n : int
            number of items expected to be stored in filter
        p : float
            False Positive probability in decimal
        """
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        '''
        Return the hash function(k) to be used using
        following formula
        k = (m/n) * lg(2)
        m : int
            size of bit array
        n : int
            number of items expected to be stored in filter
        '''
        k = (m / n) * math.log(2)
        return int(k)