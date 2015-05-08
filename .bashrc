#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

alias ls='ls --color=auto'

### FUNCTIONS

# Easy extract
extract () {
    if [ -f $1 ] ; then
	case $1 in
	    *.tar.bz2)   tar xvjf $1    ;;
	    *.tar.gz)    tar xvzf $1    ;;
	    *.bz2)       bunzip2 $1     ;;
	    *.rar)       rar x $1       ;;
	    *.gz)        gunzip $1      ;;
	    *.tar)       tar xvf $1     ;;
	    *.tbz2)      tar xvjf $1    ;;
	    *.tgz)       tar xvzf $1    ;;
	    *.zip)       unzip $1       ;;
	    *.Z)         uncompress $1  ;;
	    *.7z)        7z x $1        ;;
	    *)           echo "don't know how to extract '$1'..." ;;
	esac
    else
	echo "'$1' is not a valid file!"
    fi
    
}

# Makes directory then moves into it
function mkcdr {
    mkdir -p -v $1
    cd $1
    
}

# Creates an archive from given directory
mktar() { tar cvf  "${1%%/}.tar"     "${1%%/}/"; }
mktgz() { tar cvzf "${1%%/}.tar.gz"  "${1%%/}/"; }
mktbz() { tar cvjf "${1%%/}.tar.bz2" "${1%%/}/"; }

### ALIASES

## Keeping things organized
alias ls='ls --color=auto'
alias ll='ls -l'
alias la='ls -A'
alias rm='mv -t ~/.local/share/Trash/files'
alias cp='cp -i'
alias mv='mv -i'
alias mkdir='mkdir -p -v'
alias df='df -h'
alias du='du -h -c'
alias reload='source ~/.bashrc'
alias biggest='BLOCKSIZE=1048576; du -x | sort -nr | head -10'

## Moving around & all that jazz
alias back='cd $OLDPWD'
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias ......="cd ../../../../.."
