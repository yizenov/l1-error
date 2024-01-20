
TABLE_SCAN_COST = 0.2  # 1.0, 0.2
INDEX_COST = 2.0  # 1.0, 2.0

ZERO_VAL = 0.01  # replacing zero in denominators

class CostFunctions(object):
    def __init__(self, arg_table_nicks, arg_input_query, arg_selectivities,
                arg_base_table_sizes_file, arg_cardinality_file):
        self.TABLE_SCAN_COST = TABLE_SCAN_COST
        self.INDEX_COST = INDEX_COST

        self.base_table_sizes_file = arg_base_table_sizes_file
        self.cardinality_file = arg_cardinality_file

        self.table_nicks = arg_table_nicks
        self.input_query = arg_input_query

        self.all_table_size = {}
        self.all_cardinalities = {}

        # base table selectivities
        self.selectivities = arg_selectivities

        self.load_table_size()
        self.load_cardinalities()

    def load_table_size(self):
        with open(self.base_table_sizes_file, "r") as input_f:
            for idx, line in enumerate(input_f):
                if idx == 0: continue
                line = line.strip().split(",")

                table_name, table_size = line[0].strip(), int(line[1].strip())
                if table_name not in self.all_table_size: 
                    self.all_table_size[table_name] = table_size

    def load_cardinalities(self):
        with open(self.cardinality_file, "r") as input_f:
            for idx, line in enumerate(input_f):
                if idx == 0: continue
                line = line.strip().split(",")

                query, subquery = "_".join(line[0].split("_")[:-1]), line[0]
                join_size, true_card = int(line[1]), float(line[2])
                
                psql_card = float(line[3]) # psql estimates
                compass_card = float(line[4]) # compass estimates

                subplan = ",".join(line[5:])[2:-2].split(",")
                subplan = " ".join(sorted([node.strip()[1:-1].split("-")[1] for node in subplan]))

                if query not in self.all_cardinalities: self.all_cardinalities[query] = {}
                self.all_cardinalities[query][subplan] = [subquery, join_size, true_card, psql_card, compass_card]

    def compute_c_mm_cost(self, left_tables, right_tables):
        l, r = len(left_tables), len(right_tables)
        left_subplan = " ".join(sorted(left_tables))
        right_subplan = " ".join(sorted(right_tables))
        current_subplan = " ".join(sorted(left_tables + right_tables))

        ######################## Reading Cardinalities #####################################
        # NOTE: assume base table has true cardinality, even with selection predicate
        # NOTE: assume base table sizes are stored in catalogs

        if l == 1: 
            left_card_true = self.all_table_size[self.table_nicks[left_tables[0]]]
            left_card_psql = self.all_table_size[self.table_nicks[left_tables[0]]]
            left_card_compass = self.all_table_size[self.table_nicks[left_tables[0]]]
        elif l > 1: 
            left_card_true = self.all_cardinalities[self.input_query][left_subplan][2]
            left_card_psql = self.all_cardinalities[self.input_query][left_subplan][3]
            left_card_compass = self.all_cardinalities[self.input_query][left_subplan][4]
        if r == 1: 
            right_card_true = self.all_table_size[self.table_nicks[right_tables[0]]]
            right_card_psql = self.all_table_size[self.table_nicks[right_tables[0]]]
            right_card_compass = self.all_table_size[self.table_nicks[right_tables[0]]]
        elif r > 1: 
            right_card_true = self.all_cardinalities[self.input_query][right_subplan][2]
            right_card_psql = self.all_cardinalities[self.input_query][right_subplan][3]
            right_card_compass = self.all_cardinalities[self.input_query][right_subplan][4]

        ######################## Side Selections #####################################
        # NOTE: HJ -- zig-zag tree structure (probing, hash build)
        # NOTE: INL -- outer/inner table (scan side and index side)

        current_card_true = self.all_cardinalities[self.input_query][current_subplan][2]  # true
        current_card_psql = self.all_cardinalities[self.input_query][current_subplan][3]  # psql
        current_card_compass = self.all_cardinalities[self.input_query][current_subplan][4]  # compass

        if left_card_true < right_card_true:
            hash_build_side_true = left_card_true
            hash_join_true_info = ["HJ", right_subplan, left_subplan]
            outer_table_true = right_card_true
            inl_join_true_info = ["INL", right_subplan, left_subplan]
        else:
            hash_build_side_true = right_card_true
            hash_join_true_info = ["HJ", left_subplan, right_subplan]
            outer_table_true = left_card_true
            inl_join_true_info = ["INL", left_subplan, right_subplan]

        if left_card_psql < right_card_psql:
            hash_build_side_psql = left_card_psql
            hash_join_psql_info = ["HJ", right_subplan, left_subplan]
            outer_table_psql = right_card_psql
            inl_join_psql_info = ["INL", right_subplan, left_subplan]
        else:
            hash_build_side_psql = right_card_psql
            hash_join_psql_info = ["HJ", left_subplan, right_subplan]
            outer_table_psql = right_card_psql
            inl_join_psql_info = ["INL", left_subplan, right_subplan]

        if left_card_compass < right_card_compass:
            hash_build_side_compass = left_card_compass
            hash_join_compass_info = ["HJ", right_subplan, left_subplan]
            outer_table_compass = right_card_compass
            inl_join_compass_info = ["INL", right_subplan, left_subplan]
        else:
            hash_build_side_compass = right_card_compass
            hash_join_compass_info = ["HJ", left_subplan, right_subplan]
            outer_table_compass = right_card_compass
            inl_join_compass_info = ["INL", left_subplan, right_subplan]

        ######################## Join Operator Costs #####################################
        # NOTE: coefficients for base and intermediate table to distinguish from index scan

        if l != 1 and r != 1: # bushy join case
            hash_join_true = current_card_true + hash_build_side_true
            hash_join_psql = current_card_psql + hash_build_side_psql
            hash_join_compass = current_card_compass + hash_build_side_compass
            index_nested_loop_join_true = None  # NOTE: no index in inner tables, only base table
            index_nested_loop_join_psql = None
            index_nested_loop_join_compass = None
        elif l == 1 and r == 1: # both are base tables
            hash_join_true = current_card_true + hash_build_side_true \
                + self.TABLE_SCAN_COST * (left_card_true + right_card_true)
            hash_join_psql = current_card_psql + hash_build_side_psql \
                + self.TABLE_SCAN_COST * (left_card_psql + right_card_psql)
            hash_join_compass = current_card_compass + hash_build_side_compass \
                + self.TABLE_SCAN_COST * (left_card_compass + right_card_compass)
            index_nested_loop_join_true = self.TABLE_SCAN_COST * outer_table_true \
                + self.INDEX_COST * outer_table_true * max(current_card_true / max(outer_table_true, ZERO_VAL), 1)
            index_nested_loop_join_psql = self.TABLE_SCAN_COST * outer_table_psql \
                + self.INDEX_COST * outer_table_psql * max(current_card_psql / max(outer_table_psql, ZERO_VAL), 1)
            index_nested_loop_join_compass = self.TABLE_SCAN_COST * outer_table_compass \
                + self.INDEX_COST * outer_table_compass * max(current_card_compass / max(outer_table_compass, ZERO_VAL), 1)
        elif l == 1: # left-deep
            hash_join_true = current_card_true + hash_build_side_true + self.TABLE_SCAN_COST * left_card_true
            hash_join_psql = current_card_psql + hash_build_side_psql + self.TABLE_SCAN_COST * left_card_psql
            hash_join_compass = current_card_compass + hash_build_side_compass + self.TABLE_SCAN_COST * left_card_compass
            index_nested_loop_join_true = self.INDEX_COST * right_card_true * max(current_card_true / max(right_card_true, ZERO_VAL), 1)
            index_nested_loop_join_psql = self.INDEX_COST * right_card_psql * max(current_card_psql / max(right_card_psql, ZERO_VAL), 1)
            index_nested_loop_join_compass = self.INDEX_COST * right_card_compass * max(current_card_compass / max(right_card_compass, ZERO_VAL), 1)
        elif r == 1: # left-deep
            hash_join_true = current_card_true + hash_build_side_true + self.TABLE_SCAN_COST * right_card_true
            hash_join_psql = current_card_psql + hash_build_side_psql + self.TABLE_SCAN_COST * right_card_psql
            hash_join_compass = current_card_compass + hash_build_side_compass + self.TABLE_SCAN_COST * right_card_compass
            index_nested_loop_join_true = self.INDEX_COST * left_card_true * max(current_card_true / max(left_card_true, ZERO_VAL), 1)
            index_nested_loop_join_psql = self.INDEX_COST * left_card_psql * max(current_card_psql / max(left_card_psql, ZERO_VAL), 1)
            index_nested_loop_join_compass = self.INDEX_COST * left_card_compass * max(current_card_compass / max(left_card_compass, ZERO_VAL), 1)

        ######################## Join Operator Selection #####################################

        if index_nested_loop_join_true is None or index_nested_loop_join_true > hash_join_true:
            join_cost_true = hash_join_true
            join_true_info = hash_join_true_info
        else:
            join_cost_true = index_nested_loop_join_true
            join_true_info = inl_join_true_info
        
        if index_nested_loop_join_psql is None or index_nested_loop_join_psql > hash_join_psql:
            join_cost_psql = hash_join_psql
            join_psql_info = hash_join_psql_info
        else:
            join_cost_psql = index_nested_loop_join_psql
            join_psql_info = inl_join_psql_info

        if index_nested_loop_join_compass is None or index_nested_loop_join_compass > hash_join_compass:
            join_cost_compass = hash_join_compass
            join_compass_info = hash_join_compass_info
        else:
            join_cost_compass = index_nested_loop_join_compass
            join_compass_info = inl_join_compass_info
        
        #############################################################################

        subquery_id = self.all_cardinalities[self.input_query][current_subplan][0]
        join_size = self.all_cardinalities[self.input_query][current_subplan][1]
        results = [join_cost_true, join_cost_psql, join_cost_compass]
        results_info = [join_true_info, join_psql_info, join_compass_info]

        return [subquery_id, join_size, results, results_info]
