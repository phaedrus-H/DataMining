# -*- coding: utf-8 -*-
import operator
import itertools
from collections import OrderedDict

"""
    This function sorts the MIS values in ascending order
"""
   
def sort_mis(mis_dictionary):
    sorted_mis = OrderedDict(sorted(mis_dictionary.items(), key=operator.itemgetter(1)))
    print("M", sorted_mis)
    print("--------------------------------")
    return sorted_mis
"""
    This function performs the init-pass to generate the list L
"""

def init_pass(sorted_mis, transaction_database):
    items = sorted_mis.keys()
    items_support_count = OrderedDict()
    init_pass_dict = dict()
    init_pass = []
    for item in items:
        item_count = 0
        for transaction in transaction_database:
            if item in transaction:
                item_count = item_count + 1   
        items_support_count[item] = item_count/len(transaction_database)
    base_item_support_count = 0
    for item in items_support_count:
        if base_item_support_count == 0 and items_support_count[item] >= sorted_mis[item]:
           base_item_support_count = sorted_mis[item]
           init_pass.append(item)
        elif items_support_count[item] >= base_item_support_count:
            init_pass.append(item)
    init_pass_dict["L"] = init_pass
    init_pass_dict["L_support_count"] = items_support_count
    print("I-S", items_support_count)
    print("L", init_pass)
    print("--------------------------------")
    return init_pass_dict

"""
    This function generates 1-frequent itemsets
"""
   
def generate_F1_itemsets(init_pass_dict, sorted_mis):
    f1_itemsets = []
    init_pass = init_pass_dict["L"]
    items_support_count = init_pass_dict["L_support_count"]
    if len(init_pass) > 0 and len(items_support_count) > 0:
        for item in init_pass:
            if items_support_count[item] >= sorted_mis[item]:
                item_list = []
                item_list.append(item)
                f1_itemsets.append(tuple(item_list))
    return f1_itemsets

"""
    This function generates candidates for level 2
"""

def level2_candidate_gen(init_pass_dict, sdc, sorted_mis, cannot_be_together):
    c2_itemsets = []
    init_pass = init_pass_dict["L"]
    items_support_count = init_pass_dict["L_support_count"]
    outer_loop_iterator = 0
    while outer_loop_iterator < len(init_pass):
        item = init_pass[outer_loop_iterator]
        if items_support_count[item] >= sorted_mis[item]:
            inner_loop_iterator = outer_loop_iterator + 1
            while inner_loop_iterator < len(init_pass):
                inner_item = init_pass[inner_loop_iterator]
                if (items_support_count[inner_item] >= sorted_mis[item]) and ((abs(items_support_count[inner_item] - items_support_count[item])) <= sdc):
                    itemset = [item, inner_item]
                    if apply_cannot_be_together(itemset, cannot_be_together):
                        c2_itemsets.append(itemset)
                inner_loop_iterator = inner_loop_iterator + 1
        outer_loop_iterator = outer_loop_iterator + 1
    return c2_itemsets

def apply_cannot_be_together(itemset, cannot_be_together):
    for item in cannot_be_together:
        set_f1 = set(itemset)
        set_f2 = set(item)
        if len(set_f1.intersection(set_f2)) == len(item):
            return False
    return True
        

"""
    This function generates k-1 subsets
"""

def generate_level_down_subsets(f, sorted_mis, level):
    level_down_subsets = []
    list_of_keys = list(sorted_mis.keys())
    for itemset in itertools.combinations(set(f), level - 1):
        sorted_dict = {}
        for item in itemset:
            sorted_dict[item] = list_of_keys.index(item)
        level_down_subsets.append(tuple(OrderedDict(sorted(sorted_dict.items(), key=operator.itemgetter(1)))))
    #print(f, level_down_subsets)
    return level_down_subsets
    
"""
    This function validates the condition for merge in MS candidate generation
"""

def validate_itemsets_for_merge(f1, f2, sorted_mis, sdc, support_count):
    set_f1 = set(f1[:-1])
    set_f2 = set(f2[:-1])
    if (len(set_f1.intersection(set_f2)) == len(set_f1)):
        if (sorted_mis[f1[-1]] < sorted_mis[f2[-1]]) and (abs(support_count[f1[-1]] - support_count[f2[-1]]) <= sdc):
            return True
        else:
            return False
    else:
        return False
        
def check_subset_level_down(subset, fk_itemsets, level):
    is_present = False
    for item in fk_itemsets:
        set_item = set(item)
        set_subset = set(subset)
        if len(set_item.intersection(set_subset)) == level-1:
            is_present = True
            break
    return is_present
            

"""
    This function generates candidates for the level K
"""
    
def ms_candidate_gen(fk_itemsets, sdc, sorted_mis, no_of_transactions, level, support_count, cannot_be_together):
    ck_itemsets = []
    outer_loop_iterator = 0
    while outer_loop_iterator < len(fk_itemsets):
        inner_loop_interator = outer_loop_iterator + 1
        f1 = tuple(fk_itemsets[outer_loop_iterator])
        while inner_loop_interator < len(fk_itemsets):
            f2 = tuple(fk_itemsets[inner_loop_interator])
            merge_result = validate_itemsets_for_merge(f1, f2, sorted_mis, sdc, support_count)
            if merge_result:
                f = list(f1[:]) 
                f.append(f2[-1])
                if apply_cannot_be_together(f, cannot_be_together):
                    ck_itemsets.append(f)
                    level_down_subsets = generate_level_down_subsets(f, sorted_mis, level)
                    for subset in level_down_subsets:
                        if (f[0] in subset) or (sorted_mis[f[1]] == sorted_mis[f[0]]):
                            if not(check_subset_level_down(subset, fk_itemsets, level)):
                                ck_itemsets.remove(f)
                                break
            inner_loop_interator = inner_loop_interator + 1
        outer_loop_iterator = outer_loop_iterator + 1
    return ck_itemsets
 
def generate_subset(itemsets, count):
    subset = []
    for itemset in itertools.combinations(set(itemsets), count):
        subset.append(itemset)
    return subset
    
def msap(transaction_database, parameters): 
    level = 1 # k as per the algorithm
    frequent_item_set_dict = OrderedDict()
    sorted_mis = sort_mis(parameters["mis_dictionary"]) # M as per the algorithm
    cannot_be_together = generate_subset(parameters["cannot_be_together"], 2)
    must_have = generate_subset(parameters["must_have"], 1)
    init_pass_dict = init_pass(sorted_mis, transaction_database) # Holds L as well as their support counts
    f1_itemsets = generate_F1_itemsets(init_pass_dict, sorted_mis)
    frequent_item_set_dict[level] = f1_itemsets
    print("f", level, f1_itemsets)
    print("--------------------------")
    level = level + 1
    no_of_transactions = len(transaction_database)
    sdc = parameters["SDC"]
    fk_itemsets = []
    while ((level -1) in frequent_item_set_dict.keys()):
        candidate_list = []
        if level == 2:
            candidate_list = level2_candidate_gen(init_pass_dict, sdc, sorted_mis, cannot_be_together)
        else:
            candidate_list = ms_candidate_gen(fk_itemsets, sdc, sorted_mis, no_of_transactions, level, init_pass_dict["L_support_count"], cannot_be_together)   
        if len(candidate_list) > 0:
            print("C", level, candidate_list)
            print("-------------------------")
        candidate_count_dict = OrderedDict()
        for transaction in transaction_database:
            transaction_set = set(transaction)
            for candidate in candidate_list:
                candidate_set = set(candidate)
                if tuple(candidate) not in candidate_count_dict.keys():
                        candidate_count_dict[tuple(candidate)] = 0
                if len(candidate_set.intersection(transaction_set)) == len(candidate_set):
                        count = candidate_count_dict[tuple(candidate)]
                        candidate_count_dict[tuple(candidate)] = count + 1
        fk_itemsets = []
        for candidate in candidate_count_dict.keys():
           if (candidate_count_dict[candidate]/no_of_transactions) >= sorted_mis[candidate[0]]:
                fk_itemsets.append(candidate)
        if len(fk_itemsets) > 0:
            print("f", level, fk_itemsets)
            print("-------------------------")
            frequent_item_set_dict[level] = fk_itemsets
        level = level + 1
    print_frequent_itemsets_with_must_have(frequent_item_set_dict, must_have, transaction_database)
        
def print_frequent_itemsets_with_must_have(frequent_item_set_dict, must_have, transaction_database):
    file_write = open("output-patterns.txt", "w")
    output_dictionary = OrderedDict()
    for level in frequent_item_set_dict.keys():
        fk_itemsets = frequent_item_set_dict[level]
        count_list = []
        for itemset in fk_itemsets:
            count_dictionary = OrderedDict()
            for item in must_have:
                set_item = set(item)
                set_itemset = set(itemset)
                if len(set_item.intersection(set_itemset)) > 0:
                    total_count = 0
                    tail_count = 0
                    for transaction in transaction_database:
                        transaction_set = set(transaction)
                        if set_itemset.issubset(transaction_set):
                            total_count = total_count + 1
                        if level > 1:
                            tail_set = set(itemset[1:])
                            if tail_set.issubset(transaction_set):
                                tail_count = tail_count + 1
                    count_dictionary[itemset] = {"total_count":total_count, "tail_count":tail_count}
            if len(count_dictionary) > 0:
                count_list.append(count_dictionary)
        if len(count_list) > 0:
            output_dictionary[level] = count_list
    for level in output_dictionary.keys():
        file_write.write("Frequent "+str(level)+"-itemsets")
        file_write.write("\n")
        file_write.write("\n")
        count_list = output_dictionary[level]
        for dictionary in count_list:
            for itemset in dictionary:
                string = "{"+','.join(itemset)+"}"
                file_write.write("\t" + str(dictionary[itemset]["total_count"]) +" : "+ string)
                file_write.write("\n")
                if level != 1:
                    file_write.write("Tail Count = "+str(dictionary[itemset]["tail_count"]))
                    file_write.write("\n")
        file_write.write("\n")
        file_write.write("\t" + "Total number of frequent " + str(level)+"-itemsets = "+str(len(count_list)))
        file_write.write("\n")
        file_write.write("\n")
                    
    

    
