# Dawn-of-Thunder-

Dawn of Thunder is a turn based strategy game created as a school project using Qt4 and python. It is inspired by games called Civilization and Travian web browser game. The basic idea of the game is to gather resources, construct buildings, train different kind of troops and to ultimately destroy the enemy. 

Every turn each player has a certain number of moves and attacks, meaning a player can only move and attack with a fixed number of troops each turn. Training troops and constructing buildings takes a fixed number of turns depending on the troop/building. For example training an archer only takes 2 turns when training a knight takes 4. When the player is done with his turn, he can pass the turn to the other player.


There are 4 kinds of resources gold, wood, iron and food. Every building and troop will cost a certain amount of each resource. Each building and troop has its own functionality. Each resource has its own building to increase the income of that resource: 

---Mine increases iron income (can only be built in mountains)

---Farm increases food income (can only be built in an open area 

---Lumbermill increases wood income (can only be built in a forest) 

---Market increases gold income (can only be built in an open area).

In addition to the commercial buildings the player is also able to build a barracks (for training troops) and capital buildings (a player may only construct other buildings near these structures).

There are many kinds of troops in the game:

  ---Archer    (ranged) cheap and easy to train, weak if not protected.
  
  ---Swordman  (melee) also cheap but vunerable to ranged attacks.
  
  ---Pikeman   (melee) very effective against knights.
  
  ---Knight    (melee) expensive but fast and powerful.
  
  ---Catapult  (ranged)  specializes in destroying buildings, very weak against melee.

For each game, the game creates a random map consisting of varying terrain (open areas, mountains, lakes, forests).
