from sage.all import *
from gns import Digits, SemiRadixSystem


class SimultaneousDigitSet(Digits):
    def __init__(self, rs_array):
        super(Digits, self).__init__()
        self.rs_array = rs_array
        if len(self.rs_array) != 2:
            raise Exception('SimultaneousDigitSet can be used only for 2 input')

    def get_digit_set(self, rs):
        ret = []
        for d2 in self.rs_array[1].get_digits():
            for d1 in self.rs_array[0].get_digits():
                for x in [self.rs_array[0].get_base() * vector(d2) + vector(d1)]:
                    ret.append([x[0], x[1], x[0], x[1]])
        return ret



class SimultaneousSystem(SemiRadixSystem):
    def __init__(self, rs_array):
        combined_base = matrix(rs_array[0].get_dimension() + rs_array[1].get_dimension(),rs_array[0].get_dimension() + rs_array[1].get_dimension())
        combined_base.set_block(0,0,rs_array[0].get_base())
        combined_base.set_block(rs_array[0].get_dimension(),rs_array[0].get_dimension(),rs_array[1].get_base())
        #print(combined_base)
        super().__init__(combined_base,SimultaneousDigitSet(rs_array))
