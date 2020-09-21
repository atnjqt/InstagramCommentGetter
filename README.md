# ATN's Parsimonious WWE Instagram Comment Getter (Using Selenium + Docker)

## Getting Started - 09/21/2020

- Added configurations & testing for `docker-compose` which handles running both the `commentGetter` & `chrome` containers needed for automated web browsing data collection of loading more Instagram comments ...

- Currently, the Dockerfile references a specific Instagram URL for a known post w/ many comments --> https://www.instagram.com/p/B61fZE1n9Nv/

```
cd /path/to/repo/InstagramCommentGetter/docker-compose-app

# This used just one example post w/ lots of comments (testing for scalability)
cat ./Dockerfile | grep python3

# To build containers
docker-compose up --build

# If something goes wrong, you can take down just as easily
docker-compose down
```
_______
### So, how does the docker-composed `commentGetter` container perform?

- The composed container works really nicely, convenient to *not* reuse the same `selenium:chrome-standalone` container for different URLs!

- In my testing, this performed **394 clicks** before crashing (took nearly 12+ hours)... ETL conversion for .html file returned **4936 comments**... We can review this here:

``` python
# From a jupyter notebook reviewing ./data
B61fZE1n9Nv_df = pd.read_json('./data/B61fZE1n9Nv.json')

wwe_df = pd.read_json('/Users/etiennejacquot/Documents/Bitbucket/wwe-instagram-rekogcomments/docker_comment_getter2/configs/wwe_df.json')

percentage_of_comments = round((B61fZE1n9Nv_df.shape[0] / wwe_df[wwe_df.posturl.str.contains('B61fZE1n9Nv')].commentcount.values * 100)[0],2)

print('{}% of the comments for {}'.format(percentage_of_comments,wwe_df[wwe_df.posturl.str.contains('B61fZE1n9Nv')].posturl.values[0]))
```

    67.76% of the comments** for https://www.instagram.com/p/B61fZE1n9Nv/! 

- Not bad, but not great given 394 clicks seems to be an upper limit for how much a browser can click & load into memory...
    - __PLEASE REMEMBER:__, this percentage is based on the *commentcount.sum* at the time of post extraction w/ PhantomBuster ... likely the true commentcount on IG has gone up, given users are still engaging w/ the post while some bot accounts were probably deleted so some comments are lost ...


### Thus, I think this parsimonious commentGetter web automation has some hard limitations for scaling up
- The problem of scaling up for all posts still remains, as I'm guessing there are some posts w/ MANY comments! 
- It's approximately a ratio of `1 # of clicks : 12 # comments returned`

![](https://i.imgur.com/MCvSbgO.png)


________________

## OLD NOTES (PRE DOCKER-COMPOSE IF YOU WANT TO JUST RUN JHUB NOTEBOOK TO LOOP W/ DOCKERFILES)

- So far I have at least `1.16%` of comments in the **wwe_df**!

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