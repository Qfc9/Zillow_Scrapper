#!/usr/bin/env python3
"""
Menu module has a menu class and a menu item class. Menus use menuItems
to construct it's output.
"""


class Menu:
    """
    Menu class to make menus. Uses the menu item class.
    """
    def __init__(self):
        """
        Initializing menu object, no arguments required
        """
        self.menuItems = []

    def addItem(self, func, label, weight):
        """
        Adding a menuItem to the Menu list
        """
        self.menuItems.append(MenuItem(func, label, weight))

    def menuChoice(self, choice, weight):
        """
        Checking if your choice is valid
        """
        print()

        # Going through every menu Item
        for item in self.menuItems:

            # Going to the next item if it's not the right weight
            if item.weight not in weight and item.weight != 0:
                continue

            # If the item is the choice
            if item.key == choice.upper():
                item.ability()
                return

        print("Please choose a valid command\n")

    def printMenu(self, weight):
        """
        Printing the menu based off valid weights
        """
        alwaysPrint = []

        # Going through every menu Item
        for item in self.menuItems:

            # Checking if it has a valid weight
            if item.weight in weight:
                print(item)

            # Always print 0 weighted items
            elif item.weight == 0:
                alwaysPrint.append(str(item))

        print("\n".join(alwaysPrint))


class MenuItem:
    """
    MenuItem class. Is used is the Menu class.
    Stores corresponding functions to the menu item
    """
    def __init__(self, ability, label, weight):
        """
        Initializing the MenuItem. Needs a function, label, and a weight
        """
        self.key = label[0].upper()
        self.ability = ability
        self.weight = weight
        self.label = label.lower()

    def __str__(self):
        """
        Returns label with a ) after the first letter
        """
        msg = "{}){}"
        return msg.format(self.key, self.label[1:])
