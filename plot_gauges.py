#!/usr/bin/env python

import os

import numpy
import matplotlib.pyplot as plt

import clawpack.pyclaw.gauges
import clawpack.geoclaw.surge.plot as surgeplot


def plot_gauge_alpha(gauge_nums, base_path):
    
    alphas = range(11)

    fig = plt.figure()
    axes = fig.add_subplot(1, 1, 1)

    for n in gauge_nums:
        path = os.path.join(base_path, "all_wall_10_output")
        wall_gauge = clawpack.pyclaw.gauges.GaugeSolution(gauge_id=n, path=path)
        t = surgeplot.sec2days(wall_gauge.t)
        axes.plot(t, wall_gauge.q[3, :], color="black")

        path = os.path.join(base_path, "channel_%s_output" % str(0).zfill(2))
        channel_gauge = clawpack.pyclaw.gauges.GaugeSolution(gauge_id=n, path=path)
        t = surgeplot.sec2days(channel_gauge.t)
        axes.plot(t, channel_gauge.q[3, :], color="blue")
        for alpha in alphas[1:-1]:
            path = os.path.join(base_path, "channel_%s_output" % str(alpha).zfill(2))
            channel_gauge = clawpack.pyclaw.gauges.GaugeSolution(gauge_id=n, path=path)
            t = surgeplot.sec2days(channel_gauge.t)
            axes.plot(t, channel_gauge.q[3, :], color="lightgray")
        path = os.path.join(base_path, "channel_%s_output" % str(10).zfill(2))
        channel_gauge = clawpack.pyclaw.gauges.GaugeSolution(gauge_id=n, path=path)
        t = surgeplot.sec2days(channel_gauge.t)
        axes.plot(t, channel_gauge.q[3, :], color="red")

    axes.set_title('Station %s' % gauge_nums)
    axes.set_xlim([-1, 5])
    axes.set_xlabel('Days relative to landfall')
    axes.set_xticks([-1, 0, 1, 2, 3, 4, 5])
    axes.set_xticklabels([r"$-1$", r"$0$", r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"])
    axes.set_ylim([-0.25, 2.25])

    return fig


if __name__ == '__main__':
    base_path = os.path.join(os.environ.get("DATA_PATH", os.getcwd()), 
                             "boundary_tests")
    
    figs = []
    gauge_pairs = [[0, 6], [1, 3], [2, 4, 5]]
    for pair in gauge_pairs:
        file_name = "gauge_comparison_"
        for n in pair:
            file_name += str(n)
        file_name += ".png"
        figs.append(plot_gauge_alpha(pair, base_path))
        figs[-1].savefig(os.path.join(os.getcwd(), file_name))

    plt.show()