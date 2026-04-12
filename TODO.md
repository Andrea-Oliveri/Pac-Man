* Reset GhostsCoordinator.\_mode\_timer to 0 when life is lost and level is completed
* Pinky can reverse direction immediately at start of level to exit house: even though its eyes point downwards, as she gets the exiting house command immediately she can move upwards from frame 0.
  Same for the other ghosts at level 3 and above: as they get immediately the leave house command, they don't need to do a back and forth up and down before changing directions
* Life lost sound slightly delayed with respect to animation
* Try nuitka: https://api.arcade.academy/en/latest/tutorials/compiling\_with\_nuitka/index.html