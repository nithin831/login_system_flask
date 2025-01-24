#pypy Jit compilation

import time
#
# def sum_of_squares(limit, iterations):
#     total = 0
#     for j in range(iterations):
#         for i in range(limit):
#             total += i * i
#     return total
#
# # Parameters
# limit = 10000
# iterations = 1000
# start_time = time.time()
# result = sum_of_squares(limit, iterations)
# end_time = time.time()
# print(f"Sum of squares calculated: {result}")
# print(f"Execution time: {end_time - start_time:.6f} seconds")




# 10k api calls with asyncio

# import asyncio
# import httpx
# import time  # Import the time module to measure execution time
#
# API_URL = "https://jsonplaceholder.typicode.com/posts"
#
# async def fetch(client, url, index):
#     # Make the GET request without query parameters (asynchronously)
#     response = await client.get(url)
#     # print(f"Request {index}: {response.json()}")
#     return response.json()
#
# async def make_requests():
#     async with httpx.AsyncClient() as client:  # Use asynchronous Client
#         tasks = [fetch(client, API_URL, i) for i in range(100)]  # 10,000 requests
#         start_time = time.time()  # Record start time
#         results = await asyncio.gather(*tasks)  # Run all requests concurrently
#         end_time = time.time()  # Record end time
#         print(f"Total time for async is  10,000 requests: {end_time - start_time} seconds")
#         # return results
#
# if __name__ == "__main__":
#     asyncio.run(make_requests())  # Run the async function



#10k api calls with sync

# import time
# import httpx
#
# API_URL = "https://jsonplaceholder.typicode.com/posts"
#
# def fetch(client, url, index):
#     # Make the GET request without query parameters (synchronously)
#     response = client.get(url)
#     # print(f"Request {index}: {response.json()}")
#     return response.json()
#
# def make_requests():
#     with httpx.Client() as client:  # Use synchronous Client
#         start_time = time.time()  # Record start time
#         for i in range(100):  # 10,000 requests in a loop
#             fetch(client, API_URL, i)
#         end_time = time.time()  # Record end time
#         print(f"Total time for sync is 10,000 requests: {end_time - start_time} seconds")
#
# if __name__ == "__main__":
#     make_requests()
#

import psycopg2
from psycopg2 import pool
import time

# Function to perform a database query using psycopg2 with connection pooling
def run_query_with_pool(query, iterations):
    # Create a connection pool
    try:
        conn_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,  # Minimum number of connections
            maxconn=10,  # Maximum number of connections
            host="127.0.0.1",  # Change this if needed
            port=5432,  # Default port for PostgreSQL
            database="crudPsychopg2Db",  # Replace with your database name
            user="postgres",  # Your PostgreSQL username
            password="password"  # Your PostgreSQL password
        )

        # Start the timer
        start_time = time.time()

        # Run the query for a specified number of iterations
        for _ in range(iterations):
            # Acquire a connection from the pool
            conn = conn_pool.getconn()
            cursor = conn.cursor()

            cursor.execute(query)  # Execute the query
            cursor.fetchall()  # Fetch results (if applicable)

            # Close the cursor and release the connection back to the pool
            cursor.close()
            conn_pool.putconn(conn)

        # End the timer
        end_time = time.time()

        # Calculate requests per second
        total_time = end_time - start_time
        print(f"Total time: {total_time:.2f} seconds")
        req_per_sec = iterations / total_time
        print(f"With Pooling: {req_per_sec:.2f} requests/sec")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the pool to release all connections
        if conn_pool:
            conn_pool.closeall()

# Example query to benchmark
query = "SELECT * FROM Product;"  # Replace with a valid query for your use case
iterations = 100  # Number of iterations to run

# Run the function with connection pooling
run_query_with_pool(query, iterations)



import asyncio
import asyncpg
import time

# Async function to perform a database query (asynchronous) using connection pooling
async def run_query_async(query, iterations):
    # Create a connection pool
    pool = await asyncpg.create_pool(
        host="127.0.0.1",
        port=5432,
        database="crudPsychopg2Db",
        user="postgres",
        password="password",
        min_size=1,  # Minimum number of connections in the pool
        max_size=10  # Maximum number of connections in the pool
    )

    start_time = time.time()

    # Perform the query using the connection pool
    async with pool.acquire() as conn:  # Acquire a connection from the pool
        for _ in range(iterations):
            await conn.fetch(query)  # Execute the query and fetch results

    end_time = time.time()

    # Close the pool
    await pool.close()

    # Calculate requests per second
    total_time = end_time - start_time
    print(f"Total time: {total_time:.2f} seconds")
    req_per_sec = iterations / total_time
    print(f"Async (with pooling): {req_per_sec:.2f} requests/sec")

# Run the async code
if __name__ == "__main__":
    query = "SELECT 1;"  # Sample query
    iterations = 100  # Number of iterations to execute the query
    asyncio.run(run_query_async(query, iterations))


# import platform
# print(platform.python_implementation())



#distributed rate limit---radis