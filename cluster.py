#!/usr/bin/env python

#
# EAS cluster cost interpolator for energy model construction
# by @kdrag0n
#
# This program is licensed under the MIT License (MIT)
#
# Copyright (c) 2019 Danny "kdrag0n" Lin <danny@kdrag0n.dev>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import numpy as np
from scipy import interpolate

# Source data - cluster costs
# Format: "FREQ COST"
# The data below is from sdm632: https://source.codeaurora.org/quic/la/kernel/msm-4.9/tree/arch/arm64/boot/dts/qcom/sdm632-cpu.dtsi?h=LA.UM.7.8.r1-05600-SDM710.0#n272
src_cluster_costs0 = '''
614400	8
883200	14
1036800	18
1363200	28
1536000	35
1670400	43
1804800	54'''

src_cluster_costs1 = '''
633600	68
902400	103
1094400	132
1401600	193
1555200	233
1804800	292
1996000	374
2016000	377'''

# Target frequencies to interpolate the costs for
target_freqs0 = [633600, 902400, 1113600, 1401600, 1536000, 1612800]
target_freqs1 = [1113600, 1401600, 1747200, 1804800]

# Interpolate and show cluster costs for the given source and target datasets
def int_cluster(src_str, target_freqs):
    src_data = src_str.split()
    src_freqs = [] # x
    src_costs = [] # y

    # Populate source frequency (x) and cost (y) lists
    for freq, cost in zip(*[iter(src_data)]*2):
        src_freqs.append(freq)
        src_costs.append(cost)

    # Perform cubic-spline interpolation on the source and target datasets
    tck = interpolate.splrep(src_freqs, src_costs, s=0)
    xnew = target_freqs
    ynew = interpolate.splev(xnew, tck, der=0)
    new_costs = list(ynew)

    # Print the new interpolated costs
    for idx, cost in enumerate(new_costs):
        freq = target_freqs[idx]
        print('%7d %.0f' % (freq, cost))

def main():
    # Interpolate and show little cluster costs
    print('Little cluster')
    int_cluster(src_cluster_costs0, target_freqs0)

    # Interpolate and show big cluster costs
    print('\n\nBig cluster')
    int_cluster(src_cluster_costs1, target_freqs1)

if __name__ == '__main__':
    main()
