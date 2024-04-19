#!/usr/bin/env python

import clawpack.clawutil.data

class BCTestData(clawpack.clawutil.data.ClawData):

    def __init__(self):
        super(BCTestData, self).__init__()

        # Incoming wave momentum flux modification
        # alpha \in [0, 1]
        #   alpha = 0:      Incoming momentum is zero
        #   0 < alpha < 1:  Incoming momentum is decayed from zero-order extrapolated value
        #   alpha = 1:      Incoming momentum is zero-order extrapolated
        self.add_attribute('alpha_bc', 1.0)


    def write(self, data_source='setrun.py', out_file='geoclaw.data'):

        self.open_data_file(out_file, data_source)
        self.data_write('alpha_bc',
                        description="(Incoming momentum flux modification)")

        self.close_data_file()