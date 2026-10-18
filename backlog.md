# Backlog

Requirements gathered from the client meeting on 22-09-2026 (see [team_history](team_history/22-09-2026.md)).

## Requirements

- Store text as key:value pairs, plain text only
- Each department uses its own database
- Handle billions of records (imported from an Excel file)
- Prioritize speed, even with a lot of data
- Support special characters and every kind of text (Chinese, Russian, etc.)
- Data size can go from a single character to something encrypted
- Different permissions per user
- Deletion is permanent, no soft deletes
- Desirable: timestamps and who added each record

Example record: `age : 15`

## Planned changes

| Change | Requirements covered |
| --- | --- |
| Access control | Different permissions |
| Greater data scalability | Billions of records, speed |
| UTF-32 support | Special characters, every kind of text |
| Traceability of data and operations | Timestamps, who added each record |
