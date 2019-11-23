# QBRrecords

This project reads CSV files that have an archive of yearly Total QBR records from 2004 to 2017 and answers the following questions:

1. Which player (in which game) had the highest total_QBR in a loss? What was the value?

2. Which player (in which game) had the lowesttotal_QBR in a win? What was the value?

3. Which player (in which game) had the highest number of action_plays?

4. The player with the highest average total_QBR

In order to answer these questions, I aggregate all CSV files into objects I create. I define two classes. The first class is "Player" that has player id, first name, last name and team name. The second class is "Game" that has number of action plays, game id, home or away, opponent, totalQBR, win or lost and player id. By executing the Python script "main.py", the answers of these four questions will be printed out.
