# Agent REST API Documentation

This document provides a structured overview of the REST API endpoints available under the `/agent` blueprint. All endpoints are implemented in `app.py` and the `agent` module (`agent/agent.py`).

---

## Table of Contents
1. [Introduction](#introduction)
2. [Standard JSON Response Schema](#standard-json-response-schema)
3. [Example Response Schemas](#example-response-schemas)
    - [Designation List](#designation-list-json-schema)
    - [Team List](#team-list-json-schema)
    - [Name List](#name-list-json-schema)
    - [Directors List](#directors-list-json-schema)
4. [API Endpoints](#api-endpoints)

---

## Introduction
The `/agent` API provides endpoints for agent dashboard, booking, leads, and related resources. All endpoints are registered in `app.py` and implemented in `agent/agent.py`.

---

## Standard JSON Response Schema
All API endpoints that return JSON use the following standard structure:

```json
{
  "status": "success" | "error",   // Indicates if the request was successful
  "message": string,                 // Human-readable message
  "data": object | array | null      // The main response payload (if any)
}
```

- `status`: Indicates the result of the API call. Possible values: `success`, `error`.
- `message`: A brief message describing the result or error.
- `data`: The actual data returned by the endpoint. This can be an object, array, or null if not applicable.

---

## Example Response Schemas

### <a name="designation-list-json-schema"></a>Designation List JSON Schema
```json
{
  "Designation": [
    { "id": "Agent", "name": "Agent" },
    { "id": "Director", "name": "Director" },
    { "id": "Manager", "name": "Manager" },
    { "id": "Senior Agent", "name": "Senior Agent" },
    { "id": "Team Lead", "name": "Team Lead" }
  ],
  "status": "ok"
}
```
- `Designation`: Array of designation objects, each with `id` and `name` fields.
- `status`: Indicates the result of the API call (e.g., `ok`).

### <a name="team-list-json-schema"></a>Team List JSON Schema
```json
{
  "teams": [
    { "id": "Team A", "name": "Team A" },
    { "id": "Team Alpha", "name": "Team Alpha" },
    { "id": "Team B", "name": "Team B" },
    { "id": "Team Beta", "name": "Team Beta" },
    { "id": "Team C", "name": "Team C" },
    { "id": "Team D", "name": "Team D" },
    { "id": "Team Delta", "name": "Team Delta" },
    { "id": "Team Gamma", "name": "Team Gamma" }
  ],
  "status": "ok"
}
```
- `teams`: Array of team objects, each with `id` and `name` fields.
- `status`: Indicates the result of the API call (e.g., `ok`).

### <a name="name-list-json-schema"></a>Name List JSON Schema
```json
{
  "name": [
    { "id": 9, "name": "Jane Smith" },
    { "id": 10, "name": "Raj Yadav" }
  ],
  "status": "ok"
}
```
- `name`: Array of name objects, each with `id` and `name` fields.
- `status`: Indicates the result of the API call (e.g., `ok`).

### <a name="directors-list-json-schema"></a>Directors List JSON Schema
```json
{
  "directors": [
    { "id": 1, "name": "Satish Kumar" },
    { "id": 2, "name": "Anita Sharma" }
  ],
  "status": "ok"
}
```
- `directors`: Array of director objects, each with `id` and `name` fields.
- `status`: Indicates the result of the API call (e.g., `ok`).

---

## API Endpoints

All endpoints below are defined in `app.py` and `agent/agent.py`.

| Method     | Endpoint                          | Description                                 | Response Type         |
|------------|-----------------------------------|---------------------------------------------|----------------------|
| GET        | /                                 | Login page (login-basic.html)               | HTML                 |
| GET        | /<pagename>                       | Render template by name                     | HTML                 |
| GET        | /<path:resource>                  | Static resources from the static/ directory | Static file          |
| POST       | /login                            | Authenticate user, returns user info        | JSON                 |
| GET        | /get_name                         | Get logged-in user's name (auth required)   | JSON                 |
| GET        | /logout                           | Logout user (auth required)                 | JSON                 |
| GET, POST  | /test                             | MOCK Test endpoint for JSON/multipart data  | JSON/HTML            |
| GET, POST  | /register-agent                   | Register an agent (see views.py)            | JSON/HTML            |
| GET, POST  | /register-customer                | Register a customer (see views.py)          | JSON/HTML            |
| GET        | /agent/                           | Agent dashboard page                        | HTML                 |
| GET        | /agent/<resource>                 | Static resources from the static/ directory | Static file          |
| GET        | /agent/book-site-visit.html       | Site visit booking page                     | HTML                 |
| GET, POST  | /agent/book-visit                 | Book a site visit (see booking.py)          | JSON/HTML            |
| GET, POST  | /agent/dashboad2                  | Book a site visit (same as above)           | JSON/HTML            |
| GET, POST  | /agent/leads                      | Agent leads (see leads.py)                  | JSON/HTML            |
| GET        | /agent/plotdata-tables1.html      | Plot data table page                        | HTML                 |

---

For more details on the request/response structure of `/agent/book-visit` and `/agent/leads`, refer to the implementation in `booking.py` and `leads.py` respectively.