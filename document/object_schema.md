# Object Schema

---

## trip
| **屬性名稱**       | **類型**         | **必填** | **取值範圍**  | **預設值** | **描述**                                  |
|-------------------|------------------|----------|--------------|------------|------------------------------------------|
| **title**         | string           | 是       | 無           | 無         | The title of the trip.                   |
| **description**   | string           | 是       | 無           | 無         | A brief description of the trip.         |
| **range**         | object           | 是       | 無           | 無         | The start and end date of the trip.      |
| ├─ start          | string (date)    | 是       | 無           | 無         | The starting date of the trip (YYYY-MM-DD). |
| └─ end            | string (date)    | 是       | 無           | 無         | The ending date of the trip (YYYY-MM-DD). |
| **travel_plan**   | array            | 是       | 無           | 無         | A list of activities and travel details for the trip.|
| **(attraction)**  | object           | 否       | 無           | 無         | Attraction details within travel_plan.   |
| ├─ type           | string (const)   | 是       | "attraction" | 無         | 固定為 "attraction".                     |
| ├─ name           | string           | 是       | 無           | 無         | The name of the attraction.              |
| ├─ location       | string           | 是       | 無           | 無         | The location of the attraction.          |
| ├─ description    | string           | 否       | 無           | 無         | A description of the attraction.         |
| └─ visit_duration | integer          | 是       | 最小值: 0     | 無         | Visit duration in minutes.               |
| **(travel)**      | object           | 否       | 無           | 無         | Travel details within travel_plan.       |
| ├─ type           | string (const)   | 是       | "travel"     | 無         | 固定為 "travel".                         |
| ├─ travelMode     | string           | 是       | 無           | 無         | The mode of travel.                      |
| ├─ from           | string           | 是       | 無           | 無         | Starting location of travel.             |
| ├─ to             | string           | 是       | 無           | 無         | Destination of travel.                   |
| ├─ time           | integer          | 是       | 最小值: 0     | 無         | Travel time in minutes.                  |
| └─ notes          | string           | 否       | 無           | 無         | Additional notes about the travel.       |

---

## place