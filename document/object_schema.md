# Object Schema

---

## trip
| **Attribute Name** | **Type**         | **Required** | **Value Range** | **Default** | **Description**                          |
|--------------------|------------------|--------------|-----------------|-------------|------------------------------------------|
| **title**          | string           | Yes          | None            | None        | The title of the trip.                   |
| **description**    | string           | Yes          | None            | None        | A brief description of the trip.         |
| **range**          | object           | Yes          | None            | None        | The start and end dates of the trip.     |
| ├─ start           | string (date)    | Yes          | None            | None        | The starting date of the trip (YYYY-MM-DD). |
| └─ end             | string (date)    | Yes          | None            | None        | The ending date of the trip (YYYY-MM-DD). |
| **travel_plan**    | array            | Yes          | None            | None        | A list of activities and travel details for the trip. |
| **(attraction)**   | object           | No           | None            | None        | Attraction details within `travel_plan`. |
| ├─ type            | string (const)   | Yes          | "attraction"    | None        | Fixed as "attraction".                   |
| ├─ name            | string           | Yes          | None            | None        | The name of the attraction.              |
| ├─ location        | string           | Yes          | None            | None        | The location of the attraction.          |
| ├─ description     | string           | No           | None            | None        | A description of the attraction.         |
| └─ visit_duration  | integer          | Yes          | Min value: 0    | None        | Visit duration in minutes.               |
| **(travel)**       | object           | No           | None            | None        | Travel details within `travel_plan`.     |
| ├─ type            | string (const)   | Yes          | "travel"        | None        | Fixed as "travel".                       |
| ├─ travelMode      | string           | Yes          | None            | None        | The mode of travel.                      |
| ├─ from            | string           | Yes          | None            | None        | Starting location of travel.             |
| ├─ to              | string           | Yes          | None            | None        | Destination of travel.                   |
| ├─ time            | integer          | Yes          | Min value: 0    | None        | Travel time in minutes.                  |
| └─ notes           | string           | No           | None            | None        | Additional notes about the travel.       |

---
