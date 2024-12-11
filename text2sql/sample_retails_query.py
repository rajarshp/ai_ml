import random

# Define the base queries for the tables in the retail_db
def generate_select_queries():
    queries = []

    for _ in range(100):
        query_type = random.choice(["simple", "aggregated", "complex", "nested", "join_with_filter"])

        if query_type == "simple":
            query = (
                "SELECT c.first_name, c.last_name, o.order_date, p.name AS product_name, od.quantity, od.unit_price "
                "FROM Customers c "
                "JOIN Orders o ON c.customer_id = o.customer_id "
                "JOIN OrderDetails od ON o.order_id = od.order_id "
                "JOIN Products p ON od.product_id = p.product_id "
                f"WHERE o.status = '{random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'])}' "
                "ORDER BY o.order_date DESC;"
            )

        elif query_type == "aggregated":
            query = (
                "SELECT c.first_name, c.last_name, COUNT(o.order_id) AS total_orders, SUM(o.total_amount) AS total_spent "
                "FROM Customers c "
                "JOIN Orders o ON c.customer_id = o.customer_id "
                "GROUP BY c.customer_id "
                "HAVING SUM(o.total_amount) > 1000 "
                "ORDER BY total_spent DESC;"
            )

        elif query_type == "complex":
            query = (
                "SELECT c.first_name, c.last_name, o.order_date, p.name AS product_name, "
                "       od.quantity, od.unit_price, o.shipping_address, o.billing_address, o.status "
                "FROM Customers c "
                "JOIN Orders o ON c.customer_id = o.customer_id "
                "JOIN OrderDetails od ON o.order_id = od.order_id "
                "JOIN Products p ON od.product_id = p.product_id "
                f"WHERE p.category = '{random.choice(['Electronics', 'Books', 'Furniture', 'Clothing'])}' "
                f"AND o.status IN ('Shipped', 'Delivered') "
                "AND o.order_date >= CURRENT_DATE - INTERVAL '1 year' "
                "ORDER BY o.order_date DESC, p.name;"
            )

        elif query_type == "nested":
            query = (
                "SELECT p.name, p.category, p.price "
                "FROM Products p "
                "WHERE p.product_id IN ("
                "    SELECT od.product_id "
                "    FROM OrderDetails od "
                "    JOIN Orders o ON od.order_id = o.order_id "
                "    WHERE o.status = 'Delivered'"
                ");"
            )

        elif query_type == "join_with_filter":
            query = (
                "SELECT c.first_name, c.last_name, o.order_date, SUM(od.quantity * od.unit_price) AS total_order_value "
                "FROM Customers c "
                "JOIN Orders o ON c.customer_id = o.customer_id "
                "JOIN OrderDetails od ON o.order_id = od.order_id "
                "WHERE c.city = 'New York' "
                "GROUP BY c.customer_id, o.order_date "
                "HAVING SUM(od.quantity * od.unit_price) > 500 "
                "ORDER BY total_order_value DESC;"
            )

        queries.append(query)

    return queries

if __name__ == "__main__":
    queries = generate_select_queries()

    for i, query in enumerate(queries, start=1):
        print(f"Query {i}:\n{query}\n")
