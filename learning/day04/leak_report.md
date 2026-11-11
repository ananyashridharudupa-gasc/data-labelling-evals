****Validation frames:**

 "val_frames": [
    "src02-f01",
    "src00-f03",
    "src02-f02",
    "src09-f00",
    "src06-f01",
    "src06-f00"
  ],

  **Source with frames on both sides:**
src02 — f01 and f02 are in validation, but f00 and f03 
are still available for training.


**What the model could memorize:**
The model can study src02-f00 during training and get 
tested on src02-f01, which is the next frame of the same 
video — nearly identical content, so the score looks 
better than the model actually is.

