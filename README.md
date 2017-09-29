The Worst Game Nobody Ever Played
---------------------------------

Eat the food until there's no more food.

```
>>> from world_02 import World
>>> w = World()
>>> w.start_here
47.38143096192854
>>> w.episode(1)
48.28014010183533
```

Create an instance of `World` and get the initial distance to nearest food from `World.start_here`. Call `World.episode(x)` where `-1 < x < 1` to get a new distance. A return value of `None` indicates the end of the trial, either because there is no food left or `World.episodes > World.EPISODE_LIMIT`.
