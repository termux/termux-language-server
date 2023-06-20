#!/usr/bin/env -S perl -p
$title = $ARGV;
$title =~ s=.*?requirements/(.*?)\.txt=$1=;
s`^([^#\n][^\s[>=<^!^]*)`- [$1](https://pypi.org/project/$1)`;
s/^#\s*//;
s/^!.*/## $title/;
