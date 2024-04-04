#!/usr/bin/env python

import os
import numpy
import datetime

import batch.batch

days2seconds = lambda days: days * 60.0**2 * 24.0

class BoundaryJob(batch.batch.Job):
    r""""""

    def __init__(self, name, alpha, boundaries, base_path='./'):

        super(BoundaryJob, self).__init__()

        self.type = "boundary_tests"
        self.name = ""
        self.prefix = "%s_%s" % (name, str(int(alpha * 10)).zfill(2))
        self.executable = "xgeoclaw"

        # Create base data object
        import setrun
        self.rundata = setrun.setrun()

        for n in range(2):
            self.rundata.clawdata.bc_lower[n] = config[n][0]
            self.rundata.clawdata.bc_upper[n] = config[n][1]

        self.rundata.geo_data.alpha_bc = alpha

    def __str__(self):
        output = super(BoundaryJob, self).__str__()
        output += "\n  Name: %s" % self.name
        output += "\n  config: x_bcs = (%s, %s)" % (self.rundata.clawdata.bc_lower[0],
                                                    self.rundata.clawdata.bc_upper[0])
        output += "\n          y_bcs = (%s, %s)" % (self.rundata.clawdata.bc_lower[1],
                                                    self.rundata.clawdata.bc_upper[1])
        output += "\n  alpha_bc = %s" % self.rundata.geo_data.alpha_bc
        return output


    def write_data_objects(self):
        r""""""

        # Write out all data files
        super(BoundaryJob, self).write_data_objects()

        # If any additional information per storm is needed do it here
        # ...


if __name__ == '__main__':

    jobs = []
    boundary_configs = {'all_extrap': [['extrap', 'extrap'], 
                                       ['extrap', 'extrap']],
                        'all_wall':   [['wall', 'wall'], 
                                       ['wall', 'wall']],
                        'lo_wall':    [['wall', 'extrap'], 
                                       ['wall', 'wall']],
                        'hi_wall':    [['extrap', 'wall'], 
                                       ['wall', 'wall']],
                        'channel':    [['extrap', 'extrap'], 
                                       ['wall', 'wall']],
                       }
    for [name, config] in boundary_configs.items():
        for alpha in range(11):
            jobs.append(BoundaryJob(name, alpha * 0.1, config))

    controller = batch.batch.BatchController(jobs)
    print(controller)
    controller.run()
