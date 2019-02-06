import math

from bloomFilter import BloomFilter
from countingBloomFilter import CountingBloomFilter


class ScalableBloomFilter(object):
    SMALL_GROWTH = 2
    LARGE_GROWTH = 4

    def __init__(self, initial_items_count=100, fp_prob=0.001, growth=SMALL_GROWTH, countable=False):

        # TODO ratio calculations needed. New bloom filters fp probability must equal to
        #  ratio * previous filter's fp_prob
        #  (for initial filter prob = fp_prob, for second prob = r * fp_prob, for third  r^2 * fp_prob)
        self.countable = countable
        self.initial_items_count = initial_items_count
        self.fp_prob = fp_prob
        self.growth = growth

        if countable:
            self.create_filter = CountingBloomFilter
        else:
            self.create_filter = BloomFilter

        self.bloom_filters = []

    def add(self, item):

        if item in self:
            return True
        if not self.bloom_filters:
            temp_filter = self.create_filter(self.initial_items_count, self.fp_prob)
            self.bloom_filters.append(temp_filter)
        else:
            temp_filter = self.bloom_filters[-1]
            if temp_filter.count >= temp_filter.item_low_count:
                temp_filter = self.create_filter(temp_filter.size * self.growth, temp_filter.fp_prob * 0.1)  # 0.1 is the ratio for creating next filter
                # TODO check fp prob
                self.bloom_filters.append(temp_filter)

        temp_filter.add(item)

        return False

    # TODO fp_prob calculation (which calculates fp prob instantly) operation will added
    def delete(self, item):
        if not self.countable:
            print("Delete operation only available for counting scalable bloom filters")
            return False
        for temp in reversed(self.bloom_filters):
            if temp.delete(item):
                return True
        return False

    def get_total_size(self):

        return sum([temp.size for temp in self.bloom_filters])

    def __contains__(self, item):

        for temp in reversed(self.bloom_filters):
            if item in temp:
                return True
        return False

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
