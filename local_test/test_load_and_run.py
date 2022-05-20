import os
import sys

work_path = os.getcwd()
os.chdir("../runner_dir")
print(os.getcwd())
sys.path.insert(0, '.')

from db_bench_option import DEFAULT_DB_BENCH
from db_bench_option import load_config_file
from db_bench_option import set_parameters_to_env
from db_bench_runner import DB_launcher
from db_bench_runner import reset_CPUs
from parameter_generator import HardwareEnvironment
from parameter_generator import StorageMaterial

os.chdir(work_path)
if __name__ == '__main__':
    env = HardwareEnvironment()
    parameter_dict = load_config_file('config.json')
    set_parameters_to_env(parameter_dict, env)

    result_dir = "stand_alone_inlufence"


    keyrange_size = 10*1000*1000

    keyrange_setups = {
        "src":{
            "keyrange_start":0,
            "keyrange_num":5,
            "keyrange_size":keyrange_size
        },
        "dst":{
            "keyrange_start":8*keyrange_size,
            "keyrange_num":5,
            "keyrange_size":keyrange_size

        }
    }

    migrate_setups = {

    "migrate_from":6*keyrange_size,
    "migrate_range":keyrange_size,
    "migrate_keys":1*1000*1000
    }


    workload_list=["src_load","src_run","dst_load","dst_run"]

    for workload in workload_list:
         
        benchmark_opt =  {
                "load_num":10*1000*1000,
                "running_num":10*1000*1000,
                "report_interval_seconds": 1,
                "value_size":1000,
                "key_size":16,
                "subcompactions":20,
                "reads":10000,
                "benchmarks":workload+",stats",
                "report_bg_io_stats":"true",
                "histogram":True,
                "statistics":True
            }

        benchmark_opt.update(keyrange_setups[workload.split("_")[0]])
        benchmark_opt.update(migrate_setups)
        temp_result_dir = result_dir +"/"+workload
        runner = DB_launcher(
            env, temp_result_dir, db_bench=DEFAULT_DB_BENCH, extend_options=benchmark_opt)
        runner.run()
        reset_CPUs()
