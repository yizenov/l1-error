<meta name="robots" content="noindex,nofollow">

# Additional scripts to prepare all input files needed for L1-error results

- Benchmark queries are available at:
    * `input_data/job/JOB_QUERIES_COMPASS_PostgreSQL`
    * `input_data/job_light/JOB_light_QUERIES`
    * `input_data/jcch/workload_jcch_queries`
    * `input_data/dsb/workload_dsb_queries`
- Cardinality estimates are available at:
    * `input_data/job/results_estimates-JOB.csv`
    * `input_data/job_light/results_estimates-JOB-light.csv`
    * `input_data/jcch/results_estimates-JCCH.csv`
    * `input_data/dsb/results_estimates-DSB.csv`
- Base table sizes are available at:
    * `input_data/job/imdb_table_sizes.csv`
    * `input_data/job_light/imdb_table_sizes.csv`
    * `input_data/jcch/jcch_table_sizes.csv`
    * `input_data/dsb/dsb_table_sizes.csv`

#
#

- [Part 1](all_opt_exhaustive_plans). Generate all optimal plans via Exhaustive Search
    * `input_data/job/exhaustive_traversals-opt-cost.csv`
    * `input_data/job/exhaustive_traversals-opt-cost-psql.csv`
    * `input_data/job/exhaustive_traversals-opt-cost-compass.csv`
    * `input_data/job_light/exhaustive_traversals-opt-cost.csv`
    * `input_data/job_light/exhaustive_traversals-opt-cost-psql.csv`
    * `input_data/job_light/exhaustive_traversals-opt-cost-compass.csv`
    * `input_data/jcch/exhaustive_traversals-opt-cost.csv`
    * `input_data/jcch/exhaustive_traversals-opt-cost-psql.csv`
    * `input_data/dsb/exhaustive_traversals-opt-cost.csv`
    * `input_data/dsb/exhaustive_traversals-opt-cost-psql.csv`
- [Part 2](all_opt_greedy_plans). Generate all optimal plans via Greedy Search
    * `input_data/job/greedy_traversals-opt-cost.csv`
    * `input_data/job/greedy_traversals-opt-cost-psql.csv`
    * `input_data/job/greedy_traversals-opt-cost-compass.csv`
    * `input_data/job_light/greedy_traversals-opt-cost.csv`
    * `input_data/job_light/greedy_traversals-opt-cost-psql.csv`
    * `input_data/job_light/greedy_traversals-opt-cost-compass.csv`
    * `input_data/jcch/greedy_traversals-opt-cost.csv`
    * `input_data/jcch/greedy_traversals-opt-cost-psql.csv`
    * `input_data/dsb/greedy_traversals-opt-cost.csv`
    * `input_data/dsb/greedy_traversals-opt-cost-psql.csv`
- [Part 3](#l1_features). These input files are created by "L1-error features"
    * `input_data/job/L1-errors-agg-exhaustive-psql.csv`
    * `input_data/job/L1-errors-agg-exhaustive-compass.csv`
    * `input_data/job/L1-errors-agg-greedy-psql.csv`
    * `input_data/job/L1-errors-agg-greedy-compass.csv`
    * `input_data/job_light/L1-light-errors-agg-exhaustive-psql.csv`
    * `input_data/job_light/L1-light-errors-agg-exhaustive-compass.csv`
    * `input_data/job_light/L1-light-errors-agg-greedy-psql.csv`
    * `input_data/job_light/L1-light-errors-agg-greedy-compass.csv`
    * `input_data/jcch/L1-jcch-errors-agg-exhaustive-psql.csv`
    * `input_data/jcch/L1-jcch-errors-agg-greedy-psql.csv`
    * `input_data/dsb/L1-dsb-errors-agg-exhaustive-psql.csv`
    * `input_data/dsb/L1-dsb-errors-agg-greedy-psql.csv`

#
#

## 1. Generate all optimal plans via Exhaustive Search <a name="all_opt_exhaustive_plans"></a>
Figure file: N/A</br>
Script file: `scripts_prepare/collect_exhaustive_plans.py`

Output files:
- `input_data/job_light/exhaustive_traversals-opt-cost.csv`
- `input_data/job_light/exhaustive_traversals-opt-cost-psql.csv`
- `input_data/job_light/exhaustive_traversals-opt-cost-compass.csv`
- `input_data/job/exhaustive_traversals-opt-cost.csv`
- `input_data/job/exhaustive_traversals-opt-cost-psql.csv`
- `input_data/job/exhaustive_traversals-opt-cost-compass.csv`
- `input_data/jcch/exhaustive_traversals-opt-cost.csv`
- `input_data/jcch/exhaustive_traversals-opt-cost-psql.csv`
- `input_data/dsb/exhaustive_traversals-opt-cost.csv`
- `input_data/dsb/exhaustive_traversals-opt-cost-psql.csv`

Input files:
- `input_data/job/JOB_QUERIES_COMPASS_PostgreSQL`
- `input_data/job_light/JOB_light_QUERIES`
- `input_data/jcch/workload_jcch_queries`
- `input_data/dsb/workload_dsb_queries`
- `input_data/job/results_estimates-JOB.csv`
- `input_data/job_light/results_estimates-JOB-light.csv`
- `input_data/jcch/results_estimates-JCCH.csv`
- `input_data/dsb/results_estimates-DSB.csv`
- `input_data/job/imdb_table_sizes.csv`
- `input_data/job_light/imdb_table_sizes.csv`
- `input_data/jcch/jcch_table_sizes.csv`
- `input_data/dsb/dsb_table_sizes.csv`

## 2. Generate all optimal plans via Greedy Search <a name="all_opt_greedy_plans"></a>
Figure file: N/A</br>
Script file: `scripts_prepare/collect_greedy_plans.py`

Output files:
- `input_data/job/greedy_traversals-opt-cost.csv`
- `input_data/job/greedy_traversals-opt-cost-psql.csv`
- `input_data/job/greedy_traversals-opt-cost-compass.csv`
- `input_data/job_light/greedy_traversals-opt-cost.csv`
- `input_data/job_light/greedy_traversals-opt-cost-psql.csv`
- `input_data/job_light/greedy_traversals-opt-cost-compass.csv`
- `input_data/jcch/greedy_traversals-opt-cost.csv`
- `input_data/jcch/greedy_traversals-opt-cost-psql.csv`
- `input_data/dsb/greedy_traversals-opt-cost.csv`
- `input_data/dsb/greedy_traversals-opt-cost-psql.csv`

Input files:
- `input_data/job/JOB_QUERIES_COMPASS_PostgreSQL`
- `input_data/job_light/JOB_light_QUERIES`
- `input_data/jcch/workload_jcch_queries`
- `input_data/dsb/workload_dsb_queries`
- `input_data/job/results_estimates-JOB.csv`
- `input_data/job_light/results_estimates-JOB-light.csv`
- `input_data/jcch/results_estimates-JCCH.csv`
- `input_data/dsb/results_estimates-DSB.csv`
- `input_data/job/imdb_table_sizes.csv`
- `input_data/job_light/imdb_table_sizes.csv`
- `input_data/jcch/jcch_table_sizes.csv`
- `input_data/dsb/dsb_table_sizes.csv`

## 3. L1-error features <a name="l1_features"></a>
Figure file: N/A</br>
Script file:
- `scripts/L1_error.py`

Output files JOB:
- `input_data/job/L1-errors-agg-exhaustive-psql.csv`
- `input_data/job/L1-errors-agg-exhaustive-compass.csv`
- `input_data/job/L1-errors-agg-greedy-psql.csv`
- `input_data/job/L1-errors-agg-greedy-compass.csv`

Output files JOB-light:
- `input_data/job_light/L1-light-errors-agg-exhaustive-psql.csv`
- `input_data/job_light/L1-light-errors-agg-exhaustive-compass.csv`
- `input_data/job_light/L1-light-errors-agg-greedy-psql.csv`
- `input_data/job_light/L1-light-errors-agg-greedy-compass.csv`

Output files JCCH:
- `input_data/jcch/L1-jcch-errors-agg-exhaustive-psql.csv`
- `input_data/jcch/L1-jcch-errors-agg-greedy-psql.csv`

Output files DSB:
- `input_data/dsb/L1-dsb-errors-agg-exhaustive-psql.csv`
- `input_data/dsb/L1-dsb-errors-agg-greedy-psql.csv`

Input files JOB:
- `input_data/job/JOB_QUERIES_COMPASS_PostgreSQL`
- `input_data/job/results_estimates-JOB.csv`
- `input_data/job/imdb_table_sizes.csv`
- `input_data/job/exhaustive_traversals-opt-cost.csv`
- `input_data/job/exhaustive_traversals-opt-cost-psql.csv`
- `input_data/job/exhaustive_traversals-opt-cost-compass.csv`
- `input_data/job/greedy_traversals-opt-cost.csv`
- `input_data/job/greedy_traversals-opt-cost-psql.csv`
- `input_data/job/greedy_traversals-opt-cost-compass.csv`

Input files JOB-light:
- `input_data/job_light/JOB_light_QUERIES`
- `input_data/job_light/results_estimates-JOB-light.csv`
- `input_data/job_light/imdb_table_sizes.csv`
- `input_data/job_light/exhaustive_traversals-opt-cost.csv`
- `input_data/job_light/exhaustive_traversals-opt-cost-psql.csv`
- `input_data/job_light/exhaustive_traversals-opt-cost-compass.csv`
- `input_data/job_light/greedy_traversals-opt-cost.csv`
- `input_data/job_light/greedy_traversals-opt-cost-psql.csv`
- `input_data/job_light/greedy_traversals-opt-cost-compass.csv`

Input files JCCH:
- `input_data/jcch/workload_jcch_queries`
- `input_data/jcch/results_estimates-JCCH.csv`
- `input_data/jcch/jcch_table_sizes.csv`
- `input_data/jcch/exhaustive_traversals-opt-cost.csv`
- `input_data/jcch/exhaustive_traversals-opt-cost-psql.csv`
- `input_data/jcch/greedy_traversals-opt-cost.csv`
- `input_data/jcch/greedy_traversals-opt-cost-psql.csv`

Input files DSB:
- `input_data/dsb/workload_dsb_queries`
- `input_data/dsb/results_estimates-DSB.csv`
- `input_data/dsb/dsb_table_sizes.csv`
- `input_data/dsb/exhaustive_traversals-opt-cost.csv`
- `input_data/dsb/exhaustive_traversals-opt-cost-psql.csv`
- `input_data/dsb/greedy_traversals-opt-cost.csv`
- `input_data/dsb/greedy_traversals-opt-cost-psql.csv`

# 
#

Environment description:
- PostgreSQL and COMPASS
- Greedy and Exhaustive Search
- JOB, JOB-light, JCC-H, and DSB workloads
