## Block B 
**Prompt:**I have 8 dataset rows. Statuses: matched, no_positive, unmatched,
no_box, no_generator_result, outside_window.
A row is trainable only when status is matched or no_positive.
List the trainable ids and say which rejected row is the easiest
to "rescue" by mistake. Here is the table:

| id | source_id | timestamp | status | label |
| 1 | srcA | 0.5 | matched | active |
| 2 | srcA | 1.0 | no_positive | none |
| 3 | srcA | 1.5 | unmatched | active |
| 4 | srcA | 2.0 | no_box | active |
| 5 | srcB | 0.5 | matched | passive |
| 6 | srcB | 1.0 | outside_window | passive |
| 7 | srcB | 1.5 | no_generator_result | unknown |
| 8 | srcB | 2.0 | no_positive | none |

**Reply I got:**
Trainable IDs: `1, 2, 5, 8`

A row is trainable only if its status is `matched` or `no_positive`.

Rejected rows:

| ID | Status              | Rejected because                |
| -- | ------------------- | ------------------------------- |
| 3  | unmatched           | No matching result              |
| 4  | no_box              | No bounding box                 |
| 6  | outside_window      | Outside the allowed time window |
| 7  | no_generator_result | No generator output             |

Easiest to rescue by mistake: ID 3 (`unmatched`).

Why? It has label `active`, which might tempt someone to include it as a positive training example. But `unmatched` does not mean a valid match was found. Its label alone does not make it trainable.

Key distinction: `no_positive` is trainable (a valid negative example), whereas `unmatched` is rejected (matching was unsuccessful).

**My verdict:** The reply is Strong


## TASK 4 
**Prompt:** 
Here is my manifest row: id, source_id, timestamp, status, label, trainable.
Statuses that set trainable true are only matched and no_positive.
What single field is missing if two cameras recorded the same match?
Reply in 5 lines.

**Reply I accepted:** The missing field is `camera_id`.\
It uniquely identifies which camera recorded each match.\
`source_id` identifies the data source, not necessarily the camera.\
Both cameras can share the same match ID.\
Add `camera_id` to distinguish their recordings.