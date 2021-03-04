#!/bin/bash
rev=$(git rev-parse --short HEAD)
git config user.name "Thomas Hintermeier"
git config --global user.email "hintermeier-t@protonmail.com"
git config user.password "$PASSWD"
git add .
git commit -m "committed at ${rev}"
git push origin HEAD:master