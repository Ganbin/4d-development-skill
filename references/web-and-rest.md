# Web Server & REST API Reference

> Curated reference for 4D v21. For full documentation, see pointed files in docs/.

## Table of Contents

1. [Web Server Overview](#1-web-server-overview)
2. [HTTP Request Handling](#2-http-request-handling)
3. [HTTP Request Handler (Modern v21)](#3-http-request-handler-modern-v21)
4. [REST API](#4-rest-api)
5. [REST CRUD Operations](#5-rest-crud-operations)
6. [Sessions](#6-sessions)
7. [Authentication](#7-authentication)
8. [HTTPS / TLS](#8-https--tls)
9. [HTTPRequest Class (Outbound)](#9-httprequest-class-outbound)
10. [Exposed Functions via REST](#10-exposed-functions-via-rest)
11. [Go Deeper](#11-go-deeper)

---

## 1. Web Server Overview

The `WEB Server` command returns a `4D.WebServer` object to start, configure, and stop the server.

```4d
var $s:=New object("HTTPPort"; 8080; "HTTPSEnabled"; True; "scalableSession"; True)
WEB Server.start($s)
// WEB Server.stop()   WEB Server.isRunning
```

Key properties: `.HTTPPort`, `.HTTPSPort`, `.HTTPSEnabled`, `.isRunning`, `.scalableSession`, `.certificateFolder`, `.rootFolder`, `.maxConcurrentProcesses`, `.handlers`, `.HSTSEnabled`.

> Source: `docs/WebServer/webServer.md`, `docs/API/WebServerClass.md`

---

## 2. HTTP Request Handling

### On Web Connection

Called when the server receives a URL that is not a static page, custom handler, or `/rest/` request. Must be accepted by `On Web Authentication` first.

```4d
// On Web Connection database method
#DECLARE ($url : Text; $header : Text; \
  $BrowserIP : Text; $ServerIP : Text; \
  $user : Text; $password : Text)
Case of
    : ($url="/api/clients")
        WEB SEND FILE("clients.html")
    Else
        WEB SEND TEXT("{\"error\":\"not found\"}"; "application/json")
End case
```

### /4DACTION URLs

Calls a project method directly (must have "Available through 4D tags and URLs" enabled).

```html
<FORM ACTION="/4DACTION/processForm" METHOD=POST>
    <INPUT TYPE=TEXT NAME=userName VALUE="">
    <INPUT TYPE=SUBMIT NAME=OK VALUE="Submit">
</FORM>
```

```4d
// processForm method
#DECLARE ($url : Text)
ARRAY TEXT($names; 0)
ARRAY TEXT($vals; 0)
WEB GET VARIABLES($names; $vals)
```

> Source: `docs/WebServer/httpRequests.md`

---

## 3. HTTP Request Handler (Modern v21)

Custom handlers intercept URL patterns directly -- bypassing `On Web Authentication` and `On Web Connection`. Use `4D.IncomingMessage` / `4D.OutgoingMessage`.

### HTTPHandlers.json (in `Project/Sources/`)

```json
[
    {
        "class": "ApiHandler",
        "method": "handleUsers",
        "pattern": "api/users",
        "verbs": "GET, POST"
    },
    {
        "class": "ApiHandler",
        "method": "handleInvoice",
        "regexPattern": "/api/invoices/(\\d+)",
        "verbs": "GET"
    }
]
```

Rules: **class** must be a shared singleton. Use `pattern` (prefix) or `regexPattern` (regex), not both. First match wins. Forbidden: `/4DACTION`, `/rest`, `/$lib/renderer`, `/$shared`.

### Handler Implementation

```4d
shared singleton Class constructor()

Function handleUsers($req : 4D.IncomingMessage) : 4D.OutgoingMessage
    var $resp:=4D.OutgoingMessage.new()
    If ($req.verb="GET")
        $resp.setBody(JSON Stringify(ds.Users.all().toCollection("name,email")))
    Else  // POST
        var $data:=JSON Parse($req.getText())
        $resp.setBody("{\"status\":\"created\"}")
        $resp.setStatus(201)
    End if
    $resp.setHeader("Content-Type"; "application/json")
    return $resp
```

**IncomingMessage**: `.url`, `.urlPath` (collection), `.urlQuery` (object), `.verb`, `.headers`, `.getText()`, `.getBlob()`, `.getPicture()`.
**OutgoingMessage**: `.setBody()`, `.setHeader()`, `.setStatus()`.

> Source: `docs/WebServer/http-request-handler.md`, `docs/API/IncomingMessageClass.md`, `docs/API/OutgoingMessageClass.md`

---

## 4. REST API

### Enabling

Settings > Web > Web Features > check **Expose as REST server**. Requires the web server to be running. Restart the application after changes.

By default all tables/fields are exposed. To hide a table or field, uncheck **Expose as REST resource** in the Structure editor.

All REST URLs start with `/rest/`:
```
/rest/{dataClass}              -- all entities
/rest/{dataClass}({key})       -- single entity
/rest/$catalog                 -- list dataclasses
```

> Source: `docs/REST/configuration.md`, `docs/REST/gettingStarted.md`

---

## 5. REST CRUD Operations

### $filter -- Query
```
GET /rest/Employee?$filter="salary>50000"
GET /rest/Employee?$filter="lastName begin j"
GET /rest/Employee?$filter="salary>20000 AND employer.name!=acme"
GET /rest/Employee?$filter="firstName=:1 AND salary>:2"&$params='["john",20000]'
```
Comparators: `=`, `!=`, `>`, `>=`, `<`, `<=`, `begin`.

### $orderby -- Sort
```
GET /rest/Employee?$filter="salary!=0"&$orderby="salary DESC,lastName ASC"
```

### $attributes -- Select Fields / Expand Relations
```
GET /rest/Employee?$attributes=firstName,lastName
GET /rest/Employee(1)?$attributes=employer.name
GET /rest/Company(1)?$attributes=employees.*
GET /rest/Company(1)?$attributes=employees.lastname,employees.jobname
```

### $expand -- Images and BLOBs
```
GET /rest/Employee(1)/photo?$imageformat=best&$expand=photo
```
> For relations, prefer `$attributes` over `$expand` (kept for compatibility).

### $catalog
```
GET /rest/$catalog           -- list dataclasses
GET /rest/$catalog/$all      -- all dataclasses with attributes
GET /rest/$catalog/Employee  -- single dataclass structure
```

### $method=update -- Create / Update (POST)
```
POST /rest/Employee?$method=update
```
Create (no __KEY): `{"firstName":"John","lastName":"Smith"}`
Update: `{"__KEY":"340","__STAMP":2,"firstName":"Pete"}`
Batch: send a JSON array of objects.

### $method=delete -- Delete (POST)
```
POST /rest/Employee(22)?$method=delete
POST /rest/Employee?$filter="ID=11"&$method=delete
```

### $method=entityset -- Server-Side Cache
```
GET /rest/Employee?$filter="salary>40000"&$method=entityset&$timeout=600
GET /rest/Employee/$entityset/{id}?$method=release
```

### Other Parameters

`$top`/`$limit` (limit rows), `$skip` (pagination), `$compute` (aggregates), `$distinct` (unique values), `$timeout` (entity set TTL in seconds).

> Source: `docs/REST/$filter.md`, `docs/REST/$orderby.md`, `docs/REST/$attributes.md`, `docs/REST/$method.md`

---

## 6. Sessions

### Enabling Scalable Sessions

Default in new projects. Enable via Settings or programmatically with `.scalableSession:=True`.

Cookie `4DSID_AppName` identifies the session. Default idle timeout: 60 min.

### Session Object

```4d
Session.id                     // unique ID
Session.isGuest()              // true if no privileges
Session.setPrivileges("admin") // assign privilege + consume license
Session.hasPrivilege("admin")  // check privilege
Session.clearPrivileges()      // revoke all
Session.userName               // current user
Session.idleTimeout            // timeout in minutes (min 60)
```

### Session Storage (Shared Object)

```4d
Use (Session.storage)
    Session.storage.cart:=New shared collection()
    Session.storage.cart.push(New shared object("productId"; 42; "qty"; 2))
End use
```

### OTP Tokens (Third-Party Callbacks)

Generate a one-time token, include it in a callback URL. When called back, the original session is automatically restored via `$4DSID` parameter:

```4d
$token:=Session.createOTP()
$callbackURL:="https://myapp.com/validate?$4DSID="+$token
```

Or restore manually: `Session.restore($req.urlQuery.state)`

> Source: `docs/WebServer/sessions.md`, `docs/API/SessionClass.md`

---

## 7. Authentication

### REST -- Force Login Mode (Recommended)

1. Guest session created on first REST call (no license, only `$catalog` and `authentify` allowed).
2. Client calls `POST /rest/$catalog/authentify` with credentials.
3. `authentify()` validates and calls `Session.setPrivileges()` -- license consumed, full access granted.

```4d
// DataStore class
Class extends DataStoreImplementation

exposed Function authentify($cred : Object) : Text
    var $user:=ds.Users.query("name=:1"; $cred.name).first()
    If ($user#Null)
        If (Verify password hash($cred.password; $user.password))
            Session.setPrivileges("vip")
        Else
            return "Wrong password"
        End if
    Else
        return "Wrong user"
    End if
```

### Web -- On Web Authentication

```4d
#DECLARE ($url : Text; $content : Text; \
  $IPClient : Text; $IPServer : Text; \
  $user : Text; $password : Text) -> $accept : Boolean
$accept:=False
var $found:=ds.WebUser.query("User===:1"; $user)
If ($found.length=1)
    $accept:=Verify password hash($password; $found.first().password)
End if
```

Authentication modes (Settings): **Custom** (default, developer handles), **Basic** (browser dialog, needs HTTPS), **Digest** (hashed, use `WEB Validate digest`).

> Source: `docs/REST/authUsers.md`, `docs/WebServer/authentication.md`

---

## 8. HTTPS / TLS

```4d
var $s:=New object(\
    "HTTPSEnabled"; True; "HTTPSPort"; 443; \
    "certificateFolder"; "/PACKAGE/certificates/"; \
    "minTLSVersion"; 4)  // 4 = TLS 1.3
WEB Server.start($s)
```

Related properties: `.HSTSEnabled`, `.HSTSMaxAge`, `.perfectForwardSecrecy`, `.openSSLVersion`, `.cipherSuite`.

> Source: `docs/API/WebServerClass.md`

---

## 9. HTTPRequest Class (Outbound)

`4D.HTTPRequest` makes outbound HTTP calls from 4D.

```4d
// Synchronous GET
var $req:=4D.HTTPRequest.new("https://api.example.com/data"; New object("method"; "GET"))
$req.wait()
If ($req.errors=Null)
    var $data:=JSON Parse($req.response.body)
End if
```

Async: pass an options object with `onResponse`/`onError` callback functions.

Key members: `.response` (`.body`, `.headers`, `.status`), `.errors`, `.wait()`, `.terminate()`, `.terminated`.

> Source: `docs/API/HTTPRequestClass.md`

---

## 10. Exposed Functions via REST

ORDA class functions with `exposed` keyword are callable via REST POST. Add `onHTTPGet` to allow GET.

| Scope | URL Pattern |
|---|---|
| Datastore | `POST /rest/$catalog/functionName` |
| DataClass | `POST /rest/{dataClass}/functionName` |
| Entity | `POST /rest/{dataClass}(key)/functionName` |
| EntitySelection | `POST /rest/{dataClass}/functionName?$filter=...` |
| Singleton | `POST /rest/$singleton/ClassName/functionName` |

```4d
// DataClass -- POST /rest/City/getCity  body: ["Aguada"]
Class extends DataClass
exposed Function getCity($name : Text) : cs.CityEntity
    return This.query("name=:1"; $name).first()

// Entity -- POST /rest/City(2)/getPopulation
Class extends Entity
exposed Function getPopulation() : Integer
    return This.zips.sum("population")

// GET-enabled function -- GET /rest/Products/getFile?$params='[42]'
exposed onHTTPGet Function getFile($id : Integer) : 4D.OutgoingMessage
    var $r:=4D.OutgoingMessage.new()
    $r.setBody(File("/RESOURCES/doc_"+String($id)+".pdf").getContent())
    $r.setHeader("Content-Type"; "application/pdf")
    return $r
```

Parameters: **POST** body as JSON array `["val1","val2"]`. **GET** via `?$params='["val1"]'`.
Entity params: `{"__DATACLASS":"Employee","__ENTITY":true,"__KEY":55}`.
Restrict access via `Project/Sources/roles.json` privileges.

> Source: `docs/REST/ClassFunctions.md`

---

## 11. Go Deeper

| Resource | Path |
|---|---|
| REST full index | `references/rest-index.md` |
| Web Server full index | `references/webserver-index.md` |
| API class index | `references/api-index.md` |
| ORDA patterns reference | `references/orda-modern.md` |
| WebServer docs (14 files) | `docs/WebServer/` |
| REST docs (34 files) | `docs/REST/` |
| WebServerClass API | `docs/API/WebServerClass.md` |
| HTTPRequestClass API | `docs/API/HTTPRequestClass.md` |
| SessionClass API | `docs/API/SessionClass.md` |
| IncomingMessageClass API | `docs/API/IncomingMessageClass.md` |
| OutgoingMessageClass API | `docs/API/OutgoingMessageClass.md` |
