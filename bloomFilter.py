import math
import mmh3
from bitarray import bitarray


class BloomFilter(object):
    '''
    Class for Bloom filter, using murmur3 hash function 
    '''

    def __init__(self, items_count, fp_prob):
        ''' 
        items_count : int 
            Number of items expected to be stored in bloom filter 
        fp_prob : float 
            False Positive probability in decimal 
        '''

        # TODO slices calculations needed to be implemented,
        #  each hash function must work for different slice of bit array

        self.item_low_count = items_count
        # False posible probability in decimal 
        self.fp_prob = fp_prob

        # Size of bit array to use 
        self.size = self.get_size(items_count, fp_prob)

        # number of hash functions to use 
        self.hash_count = self.get_hash_count(self.size, items_count)

        # Bit array of given size 
        self.bit_array = bitarray(self.size)

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
        digests = []
        for i in range(self.hash_count):
            # create digest for given item.
            # i work as seed to mmh3.hash() function 
            # With different seed, digest created is different 
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)

            # set the bit True in bit_array
            self.bit_array[digest] = True
        self.count += 1
        return True

    def __contains__(self, item):
        ''' 
        Check for existence of an item in filter 
        '''
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if not self.bit_array[digest]:
                # if any of bit is False then,its not present
                # in filter 
                # else there is probability that it exist 
                return False
        return True

    def __len__(self):

        return self.count

    def copy(self):

        new_filter = BloomFilter(self.item_low_count, self.fp_prob)
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

    """

    def calculate_hashes(self, item):
        hashes = []
        for i in range(0, self.hash_count):
            hashes.append(mmh3.hash(item, i) % self.size)

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
