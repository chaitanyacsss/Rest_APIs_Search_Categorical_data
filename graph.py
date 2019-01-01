class Graph:
    linkCount = 0

    class Node:
        def __init__(self, id, data, type):
            self.id = id
            self.data = data
            self.type = type
            self.links = {}

        def edgeTo(self, node):
            if node.id not in self.links.keys():
                self.links[node.id] = node
                node.links[self.id] = self
                Graph.linkCount += 1

    def __init__(self):
        self.products = {}
        self.brands = {}
        self.categories = {}
        self.nodeCount = 0

    def createProductNode(self, product_dict):
        product_node = self.Node(product_dict['productId'], product_dict['title'], "Product")
        brand_node = self.Node(product_dict['brandId'], product_dict['brandName'], "Brand")
        category_node = self.Node(product_dict['categoryId'], product_dict['categoryName'], "Category")
        if product_node.id not in self.products.keys():
            self.products[product_node.id] = product_node
            if brand_node.id not in self.brands.keys():
                self.brands[brand_node.id] = brand_node
            if category_node.id not in self.categories.keys():
                self.categories[category_node.id] = category_node
            product_node.edgeTo(brand_node)
            product_node.edgeTo(category_node)
            self.nodeCount += 1
        return product_node

    def __repr__(self):
        result = ""
        for product_id in self.products:
            curr_product = self.products[product_id]
            for link in curr_product.links:
                linked_node = curr_product.links[link]
                result += "{0} -- {1}\n".format(curr_product.data, linked_node.data)
        return result
