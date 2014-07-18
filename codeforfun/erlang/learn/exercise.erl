-module(exercise).
-compile(export_all).

start(AnAtom,Func)->
    case whereis(AnAtom) of
        undefined->
            regist(AnAtom,Func);
        _Pid->
            io:format('alreadyRegiste ~n'),
            alreadyRegiste
    end.

regist(AnAtom,Func)->
    register(AnAtom,spawn(Func)),
    AnAtom.

loop()->
    receive
        die->
            void;
        Other->
            io:format("receive ~p~n",[Other]),
            loop()
    end.

temp()->
    receive
        start->
            start(test,fun()-> loop() end)
    end.

stop()->
    test! die.

demo()->
    Pid1=spawn(fun()-> temp() end),
    Pid2=spawn(fun()-> temp() end),
    Pid2!Pid1! start.



