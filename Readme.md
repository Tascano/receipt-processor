Readme 

Brief : 
This is a FastAPI based receipt processor REST API. Currently handles POST and GET requests. 
Also has a SQLite based DB. 

The default master branch has below - 
Master branch - https://github.com/Tascano/receipt-processor/tree/master

1. The default branch is built such that it has two databases - items and receipts with tables with the same names on it. 
2. Schema of the receipt table is such that it does not save the points associated with the receipts so the points are calculated with every get requests. 

The persist_points branch is such that it has below - 
persist_points branch https://github.com/Tascano/receipt-processor/tree/persist_points
1. It has one retail.db as database. In the retail.db, there are two tables - items and receipts. 
2. Schema of the receipt table is such that it calculates and saves the points associated with the receipt at the time of post request. This helps as there is no calculation needed in the get request so the speed of query reply increases. 
3. The disadvantage is, if the method to calculate points changes then we would need to backfill the receipts database. But my thought process is this. If we give a customer a receipt - the points are finalized and don't change even if the offer changes - so this backfill would not be required. 

For Most part the major development of the project is done at persist_points branch. Please consider that working with it. 

For any tests on the API consider developing your examples by looking at curl_examples.txt file. 

## Start 

Create a new virtual environment (optional but recommended) by running the following command:

```
$ python -m venv venv
```

Activate the virtual environment. The command to activate the virtual environment varies depending on your operating system:

For Windows (Command Prompt):
```
$ venv\Scripts\activate.bat
```

For Windows (PowerShell):
```
$ venv\Scripts\Activate.ps1
```
For macOS/Linux:
```
$ source venv/bin/activate
```

## To install requirements  
Update requirements.txt 
$ pip install -r requirements.txt

## To run a server 
$ uvicorn main:app --reload


## To stop a running server 

To stop a running uvicorn server started with the `uvicorn main:app --reload` command, you can use one of the following methods:

1. Press `Ctrl + C` in the terminal where the server is running. This will send a KeyboardInterrupt signal, causing the server to stop gracefully.

2. If you are running the server in the background or in a separate terminal session, you can find the process ID (PID) of the uvicorn process and terminate it using the appropriate command for your operating system.

   - On Unix/Linux:
     - Use the `ps` command to list the running processes and find the PID of the uvicorn process:
       ```bash
       ps aux | grep uvicorn
       ```
     - Once you have the PID, use the `kill` command followed by the PID to terminate the process:
       ```bash
       kill <PID>
       ```

   - On Windows:
     - Use the `tasklist` command to list the running processes and find the PID of the uvicorn process:
       ```bash
       tasklist | findstr "uvicorn"
       ```
     - Once you have the PID, use the `taskkill` command followed by the PID to terminate the process:
       ```bash
       taskkill /PID <PID>
       ```

Choose the method that is most convenient for you to stop the uvicorn server.


### To Test

# Use Postman 

If you're using Postman, you can follow these steps:

1. Open Postman and create a new request.
2. Set the request URL to http://localhost:8000/receipts/process.
3. Choose the HTTP method as POST.
4. Select the "Body" tab.
5. Select "Raw" and set the body format as JSON (application/json).
6. Paste the provided JSON payload into the request body.
7. Click the "Send" button to send the request and view the response.

Make sure your server is running on http://localhost:8000 or update the URL accordingly if it's different.

The response will include the generated ID for the processed receipt. You can also test the /receipts/{id}/points endpoint to retrieve the points for a specific receipt by replacing {id} with the actual ID of a processed receipt.


# Use Curl 

```

$ curl -X POST -H "Content-Type: application/json" -d "{\"retailer\":\"Target\",\"purchaseDate\":\"2022-01-01\",\"purchaseTime\":\"13:01\",\"items\":[{\"shortDescription\":\"Mountain Dew 12PK\",\"price\":\"6.49\"},{\"shortDescription\":\"Emils Cheese Pizza\",\"price\":\"12.25\"},{\"shortDescription\":\"Knorr Creamy Chicken\",\"price\":\"1.26\"},{\"shortDescription\":\"Doritos Nacho Cheese\",\"price\":\"3.35\"},{\"shortDescription\":\"   Klarbrunn 12-PK 12 FL OZ  \",\"price\":\"12.00\"}],\"total\":\"35.35\"}" http://localhost:8000/receipts/process

>>> {"id":"a03d8a7e-060b-4a1b-a464-40be361c6976"}

$ curl http://localhost:8000/receipts/a03d8a7e-060b-4a1b-a464-40be361c6976/points
>>> {"points":28}
```

# Swagger UI

To test the API using Swagger UI, you can follow these steps:

1. Make sure your FastAPI server is running.

2. Open your web browser and navigate to the Swagger UI URL. By default, it should be `http://localhost:8000/docs`.

3. Once the Swagger UI page is loaded, you will see the list of available endpoints and their corresponding input/output models.

4. Click on the endpoint you want to test, such as `/receipts/process` or `/receipts/{id}/points`. This will expand the endpoint and display the input parameters and response models.

5. Click on the "Try it out" button to open the input form for the selected endpoint.

6. Fill in the input fields with the desired values based on the request model. For example, for the `/receipts/process` endpoint, you can provide the input data in the "Example Value" section.

7. After filling in the input data, click the "Execute" button to send the request to the server.

8. The response from the server will be displayed below the input form. You can check the response status, response body, and any error messages returned by the server.

9. Repeat the steps for other endpoints or different input data as needed.

By using the Swagger UI, you can conveniently test your API endpoints and observe the responses in real-time. It provides an interactive interface for exploring and interacting with your API.



# For testing unit tests 
```
$ pytest - v
```

# For testing integration
If you are running on a custom ec2 or server, add the appropriate link to the base_url in the intergration_tests.py file

```
$ python integration_tests.py
```

# To run dockerized 

1. Open terminal in root directory
2. $ docker build -t myapp .
3. $ docker run -d -p 8000:8000 myapp
4. Test by doing all of the above tests such as swagger ui, or running integration tests at address http://localhost:8000
5. See all open docker containers by running ```$ docker ps```
6. To stop container and remove it run below commands 
   - docker stop <container_id>
   - docker rm <container_id>
