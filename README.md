**TripPlan API**

### Overview

The TripPlan API is a FastAPI-based web service that generates personalized travel itineraries. Users can input 
their travel plans and preferences, and the API creates a customized trip with attractions, travel modes, and 
detailed scheduling.

### Features

*   **Trip Generation**: Generates trips based on user input and existing travel plans.
*   **Customizable Itineraries**: Flexible to user preferences and planned attractions.
*   **CORS Support**: Compatible with cross-origin requests for seamless integration with front-end applications.

### Installation

1.  Clone the repository:
    ```bash
git clone 
cd 
```
2.  Install the required dependencies:
    ```bash
pip install -r requirements.txt
```
3.  Run the server:
    ```bash
uvicorn main:app –reload
```

### API Endpoints

#### Root Endpoint

*   **GET /**: Returns a simple message to confirm that the API is running.
    Response:
    ```
{
“Hello”: “World”
}
```

#### Generate Trip

*   **POST /generate_trip**: Generates a personalized trip itinerary based on the user’s input and travel plan.
    Request Body:
    ```json
{
“trip”: {
“travel_plan”: [
{
"type": "Attraction",
"name": "Home",
"address": "Starting Point",
"place_id": “home_001”,
"time_slot": “MORNING”,
"visit_duration": 0,
"travel_time_to_prev": 0,
"travel_time_to_next": 30,
"estimate_start_time": “08:00:00”,
"estimate_end_time": “08:00:00”,
"tags": [“start”],
"description": "The starting point of the journey.",
"reviews": [],
"rating": null,
"rating_count": 0,
"ticket_price": null,
"url": "",
"location": {
"latitude": 40.7128,
"longitude": -74.0060
}
}
]
},
"user_input": “Visit a museum and have lunch in the city center.”
}
```
    Response:
    ```json
{
“generated_trip”: [
{
"name": “Home”,
"address": "Starting Point",
"place_id": “home_001”,
"time_slot": “MORNING”,
"visit_duration": 0,
"travel_time_to_prev": 0,
"travel_time_to_next": 30,
"estimate_start_time": “08:00:00”,
"estimate_end_time": “08:00:00”,
"tags": [“start”],
"description": “The starting point of the journey.”,
"reviews": [],
"rating": null,
"rating_count": 0,
"ticket_price": null,
"url": "",
"location": {
"latitude": 40.7128,
"longitude": -74.0060
}
},
…
]
}
```

### Key Components

#### Models

*   **Trip**: Represents the overall travel plan.
*   **Attraction**: Represents a point of interest with details like name, address, duration, and reviews.
*   **Travel**: Represents the travel between attractions, including mode, time, and notes.

#### Utility Functions

*   **process_user_input**: Parses user preferences and returns actionable data.
*   **gen**: Core trip generation logic that creates an itinerary based on the input data.

### Configuration

#### CORS Middleware

The API uses CORSMiddleware to allow requests from all origins. You can restrict access by modifying the 
`allow_origins` parameter in the middleware configuration:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://yourdomain.com"],  # Replace with your domain(s)
    allow_credentials=True,
    allow_methods=[“”],
    allow_headers=[””],
)
```

### Running in Production

1.  Use a production-ready ASGI server, such as gunicorn or daphne:
    ```bash
gunicorn -k uvicorn.workers.UvicornWorker main:app
```
2.  Set up HTTPS with a reverse proxy like Nginx for secure communication.

### Contributing

1.  Fork the repository.
2.  Create a feature branch:
    ```bash
git checkout -b feature/new-feature
```
3.  Commit changes:
    ```bash
git commit -m “Add new feature”
```
4.  Push to your branch and create a pull request.

### License

This project is licensed under the MIT License.

### Contact

For questions or support, contact Yun Yang Liao at `your.email@example.com`.
