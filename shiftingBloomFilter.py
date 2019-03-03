import math
import mmh3
from bitarray import bitarray


class ShiftingBloomFilterM(object):
    """
    Shifting Bloom Filter for Membership Queries
    -It has same fp rate with Bloom Filter
    -It uses k/2 + 1 hash function so it 2 times faster than Bloom Filter
    and it reduces number of memory accesses by half
    -This is membership query version of shifting bloom filter
    -There are also association and multiply query versions
    """
    NUM_OF_BITS = 32
    # it will equal to 64 if computer is 64 bit
    # Number of bits in a machine word
    MAX_OFFSET = 25
    # it will equal to 57 if the computer is 64 bit

    def __init__(self, items_count, fp_prob, count_size = 0):
        """
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        """

        self.item_low_count = items_count
        # False posible probability in decimal
        self.fp_prob = fp_prob

        # Size of bit array to use
        self.size = self.get_size(items_count, fp_prob)

        # number of hash functions to use
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.hash_count //= 2
        if self.hash_count == 0:
            self.hash_count = 1

        # Bit array of given size
        self.bit_array = bitarray(self.size + self.MAX_OFFSET)

        # initialize all bits as 0
        self.bit_array.setall(0)

        self.count = 0

    def add(self, item):
        '''
        Add an item in the filter
        '''
        if item in self:
            return False
        if self.count > self.item_low_count:
            print("BloomFilter reached it's limit")
            return False
        o = self.o_function(item)
        for i in range(self.hash_count):
            # create digest for given item.
            # i work as seed to mmh3.hash() function
            # With different seed, digest created is different
            digest = mmh3.hash(item, i) % self.size

            # set the bit True in bit_array
            self.bit_array[digest], self.bit_array[digest + 0] = True, True
        self.count += 1
        return True

    def __contains__(self, item):
        '''
        Check for existence of an item in filter
        '''
        o = self.o_function(item)
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if not self.bit_array[digest] | self.bit_array[digest + o] :
                # if any of bit is False then,its not present
                # in filter
                # else there is probability that it exist
                return False
        return True

    def __len__(self):

        return self.count

    def copy(self):

        new_filter = ShiftingBloomFilterM(self.item_low_count, self.fp_prob)
        new_filter.bit_array = self.bit_array.copy()
        return new_filter

    def union(self, other):

        if self.size != other.size:
            # or self.fp_prob != other.fp.prob :
            raise ValueError("Filters must have same size for union")

        new_filter = self.copy()
        new_filter.bit_array = new_filter.bit_array | other.bit_array
        return new_filter

    def intersection(self, other):

        if self.size != other.size:
            # or self.fp_prob != other.fp.prob :
            raise ValueError("Filters must have same size for union")

        new_filter = self.copy()
        new_filter.bit_array = new_filter.bit_array & other.bit_array
        return new_filter


    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersection(other)

    def get_bitarray_size(self):
        return self.bit_array.buffer_info()[4]

    def o_function(self, item):
        return mmh3.hash(item, self.hash_count) % (self.MAX_OFFSET + 1) - 1
        # formula = h-k/2+1(e) % (W -1) + 1
        # W is max offset value

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
