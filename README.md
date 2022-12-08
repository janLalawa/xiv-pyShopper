# XIV-PyShopper
** A tool to help you buy housing items in Final Fantasy 14 **
A'shii Triglav (Raiden - Light)

---
## What does this tool do and why?

xiv-pyshopper was created to solve the issue of having to hop around worlds dozens of times when designing a new house or apartment in Final Fantasy 14. Typically you will use Universalis to search for an item, go and buy it, then search for the next and hop worlds to get it. This can take hours to do when you have 400 items to buy!

This tool simply queries the [Universalis API](https://docs.universalis.app/) for all of the furniture you have in your [Makeplace](https://makeplace.app/) JSON save file. It then returns a human readable list telling you to go and buy this stuff on the worlds you like.

---
## What CAN it do?

- Produce a shopping list from a Makeplace save.json file
- Query any particular world, datacentre, or even region depending on how far you want to travel for furniture
- Tell you what it couldn't find on the market so you can go get that from the Gold Saucer, Doman Restoration, cash shop etc.

---
## What CAN'T it do?

There are some limitations to xiv-pyshopper. This is mostly because I don't have that much time to work on the project and I am not sure how useful it is. If people really want these features then I can look at building them or am happy to look at pull requests from other devs. Reach out to me on Discord! Laura#1479

- It cannot get you the list of dyes that you need (yet, dev laziness)
- It cannot get you the list of flooring/wallpaper/lighting items (also because I am lazy)
- It does not have a UI or CLI currently. This is just a simple python script right now :)
- It doesn't check for errors as well as production code should.
- It does not accept any file formats other than a Makeplace save JSON!

Most of these are because I hacked it together, achieved my goal, and sort of relaxed. Please do say if there is a great need to expand on this and I can help.

---
## So how do I use xiv-pyshopper now?

It's quite simple, actually. Here is a step by step guide to get you going from zero

For starters, you need to have your house design saved as a JSON from [Makeplace](https://makeplace.app/). Those are found in MakePlace/MakePlace/Save. Positioning doesn't matter at all so you can just throw items on the ground and save it if you like.

1. Install [Python](https://www.python.org/downloads/) on your computer. It might be installed already, if so then head to a terminal and run `python --version` to check
2. Once you are sure Python is installed and ready to go, head to the releases tab in Github (or download main.py) and grab a copy of the script.
3. Open up the script in any text editor. I recommend [VSCode](https://code.visualstudio.com/) for devs but you can use something like [Notepad++](https://notepad-plus-plus.org/downloads/), Vim, or even regular Notepad if you like.
4. At the top of the file you will see the following: `DATACENTRE_REGION = 'Light'   MAKEPLACE_JSON = 'Save1.json'`
5. Edit the strings for Light and Save1.json to point to your datacentre, region, or world, and your save. You should drop this save into the same directory as main.py!
6. If you don't have it already. Run the command `pip install requests` to grab the API requests library for Python. If you don't have pip installed then check out [this post](https://pip.pypa.io/en/stable/installation/)
7. Go back to your terminal and run either `python main.py` or `python3 main.py` 
8. The script should now print you out a shopping list like below.

* If the talk of using a terminal on your PC is scary, don't be afraid! It's easy to use and you just need to follow the steps above. If you are Windows, grab yourself Windows Terminal instead of command prompt. It's very nice :) 


---
## Help, there was an error! What do I do?

First things first, READ the error and see what it is telling you. You might have not have the requests module installed for Python, for example and it is telling you this. In this case just go install the module.

Other kinds of errors that can break the script might be:

- Malformed JSON (Go and make a new save in MakePlace. I have an example file on this repo called SaveMeiya.JSON which should match the format)
- Universalis API is broken in some way. There is nothing I can do here. This kills the functionality entirely.
- Everything is displying as not found on market. This is another issue that would indicate a problem with the API. You might, however, just not be able to find those objects on that world. This can happen if you search a single world for items or have dozens of cash shop items.

---
 ## How does it work?

 The general idea of this script is that it follows the following steps:

 1. Build up the list of items wanted and know how many there are of each
 2. Find the largest quantity of any one item
 3. Query the Universalis API with a list of all your itemIDs and the quantity set to the max number you want
 4. The format for the call is: `universalis_query = 'https://universalis.app/api/v2/{location}/{item_list}?listings={listings}&entries=0'`
 5. From this response it begins to check where the cheapest items are found and builds a `price_list` and `world_list` for each `Item` object (representing each unique furniture item)
 6. It now builds a set of `World` objects for each world where prices were found. It populates lists on those objects full of item names and prices.
 7. This data is then used to present back to the use a neat shopping list per world as well as rough prices.

It has been refactored a little since by my good friend Thelamos, but that's the gist.

---
## What does the output look like?

It's pretty self explanatory. You'll get a shopping list like this if all things go well. I coloured it below becuase it looks nice :D

```python

Your shopping list for Shiva will cost approx. 4,454,905 gil
------------------------
19x Stage Panel
1x Hingan Cupboard
2x Zabuton Cushion
6x Wood Slat Partition
1x Hingan Andon Lamp
2x Hingan Bench
1x Verdant Partition
1x Hingan Pillar
3x Hingan Chochin Lantern
1x Potted Spider Plant
1x Kotetsu Replica
1x Low Bookshelf
------------------------
 
Your shopping list for Raiden will cost approx. 389,475 gil
------------------------
1x Wooden Blinds
3x White Screen
5x Mounted Bookshelf
4x Wall Planter
2x Mounted Box Shelf
2x Staggered Shelf
1x Hingan Desk
1x Open Partition
------------------------
 
Your shopping list for Phoenix will cost approx. 1,123,682 gil
------------------------
2x Tier 4 Aquarium
1x Hingan Cupboard
6x Combed Wool Rug
6x Wall Planter
3x Potted Dragon Tree
13x Wooden Handrail
1x Oriental Altar
1x Hingan Windowed Partition
7x Verdant Partition
1x Crystal Bell
------------------------
 
Your shopping list for Zodiark will cost approx. 551,848 gil
------------------------
11x Hingan Sideboard
4x Flooring Mat
5x White Partition
4x Mounted Box Shelf
6x Hingan Andon Lamp
4x Paper Partition
1x Summoning Bell
1x Hingan Armor Display
1x Oriental Dressing Case
2x Imitation Square Window
1x Oriental Round Table
1x Suzaku Wall Hanging
------------------------
 
Your shopping list for Lich will cost approx. 1,667,065 gil
------------------------
12x White Rectangular Partition
1x Mahogany Aqueduct
8x Flooring Mat
2x Azim Steppe Phasmascape
4x Hingan Cupboard
3x White Screen
5x Oasis Stall
2x Troupe Stage
4x Fool's Portal
2x Hingan Andon Lamp
1x Indoor Oriental Waterfall
3x Hingan Open-shelf Bookcase
2x Eastern Indoor Pond
1x Message Book Stand
------------------------
 
Your shopping list for Odin will cost approx. 2,222,686 gil
------------------------
2x White Rectangular Partition
6x Mahogany Aqueduct
5x Wooden Steps
5x Oasis Stall
2x Potted Oliphant's Ear
1x Staggered Shelf
1x Eastern Indoor Pond
3x Bamboo Planter
------------------------
 
Your shopping list for Alpha will cost approx. 3,743,070 gil
------------------------
4x Hingan Sideboard
6x Leather Sofa
10x White Partition
5x Glade Lantern
1x Verdant Partition
2x Hokonin Permit
2x Hingan Pillar
------------------------
 
Your shopping list for Twintania will cost approx. 486,705 gil
------------------------
5x Wooden Blinds
2x Manor Fireplace
3x Hingan Andon Lamp
2x Oriental Breakfast
4x Indoor Oriental Waterfall
2x Bamboo Planter
1x Ruby Sea Phasmascape
1x Hingan Chochin Lantern
1x Oriental Wall Scroll
1x Imitation Wooden Skylight
------------------------
 
This shopping list was created at 08/12/2022 00:59:33
Total Cost: 10,965,509 gil
Items found on {'Shiva', 'Raiden', 'Phoenix', 'Zodiark', 'Lich', 'Odin', 'Alpha', 'Twintania'}

Could not find these items on the market. Perhaps they are cash shop or not sellable?
1x Four Lords
23x Fool's Threshold
4x Doman Dogwood
3x Il Mheg Flower Lamp
2x Sake Set

Thank you for shopping with us today!
```