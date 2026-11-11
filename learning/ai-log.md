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

## DAY 2

**Prompt :**
FPS is 30. I must ADD 0.2 seconds to an annotation timestamp
before converting to a frame index. For annotation time 1.0 seconds,
which frame index do I want, and which frame index is the bug?
Also: I set pixel channel 0 to 255 in an OpenCV image and expected red.
What color did I actually store?

**Reply:**

### 1. Timestamp to frame index

Given:

- FPS = 30
- Annotation timestamp = 1.0 seconds
- Offset = +0.2 seconds

Correct calculation:

\\[ (1.0 + 0.2) \times 30 = 36 \\]

Correct frame index: 36

Bug: If you forget to add the 0.2-second offset:

\\[ 1.0 \times 30 = 30 \\]

Buggy frame index: 30

### 2. OpenCV pixel channel

OpenCV uses BGR, not RGB, channel ordering.

- Channel 0 = Blue
- Channel 1 = Green
- Channel 2 = Red

If you set channel 0 to 255, you actually stored BLUE, not red.

For reference:

| Color | OpenCV BGR value |
| ----- | ---------------- |
| Blue  | `(255, 0, 0)`    |
| Green | `(0, 255, 0)`    |
| Red   | `(0, 0, 255)`    |

Final answers:

1. Correct frame: 36; bug: 30.
2. Actual stored color: Blue.

## Task 5 — Sign question

**Q1:** offset +0.2, annotation time 1.5s, FPS 30 → frame 51, x=51 

**Q2:** What changes if the video clock is behind?
Answer: sign flips, you subtract instead of add.
Frame = (1.5 - 0.2) × 30 = 39.

**Key takeaway:** the sign is not a rule — it depends on which 
clock is behind. Today's file says +0.2 so we add.

## Block B — Day 3

**Prompt:** Explain IoU using only boxes (0,0,2,2) and (1,1,3,3).
Compute intersection area, union area, and IoU.
Then say whether IoU threshold 0.5 matches them.
Do not switch to a different example.

**Reply verdict:** Strong — got intersection=1, union=7, 
IoU=0.143, correctly said not a match at 0.5.

## Task 4 — YOLO conversion

**Prompt:** Image is 100 by 100. xyxy box is (10, 20, 50, 60). Class id 1.
Write the YOLO line with 2 decimal places.
Then convert that line back to xyxy and show the arithmetic.

**Reply verdict:** Strong — correct YOLO line 1 0.30 0.40 0.40 0.40,
correctly recovered (10, 20, 50, 60). Round trip worked.

**Key takeaway:** YOLO stores center + size normalized, not corners.


## Block B — Day 4

**Prompt:** 16 passive, 4 active, model predicts all passive.
Give accuracy, active precision, active recall.
Which number to refuse and why?

**Reply verdict:** Strong — accuracy 0.80, recall 0, 
precision undefined. Refuse accuracy because dataset is 
imbalanced and model never finds the active player.

## Task 5 — mAP question

**Prompt:** Product question is: did we mark the correct player 
as active? mAP50-95 = 0.72. What can it tell me and what can't 
it, if the candidate box was already given?

**Reply verdict:** Strong — mAP measures box detection quality, 
not whether the correct player was selected. When the box is 
already provided, mAP mostly confirms the model agreed with 
a box it was handed.

**Sentence to reuse on Day 13:**
Do not use mAP50-95 as evidence that your product correctly 
identifies the active player — it measures detection quality, 
not the correctness of the active-player decision when the 
candidate box is already supplied.