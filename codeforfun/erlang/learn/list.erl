-module(learn_list).
-export([qsort/1,
         perm/1,
         showModule/0,
         pythag/1,
         showFile/0,
         showLine/0]).

% ++ connect list
qsort([])->[];
qsort([Head|Tail])->qsort([X||X<-Tail,X<Head])++
                    [Head]++
                    qsort([X||X<-Tail,X>=Head]).

%A--B means a list that member in  A not in B
perm([])->[[]];
perm(List)->[[Head|Tail]||Head<-List,Tail<-perm(List--[Head])].

pythag(N)->
    [{A,B,C}||A<-lists:seq(1,N),
              B<-lists:seq(1,N),
              C<-lists:seq(1,N),
              A+B+C=<N,
              A*A+B*B=:=C*C].

showModule()->
    ?MODULE.

showFile()->
    ?FILE.

showLine()->
    ?LINE.
