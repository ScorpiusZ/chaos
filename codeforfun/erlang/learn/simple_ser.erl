-module(simple_ser).
-export([demo/0,
        rpcdemo/0]).

area({circle,R})->
    3.14159*R*R;
area({rectangle,Width,Height})->
    Width*Height;
area(_)->
    error.

loop()->
    receive
        {From,{area,Request}}->
            Response=area(Request),
            io:format("get Request ~p ~n",[Request]),
            From! {self(),Response},
            loop();
        _->
            io:format("Invalidate Argument ~n"),
            io:format("server down ~n")
    end.

getRandomParams()->
    {_,_,MicroSecs}=now(),
    case MicroSecs rem 2 of
        1->
            {circle,MicroSecs};
        0->
            {rectangle,MicroSecs,MicroSecs};
        _->
            {circle,1}
    end.

getThreads(0)->
    [];
getThreads(N)->
    Pid=spawn(fun loop/0),
    [Pid|getThreads(N-1)].

sendMsg([])->
    [];
sendMsg([Pid|T])->
    Msg=getRandomParams(),
    Pid! {self(),{area,Msg}},
    sendMsg(T).

rpc(Pid,Request)->
    Pid! {self(),{area,Request}},
    receive
        {Pid,Response}->
            io:format("Response is ~p~n",[Response]),
            Response
    end.

rpcdemo()->
    Pid=spawn(fun loop/0),
    rpc(Pid,{circle,5}),
    rpc(Pid,{rectangle,5,3}),
    rpc(Pid,{rectangle,5,3,111}).

demo()->
    Threads=getThreads(10),
    sendMsg(Threads),
    Pid=spawn(fun loop/0),
    Pid1=spawn(fun loop/0),
    Pid! Pid1! {self(),{area,{circle,5}}},
    Pid! {self(),{area,{rectangle,3,4}}},
    Pid! Pid1! {self(),{area,{haha,a}}}.
