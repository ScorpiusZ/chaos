-module(try_catch).
-export([demo/0,
        demo3/0,
        demo2/0]).

generate_exception(1)->a;
generate_exception(2)->throw(a);
generate_exception(3)->exit(a);
generate_exception(4)->{'EXIT',a};
generate_exception(5)->erlang:error(a).

demo()->
    [catcher(I)|| I<-[1,2,3,4,5]].

demo2()->
    [{I,(catch generate_exception(I))}|| I<-[1,2,3,4,5]].

%stack trace
demo3()->
    try generate_exception((5))
    catch
        error:X->
            {X,erlang:get_stacktrace()}
    end.

%it's better use
%
%try foo() of
%   Val->...
%catch
%   exit:Why->
%       ...
%
%instead of 
%
%case (catch foo()) of
%   {'Exit",Why}->
%      ...
%   Val->
%      ...
%
catcher(N)->
    try generate_exception(N) of
        Val->{N,normal,Val}
    catch
        throw:X->{N,caught,throw,X};
        exit:X->{N,caught,exit,X};
        error:X->{N,caught,error,X}
    end.

