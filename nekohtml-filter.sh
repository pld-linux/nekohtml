#!/bin/sh
# 
# nekohtml filter script
# JPackage Project <http://www.jpackage.org/>

# Source functions library
if [ -f /usr/share/java-utils/java-functions ] ; then 
  . /usr/share/java-utils/java-functions
else
  echo "Can't find functions library, aborting"
  exit 1
fi

# Configuration
MAIN_CLASS=org.cyberneko.html.filters.Writer
BASE_JARS="nekohtml xerces-j2"

# Set parameters
set_jvm
set_classpath $BASE_JARS

# Let's start
run "$@"
