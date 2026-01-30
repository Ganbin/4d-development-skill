## 4D Code Review Guidelines

Here are some remarks after some of your review using 4d-skill so those are user reviewd rules and must be taken into account when writing or reviewing code.

- **TRACE command**: Not critical - compiled 4D code ignores TRACE. Worth noting but not a blocker.
- **Nested transactions**: Perfectly valid pattern in 4D. Each function manages its own transaction internally (closure principle). The inner function returns a result; the caller handles its own transaction based on that result. Inner functions don't need to know if the caller has a transaction.

- **`local` keyword in ORDA**: Does NOT mean "private to class". It controls execution context in client/server:
  - `local` = executes on client process
  - Without `local` = executes on server in preemptive (thread-safe) mode with isolated variable context
  - Choose based on thread-safety requirements and where data access is needed.