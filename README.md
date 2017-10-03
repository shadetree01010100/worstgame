The Worst Game Nobody Ever Played
---------------------------------

Eat the food until there's no more food.

```
>>> from world_02 import World
>>> w = World()
>>> w.player.closest_food()
47.38143096192854
>>> w.episode(1)
>>> w.player.closest_food()
48.28014010183533
>>> w.done()
False
```

Create an instance of `World` and get the initial distance to nearest food with `w.player.closest_food()`. Call `World.episode(x)` with `-1 <= x <= 1` to move to a new location. `World.done()` returns `True` when there is no food left or `w.episodes > World.EPISODE_LIMIT`.
