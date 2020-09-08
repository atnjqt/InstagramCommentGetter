## ATN's Parsimonious WWE Instagram Comment Getter (using Selenium + Docker)

- So far I have `1.16%` of comments in the **wwe_df**!

- Cloud deployment & docker compose are next ...

### Getting Started with Selenium Standalone Docker Container

- Keeping it simple as possible in our efforts to grab Instagram comments ... 

- Using a standalone-selenium containerized instance of chrome:

``` bash
docker run -d -p 4444:4444 -v --shm-mem=4G selenium/standalone-chrome
# you can rename this container

docker rename _whatever_random_docker_name_is_ selenium-chrome

# nice to have a terminal windows visible with docker stats for monitoring
docker stats
```

### Jupyter Notebook for extracting comments from df w/ list of URLs

- **You must edit the docker mount:*`-v` in the file [deploy.sh](./deploy.sh) for your specific local host! On my local Macbook I have this pointing to `~\Documents\Bitbucket\wwe-instagram-rekogcomments\docker_comment_getter2\data\:\data\` but I believe this requires absolute path!

- [comment_getter.ipynb](./comment_getter.ipynb) is a python notebook which contains simple instructions for looping through `./configs/wwe_df.json` instagram URLs for HTML & ETL comment extraction to `./data`.
    - There is a cell to input the specific WWE instagram url!
    - You'll notice around 30+ clicks to load more comments that it very much is slowed down... It'll just click and do it's thing now that this is working correctly! This solution is parsimonious in that it uses all tools / techniques used are simple!
    - I've watched as this gets to 200, even 300+ clicks... this takes a long time to complete and therefore linearly running for URLs is unfeasible given we need 1.8 million extracted (at least that's the aspiration...)
- [review_etl.ipynb](./review_etl.ipynb) is a python notebook which contains examples for filtering `wwe_df[wwe_df.username == wwe_instagram_username].posturls.unique()` on all outifles `.\data\*.json`

- [dockerfile](./dockerfile) gets overwriten w/ instagram url & then `deploy.sh` does a build & run!

- [data/](./data) directory contains .html & .json outfiles of url, author, comment extraction 
    - this quickly is growing to contain *MANY* files... is this a problem or do we not care if it's organized by username?
- [configs/](./configs) directory contains various config files which keep this subdir of the repo clean :)

_______
### Thoughts on next iteration ... 

- Does the time to click & load more comments go logarithmic or linear? Hard to tell at 300+ clicks as seemingly it has plateaued...
- Slurm or cloud deployment?
- docker-compose w/ yaml file
- what about failed runs? how come it sometimes does *NOT* get all the comments for a post? Moreover, how do we go back through & identify posts that exported a file without all the comments (low filesize as indicator of failed commentextraction?)


- I am curious if Instagram will block IP after so many attempts / clicks to load more comments... 
- convenient that we don't need to login to IG to click and load more comments. The posts are public afterall!
- Do we want comments on videos? I know that the imghost URL is only, at least based on limited examples shared by Mbod, just blank thumbnails so we are ignoring this...