import math
from bloomFilter import BloomFilter

class ScalableBloomFilter(object):
    SMALL_GROWTH = 2
    LARGE_GROWTH = 4


    def __init__(self, initial_items_count, fp_prob, growth=SMALL_GROWTH ,countable=False):

        self.initial_items_count = initial_items_count
        self.fp_prob = fp_prob
        self.growth = growth

        if countable:
            pass #TODO countable bloom filter constructor will added
        else:
            self.create_filter = lambda: BloomFilter(initial_items_count, fp_prob)












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

