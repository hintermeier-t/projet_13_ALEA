#!/bin/sh

setup_git() {
  git config --global user.email "hintermeier-t@protonmail.com"
  git config --global user.name "Thomas Hintermeier"
}

commit_country_json_files() {
  git checkout master
  # Current month and year, e.g: Apr 2018
  dateAndMonth=`date "+%b %Y"`
  git add *
  # Create a new commit with a custom build message
  # with "[skip ci]" to avoid a build loop
  # and Travis build number for reference
  git commit -m "Travis update: $dateAndMonth (Build $TRAVIS_BUILD_NUMBER)" -m "[skip ci]"
}

upload_files() {
  # Remove existing "origin"
  git remote rm origin
  # Add new "origin" with access token in the git URL for authentication
  git remote add origin https://hintermeier-t:${GH_TOKEN}@github.com//hintermeier-t/projet_13_ALEA.git > /dev/null 2>&1
  git push origin master --quiet
}

setup_git

commit_country_json_files
upload_files

