# Event log notes

An event log stores one JSON object per line. Each event has a `type` string and
an ISO 8601 `timestamp`. Readers should parse each line separately. A malformed
line is an error for that line; it does not make the remaining lines invalid.
To inspect a log, identify the event type, validate those two fields, and report
the line number of any malformed record.
