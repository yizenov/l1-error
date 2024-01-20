import sys, random
import pandas as pd
import matplotlib.pyplot as plt

# CART (Classification and Regression Trees)
    # scikit-learn uses an optimized version of the CART algorithm.
    # https://scikit-learn.org/stable/modules/tree.html#tree-algorithms-id3-c4-5-c5-0-and-cart
# C4.5, C5.0, ID3
from sklearn import tree

from sklearn.model_selection import GridSearchCV, train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import make_scorer, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score

# This script is to build Table 1, 2, 3, 4 
#   running Greedy and Exhaustive Searches
# Terminologies: PostgreSQL, COMPASS

# screen -S l1_classify -dm -L -Logfile scr_l1_classify.0 sh -c 'time /usr/bin/python3 scripts/run_L1_classifier.py 0 0 0 0'

print(
"\n \
1. Enter: ~/L1_error_indicator\n \
2. Run the following command: /usr/bin/python3 scripts/run_L1_classifier.py arg1 arg2 arg3 arg4\n \
\t Script requires 4 arguments:\n \
\t a) Workload: (0 = JOB, 1 = JOB-light, 2 = JCCH, 3 = DSB)\n \
\t b) Optimizer: (0 = PostgreSQL, 1 = COMPASS)\n \
\t c) Search algorithm: (0 = Exhaustive, 1 = Greedy)\n \
\t c) Classifier type: (0 = L1-error, 1 = Q-error)\n \
")

###################### Output File Name #########################

print('Number of arguments:', len(sys.argv) - 1, 'arguments.')
print('Argument List:', str(sys.argv[1:]), '\n')

if len(sys.argv) != 5:
    print("Wrong number of arguments.\n")
else:
    try:
        benchmark_type = int(sys.argv[1])
        is_compass = int(sys.argv[2])
        is_greedy = int(sys.argv[3])
        is_q_error = int(sys.argv[4])

        PERFORMANCE_RATIO = 1.0  # NOTE: true labeling
        MAX_DEPTH = 3  # NOTE: tree depth or None (def, no limit)

        TEST_SIZE = 0.2 # test and train size split
        IS_SHUFFLE = True

        # NOTE: 5 (def, None), 2 (minimum)
        #       UndefinedMetricWarning: Recall is ill-defined and being set to 0.0 due to no true samples. 
        #       Use `zero_division` parameter to control this behavior.
        #       UserWarning: The least populated class in y has only 6 members, which is less than n_splits=10.
        if benchmark_type == 0: CROSS_VALIDATION_FOLDS = 6
        elif benchmark_type == 1: CROSS_VALIDATION_FOLDS = 2
        else: CROSS_VALIDATION_FOLDS = 10 

        RANDOM_STATES = [10000]
        # RANDOM_STATES = [random.randint(1, 10000)]
        # RANDOM_STATES = [random.randint(1, 10000) for i in range(CROSS_VALIDATION_FOLDS)]

        # NOTE: DecisionTreeClassifier: sample_weight class_weight
        # NOTE: GridSearchCV: error_score, return_train_score, verbose

        # https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier
        CRITERIA_NAME = "entropy" # gini (def), entropy, log_loss
        SPLITTER_TYPE = "best"  # best (def), random

        MIN_SAMPLES_LEAF = 1 # 1 (def)
        MIN_SAMPLES_SPLIT = 2 # 2 (def)
        MAX_SAMPLES_LEAF = 10
        MAX_SAMPLES_SPLIT = 10

        # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
        ENABLE_REFIT = 'recall'  # True, accuracy, precision, recall, f1_score
            # refit an estimator using the best found parameters on the whole dataset

        SCORING_TYPE = {
            # "accuracy": make_scorer(accuracy_score),
            # "precision": make_scorer(precision_score),
            "recall": make_scorer(recall_score),
            # "f1_score": make_scorer(f1_score)
        }

        TREE_PARAMS = {
            "criterion": ['gini', 'entropy', 'log_loss'],
            "splitter": ["best"],
            "max_depth": [MAX_DEPTH],
            "min_samples_split": range(MIN_SAMPLES_SPLIT, MAX_SAMPLES_SPLIT),
            "min_samples_leaf": range(MIN_SAMPLES_LEAF, MAX_SAMPLES_LEAF),
            "random_state": RANDOM_STATES
        }

        ###################### Classifier Configuration #########################

        # TN - 0's or true fast/good queries
        # TP - 1's or true slow/bad queries
        # FP - fast/good queries BUT classified as slow/bad queries
        # FN - slow/bad queries BUT classified as fast/good queries
        
        if benchmark_type == 0:
            parent_folder = "input_data/job/"
            input_queries = parent_folder + "JOB_QUERIES_COMPASS_PostgreSQL/"
            file_name_prefixes = parent_folder + "L1-errors-agg-"
        elif benchmark_type == 1:
            parent_folder = "input_data/job_light/"
            input_queries = parent_folder + "JOB_light_QUERIES/"
            file_name_prefixes = parent_folder + "L1-light-errors-agg-"
        elif benchmark_type == 2:
            parent_folder = "input_data/jcch/"
            input_queries = parent_folder + "workload_jcch_queries/"
            file_name_prefixes = parent_folder + "L1-jcch-errors-agg-"
        elif benchmark_type == 3:
            parent_folder = "input_data/dsb/"
            input_queries = parent_folder + "workload_dsb_queries/"
            file_name_prefixes = parent_folder + "L1-dsb-errors-agg-"

        if is_greedy: file_name_prefixes += "greedy-"
        else: file_name_prefixes += "exhaustive-"

        if is_compass: file_name_prefixes += "compass.csv"
        else: file_name_prefixes += "psql.csv"

        data_feature_name = "Q-error" if is_q_error else "L1-error"
        data_class_names = ["Optimal", "Sub-Optimal"]

        ###################### Data Preparation #########################

        query_meta_data, initial_all_data = {}, []
        true_negatives, true_positives = 0, 0

        with open(file_name_prefixes, "r") as input_f:
            for idx, line in enumerate(input_f):
                if idx == 0: continue
                line = line.strip().split(',')

                query, cost_ratio = line[0], float(line[4])
                query_meta_data[query] = [int(line[1]), cost_ratio]

                max_q_error = float(line[5])
                max_norm_L1 = float(line[6])
                sum_norm_L1 = float(line[7])
                weighted_sum_norm_L1 = float(line[8])

                # NOTE: true labeling
                if cost_ratio <= PERFORMANCE_RATIO: 
                    label = 0
                    true_negatives += 1
                else: 
                    label = 1
                    true_positives += 1

                # NOTE: feature data
                if is_q_error: initial_all_data.append([query, max_q_error, label]) 
                else: initial_all_data.append([query, weighted_sum_norm_L1, label]) 

        pd.set_option('display.max_rows', 500)
        column_names = ["query", data_feature_name, "label"]
        data_df = pd.DataFrame(initial_all_data, columns = column_names)

        ###################### Classifier #########################

        feature_indexes = [i for i in range(1, len(initial_all_data[0]) - 1)]
        label_index = len(initial_all_data[0]) - 1
        all_data = pd.DataFrame(data_df.iloc[:, feature_indexes])
        all_label_data = pd.DataFrame(data_df.iloc[:, label_index])

        try:
            # NOTE:
            #   The least populated class in y has only 1 member, which is too few. 
            #   The minimum number of groups for any class cannot be less than 2.
            X_train, X_test, \
            y_train, y_test = train_test_split(
                            all_data, all_label_data, 
                            test_size=TEST_SIZE, 
                            shuffle=IS_SHUFFLE,
                            stratify=all_label_data,
                            random_state=RANDOM_STATES[0])
        except Exception as e: print(e)

        dt_clf = tree.DecisionTreeClassifier(
            criterion=CRITERIA_NAME,
            splitter=SPLITTER_TYPE,
            max_depth=MAX_DEPTH if MAX_DEPTH is not None else None,
            min_samples_split=MIN_SAMPLES_SPLIT,
            min_samples_leaf=MIN_SAMPLES_LEAF,
            random_state=RANDOM_STATES[0])
        
        if benchmark_type != 1:
            dt_clf = GridSearchCV(dt_clf, 
                param_grid=TREE_PARAMS, 
                cv=CROSS_VALIDATION_FOLDS if CROSS_VALIDATION_FOLDS is not None else None,
                refit=ENABLE_REFIT,
                scoring=SCORING_TYPE,
                return_train_score=True)

        try: dt_clf.fit(X_train, y_train)
        except Exception as e: print(e)
        y_predict_train = dt_clf.predict(X_train)
        y_predict_test = dt_clf.predict(X_test)

        if benchmark_type == 1: estimator = dt_clf
        else: estimator = dt_clf.best_estimator_

        print(estimator)
        text_representation = tree.export_text(estimator)
        print(text_representation)

        ########################################################
        
        print("\n-------------")
        print("\nInput file: " + file_name_prefixes)
        
        if benchmark_type == 0: print("\tBenchmark: JOB")
        elif benchmark_type == 1: print("\tBenchmark: JOB-light")
        elif benchmark_type == 2: print("\tBenchmark: JCCH")
        elif benchmark_type == 3: print("\tBenchmark: DSB")

        if is_compass: print("\tCardinality Estimator: COMPASS")
        else: print("\tCardinality Estimator: PostgreSQL")

        if is_greedy: print("\tEnumerator: Greedy")
        else: print("\tEnumerator: Exhaustive")

        if is_q_error: print("\tFeature: Q-error")
        else: print("\tFeature: L1-error")

        print("\nTotal: " + str(true_positives + true_negatives)
            + " (train " + str(len(X_train)) + ", test " + str(len(X_test)) + ")")

        tn_train, fp_train, fn_train, tp_train = confusion_matrix(y_train, y_predict_train, labels = [0, 1]).ravel()
        tn_test, fp_test, fn_test, tp_test = confusion_matrix(y_test, y_predict_test, labels = [0, 1]).ravel()
        tn, fp, fn, tp = tn_test + tn_train, fp_test + fp_train, fn_test + fn_train, tp_test + tp_train
        
        print("Confusion Matrix (Train + Test)")
        print("\nTOTAL    | estimated bad | estimated good |          ")
        print("true bad | "
              + str(tp) + "=" + str(tp_train) + "+" + str(tp_test) + " (TP) | "
              + str(fn) + "=" + str(fn_train) + "+" + str(fn_test) + " (FN) | "
              + str(true_positives) + "=" + str(tp_train + fn_train) + "+" + str(tp_test + fn_test))
        print("true good| "
              + str(fp) + "=" + str(fp_train) + "+" + str(fp_test) + " (FP) | "
              + str(tn) + "=" + str(tn_train) + "+" + str(tn_test) + " (TN) | "
              + str(true_negatives) + "=" + str(fp_train + tn_train) + "+" + str(fp_test + tn_test))
        print("         | " + str(fp + tp) + "=" + str(tp_train + fp_train) + "+" + str(tp_test + fp_test)
              + "      | " + str(fn + tn) + "=" + str(fn_train + tn_train) + "+" + str(fn_test + tn_test) + "     | ")

        score_train = round(accuracy_score(y_train, y_predict_train), 2)
        print("Prediction Accuracy (Train): " + str(score_train))
        score_test = round(accuracy_score(y_test, y_predict_test), 2)
        print("Prediction Accuracy (Test): " + str(score_test))

        ###################### Additional Printings #########################

        false_n, false_p = 0, 0
        fn_query_costs, fp_query_costs = {}, {}
        for idx, query_idx in enumerate(y_train.index):
            query, label = initial_all_data[query_idx][0], initial_all_data[query_idx][2]

            join_predicates, level = query_meta_data[query][0], -1
            if join_predicates < 10: level = "Simple"
            elif 9 < join_predicates < 20: level = "Moderate"
            else: level = "Complex"

            if label == 1 and label != y_predict_train[idx]:
                false_n += 1
                fn_query_costs[query] = [query, level, query_meta_data[query][1]]
            elif label == 0 and label != y_predict_train[idx]:
                false_p += 1
                fp_query_costs[query] = [query, level, query_meta_data[query][1]]
        print("\n-------------")
        print("train data stats (FN, FP):" + str([false_n, false_p]))
        print("\nFN train queries:")
        [print("\t" + str(fn_query_costs[query])) for query in fn_query_costs]
        print("\nFP train queries:")
        [print("\t" + str(fp_query_costs[query])) for query in fp_query_costs]
        print("\n-------------")

        false_n, false_p = 0, 0
        fn_query_costs, fp_query_costs = {}, {}
        for idx, query_idx in enumerate(y_test.index):
            query, label = initial_all_data[query_idx][0], initial_all_data[query_idx][2]

            join_predicates, level = query_meta_data[query][0], -1
            if join_predicates < 10: level = "Simple"
            elif 9 < join_predicates < 20: level = "Moderate"
            else: level = "Complex"

            if label == 1 and label != y_predict_test[idx]:
                false_n += 1
                fn_query_costs[query] = [query, level, query_meta_data[query][1]]
            elif label == 0 and label != y_predict_test[idx]:
                false_p += 1
                fp_query_costs[query] = [query, level, query_meta_data[query][1]]
        print("test data stats (FN, FP):" + str([false_n, false_p]))
        print("\nFN test queries:")
        [print("\t" + str(fn_query_costs[query])) for query in fn_query_costs]
        print("\nFP test queries:")
        [print("\t" + str(fp_query_costs[query])) for query in fp_query_costs]

        print("\nSuccess.")
    except:
        print("Wrong parameter type or code error.\n")