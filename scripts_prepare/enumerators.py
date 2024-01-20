
from heapq import heapify, heappush, heappop
import cost_module

class Undirected_Weighted_Graph_Greedy:
    def __init__(self, arg_query, arg_table_nicks, arg_card_type,
                 arg_base_table_file, arg_cardinality_file):
        self.min_heap, self.components  = [], {}
        self.card_type = arg_card_type
        self.cost_functions = cost_module.CostFunctions(arg_table_nicks, arg_query, 
                                    None, arg_base_table_file, arg_cardinality_file)

    def addEdge(self, u, v, w, cards, join_info):
        heappush(self.min_heap, (w, sorted([u, v]), cards[0], cards[1], cards[2], join_info))

        # computing as adjacent edges have redundant steps in cycles
        if u not in self.components: self.components[u] = (u, set(), [u])
        if v not in self.components: self.components[v] = (v, set(), [v])
        self.components[u][1].add(v)
        self.components[v][1].add(u)

    def removeFromMinHeap(self, arg_edge):
        # NOTE: double edge case e.g. t.id joins with two tables on the same attribute
        if arg_edge[1] in self.components[arg_edge[0]][1]:
            self.components[arg_edge[0]][1].remove(arg_edge[1])
        if arg_edge[0] in self.components[arg_edge[1]][1]:
            self.components[arg_edge[1]][1].remove(arg_edge[0])

        # edges to be deleted from min_heap
        arg_edge = " ".join(sorted(arg_edge))
        for idx, h_edge in enumerate(self.min_heap):
            temp_edge = " ".join(h_edge[1])
            if temp_edge == arg_edge:
                self.min_heap.pop(idx)
                heapify(self.min_heap)
                break

    def updateMinHeap(self, arg_edge, left_part, right_part):
        arg_edge = " ".join(sorted(arg_edge))
        for idx, h_edge in enumerate(self.min_heap):
            temp_edge = " ".join(h_edge[1])
            if temp_edge == arg_edge:
                edge_weight = self.cost_functions.compute_c_mm_cost(left_part, right_part)

                self.min_heap[idx] = (edge_weight[2][self.card_type], h_edge[1],
                                    edge_weight[2][0], edge_weight[2][1], edge_weight[2][2], 
                                    edge_weight[3][self.card_type])
                heapify(self.min_heap)
                break
    
    def find_component(self, root):
        while self.components[root][0] != root: 
            root = self.components[root][0]
        return root
    
    def union_components(self, x, y, left, right):
        # NOTE: given two components do not overlap
        if right in self.components[x][1]: self.components[x][1].remove(right)
        if left in self.components[y][1]: self.components[y][1].remove(left)

        # NOTE: REMOVE: multi-connections between given two components
        left_delete_nodes = [n for n in self.components[x][1] if n in self.components[y][2]]
        right_delete_nodes = [n for n in self.components[y][1] if n in self.components[x][2]]

        for n in left_delete_nodes:
            self.components[x][1].remove(n)
            self.removeFromMinHeap([x, n])
        for n in right_delete_nodes:
            self.components[y][1].remove(n)
            self.removeFromMinHeap([y, n])

        # NOTE: REMOVE untraversed common nodes for the next expansion
        common_delete_nodes = []
        for n in self.components[y][1]:
            if n in self.components[x][1]: common_delete_nodes.append(n)
            else: self.components[x][1].add(n)
        for n in common_delete_nodes:
            self.components[y][1].remove(n)
            self.removeFromMinHeap([y, n])
        
        # NOTE: merging already traversed nodes (common component)
        [self.components[x][2].append(n) for n in self.components[y][2]]
        self.components[y] = (x, set(), [])

        # NOTE: update costs with untraversed nodes in min-heap
        for untraversed_adj_node in self.components[x][1]:
            adj_node_component = self.find_component(untraversed_adj_node)
            for in_node in self.components[adj_node_component][2]:
                for out_node in self.components[x][2]:
                    # NOTE: update all multi-connections between the two components
                    self.updateMinHeap([out_node, in_node], 
                                       self.components[x][2], 
                                       self.components[adj_node_component][2])

    def greedy_enumerate(self):
        ge_order, ge_joins_info, ge_length = [], [], len(self.components) - 1
        ge_est_costs, ge_true_costs = 0, 0
        compass_est_costs, psql_est_costs = 0, 0
        while len(ge_order) < ge_length:
            edge_info = heappop(self.min_heap)

            x = self.find_component(edge_info[1][0])
            y = self.find_component(edge_info[1][1])

            # Discard the edge if both are in the same component
            if x != y:
                ge_order.append([edge_info[1][0], edge_info[1][1]])
                ge_joins_info.append(edge_info[5])
                ge_est_costs += edge_info[0]
                ge_true_costs += edge_info[2]  # NOTE: always compute true cost
                psql_est_costs += edge_info[3]
                compass_est_costs += edge_info[4]
                self.union_components(x, y, edge_info[1][0], edge_info[1][1])
        return ge_est_costs, ge_true_costs, psql_est_costs, compass_est_costs, ge_order, ge_joins_info

class Undirected_Weighted_Graph_Exhaustive:
    def __init__(self, arg_query, arg_table_nicks, arg_card_type, 
                 arg_base_table_file, arg_cardinality_file):
        self.card_type = arg_card_type
        self.cost_functions = cost_module.CostFunctions(arg_table_nicks, arg_query, 
                                    None, arg_base_table_file, arg_cardinality_file)

    ############## Exhaustive #########################

    def pruned_exhaustive_enumeration(self, plan_size, edge_list):

        def insert_edge(arg_comp, arg_idx, arg_edge):
            if arg_edge not in arg_comp[arg_idx]: arg_comp[arg_idx][arg_edge] = 0
            arg_comp[arg_idx][arg_edge] += 1

        def delete_edge(arg_comp, arg_idx, arg_edge):
            if arg_comp[arg_idx][arg_edge] == 1: arg_comp[arg_idx].pop(arg_edge)
            else: arg_comp[arg_idx][arg_edge] -= 1

        glabal_min_cost = [None]
        best_perm, current_permutation, components = [None, None, None, None, None, None], [], []

        def recursion(arg_best_perm, current_perm, elements, count, plan_size, 
                      components, global_min, est_cost, 
                      true_cost, psql_cost, compass_cost, all_join_info):

            if global_min[0] is not None and est_cost >= global_min[0]:
                return

            if count == plan_size:
                if global_min[0] is None or est_cost < global_min[0]: 
                    arg_best_perm[0], arg_best_perm[1], arg_best_perm[2] = current_perm[:], est_cost, true_cost
                    arg_best_perm[3], arg_best_perm[4], arg_best_perm[5] = psql_cost, compass_cost, all_join_info[:]
                    global_min[0] = est_cost
                return

            for idx, i in enumerate(elements):
                is_cycle = False
                left, right = False, False
                left_idx, right_idx = -1, -1
                for c_idx, comp in enumerate(components):
                    if i[0] in comp and i[1] in comp: 
                        is_cycle = True
                        break
                    if i[0] in comp: left, left_idx = True, c_idx
                    if i[1] in comp: right, right_idx = True, c_idx
                if is_cycle: continue

                is_bushy, temp_comp = False, None
                is_new_comp, local_join_info = False, False
                if not left and not right:  # new component
                    components.append({})
                    components[-1][i[0]] = 1
                    components[-1][i[1]] = 1
                    is_new_comp = True

                    left_component, right_component = [i[0]], [i[1]]
                    edge_weight = self.cost_functions.compute_c_mm_cost(left_component, right_component)
                    est_cost += edge_weight[2][self.card_type]
                    true_cost += edge_weight[2][0]
                    psql_cost += edge_weight[2][1]
                    compass_cost += edge_weight[2][2]
                    local_join_info = edge_weight[3][self.card_type]
                elif left and right:  # bushy case
                    left_component, right_component = list(components[left_idx]), list(components[right_idx])
                    edge_weight = self.cost_functions.compute_c_mm_cost(left_component, right_component)
                    est_cost += edge_weight[2][self.card_type]
                    true_cost += edge_weight[2][0]
                    psql_cost += edge_weight[2][1]
                    compass_cost += edge_weight[2][2]
                    local_join_info = edge_weight[3][self.card_type]

                    insert_edge(components, left_idx, i[0])
                    insert_edge(components, left_idx, i[1])
                    insert_edge(components, right_idx, i[0])
                    insert_edge(components, right_idx, i[1])

                    is_bushy = True
                    temp_comp = components[right_idx]
                    for node in components[right_idx]:
                        if node not in components[left_idx]: 
                            components[left_idx][node] = components[right_idx][node]
                        else: components[left_idx][node] += components[right_idx][node]
                    components.pop(right_idx)
                elif left:
                    left_component = list(components[left_idx])
                    if i[0] not in components[left_idx]: right_component = [i[0]]
                    else: right_component = [i[1]]
                    edge_weight = self.cost_functions.compute_c_mm_cost(left_component, right_component)
                    est_cost += edge_weight[2][self.card_type]
                    true_cost += edge_weight[2][0]
                    psql_cost += edge_weight[2][1]
                    compass_cost += edge_weight[2][2]
                    local_join_info = edge_weight[3][self.card_type]

                    insert_edge(components, left_idx, i[0])
                    insert_edge(components, left_idx, i[1])
                elif right:
                    left_component = list(components[right_idx])
                    if i[0] not in components[right_idx]: right_component = [i[0]]
                    else: right_component = [i[1]]
                    edge_weight = self.cost_functions.compute_c_mm_cost(left_component, right_component)
                    est_cost += edge_weight[2][self.card_type]
                    true_cost += edge_weight[2][0]
                    psql_cost += edge_weight[2][1]
                    compass_cost += edge_weight[2][2]
                    local_join_info = edge_weight[3][self.card_type]

                    insert_edge(components, right_idx, i[0])
                    insert_edge(components, right_idx, i[1])

                current_perm.append(i)
                all_join_info.append(local_join_info)
                elements.pop(idx)
                recursion(arg_best_perm, current_perm, elements, count + 1, 
                          plan_size, components, global_min, est_cost, 
                          true_cost, psql_cost, compass_cost, all_join_info)
                elements.insert(idx, i)
                current_perm.pop()
                all_join_info.pop()

                if is_new_comp:
                    left_component, right_component = [i[0]], [i[1]]
                    edge_weight = self.cost_functions.compute_c_mm_cost(left_component, right_component)
                    est_cost -= edge_weight[2][self.card_type]
                    true_cost -= edge_weight[2][0]
                    psql_cost -= edge_weight[2][1]
                    compass_cost -= edge_weight[2][2]
                    components.pop()
                elif is_bushy:
                    components.insert(right_idx, temp_comp)
                    for node in temp_comp:
                        if components[left_idx][node] == temp_comp[node]: 
                            components[left_idx].pop(node)
                        else: components[left_idx][node] -= temp_comp[node]

                    delete_edge(components, left_idx, i[0])
                    delete_edge(components, left_idx, i[1])
                    delete_edge(components, right_idx, i[0])
                    delete_edge(components, right_idx, i[1])

                    left_component, right_component = list(components[left_idx]), list(components[right_idx])
                    edge_weight = self.cost_functions.compute_c_mm_cost(left_component, right_component)
                    est_cost -= edge_weight[2][self.card_type]
                    true_cost -= edge_weight[2][0]
                    psql_cost -= edge_weight[2][1]
                    compass_cost -= edge_weight[2][2]
                elif left:
                    delete_edge(components, left_idx, i[0])
                    delete_edge(components, left_idx, i[1])

                    left_component = list(components[left_idx])
                    if i[0] not in components[left_idx]: right_component = [i[0]]
                    else: right_component = [i[1]]
                    edge_weight = self.cost_functions.compute_c_mm_cost(left_component, right_component)
                    est_cost -= edge_weight[2][self.card_type]
                    true_cost -= edge_weight[2][0]
                    psql_cost -= edge_weight[2][1]
                    compass_cost -= edge_weight[2][2]
                elif right:
                    delete_edge(components, right_idx, i[0])
                    delete_edge(components, right_idx, i[1])

                    left_component = list(components[right_idx])
                    if i[0] not in components[right_idx]: right_component = [i[0]]
                    else: right_component = [i[1]]
                    edge_weight = self.cost_functions.compute_c_mm_cost(left_component, right_component)
                    est_cost -= edge_weight[2][self.card_type]
                    true_cost -= edge_weight[2][0]
                    psql_cost -= edge_weight[2][1]
                    compass_cost -= edge_weight[2][2]
        
        recursion(best_perm, current_permutation, edge_list, 0, plan_size, components, glabal_min_cost, 0, 0, 0, 0, [])

        return best_perm
