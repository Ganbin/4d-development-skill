# 4D Modern Development

Modern 4D development patterns: ORDA, classes, entity methods, and contemporary architecture.

## Class System

### Basic Class Structure

```4d
// File: Classes/Person.4dm
Class constructor($firstName : Text; $lastName : Text)
    This.firstName := $firstName
    This.lastName := $lastName

// Computed properties
Function get fullName() : Text
    return This.firstName + " " + This.lastName

Function set fullName($name : Text)
    $parts := Split string($name; " ")
    This.firstName := $parts[0]
    This.lastName := $parts[1]

// Instance methods
Function greet($greeting : Text) : Text
    return $greeting + ", " + This.fullName
```

### Inheritance & Singletons

```4d
// Inheritance
Class extends Person
Class constructor($firstName : Text; $lastName : Text; $role : Text)
    Super($firstName; $lastName)
    This.role := $role

// Singleton (shared across app)
singleton Class constructor()
    This.settings := New object

// Shared singleton (thread-safe) - v20 R5+
shared singleton Class constructor()
    This.cache := New shared object
```

## ORDA Entity Patterns

### Entity Class Methods

```4d
// File: Classes/PROJ_TIMERSEntity.4dm
Class extends Entity

// Constants as computed properties
Function get STATUS_RUNNING() : Text
    return "running"

// Business logic methods
Function startTimer() -> $result : Object
    $result := New object("success"; False)
    If (This.status = "stopped")
        This.status := This.STATUS_RUNNING
        This.startedAt := Current time
        This.save()
        $result.success := True
    End if
    return $result

// Computed properties
Function get isActive() : Boolean
    return (This.status = This.STATUS_RUNNING) | (This.status = "paused")
```

### DataClass Methods (Factory & Queries)

```4d
// File: Classes/PROJ_TIMERS.4dm
Class extends DataClass

// Query methods
Function getActiveTimersForUser($userId : Integer) -> $timers : cs.PROJ_TIMERSSelection
    return This.query("userId = :1 AND status IN :2"; $userId; New collection("running"; "paused"))

// Factory methods
Function createTimerForProject($userId : Integer; $projectId : Integer) -> $timer : cs.PROJ_TIMERSEntity
    $timer := This.new()
    $timer.userId := $userId
    $timer.projectId := $projectId
    $timer.status := "stopped"
    $timer.save()
    return $timer
```

### EntitySelection Methods

```4d
// File: Classes/PROJ_TIMERSSelection.4dm
Class extends EntitySelection

Function toAPIFormat() -> $result : Collection
    $result := New collection
    For each ($timer; This)
        $result.push(New object("id"; $timer.id; "status"; $timer.status; "isActive"; $timer.isActive))
    End for each
    return $result

Function getTotalDuration() -> $total : Integer
    For each ($timer; This)
        $total += $timer.totalSeconds
    End for each
```

## Modern API Architecture (Thin Layer)

### TSAPI Method Pattern

```4d
// File: Methods/TSAPI_timer.4dm
#DECLARE() -> $result : cs.TSAPI_callbackResult
$result := cs.TSAPI_callbackResult.new()
$result.statusCode := 200

// Delegate business logic to dataclass methods
Case of
    : (webRequest.request.method = "GET")
        $timers := ds.PROJ_TIMERS.getActiveTimersForUser(Session.storage.user.id)
        $result.data := $timers.toAPIFormat()

    : (webRequest.request.method = "POST")
        $data := webRequest.request.data
        $timer := ds.PROJ_TIMERS.createTimerForProject(Session.storage.user.id; $data.projectId)
        $result.data := $timer.toObject("id,status,projectId")

    : (webRequest.request.method = "PATCH")
        $timer := ds.PROJ_TIMERS.get(webRequest.request.parameters.id)
        $actionResult := $timer.startTimer()  // Entity method
        $result.data := $actionResult
End case

return $result
```

## Shared Objects & Storage

### Application State Management

```4d
// Initialize in On Startup
Use (Storage)
    Storage.app := New shared object("config"; New shared object; "cache"; New shared object)
End use

// Configuration methods
Function setGlobalConfig($key : Text; $value : Variant)
    Use (Storage.app.config)
        Storage.app.config[$key] := $value
    End use

// Caching with loader pattern
Function getCachedData($key : Text; $loader : Object) -> $data : Variant
    Use (Storage.app.cache)
        $data := Storage.app.cache[$key]
        If ($data = Null)
            $data := $loader.call()
            Storage.app.cache[$key] := $data
        End if
    End use
```

## Modern Error Handling

### Service Method Pattern

```4d
Function createProject($data : Object) -> $result : Object
    $result := New object("success"; False)

    Try
        If (This._validateProjectData($data))
            $project := ds.Projects.new()
            $project.fromObject($data)
            $project.created := Current time

            $saveResult := $project.save()
            If ($saveResult.success)
                $result.success := True
                $result.project := $project.toObject("id,name,status")
            Else
                $result.errors := $saveResult.errors
            End if
        Else
            $result.error := "Invalid project data"
        End if

    Catch
        $result.error := "Unexpected error"
        $result.details := Last errors
    End try

    return $result

Function _validateProjectData($data : Object) -> $valid : Boolean
    return ($data # Null) & ($data.name # "") & ($data.clientId # Null)
```

### Try Function for Safety (v20 R4+)

```4d
// Safe property access with defaults
$userName := Try($user.name; "Anonymous")
$userEmail := Try($user.contact.email; "no-email@domain.com")
$permissions := Try($user.getPermissions(); New collection)

// Safe calculations
$average := Try($total / $count; 0)  // Avoid division by zero
$percentage := Try(($value / $total) * 100; 0)
```

## Design Patterns

### Repository Pattern

```4d
// File: Classes/UserRepository.4dm
Class constructor($datastore : Object)
    This.ds := $datastore

Function findByEmail($email : Text) -> $user : cs.USERSEntity
    return This.ds.Users.query("email = :1"; $email).first()

Function createUser($data : Object) -> $result : Object
    $result := New object("success"; False)
    Try
        $user := This.ds.Users.new()
        $user.fromObject($data)
        $user.created := Current time
        $saveResult := $user.save()
        $result := New object("success"; $saveResult.success; "user"; $user)
    Catch
        $result.error := "Creation failed"
    End try
    return $result
```

## Best Practices

1. **Business Logic in Classes**: Entity/DataClass methods, not separate project methods
2. **Thin API Layer**: TSAPI methods delegate to dataclass methods
3. **Shared Objects**: Replace interprocess variables with Storage
4. **Try/Catch**: Modern error handling over ON ERR CALL (v20 R5+)
5. **Entity Methods**: Record-specific operations (startTimer, validate)
6. **DataClass Methods**: Queries and factory methods (getActiveUsers, createUser)
7. **EntitySelection Methods**: Collection operations (toAPIFormat, getTotalDuration)
8. **Computed Properties**: Use getters/setters for calculated values
9. **Design Patterns**: Repository, singleton, dependency injection where appropriate
10. **Type Safety**: Always declare parameter and return types
