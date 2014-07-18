-module(clock).
-export([demo/0]).


demo()->
    start(3000,fun()-> io:format('time tick ~p~n',[now()]) end),
    sleep(30),
    stop().

sleep(Time)->
    receive
    after Time*1000->
              void
    end.

start(Time,Func)->
    register(clock,spawn(fun()-> tick(Time,Func) end)).

stop()->
    clock! stop.

tick(Time,Func)->
    receive
        stop->
            io:format('tick server stop ~n'),
            void
    after Time->
              Func(),
              tick(Time,Func)
    end.

