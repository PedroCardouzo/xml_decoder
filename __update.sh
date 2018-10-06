#!/bin/bash

while getopts 'd' OPT; do
  case "$OPT" in
    'd') DEV='true';
		 echo 'dev mode (.git not deleted)';
       ;;
    '?') echo "illegal option @ ""$0" >&2
       exit -1
       ;;
  esac
done

git pull origin master
if [[ $DEV != 'true' ]]; then
	rm -Rf .git
fi
