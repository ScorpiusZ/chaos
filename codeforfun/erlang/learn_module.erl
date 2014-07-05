-module(learn_module).
%module name must as same as file name
-export([cost/1,shop/1,buylist/0]).
%you can only use the exported functions

cost(apple) -> 2;
cost(banana)-> 4;
cost(orange)-> 11;
cost(pitch)->7.

shop([{What,Num}|Rest])->
    cost(What)*Num+shop(Rest);
shop([])->0.

buylist() ->
    [{apple,11},{banana,2},{orange,3},{pitch,9}].

