-module(concurrency).
-compile(export_all).


start()->
    register(server,spawn(fun concurrency:loop/0)).

loop()->
    receive
        {stop,_,_}->
            io:format('server stop ~n');
        {calc,Fun,Args}->
            io:format('result of the func is : ~p~n',[Fun(Args)]),
            loop();
        Msg->
            io:format('receive msg :~p~n',[Msg]),
            loop()
    end.

sendMsg(Msg)->
    server ! Msg.

fac(1)->1;
fac(N)->N*fac(N-1).

sum_list([])->0;
sum_list([H|T])->H+sum_list(T).

say_something(Words)->
    io:format('you say : ~p~n',[Words]).

fibo(1)->1;
fibo(2)->1;
fibo(N)->fibo(N-1)+fibo(N-2).

