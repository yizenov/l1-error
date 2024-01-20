import os
import csv
import sys

import enumerators

# This script is to prepare greedy plans on a given workload
# Terminologies: optimal (opt), PostgreSQL (psql), COMPASS (compass)

# screen -S l1_gre -dm -L -Logfile scr_l1_gre.0 sh -c 'time /usr/bin/python3 scripts_prepare/collect_greedy_plans.py 0 0'

print(
"\n \
1. Enter: ~/L1_error_indicator\n \
2. Run the following command: /usr/bin/python3 scripts_prepare/collect_greedy_plans.py arg1 arg2\n \
\t Script requires 2 argument\n \
\t Workload: (0 = JOB, 1 = JOB-light, 2 = JCCH, 3 = DSB)\n \
\t Cardinality: (0 = True, 1 = PostgreSQL, 2 = COMPASS)\n \
")

print('Number of arguments:', len(sys.argv) - 1, 'arguments.')
print('Argument List:', str(sys.argv[1:]), '\n')

if len(sys.argv) != 3:
    print("Wrong number of arguments.\n")
else:
    try:
        benchmark_type = int(sys.argv[1])
        engine_idx = int(sys.argv[2])

        if benchmark_type == 0: 
            parent_folder = "input_data/job/"
            base_tables_file = parent_folder + "imdb_table_sizes.csv"
            workload_folder = parent_folder + "JOB_QUERIES_COMPASS_PostgreSQL"
            cardinality_file = parent_folder + "results_estimates-JOB.csv"
        elif benchmark_type == 1:
            parent_folder = "input_data/job_light/"
            base_tables_file = parent_folder + "imdb_table_sizes.csv"
            workload_folder = parent_folder + "JOB_light_QUERIES"
            cardinality_file = parent_folder + "results_estimates-JOB-light.csv"
        elif benchmark_type == 2:
            parent_folder = "input_data/jcch/"
            base_tables_file = parent_folder + "jcch_table_sizes.csv"
            workload_folder = parent_folder + "workload_jcch_queries"
            cardinality_file = parent_folder + "results_estimates-JCCH.csv"
        elif benchmark_type == 3:
            parent_folder = "input_data/dsb/"
            base_tables_file = parent_folder + "dsb_table_sizes.csv"
            workload_folder = parent_folder + "workload_dsb_queries"
            cardinality_file = parent_folder + "results_estimates-DSB.csv"

        if engine_idx == 0: output_f_file_opt = parent_folder + "greedy_traversals-opt-cost.csv"
        elif engine_idx == 1: output_f_file_opt = parent_folder + "greedy_traversals-opt-cost-psql.csv"
        elif engine_idx == 2: output_f_file_opt = parent_folder + "greedy_traversals-opt-cost-compass.csv"

        output_f_opt = open(output_f_file_opt, "w")
        output_f_writer_opt = csv.writer(output_f_opt, delimiter=',')
        output_f_writer_opt.writerow(["query_name", "plan_size", "true_cost", "compass_est", "psql_est", "plan"])
        output_f_opt.close()

        ######################################################################################

        for f_idx, file_name in enumerate(sorted(os.listdir(workload_folder))):
            input_query = workload_folder + "/" + file_name

            if benchmark_type == 0: query = file_name.split(".")[0].split("_")[1]
            elif benchmark_type == 1: query = file_name.split(".")[0]
            elif benchmark_type == 2: query = file_name.split(".")[0]
            elif benchmark_type == 3: query = file_name.split(".")[0]
        
            with open(input_query, "r") as query_input_f:
                original_query = [query_line for query_line in query_input_f]
                original_query = "".join(original_query).strip()

                from_and_where = original_query.split('FROM')[1].split('WHERE')
                table_list = from_and_where[0].split(',')
                table_list = [table.strip() for table in table_list]
                table_nicks = {info[1]: info[0] for info in [table.split(" AS ") for table in table_list]}

                where_clause = from_and_where[1].split('\n\n')
                where_clause = [clause_set for clause_set in where_clause if clause_set]

                join_predicates = where_clause[1].split('AND')
                join_predicates = [join.strip() for join in join_predicates if join.strip()]
                join_predicates[-1] = join_predicates[-1][:-1]

                edge_graph = enumerators.Undirected_Weighted_Graph_Greedy(query, table_nicks, engine_idx, 
                                                        base_tables_file, cardinality_file)
                for join in join_predicates:
                    left, right = join.split(" = ")
                    left, right = left.split(".")[0], right.split(".")[0]

                    edge_weight = edge_graph.cost_functions.compute_c_mm_cost([left], [right])

                    # tables may connect on different join attributes
                    edge_graph.addEdge(left, right, edge_weight[2][engine_idx], 
                                       edge_weight[2], edge_weight[3][engine_idx])
                
                ge_est_costs, ge_true_costs, ge_psql_costs, ge_compass_costs, ge_plan, ge_physical_plan = edge_graph.greedy_enumerate()

                plan_final = ""
                for edge in ge_plan:
                    plan_final += edge[0] + "-" + edge[1] + " "
                info_print = [query, len(table_nicks), ge_true_costs, ge_compass_costs, ge_psql_costs, plan_final[:-1]]

                output_f_opt = open(output_f_file_opt, "a")
                output_f_writer_opt = csv.writer(output_f_opt, delimiter=',')
                output_f_writer_opt.writerow(info_print)
                output_f_opt.close()

        print("Success.\n")
    except:
        print("Wrong parameter type or code error.\n")
