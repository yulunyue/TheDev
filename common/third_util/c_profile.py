import cProfile
import pstats
from common.util.export import File, logger


class CProfileUtil:
    def run(self, f):
        p = cProfile.Profile()
        p.enable()
        f()
        p.disable()
        f = File("data/cprofile.txt")
        logger.info(f.path)
        pstats.Stats(p, stream=f.get_writer()).sort_stats(-1).print_stats()
