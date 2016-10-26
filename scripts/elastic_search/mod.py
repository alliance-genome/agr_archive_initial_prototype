from sgd import SGD
from zfin import ZFin
from worm import Worm
from fly import Fly
from mouse import Mouse


class MOD():
    @staticmethod
    def factory(organism):
        if organism in ("Saccharomyces cerevisiae", "S. cerevisiae"):
            return SGD()
        elif organism in ("Danio renio", "D. renio"):
            return ZFin()
        elif organism in ("Caenorhabditis elegans", "C. elegans"):
            return Worm()
        elif organism in ("Drosophila melanogaster", "D. melanogaster"):
            return Fly()
        elif organism in ("Mus musculus", "M. musculus"):
            return Mouse()
        else:
            return None
