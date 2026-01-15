# Chess_pygame
This repository was created to emulate the game of chess with pygames, a python library which can be easily installed.

# Disclaimer
This games differs a bit from normal chess.

In this version of chess a player wins when he eats the enemy king, so checkmate or checks are not implemented. It is implemented a very naive version of draw, which is when both sides have just the king left.

Also for this reason castle can be done whatever the player likes it (of course if the cells between king and rook are free and both pieces has never moved), meaning that if the cell in which the king will end after castle is under attack you can still perform the movement at your own risk.

# TO DO
- [ ] FIRST OF ALL DIVIDE AND CONQUER! IT'S ALL IN THE SAME SHITTY FILE.
- [ ] CREATE A CHESS PIECE CLASS AND ALL THE SUBCLASSES TO TAKE CARE OF PIECE MOVEMENTS
- [ ] IMPLEMENT BASIC CHESS GAMEPLAY LOOP
- [ ] IMPLEMENTS CHECKS AND CHECKMATES
- [ ] CREATE DIFFERENT SIZES TO PLAY WITH (maybe yaml file to get the configuration?)
- [ ] IMPLEMENT CHESS AI TO PLAY AGAINST (ALSO CAN CHOOSE IF YOU WANT TO PLAY WHITE OR BLACK)
- [ ] IMPLEMENT A SERVER TO PLAY AGAINST FRIENDS ONLINE
