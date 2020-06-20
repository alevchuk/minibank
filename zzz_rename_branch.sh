#!/bin/bash
# set -u
# set -e

exclude=".git|zzz_.*.sh"
find . -type f | grep -vE "$exclude" | xargs perl -pi -e 's/master/first/gi'
