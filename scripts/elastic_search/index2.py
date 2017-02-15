import time

from mods import *

mods = [MGI(), ZFIN(), SGD(), WormBase(), FlyBase(), RGD()]

start_time = time.time()

for m in mods:
	m.load_genes()
	m.load_homologs()
	m.load_go()
	m.load_diseases()

mod.save_into_file()

mod.delete_mapping()
mod.put_mapping()

mod.index_genes_into_es()
mod.index_go_into_es()
mod.index_diseases_into_es()
