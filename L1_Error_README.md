<meta name="robots" content="noindex,nofollow">

# L1-Error Evaluation
We provide instructions to reproduce figures and tables in the paper.

## Table of Contents
1. [Figure 1](#figure1). Correlation of Q-error and P-error.
2. [Figure 2](#figure2). Example query 2c from JOB.
3. [Figure 3](#figure3). Query 2c cardinalities.
4. [Figure 6](#figure6). Query 2c cardinality weights.
5. [Tables 1 and 2](#tables12). L1-error classifier results.

Each figure instruction specifies its figure file, Python script, input and output files. Each Python script includes the instruction on how to run along with its arguments. All scripts are run from `~/L1_error_indicator` folder.

#
#

## Figure 1. Correlation of Q-error and P-error <a name="figure1"></a>
Figure file: `figures/figure_max_qerror_perror.ods`</br>
Script file: `scripts/run_max_qerror_perror.py`</br>
Output files: `output_data/res_max_qerror_perror.csv`</br>
Input files:
- `input_data/job/JOB_QUERIES_COMPASS_PostgreSQL`
- `input_data/job/exhaustive_traversals-opt-cost-psql.csv`
- `input_data/job/exhaustive_traversals-opt-cost.csv`
- `input_data/job/results_estimates-JOB.csv`

Environment description: PostgreSQL, Exhaustive Search, JOB workload.

## Figure 2. Example query 2c from JOB <a name="figure2"></a>
The figure is built based on `input_data/job/results_estimates-JOB.csv`.

## Figure 3 (a,b). Query 2c cardinalities <a name="figure3"></a>
The figure is built based on `input_data/job/results_estimates-JOB.csv`.

## Figure 6. Query 2c cardinality weights <a name="figure6"></a>
The figure is built based on `input_data/job/results_estimates-JOB.csv`

## Table 1 and 2. L1-error classifier results <a name="tables12"></a>
Figure file: N/A</br>
Script file: `scripts/run_L1_classifier.py`</br>
Output files: results are printed in the terminal</br>
Input files JOB:
- `input_data/job/JOB_QUERIES_COMPASS_PostgreSQL`
- `input_data/job/L1-errors-agg-exhaustive-psql.csv`
- `input_data/job/L1-errors-agg-exhaustive-compass.csv`
- `input_data/job/L1-errors-agg-greedy-psql.csv`
- `input_data/job/L1-errors-agg-greedy-compass.csv`

Input files JOB-light:
- `input_data/job_light/JOB_light_QUERIES`
- `input_data/job_light/L1-light-errors-agg-exhaustive-psql.csv`
- `input_data/job_light/L1-light-errors-agg-exhaustive-compass.csv`
- `input_data/job_light/L1-light-errors-agg-greedy-psql.csv`
- `input_data/job_light/L1-light-errors-agg-greedy-compass.csv`

Input files JCC-H:
- `input_data/jcch/workload_jcch_queries`
- `input_data/jcch/L1-jcch-errors-agg-exhaustive-psql.csv`
- `input_data/jcch/L1-jcch-errors-agg-greedy-psql.csv`

Input files DSB:
- `input_data/dsb/workload_dsb_queries`
- `input_data/dsb/L1-dsb-errors-agg-exhaustive-psql.csv`
- `input_data/dsb/L1-dsb-errors-agg-greedy-psql.csv`

# 
#

Environment description:
- PostgreSQL and COMPASS
- Greedy and Exhaustive Search
- JOB, JOB-light, JCC-H, and DSB workloads
