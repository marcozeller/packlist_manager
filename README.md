# Packlist Manager
Console interface tool written in python to create and manage packing lists with hierarchical structures.

# Implemented Features
* First Functional Release
  * Store new Items in Database
  * List all Items in Database
  * Show an Item in Database
  * Modify and delete an Item in Database
  * Store new Packs in Database without included Packs
  * List all Packs in Database
  * Show a Pack in Database without included Packs
  * Modify a Pack in Database without included Packs
  * Store new Packs in Database with included Packs
  * Show a Pack in Database with included Packs (except amount)
  * Modify a Pack in Database with included Packs
  * Store weight, volume, price, as decimals with a unit

# Planned Features
## Basic Features
* First Functional Release
  * Add better shortcuts and make them visible for user
  * Make it possible for the Database to be imported and converted for future releases

* Fast (rewritten) tests for all the functionalities
* Properly calculate the amounts for packs
* Add Security Constraints (e.g. no including loops) on DB-Level and User-Level
* Add NeedToBuy function
* Give some additional units for the user to convert to and from
* Export a Printable Version of a Packlist
* Add a Screen for going through a Pack and use as virtual Checklist on screen
* Support for additional Item classes
  * Support for Item class Food
    * (Calories, Protein, Carbohydrates, Fat, Best-Before-Date, ...)
    * Modify NeedToBuy function to include perished Items
* Support for different languages
  * English
  * German
  * Make it easy to support additional languages

## Advanced Features
* Make it possible to save a picture of every item or list
