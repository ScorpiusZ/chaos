# Oh-my-Zsh prompt created by gianu
#
# https://github.com/ScorpiusZ
# 

PROMPT='[%{$fg_bold[red]%}%D{%I:%M:%S}%{$reset_color%} %{$fg_bold[white]%}%n%{$reset_color%} %{$fg[magenta]%}%~ %{$reset_color%}\
$(git_prompt_info)\
%{$fg[magenta]%}%(!.#.)%{$reset_color%}]$ '


ZSH_THEME_GIT_PROMPT_PREFIX="(%{$fg_bold[green]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX=")"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[green]%} %{$fg[yellow]%}✗%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$reset_color%}"
