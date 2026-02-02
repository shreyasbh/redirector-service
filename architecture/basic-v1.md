### Create Short URL

**Purpose** 
Creates a new shortened URL that maps to an existing destination URL 

**Endpoint** 
POST /short-urls 


### Request

**Body** 
- source_url (string, required)
  Destination URL to which requests will be redirected 
- shortened_url (string, required)
  Custom short URL identifier provided by the creator 

--- 

### Response

### Success

- Status: 200 OK 
- Body:
  - shortened_url (string)
  - source_url (string)
  - creation_timestamp (timestamp)

### Client Errors
- Status: 4XX
  - Shortened URL already exists 
  - Invalid source URL format 

### Server Errors

- Status: 5XX
  - Internal Server Error

### Behavioural Guarantees
- Shortened URLs are unique 
- If a shortened URL already exists, creation fails 
- Created mappings are immutable 

## Consumer Interface

### Redirect Behavior

**Purpose**  
Redirects incoming requests from a shortened URL to the corresponding destination URL.

---

### Behavior

#### Valid Shortened URL
- Client receives a redirection response.
- Request is redirected to the destination (source) URL.

#### Unknown Shortened URL
- Client receives a 404 Not Found response.
- Request is routed to a standard backend error handler.

#### Malformed Request
- Client receives a 4XX client error response.

---

### Guarantees
- Redirect behavior is deterministic.
- No best-effort or partial redirects are attempted.


## Data Model 

### Entity: Short URL

**Fields** 
- shortened_url (string, immutable)
- source_url (string, immutable)
- created_at (timestamp)

**Constraints** 
- shortened_url cannot be updated after creation 
- source_url cannot be updated after creation 





