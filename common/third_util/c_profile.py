import cProfile
import pstats
from common.util.export import File


class CProfileUtil:
    def run(self, f):
        p = cProfile.Profile()
        p.enable()
        f()
        p.disable()
        f = File("data/cprofile.txt")
        pstats.Stats(p, stream=f.get_writer()).sort_stats(-1).print_stats()
