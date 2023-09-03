# Evil Exyrs Discord
 The source code for my Evil Exyrs Discord Bot. This project is mainly for fun.
## Issues
   * Timer doesn't automatically stop after revealing the spy.
   * Refactoring code to have cogs instead of discord.Client().
## Features
Play SpyFall with your friends; Here is how to get started:
   * ```%spy game``` - creates a new game of spyfall in your server.
   * Emote '🕵🏻' to the bot's message to join.
   * ```%spy start``` - begins the spyfall game; This will send a private message with the player's role and map.
   * ```%spy maps``` - lists the current map collection.
   * ```%spy reveal``` - Ends the game and reveals the spy.


**note:** The bot can handle unique games of spyfall from different servers.


Maps are fully customizable, You can add fictional places from your favorite games and shows or add places that you and your friends can relate to.
 * Create a new map: **%spy mkmap** <map name\>, <role 1\>, <role 2\>...
    * **Example:** ```%spy mkmap Train, Passenger, Cashier, Train Operator, Guard```
 * Remove a map: **%spy rmmap** <map name\>
    * **Example:** ```%spy rmmap Train```

The bot supports multiple map profiles; You can categorize your collection of places if you want to.
   *  ```%spy pfnew mapcollection``` - creates a new profile with the "mapcollection" name.
   *  ```%spy pfswitch mapcollection``` - switches to the new profile.
   *  ```%spy pfswitch default``` to go back to the original profile.
   *  ```%spy pflist``` - lists the profiles in the server.
   *  ```%spy pfdel mapcollection``` - deletes the new profile.
## Screenshots
![image](https://github.com/VintanaEnf/Evil-Exyrs-Discord/assets/104513214/deaf26db-87c0-4bda-9000-21849300d1c9)
![image](https://github.com/VintanaEnf/Evil-Exyrs-Discord/assets/104513214/7fbcfa5f-8749-43ec-a16f-42ffcfa30396)
