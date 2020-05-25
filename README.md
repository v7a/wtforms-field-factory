# wtforms field factory
Create fields on-the-fly at form construction time.

## Why?
In order to e.g. translate field labels depending on the request without relying on global state.
Additionally, you can conditionally exclude fields. This avoids dodgy workarounds needed when e.g.
having a form field that is not relevant or feasible to pass for testing.

## How?
TBD
