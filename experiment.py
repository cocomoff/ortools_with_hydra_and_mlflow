import os
import logging
import hydra
from solver import main
from omegaconf import OmegaConf

log = logging.getLogger(__name__)

@hydra.main(config_name="conf/default.yaml")
def run_experiment(cfg):
    res, ds, td, tl = main(cfg.solver.penalty, cfg.solver.num_vehicle)
    log.info("Dropped nodes :{}".format(",".join(map(str, ds))))
    log.info("Total distance:{}".format(td))
    log.info("Total load    :{}".format(tl))
    for uid in res:
        route, load = res[uid]
        route_str = "->".join(map(str, route))
        load_str = "->".join(map(str, load))
        log.info("user id:{}".format(uid))
        log.info("  route:{}".format(route_str))
        log.info("   load:{}".format(load_str))

if __name__ == '__main__':
    run_experiment()