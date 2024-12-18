# TripPlan API

## Overview

The TripPlan API is a FastAPI-based web service that generates personalized travel itineraries. Users can input 
their travel plans and preferences, and the API creates a customized trip with attractions, travel modes, and 
detailed scheduling.

## Features

*   **Trip Generation**: Generates trips based on user input and existing travel plans.
*   **Customizable Itineraries**: Flexible to user preferences and planned attractions.
*   **CORS Support**: Compatible with cross-origin requests for seamless integration with front-end applications.

## Installation

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
    fastapi dev triplan_api/main.py
    ```

## API Endpoints

Refer to [this document](https://triplan-api.vercel.app/docs#/).

## Key Components

### Models

*   **Trip**: Represents the overall travel plan.
*   **Attraction**: Represents a point of interest with details like name, address, duration, and reviews.
*   **Travel**: Represents the travel between attractions, including mode, time, and notes.

### Utility Functions

*   **process_user_input**: Parses user preferences and returns actionable data.
*   **gen**: Core trip generation logic that creates an itinerary based on the input data.

## Contributing

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

## License

This project is licensed under the MIT License.

## Contact

For questions or support, you can raise an issue.
