# gammaGo
---
Simple go playing bot based on AlphaGo technology
---
File structure:

* **djgo** - Bot library
    * **agent** -  Our Bot
        * **base** - Bot main class
        * **naive** - First Bot generation (KU 30)
        * **naive_fast** - Boosted First Bot (KU 30)
        * **helpers** - Helper functions
        * **helpers_fast** - Boosted Helper functions
    * **goboard_slow** - Basic board realization
    * **goboard** - Basic board realization with hash
    * **goboard_fast** - Boosted Basic board realization with hash
    * **gotypes** - Basic types
    * **utils** - Functions to print board
* **bot_v_bot** - Simple algorithm to 2 bots game
* **human_v_bot** - Simple algorithm to player vs bot game

---
**Used materials from "Deep learning and game of GO book"** 

[Original code here](https://github.com/maxpumperla/deep_learning_and_the_game_of_go/tree/chapter_3)