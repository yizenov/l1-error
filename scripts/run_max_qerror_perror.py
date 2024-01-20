import csv
import sys
import os

# This script is to build Figure-1 based on PostgreSQL, Exhaustive Search, JOB workload
# Terminologies: optimal (opt), PostgreSQL (psql)

print(
"\n \
1. Enter: ~/L1_error_indicator\n \
2. Run the following command: /usr/bin/python3 scripts/run_max_qerror_perror.py\n \
\t Script requires 0 argument\n \
")

print('Number of arguments:', len(sys.argv) - 1, 'arguments.')
print('Argument List:', str(sys.argv[1:]), '\n')

if len(sys.argv) != 1:
    print("Wrong number of arguments.\n")
else:
    try:
        input_queries = "input_data/job/JOB_QUERIES_COMPASS_PostgreSQL/"
        cardinality_job_file = "input_data/job/results_estimates-JOB.csv"

        opt_plan_cost_file = "input_data/job/exhaustive_traversals-opt-cost.csv"
        psql_plan_cost_file = "input_data/job/exhaustive_traversals-opt-cost-psql.csv"
        output_f_file = "output_data/res_max_qerror_perror.csv"

        ############ Original Queries ###################

        query_complexities = {}
        for file_name in sorted(os.listdir(input_queries)):
            input_query = input_queries + file_name
            with open(input_query, "r") as query_input_f:
                original_query = [query_line for query_line in query_input_f]
                original_query = "".join(original_query)

                # extracting tables and join predicates
                from_and_where = original_query.split('FROM')[1].split('WHERE')
                where_clause = from_and_where[1].split('\n\n')
                where_clause = [clause_set for clause_set in where_clause if clause_set]

                join_predicates = where_clause[1].split('AND')
                join_predicates = [join.strip() for join in join_predicates if join.strip()]
                join_predicates[-1] = join_predicates[-1][:-1]

                query_family = file_name[2:].split(".")[0][:-1]
                query_complexities[query_family] = len(join_predicates)

        ############ Parsing Cardinalities ##################

        all_info = {}
        with open(cardinality_job_file, "r") as input_f:
            for idx, line in enumerate(input_f):
                if idx == 0: continue

                query = line.strip().split(",")[0].split("_")[0]
                query_family = query[:-1]
                subquery = line.strip().split(",")[0].split("_")[1]
                if query_family not in all_info: all_info[query_family] = {}
                if query not in all_info[query_family]: all_info[query_family][query] = {}

                join_size = int(line.strip().split(",")[1])
                if join_size not in all_info[query_family][query]: 
                    all_info[query_family][query][join_size] = []

                true_cardinality = float(line.strip().split(",")[2])
                psql_estimate = round(float(line.strip().split(",")[3]))

                psql_qerror = max(max(psql_estimate, 1.0) / max(true_cardinality, 1.0), \
                    max(true_cardinality, 1.0) / max(psql_estimate, 1.0))

                all_info[query_family][query][join_size].append([subquery, true_cardinality,
                    psql_estimate, psql_qerror])

        ################# Optimal Plans #######################

        opt_plan_costs = {}
        with open(opt_plan_cost_file, "r") as input_f:
            for idx, line in enumerate(input_f):
                if idx == 0: continue
                line = line.strip().split(',')
                query = line[0]

                cost = float(line[2])
                opt_plan_costs[query] = cost

        ########### PSQL Plans ###############################

        psql_plan_costs = {}
        with open(psql_plan_cost_file, "r") as input_f:
            for idx, line in enumerate(input_f):
                if idx == 0: continue
                line = line.strip().split(',')
                query = line[0]

                cost = float(line[2])
                psql_plan_costs[query] = cost

        #####################################################

        output_f = open(output_f_file, "w")
        output_f_writer = csv.writer(output_f, delimiter=',')

        output_f_writer.writerow(["query_name", "tables_nbr", "query_complexity", 
            "max_q_error_psql", "cost-DP_psql"])

        group1_queries, group2_queries, group3_queries = [], [], []
        for query_family in all_info:
            max_join = query_complexities[query_family]
            if max_join < 10: group1_queries.append(query_family)
            elif 9 < max_join < 20: group2_queries.append(query_family)
            else: group3_queries.append(query_family)

        for group_idx, group in enumerate([group1_queries, group2_queries, group3_queries]):
            for query_family in group:
                for query in all_info[query_family]:
                    if query not in opt_plan_costs or query not in psql_plan_costs:
                        output_f_writer.writerow([query, max_join, group_idx, max(all_psql_qerrors), -1])
                        print("missing plans: " + query)
                        continue

                    all_psql_qerrors = []
                    max_join = max(all_info[query_family][query])

                    for join_size in sorted(all_info[query_family][query]):
                        for subplan_info in all_info[query_family][query][join_size]:
                            all_psql_qerrors.append(subplan_info[3])

                    output_f_writer.writerow([query, max_join, group_idx, 
                        max(all_psql_qerrors), 
                        psql_plan_costs[query] / opt_plan_costs[query]])

        output_f.close()
        print("The results will be saved at: " + output_f_file)
        print("Success.\n")
    except:
        print("Wrong parameter type or code error.\n")
