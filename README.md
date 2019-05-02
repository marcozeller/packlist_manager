# Packlist Manager
Console interface tool written in python to create and manage packing lists with hierarchical structures.

# Implemented Features
* First Functional Release
  * Store new Items in Database
  * List all Items in Database
  * Show an Item in Database
  * Modify and delete an Item in Database

# Planned Features
## Basic Features
* First Functional Release
  * Store new Packs in Database without included Packs
  * List all Packs in Database
  * Show a Pack in Database without included Packs
  * Modify a Pack in Database without included Packs
  * Store new Packs in Database with included Packs
  * Show a Pack in Database with included Packs
  * Modify a Pack in Database with included Packs
  * Make it possible for the Database to be imported and converted for future releases

* Add Security Constraints (e.g. no including loops) on DB-Level and User-Level
* Add NeedToBuy function
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
