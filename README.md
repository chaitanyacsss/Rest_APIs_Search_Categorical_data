### Introduction  ###
Simple API: Load and Search Product data, which has brand and categorical information.


* The following 3 APIs were created:

```
POST /api/products/autocomplete

Example query: curl -i -H "Content-Type: application/json" -X POST -d "{\"type\":\"categoryName\",\"prefix\":\"d\"}" localhost:8088/api/products/autocomplete

This example results in a list of category names starting with d or D.
```
```
POST /api/products/search

Example query: curl -i -H "Content-Type: application/json" -X POST -d "{\"conditions\": [{ \"type\": \"brandName\", \"values\": [\"Brother\", \"Canon\"] }],\"pagination\": { \"from\": 1, \"size\": 3 }}" localhost:8088/api/products/search

This results in a list of products that satisfy the field/value conditions. 
```
```
POST /api/products/keywords

Example query: curl -i -H "Content-Type: application/json" -X POST -d "{ \"keywords\": [\"toner\", \"book\", \"phone\" ] }" localhost:8088/api/products/keywords

This results in the word frequencies for the given keywords.
```

### Implementation ###

As an initial straightforward approach, each datapoint is loaded as a dictionary and the list is traversed everytime a query comes in. For this approach,
- Space complexity is O(N), where N is the total number of products.
- Autocomplete has a time complexity of O(N) since we will need to traverse through all products to autocomplete any field.
- Similarly, M conditions will take atmost O(MN) time.
- Keywords query takes O(1) since the frequencies are stored in a dictionary with the keywords as keys.

- It is clear that the performance for the first two can be improved. For this, We can make use of the limited number of Brand and Category names, compared to the total number of products.

- Therefore, an undirected graph is built with nodes of types Brand, Category and Product.
- Each product, which has product id and product title as properties, is linked to it's brand node (with properties brandId and brandName) 
and it's category (categoryId + categoryName). This makes traversing through categories and brands much faster.
- So, for the first query of autocompletion, The time-complexity reduces to O(c) or O(b), where c and b are number of categories and brands respectively.
- Similarly for search query, we can start the search query with category fields (since there are only ~70 categories while there are 50k products). We then 
traverse through the brand fields and finally the product fields.

- Pagination is also implemented with the search traversal results.

### Tech Stack ###
Python3, Apache Flask, Docker

