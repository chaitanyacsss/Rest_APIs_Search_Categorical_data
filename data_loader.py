import csv
import re
from graph import Graph

fieldnames = ['categoryId', 'categoryName', 'brandId', 'brandName', 'productId', 'title']
fieldnames_original_order = ['productId', 'title', 'brandId', 'brandName', 'categoryId', 'categoryName']

data_graph = Graph()
word_dictionary = {}
with open('sample_product_data.tsv', encoding="utf-8") as data_file:
    tsv_reader = csv.DictReader(data_file, delimiter='\t', fieldnames=fieldnames_original_order)
    line_count = 0
    for row in tsv_reader:
        data_graph.createProductNode(row)

        for each_word in row['title'].split(' '):
            each_word = re.sub(r'[^\w]', ' ', each_word)
            each_word = each_word.lower().strip()
            if each_word not in word_dictionary:
                word_dictionary[each_word] = 0
            word_dictionary[each_word] += 1


def autocomplete(key, prefix_text, complete_graph=data_graph):
    """Performs Autocomplete on the given field"""
    if key.startswith("category"):
        search_nodes = complete_graph.categories
    elif key.startswith("brand"):
        search_nodes = complete_graph.brands
    else:
        search_nodes = complete_graph.products
    return [k.data for k in search_nodes.values() if k.data.lower().startswith(prefix_text.lower())]


def get_frequencies(keywords, keyword_dictionary=word_dictionary):
    return {k: keyword_dictionary[k] for k in keyword_dictionary.keys() & keywords}


def get_product(id, complete_graph):
    """Gives The Product Node for the given ID"""
    product_dict = {'productId': id}
    product = complete_graph.products[id]
    product_dict['title'] = product.data
    for each_id in product.links:
        each_data = product.links[each_id].data
        each_type = product.links[each_id].type
        if each_type == "Brand":
            product_dict["brandId"] = each_id
            product_dict["brandName"] = each_data
        else:
            product_dict["categoryId"] = each_id
            product_dict["categoryName"] = each_data
    return product_dict


def search_by_conditions(conditions, pagination, complete_graph=data_graph):
    """Traverse Graph to Output the Products That Satisfy the Conditions
    Currently, the results are a union of all conditions as per the example given
    in the problem statement"""
    conditions.sort(key=lambda x: fieldnames.index(x['type']))
    results = []

    '''initial filter'''
    initial_condition = conditions.pop(0)
    condition_type = initial_condition['type']
    condition_values = initial_condition['values']

    if condition_type.startswith("category"):
        if "Id" in condition_type:
            for each_value in condition_values:
                results += complete_graph.categories[str(each_value)].links.keys()
        else:
            for each_category in complete_graph.categories.values():
                if each_category.data in condition_values:
                    results += each_category.links.keys()
    elif condition_type.startswith("brand"):
        if "Id" in condition_type:
            for each_value in condition_values:
                results += complete_graph.brands[str(each_value)].links.keys()
        else:
            for each_brand in complete_graph.brands.values():
                if each_brand.data in condition_values:
                    results += each_brand.links.keys()
    else:
        if "Id" in condition_type:
            results = condition_values
        else:
            for each_product_key in complete_graph.products.keys():
                if complete_graph.products[each_product_key].data in condition_values:
                    results += [each_product_key]

    '''following condition filters'''
    for each_condition in conditions:
        condition_type = each_condition['type']
        condition_values = each_condition['values']

        local_results = []
        if condition_type.startswith("category"):
            if "Id" in condition_type:
                for each_value in condition_values:
                    local_results += complete_graph.categories[str(each_value)].links.keys()
            else:
                for each_category in complete_graph.categories.values():
                    if each_category.data in condition_values:
                        local_results += each_category.links.keys()
        elif condition_type.startswith("brand"):
            if "Id" in condition_type:
                for each_value in condition_values:
                    local_results += complete_graph.brands[str(each_value)].links.keys()
            else:
                for each_brand in complete_graph.brands.values():
                    if each_brand.data in condition_values:
                        local_results += each_brand.links.keys()
        else:
            if "Id" in condition_type:
                local_results = condition_values
            else:
                for each_product_key in complete_graph.products.keys():
                    if complete_graph.products[each_product_key].data in condition_values:
                        local_results += [each_product_key]

        results = list(set(results).union(local_results))

    result_dicts = []
    for each in results:
        result_dicts.append(get_product(each, complete_graph))
    pagination_start = pagination['from']
    pagination_count = pagination['size']
    print("Search Results : ", result_dicts)
    return result_dicts[pagination_start-1:max(pagination_start+pagination_count-1,len(result_dicts))]
