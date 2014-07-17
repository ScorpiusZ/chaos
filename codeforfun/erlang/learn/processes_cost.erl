-module(processes_cost).
-export([max/1]).

max(Num)->
    Max=erlang:system_info(process_limit),
    io:format("Maxinum allowed processes : ~p ~n",[Max]),
    statistics(runtime),
    statistics(wall_clock),
    L = for(1,Num,fun()-> spawn(fun()-> wait() end ) end),
    {_,Time1}=statistics(runtime),
    lists:foreach(fun(Pid)-> Pid! die end,L),
    {_,Time2}=statistics(wall_clock),
    U1=Time1*1000/Num,
    U2=Time2*1000/Num,
    io:format("Process spawn time = ~p (~p) msecs~n",[U1,U2]).

wait()->
    receive
        die->void
    end.

for(N,N,Func)->[Func()];
for(I,N,Func)->[Func()|for(I+1,N,Func)].


