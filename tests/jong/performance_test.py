
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))  # NOQA: E402

from matchbox.games.jong.judge.util import *
from matchbox.games.jong.judge.shanten import *

import cProfile
from timeit import timeit
#cProfile.run('[ shanten(randomhand()) for i in range(1000) ]')


%timeit


def fn():
    [shanten(randomhand()) for i in range(1000)]
