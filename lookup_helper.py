## because a lot of the endpoints return an array of IDs that correspond to a table, we need 
## a class for conversion that can take an array of IDs and translate them to something we can use
## for example, we can build a dataframe that has the name and id of each table, and then convert to something actually useful

## sometimes, it makes more sense to not put *everything* in our df, only what is absolutely necessary; the rest can be queried
## for example, we dont need a dataframe of every single game engine, just the ones that are used in our dataset
import testing as ts


#platform type; 1 = console, 6 = computer