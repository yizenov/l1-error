import os, sys, csv, math

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts_prepare.cost_module import CostFunctions

ZERO_REPLACE = 0.0001  # in case denominators are equal to zero

# screen -S l1_comp -dm -L -Logfile scr_l1_compute.0 sh -c 'time /usr/bin/python3 scripts/L1_error.py 0 0 0'

print(
"\n \
1. Enter: ~/L1_error_indicator\n \
2. Run the following command: /usr/bin/python3 scripts/L1_error.py arg1 arg2 arg3\n \
\t Script requires 3 arguments\n \
\t a) Workload: (0 = JOB, 1 = JOB-light, 2 = JCCH, 3 = DSB)\n \
\t b) Optimizer: (0 = PostgreSQL, 1 = COMPASS)\n \
\t c) Search algorithm: (0 = Exhaustive, 1 = Greedy)\n \
")

print('Number of arguments:', len(sys.argv) - 1, 'arguments.')
print('Argument List:', str(sys.argv[1:]), '\n')

def similarity_weights_L1_error_combined(true_subs, est_subs, true_card):
    # similarity weights: D_i >= 0 and diagonals = 1
    # position weights: delta d_i >= 0 and rho p_1 = 1

    mu_weights = [1.0]  # monotonic increase
    for i in range(1, len(true_subs)):
        curr_mu = mu_weights[-1] + true_card[true_subs[i]] / max(true_card[true_subs[i - 1]], ZERO_REPLACE)
        mu_weights.append(curr_mu)

    # NOTE: symmetric matrix, similar to Q-error
    D_weights = {}
    for sub in true_subs:
        D_weights[sub] = {}
        for inner_sub in true_subs:
            # NOTE: in case of zero cardinality, use ZERO_REPLACE value
            q_error = max([true_card[inner_sub] / max(true_card[sub], ZERO_REPLACE), 
                        true_card[sub] / max(true_card[inner_sub], ZERO_REPLACE)])
            D_weights[sub][inner_sub] = q_error

    join_l1_error = 0
    for out_t_id, sub in enumerate(true_subs):
        est_id = est_subs.index(sub)
        left_term, right_term = 0, 0
        for in_t_id in range(out_t_id):
            e_id = est_subs.index(true_subs[in_t_id])
            if e_id > est_id:
                left_term += D_weights[sub][true_subs[in_t_id]]
        for in_t_id in range(out_t_id + 1, len(true_subs)):
            e_id = est_subs.index(true_subs[in_t_id])
            if e_id < est_id:
                right_term += D_weights[sub][true_subs[in_t_id]]
        left_term /= mu_weights[out_t_id]
        right_term /= mu_weights[out_t_id]
        join_l1_error += left_term + right_term
    return join_l1_error

def rec_subsets(left, right, n, min_costs, memo, subplan, cost_functions, est_index, query):
    if n == -1: return

    left.append(subplan[n])
    right.remove(subplan[n])
    left_str = " ".join(sorted(left))
    right_str = " ".join(sorted(right))

    if left_str + "-" + right_str in memo: return
    memo.add(left_str + "-" + right_str)
    memo.add(right_str + "-" + left_str)

    if (left_str in cost_functions.all_cardinalities[query] 
            or left_str in cost_functions.table_nicks) \
        and (right_str in cost_functions.all_cardinalities[query] 
             or right_str in cost_functions.table_nicks):

        edge_weight = cost_functions.compute_c_mm_cost(left, right)
        min_costs[0] = min(min_costs[0], edge_weight[2][0])
        min_costs[1] = min(min_costs[1], edge_weight[2][est_index])

    rec_subsets(left, right, n - 1, min_costs, memo, subplan, cost_functions, est_index, query)
    left.remove(subplan[n])
    right.append(subplan[n])

    rec_subsets(left, right, n - 1, min_costs, memo, subplan, cost_functions, est_index, query)

# NOTE: this can be used in exhaustive search
def updateCardWithCost(subquery_plans, query, arg_table_nicks, is_compass,
                       arg_base_table_file, arg_cardinality_file):

    cost_functions = CostFunctions(arg_table_nicks, query, None, 
                        arg_base_table_file, arg_cardinality_file)
    est_index = 2 if is_compass else 1
    
    query_max_join = 0
    for subquery in subquery_plans[query]:
        curr_join_size = subquery_plans[query][subquery][0]
        query_max_join = max(query_max_join, curr_join_size)

    for curr_join_size in range(3, query_max_join):
        for subquery in subquery_plans[query]:
            if curr_join_size == subquery_plans[query][subquery][0]:
                min_costs = [float('inf'), float('inf')]
                subplan = subquery_plans[query][subquery][3]

                # NOTE: bushy and greedy
                rec_subsets([], subplan[:], curr_join_size - 1, min_costs, set(), 
                            subplan, cost_functions, est_index, query)

                # NOTE: prev cost + curr cost
                subquery_plans[query][subquery][1] = min_costs[0]
                subquery_plans[query][subquery][2] = min_costs[1]
                # subquery_plans[query][subquery].append(edge_weight[2][0] + min_costs[0])
                # subquery_plans[query][subquery].append(edge_weight[2][est_index] + min_costs[1])

if len(sys.argv) != 4:
    print("Wrong number of arguments.\n")
else:
    try:
        benchmark_type = int(sys.argv[1])
        is_compass = int(sys.argv[2])
        is_greedy = int(sys.argv[3])

        is_cost_enabled = 0
        LOGISTIC_GROWTH_RATE = -1.5
        skip_queries = [] # 29a

        if is_compass not in [0, 1]: 
            print("Wrong argument types.\n")
        else:
            if is_compass: optimizer_type, est_index = "compass", 4
            else: optimizer_type, est_index = "psql", 3

            if is_greedy: enum_type = "greedy"
            else: enum_type = "exhaustive"
        
            if benchmark_type == 0:
                parent_folder = "input_data/job/"
                query_files = parent_folder + "JOB_QUERIES_COMPASS_PostgreSQL"
                cardinality_file = parent_folder + "results_estimates-JOB.csv"
                base_tables_file = parent_folder + "imdb_table_sizes.csv"
                opt_plans_file = parent_folder + enum_type + "_traversals-opt-cost.csv"
                est_plans_file = parent_folder + enum_type + "_traversals-opt-cost-" + optimizer_type + ".csv"
                output_f_file = parent_folder + "L1-errors-agg-" + enum_type + "-" + optimizer_type + ".csv"
            elif benchmark_type == 1:
                parent_folder = "input_data/job_light/"
                query_files = parent_folder + "JOB_light_QUERIES"
                cardinality_file = parent_folder + "results_estimates-JOB-light.csv"
                base_tables_file = parent_folder + "imdb_table_sizes.csv"
                opt_plans_file = parent_folder + enum_type + "_traversals-opt-cost.csv"
                est_plans_file = parent_folder + enum_type + "_traversals-opt-cost-" + optimizer_type + ".csv"
                output_f_file = parent_folder + "L1-light-errors-agg-" + enum_type + "-" + optimizer_type + ".csv"
            elif benchmark_type == 2:
                parent_folder = "input_data/jcch/"
                query_files = parent_folder + "workload_jcch_queries"
                cardinality_file = parent_folder + "results_estimates-JCCH.csv"
                base_tables_file = parent_folder + "jcch_table_sizes.csv"
                opt_plans_file = parent_folder + enum_type + "_traversals-opt-cost.csv"
                est_plans_file = parent_folder + enum_type + "_traversals-opt-cost-" + optimizer_type + ".csv"
                output_f_file = parent_folder + "L1-jcch-errors-agg-" + enum_type + "-" + optimizer_type + ".csv"
            elif benchmark_type == 3:
                parent_folder = "input_data/dsb/"
                query_files = parent_folder + "workload_dsb_queries"
                cardinality_file = parent_folder + "results_estimates-DSB.csv"
                base_tables_file = parent_folder + "dsb_table_sizes.csv"
                opt_plans_file = parent_folder + enum_type + "_traversals-opt-cost.csv"
                est_plans_file = parent_folder + enum_type + "_traversals-opt-cost-" + optimizer_type + ".csv"
                output_f_file = parent_folder + "L1-dsb-errors-agg-" + enum_type + "-" + optimizer_type + ".csv"

            ###############################################################################

            opt_plans_costs = {}
            with open(opt_plans_file, "r") as input_f:
                for idx, line in enumerate(input_f):
                    if idx == 0: continue
                    line = line.split(",")
                    query, opt_plan_true_cost = line[0], float(line[2])
                    opt_plans_costs[query] = opt_plan_true_cost

            est_plans_costs = {}
            with open(est_plans_file, "r") as input_f:
                for idx, line in enumerate(input_f):
                    if idx == 0: continue
                    line = line.strip().split(",")
                    query, est_plan_true_cost = line[0], float(line[2])
                    est_plans_costs[query] = est_plan_true_cost

            all_cardinalities, all_queries = {}, {}
            with open(cardinality_file, "r") as input_f:
                for idx, line in enumerate(input_f):
                    if idx == 0: continue
                    line = line.strip().split(",")

                    query, subquery = "_".join(line[0].split("_")[:-1]), line[0]
                    join_size = int(line[1])
                    true_card, est_card = float(line[2].strip()), float(line[est_index].strip())

                    subplan = ",".join(line[5:])[2:-2].split(",")
                    subplan = [node.strip()[1:-1].split("-")[1] for node in subplan]

                    if query not in all_cardinalities: all_cardinalities[query] = {}
                    all_cardinalities[query][subquery] = [join_size, true_card, est_card, subplan]

            ############################# Calculate L1-error ##############################

            l1_join_level = []
            for idx, file_name in enumerate(sorted(os.listdir(query_files))):
                input_query = query_files + "/" + file_name
                with open(input_query, "r") as query_input_f:
                    if benchmark_type == 0: query_name = file_name.split("_")[1][:-4]
                    elif benchmark_type == 1: query_name = file_name[:-4]
                    elif benchmark_type == 2: query_name = file_name[:-4]
                    elif benchmark_type == 3: query_name = file_name[:-4]

                    original_query = [query_line for query_line in query_input_f]
                    original_query = "".join(original_query)

                    # extracting tables and join predicates
                    from_and_where = original_query.split('FROM')[1].split('WHERE')
                    table_list = from_and_where[0].split(',')
                    table_list = [table.strip() for table in table_list]
                    table_nicks = {info[1]: info[0] for info in [table.split(" AS ") for table in table_list]}

                    # collecting tables and join predicates information
                    where_clause = from_and_where[1].split('\n\n')
                    where_clause = [clause_set for clause_set in where_clause if clause_set]

                    join_predicates = where_clause[1].split('AND')
                    join_predicates = [join.strip() for join in join_predicates if join.strip()]
                    join_predicates[-1] = join_predicates[-1][:-1]

                    # NOTE: exhaustive enumeration 
                    #           cost + cardinality
                    if not is_greedy and is_cost_enabled:
                        updateCardWithCost(all_cardinalities, query_name, table_nicks, is_compass, 
                                        base_tables_file, cardinality_file)

                    # NOTE: add +1 if last join is included
                    for join_size in range(2, len(table_list)):
                        true_cards, est_cards = {}, {}
                        for sub in all_cardinalities[query_name]:
                            if all_cardinalities[query_name][sub][0] == join_size:
                                true_cards[sub] = all_cardinalities[query_name][sub][1]
                                est_cards[sub] = all_cardinalities[query_name][sub][2]

                        ordered_true_cards = {k: v for k, v in sorted(true_cards.items(), key=lambda item: item[1])}
                        ordered_true_subs = [sub for sub in ordered_true_cards]
                        ordered_est_cards = {k: v for k, v in sorted(est_cards.items(), key=lambda item: item[1])}
                        ordered_est_subs = [sub for sub in ordered_est_cards]

                        max_q_error = -1
                        for i in range(len(ordered_est_subs)):
                            sub = ordered_true_subs[i]
                            t_card = ordered_true_cards[sub]
                            e_card = ordered_est_cards[sub]
                            q_error_curr = max([e_card / max(t_card, ZERO_REPLACE), t_card / max(e_card, ZERO_REPLACE)])
                            max_q_error = max(max_q_error, q_error_curr)

                        if query_name in skip_queries: continue
                        curr_l1_error = similarity_weights_L1_error_combined(ordered_true_subs, 
                                                                             ordered_est_subs, ordered_true_cards)
                        l1_join_level.append([query_name, join_size, len(table_list), 
                                              len(join_predicates), curr_l1_error, max_q_error])

            ############################# Aggregation all sub-queries within the same join size ##################
            
            l1_query_level = {}
            for query in all_cardinalities:
                max_join_size, tables_nbr, predicates_nbr, max_q_error = -1, None, None, -1
                max_norm_L1, sum_norm_L1, weighted_sum_l1 = -1, 0, 0
                for l1 in l1_join_level:
                    if l1[0] == query:
                        join_size = l1[1]
                        max_join_size = max(max_join_size, join_size)
                        tables_nbr = l1[2]
                        predicates_nbr = l1[3]

                        join_weight = math.exp(LOGISTIC_GROWTH_RATE * join_size) \
                            / (1 + math.exp(LOGISTIC_GROWTH_RATE * join_size))

                        max_norm_L1 = max(max_norm_L1, l1[4])
                        sum_norm_L1 += l1[4]
                        weighted_sum_l1 += l1[4] * join_weight
                        max_q_error = max(max_q_error, l1[5])
                l1_query_level[query] = [max_join_size, tables_nbr, predicates_nbr, 
                                         max_q_error, max_norm_L1, sum_norm_L1, weighted_sum_l1]        

            ############################# Aggregation across join sizes ###########################################

            output_f = open(output_f_file, "w")
            output_f_writer = csv.writer(output_f, delimiter=',')
            output_f_writer.writerow(["query", "complexity", "tables", 
                "predicates", "cost ratio", "MAX Q-error", 
                "MAX L1-error", "SUM L1-error", "Weighted SUM L1-error"])

            workload_max_join = 0
            complexity_counter = [set(), set(), set()]
            query_complexities = [[2, 9], [10, 19], [20, 28]]

            # NOTE: first process sub-optimal plans and then optimal plans for each complexity
            for c_idx, complexity in enumerate(query_complexities):
                for query in all_cardinalities:
                    if query not in opt_plans_costs: continue
                    if query not in est_plans_costs: continue
                    if query in skip_queries: continue 
                    cost_ratio = est_plans_costs[query] / opt_plans_costs[query]
                    l1_info = l1_query_level[query]
                    workload_max_join = max(workload_max_join, l1_info[0])
                    if complexity[0] <= l1_info[2] <= complexity[1]:
                        complexity_counter[c_idx].add(query)
                        output_f_writer.writerow([query, c_idx + 1, l1_info[1], 
                            l1_info[2], cost_ratio, 
                            l1_info[3], l1_info[4], l1_info[5], l1_info[6]])  
            output_f.close()

            print("\nworkload max join: " + str(workload_max_join))
            print("simple, moderate, complex, TOTAL: " + 
                str([len(complexity_counter[0]), len(complexity_counter[1]), len(complexity_counter[2]),
                    len(complexity_counter[0]) + len(complexity_counter[1]) + len(complexity_counter[2])]))
        
        print("\nThe results will be saved at: " + output_f_file)
        print("Success.\n")
    except:
        print("Wrong parameter type or code error.\n")
