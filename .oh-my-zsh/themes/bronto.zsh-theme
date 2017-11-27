ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg[blue]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%} "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[cyan]%}"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%}"

PROMPT='
%{$fg[cyan]%}%~ $(git_prompt_info)
%{$fg[white]%}%(?.∴.%{$fg[red]%}∵%{$reset_color%})% %n@%m%{$fg_bold[white]%}> %{$reset_color%}'
