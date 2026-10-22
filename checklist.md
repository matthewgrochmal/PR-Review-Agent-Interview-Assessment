# PR review checklist

Every PR is reviewed against these rules. Report a violation only when the PR's own changes break a rule.

| ID | Rule |
|---|---|
| **R1** | **No secrets.** Don't commit credentials, keys, tokens, or connection strings that contain a password or key, in source or config. Placeholders and obviously fake values in test projects are acceptable. |
| **R2** | **Parameterized SQL.** Values from users or data must be passed as SQL parameters. Never concatenate or interpolate them into SQL text. Identifiers (column or table names) chosen from a fixed allowlist in code are acceptable. |
| **R3** | **No PHI in logs.** Don't log patient identifiers or health information (name, date of birth, MRN, member ID, SSN, address, diagnosis). Log internal IDs such as ClaimId instead. This includes logging whole objects that contain PHI. |
| **R4** | **Tests.** New or changed public methods that contain logic need at least one test in the same PR that exercises them. |
| **R5** | **No swallowed exceptions.** A catch block must rethrow, or log at Warning or above and handle the failure deliberately. Catching `OperationCanceledException` to stop work is acceptable. |
| **R6** | **Async all the way.** Don't block on async code (`.Result`, `.Wait()`, `.GetAwaiter().GetResult()`). Don't use `async void` except for event handlers. |
| **R7** | **Dispose what you create.** `IDisposable` objects created in a method must be disposed (`using` statement or declaration), unless ownership is clearly handed to something else. |
