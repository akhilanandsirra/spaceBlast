# Space Blast

Space Blast is a space-themed multidirectional shooter game created using python in **PyCharm IDE** using **Pygame** module. The player controls a single spaceship
in space field which is periodically traversed by asteroids. The object of the game is to
shoot and destroy the asteroids, while not colliding with either. The game becomes
harder as the score of game increases.

## Gameplay

<a href="https://imgur.com/GnIplqJ"><img src="https://i.imgur.com/GnIplqJ.gif" title="source: imgur.com" /></a>

## Player Movement

<a href="https://imgur.com/ZOQKRNc"><img src="https://i.imgur.com/ZOQKRNc.gif" title="source: imgur.com" /></a>

The player always faces in the cursor position.

<a href="https://imgur.com/6e2iGvl"><img src="https://i.imgur.com/6e2iGvl.gif" title="source: imgur.com" /></a>

AWSD Keys are used to move the position of the player.

## Enemy Movement

<a href="https://imgur.com/hyMCssI"><img src="https://i.imgur.com/hyMCssI.gif" title="source: imgur.com" /></a>

The Enemy Sprite by using a directional vector moves towards the player until they collide.

<a href="https://imgur.com/cRtcwGa"><img src="https://i.imgur.com/cRtcwGa.gif" title="source: imgur.com" /></a>

If Player changes position the directional vector is normalized and recalculated to follow the enemy.

## Collision/Animation

<a href="https://imgur.com/t4YvBmt"><img src="https://i.imgur.com/t4YvBmt.gif" title="source: imgur.com" /></a>

Collision of Player Sprite with Enemy Sprite.

<a href="https://imgur.com/1inbCb1"><img src="https://i.imgur.com/1inbCb1.gif" title="source: imgur.com" /></a>

Collision of Enemy Sprite with Bullet.
