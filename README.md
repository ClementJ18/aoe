# Age of Empires: Age of Kings DS Battle Simulator

A simple WIP simulator to allow a user to know the outcome of any battle ahead of time 
between any two units, with a GUI (PyQT5). This was the project I used to familiarize myself
with UI development, enums and further push my understanding of classes. The logic for
the simulations was created entirely by observing the game's battle system, comparing
the data given by the game with hundreds of battles conducted in the game under various
conditions. The simulator still has a minor margin of error of usually one or two health
points due to the reason that rounding of decimals is conducted behind the scenes.

![alt text](https://i.imgur.com/GvZcUmM.png "v1 gui")
![alt text](https://imgur.com/wop9ehF.png "current gui")

## TODO
* [x] Add the distance slider to emulate long ranged battles
* [ ] Fix remaining broken math (something to do with health percentages)
* [ ] Overall quality improvement of the code

## Possibilities
* [ ] Unit and Terrain creators
* [ ] Ability to save states
* [x] More details about battles  