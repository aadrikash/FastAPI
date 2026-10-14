# Enum lets us define a fixed set of allowed values.
from enum import Enum

# Optional allows a parameter to contain a value or None.
from typing import Optional

# FastAPI creates our API application.
# HTTPException returns HTTP errors, such as 404 Not Found.
# Path validates path parameters.
# Query validates query parameters.
from fastapi import FastAPI, HTTPException, Path, Query


# Create the FastAPI application.
app = FastAPI(title="Params Practice")


# Define the categories a product is allowed to have.
# Inheriting from str makes each enum value string-compatible.
class Category(str, Enum):
    skincare = "skincare"
    haircare = "haircare"
    wellness = "wellness"


# Store sample product data outside the Category class.
PRODUCTS = [
    {
        "id": 1,
        "name": "Vitamin C Serum",
        "category": "skincare",
        "price": 599.0,
    },
    {
        "id": 2,
        "name": "Onion Hair Oil",
        "category": "haircare",
        "price": 349.0,
    },
    {
        "id": 3,
        "name": "Ashwagandha Gummies",
        "category": "wellness",
        "price": 799.0,
    },
    {
        "id": 4,
        "name": "Sunscreen SPF 50",
        "category": "skincare",
        "price": 449.0,
    },
]


# --------------------------------------------------
# 1. PATH PARAMETER
# --------------------------------------------------

# The product ID is part of the URL path.
# Example: GET /products/1
@app.get("/products/{product_id}")
def get_product(
    # Require an integer greater than zero.
    # The ellipsis (...) means the parameter is required.
    product_id: int = Path(
        ...,
        gt=0,
        description="Unique product ID",
    ),
):
    # Check each product in the PRODUCTS list.
    for product in PRODUCTS:

        # Compare the product's ID with the requested ID.
        if product["id"] == product_id:

            # Return the matching product.
            return product

    # If no product matches, return HTTP 404.
    raise HTTPException(
        status_code=404,
        detail="Product {} not found".format(product_id),
    )


# --------------------------------------------------
# 2. QUERY PARAMETERS, FILTERING AND PAGINATION
# --------------------------------------------------

# Example: GET /products?category=skincare&max_price=500
@app.get("/products")
def list_products(

    # Optional category filter.
    # Allowed values: skincare, haircare, wellness.
    category: Optional[Category] = None,

    # Optional text search.
    # Example: ?search=serum
    search: Optional[str] = Query(None),

    # Optional maximum price.
    # ge=0 means the price cannot be negative.
    max_price: Optional[float] = Query(None, ge=0),

    # Number of products to return.
    # The limit must be between 1 and 100.
    limit: int = Query(10, ge=1, le=100),

    # Number of products to skip.
    # Cannot be negative.
    skip: int = Query(0, ge=0),
):
    # Start with the complete product list.
    results = PRODUCTS.copy()

    # Filter by category if the client supplied one.
    if category is not None:
        results = [
            product
            for product in results
            if product["category"] == category.value
        ]

    # Filter by maximum price if the client supplied one.
    if max_price is not None:
        results = [
            product
            for product in results
            if product["price"] <= max_price
        ]

    # Filter by search text if the client supplied one.
    if search is not None:

        # Convert the search text to lowercase.
        # This makes the search case-insensitive.
        search_lower = search.lower()

        # Keep products whose name OR category contains the search text.
        results = [
            product
            for product in results
            if (
                search_lower in product["name"].lower()
                or search_lower in product["category"].lower()
            )
        ]

    # Count the products remaining after filtering.
    total = len(results)

    # Apply pagination after filtering.
    # Example: skip=1 and limit=2 returns two products,
    # starting with the second product in the filtered list.
    page = results[skip : skip + limit]

    # Return the total count and the requested page of products.
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": page,
    }