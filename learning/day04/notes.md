**Sentence to remember:** Never use accuracy alone as the 
shipping score for an imbalanced classification problem.


1 - when we use frame shuffle the same source can show up in both train and validation sets which are near duplicates 

2 -42 makes sure each time the shuffle is carried out it gives the same result but it can not guarantee if the results are useful or correct

3 accuracy is misleading when there is a class imbalance it can classify all classses to one majority class and still end up having good percentage

4 - Correct, Missed, Wrong instance, False positive