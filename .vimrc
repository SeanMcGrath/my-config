set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'gmarik/Vundle.vim'
Plugin 'Valloric/YouCompleteMe'
Plugin 'mattn/emmet-vim'

set runtimepath+=~/.vim_runtime
execute pathogen#infect()

syntax on
filetype indent plugin on

try
source ~/.vim_runtime/my_configs.vim
catch
endtry

map - :Explore<cr>
