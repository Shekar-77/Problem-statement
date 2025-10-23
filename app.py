import pathway as pw

# Define a schema for our data
class MySchema(pw.Schema):
    name: str
    age: int

# Create a static input using Pathway's built-in method
data = pw.debug.table_from_rows(
    MySchema,
    [
        ("Alice", 25),
        ("Bob", 30),
        ("Charlie", 35),
    ],
)

# Perform transformation (filter people older than 28)
older_than_28 = data.filter(pw.this.age > 28)

# Print results to console
pw.debug.compute_and_print(older_than_28)
