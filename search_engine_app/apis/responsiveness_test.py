import aiohttp
import asyncio
import time
import pandas as pd
import matplotlib.pyplot as plt

# Your original API configuration
api_endpoint = 'http://145.100.135.119/api/' 
api_config = {'headers': {'Authorization': 'Token 2d23b88f724f5d95072d011786f7133e1e517675'}}  # Replace with your config
queries = [
    'how to learn python programming',
    'best practices for machine learning',
    'what is deep learning',
    'top 10 algorithms in data science',
    'how to preprocess data in python',
    'what is overfitting in machine learning',
    'ways to prevent overfitting',
    'explain bias-variance tradeoff',
    'how to handle missing data in pandas',
    'what is a confusion matrix',
    'understanding precision and recall',
    'examples of supervised learning algorithms',
    'how to tune hyperparameters in sklearn',
    'what is cross-validation in machine learning',
    'how to evaluate a machine learning model',
    'what is natural language processing',
    'how does a neural network work',
    'explain gradient descent algorithm',
    'how to train a model in tensorflow',
    'what is transfer learning in deep learning',
    'ways to improve model performance',
    'understanding convolutional neural networks',
    'how to deploy a machine learning model',
    'what is reinforcement learning',
    'how to use XGBoost for classification',
    'how to visualize data with matplotlib',
    'explain principal component analysis',
    'what is t-SNE used for',
    'how to build a recommendation system',
    'what is feature engineering in machine learning'
]


# Function to fetch a single URL with parameters and record the time it takes
async def fetch(query, session):
    url = api_endpoint + "notebook_search/"
    params = {
        "page": "1",
        "query": query,
        "filter": "",
        "facet": "",
    }
    
    start_time = time.perf_counter()  # Record start time
    async with session.get(url, params=params, **api_config) as response:
        status_code = response.status  # Capture the status code
        await response.text()  # Wait for the response text (content of the API call)
        end_time = time.perf_counter()  # Record end time
        return query, end_time - start_time, status_code  # Return query, time taken, and status code

# Main async function to gather all requests asynchronously
async def fetch_all(queries):
    async with aiohttp.ClientSession() as session:
        # Gather all requests asynchronously
        tasks = [fetch(query, session) for query in queries]
        responses = await asyncio.gather(*tasks)
        return responses

# Run the async function
def run_requests():
    return asyncio.run(fetch_all(queries))

for count in range(5): 
    # Get the response times and status codes for each query
    responses = run_requests()

    # Extract queries, response times, and status codes
    queries, response_times, status_codes = zip(*responses)

    # Create a DataFrame to store queries, response times, and status codes
    df = pd.DataFrame({
        'Query': queries,
        'Response Time (seconds)': response_times,
        'Status Code': status_codes
    })


    # Save to CSV
    df.to_csv(f'queries_response_times_{count}.csv', index=False)
    print(f'Saved responses {count}')

