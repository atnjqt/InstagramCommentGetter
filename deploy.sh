#!/bin/bash

# Jupyterhub takes take of looping through URLs and writing over dockerfile each iteration
docker build -t wwe_insta_comment_docker_name -f ./dockerfile .

docker run -it -v /Users/etiennejacquot/Documents/Bitbucket/wwe-instagram-rekogcomments/docker_comment_getter2/data/:/data --network=host --restart=on-failure --name=commentGetter wwe_insta_comment_docker_name:latest

# remove the previous container to keep things clean, we'll reuse this container name each time
docker rm commentGetter