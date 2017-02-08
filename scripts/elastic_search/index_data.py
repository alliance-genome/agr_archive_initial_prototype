import time

from sgd import SGD
from zfin import ZFIN
from worm import WormBase
from fly import FlyBase
from mouse import MGI
from rat import RGD

from mod import MOD

sgd = SGD()
zfin = ZFIN()
worm = WormBase()
fly = FlyBase()
mouse = MGI()
rat = RGD()

mod = MOD()

mods = [mouse, zfin, sgd, worm, fly, rat]

mod.load_data_from_file()

mod.delete_mapping()
mod.put_mapping()

mod.index_genes_into_es()
mod.index_go_into_es()
mod.index_diseases_into_es()
