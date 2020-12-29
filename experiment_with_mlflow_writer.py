import os
import os.path
import logging
import hydra
import mlflow
from solver import main
from omegaconf import OmegaConf
from mlflow import log_metric, log_param, log_artifacts

from util import MlflowWriter
EXP_NAME = "ORtools-with-hydra-and-mlflow"

log = logging.getLogger(__name__)

@hydra.main(config_name="conf/default.yaml")
def run_experiment(cfg):
    writer = MlflowWriter(EXP_NAME)

    # パラメータの保存
    writer.log_param("penalty", cfg.solver.penalty)
    writer.log_param("num_vehicle", cfg.solver.num_vehicle)

    # ソルバで解を求める
    res, ds, td, tl = main(cfg.solver.penalty, cfg.solver.num_vehicle)

    # metricの保存
    writer.log_metric("total distance", td)
    writer.log_metric("total load", tl)
    writer.log_metric("number of dropped nodes", len(ds))

    # Hydraのlogging
    log.info("Dropped nodes :{}".format(",".join(map(str, ds))))
    log.info("Total distance:{}".format(td))
    log.info("Total load    :{}".format(tl))
    lines = []
    for uid in res:
        route, load = res[uid]
        route_str = "->".join(map(str, route))
        load_str = "->".join(map(str, load))
        lines.append("{}\t{}".format(route_str, load_str))
        log.info("user id:{}".format(uid))
        log.info("  route:{}".format(route_str))
        log.info("   load:{}".format(load_str))

    # 各ユーザの経路と積込(?)量をファイルとartifactsに出力
    raw_path = os.path.join(os.getcwd(), "rawlog.txt")
    with open(raw_path, "w") as f:
        for line in lines:
            f.write("{}\n".format(line))
    # writer.log_artifacts(raw_path)
    writer.set_terminated()

if __name__ == '__main__':
    run_experiment()