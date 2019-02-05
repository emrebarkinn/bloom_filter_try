import math
import mmh3
import numpy as np
from bitarray import bitarray
from bitstring import BitArray


class CountingBloomFilter(object):

    def __init__(self, items_count, fp_prob, count_size=5):
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

        self.size -= self.size % self.hash_count

        # slice size
        self.slice_size = self.size // self.hash_count

        # self.int_array = bytearray(self.size)

        self.bit_array = BitArray(length=self.size*self.count_size)

        self.count = 0

    def add_value_bit(self, index, value):

        temp = self.bit_array[index: index + self.count_size].uint

        if format(temp + value, '#0'+str(self.count_size + 2)+'b').__len__() <= 2+self.count_size:
            self.bit_array.overwrite(format(temp + value, '#0'+str(self.count_size)+'b'), index)
        else:
            pass
            # overflow on bit value

    def set_value_bit(self, index, value):

        if format(value, '#0' + str(self.count_size + 2) + 'b').__len__() <= 2 + self.count_size:
            self.bit_array.overwrite(format(value, '#0' + str(self.count_size) + 'b'), index)
        else:
            pass
            # overflow on bit value

    def get_bit_value(self, index):

        return self.bit_array[index: index + self.count_size].uint

    def check_bit(self, index):

        return self.bit_array[index: index + self.count_size].uint > 0

    def add(self, item):
        '''
        Add an item in the filter
        '''
        if item in self:
            return False
        if self.count > self.item_low_count:
            print("BloomFilter reached it's limit")
            return False
        digests = []
        start_point = 0
        for i in range(self.hash_count):
            # create digest for given item.
            # i work as seed to mmh3.hash() function
            # With different seed, digest created is different
            digest = mmh3.hash(item, i) % self.slice_size
            digests.append(start_point + digest*self.count_size)

            # set the bit True in int_array
            self.add_value_bit(start_point + digest*self.count_size, 1)
            start_point += self.slice_size*self.count_size
        self.count += 1
        return True

    def delete(self, item):

        if item in self:
            digests = []
            start_point = 0
            for i in range(self.hash_count):
                digest = mmh3.hash(item, i) % self.slice_size
                digests.append(start_point + digest*self.count_size)
                self.add_value_bit(start_point + digest*self.count_size, -1)
                start_point += self.slice_size*self.count_size
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
            if not self.check_bit(start_point + digest*self.count_size):
                # if
                return False
            start_point += self.slice_size*self.count_size
        return True

    def __len__(self):

        return self.count

    # TODO consider union and intersection operations can be useful and work correctly
    #  for counting and scalable bloom filters

    def copy(self):

        new_filter = CountingBloomFilter(self.item_low_count, self.fp_prob)
        new_filter.int_array = self.bit_array.copy()
        return new_filter

    def union(self, other):

        if self.size != other.size:
            # or self.fp_prob != other.fp.prob :
            raise ValueError("Filters must have same size for union")

        new_filter = self.copy()
        for i in range(0, new_filter.size):
            new_filter.add_value_bit(i*self.count_size, other.get_bit_value(i))
        return new_filter

    def intersection(self, other):

        if self.size != other.size:
            # or self.fp_prob != other.fp.prob :
            raise ValueError("Filters must have same size for union")

        new_filter = self.copy()
        for i in range(0, new_filter.size):
            new_filter.set_value_bit(i*self.count_size, min(new_filter.get_bit_value(i),other.get_bit_value(i)))
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
