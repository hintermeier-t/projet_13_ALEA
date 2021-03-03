#!/bin/sh

git config --global user.email "hintermeier-t@protonmail.com"
git config --global user.name "Thomas Hintermeier"
git checkout master
git add *
git commit -m "Travis update: (Build $TRAVIS_BUILD_NUMBER)"
# Remove existing "origin"
git remote rm origin
# Add new "origin" with access token in the git URL for authentication
git remote add origin https://${GH_TOKEN}@github.com//hintermeier-t/projet_13_ALEA.git >
git push origin master --quiet


