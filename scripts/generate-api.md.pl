#!/usr/bin/env -S perl -n
$.       = 1 unless $#ARGV == $oldargc;
$oldargc = $#ARGV;
next unless $. == 1;
$_ = $ARGV;
s=src/=.. automodule:: =;
s=\.py$=\n    :members:\n=;
s=/__init__==;
s=/=.=g;
print;
