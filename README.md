# **Tic Tac Tie API**
API of the game Tic Tac Toe for two players with a leader board and seasoning.
### Data storing
For storing data used SQLite. As there is no JSON field in SQLite database for storing board schema used Text field
where the matrix in json format is stored. For databases such as PostgreSQL JSON field should be used instead of Text
field.
### CRON jobs
To start a new game league a cron job should be used that should run each week or each month. As a script for cron job
should be used script /app/user/start_league.py which bulk updates `user_rate` table and set all rates to zero.