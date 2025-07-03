# API Documentation: `/test` Endpoint

## Endpoint

`/test`

## Methods Supported
- `GET`
- `POST`

---

## POST `/test`

### Description
Handles test requests for both JSON and multipart form data. Used for testing data reception and file uploads.

### Request Content Types
- `application/json`
- `multipart/form-data`

### Request Body
#### For `application/json`
- Send a JSON object in the request body.

#### For `multipart/form-data`
- Send a file field named `data` containing a JSON blob.
- Additional files and form fields can be included.

### Example Requests
#### JSON Example
```http
POST /test HTTP/1.1
Content-Type: application/json

{
  "key": "value"
}
```

#### Multipart Example
```
POST /test HTTP/1.1
Content-Type: multipart/form-data; boundary=... (auto-generated)

--boundary
Content-Disposition: form-data; name="data"; filename="data.json"
Content-Type: application/json

{"key": "value"}
--boundary--
```

### Responses
- **On JSON POST:**
  - setting this as errors response to test error handling for front end
  - Status: `500 Internal Server Error`
  - Body:
    ```json
    {
      "status": "error",
      "message": "data received"
    }
    ```
- **On Multipart POST:**
  - Status: `200 OK` (if handled further in code)
  - Body: (Not fully shown in code, but prints files and form fields)

---

## GET `/test`

### Description
No specific logic is shown for GET requests in the provided code. Typically used for testing endpoint availability.

### Response
- Status: `200 OK` (if implemented)
- Body: (Not specified)

---

## Notes
- The endpoint prints received data to the server logs for debugging.
- The endpoint is intended for development/testing purposes only.
- Error handling and response codes may be adjusted as needed.
- The endpoint is accessible at:
  - `https://con.qbits4dev.com/test`
  - `http://124.123.27.63/test`
- The JSON request/response structure can be extended as per requirements.

---

## Changelog
- **2025-07-03:** Initial documentation created for `/test` endpoint.