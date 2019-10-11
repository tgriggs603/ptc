# Setting up the application
This application has some dependencies that are required. Flask, flask_restplus, dnspython DNS toolkit, json. I've installed them into a virtual environment for development. It was developed with Python version 3.7.4.
The dependencies should be handled by the requirements.txt file when the docker image is built.
You can manually start the Python/Flask Restful HTTP API by entering **"python app.py"** or if you have deployed the Docker image the service should initialize by itself. The API endpoint will be available at [http://localhost:5000/mxrecords/] 

# Usage
Since the Restful HTTP API requires no authtoken for access you should be able to return MX records for a single domain by entering that domain as the last value on the API endpoint. For example [http://localhost:5000/mxrecords/oracle.com] 

# Running the tests
By convention the tests are in a file named test_app.py. They are located in the same top level folder as the application app.py.
They can be run by entering **"python test_app.py"**. They also have some dependencies that are required. The main app of course, unittest, along with some modules and classes from Flask, dns.resolver, werkzeug.

# Documentation
The dependencies should be handled by the requirements.txt file when the docker image is built.
The documentation consists of this README file and the Swagger/OpenAPI UI available in the [http://localhost:5000/docs] endpoint.

# Improvements needed
Only the MX record read functionality is currently implemented for this API. Future improvements would be to build out the other CRUD operations for creation, update and deletion of MX records. At that point the project layout would most likely change to organize source files and seperate the tests out.