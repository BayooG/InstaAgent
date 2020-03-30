import csv
import pandas as pd

from igramscraper.instagram import Instagram


class InstaAgent():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.scraper = Instagram()
        self.target = self.scraper.get_account(username)
        self.scraper.with_credentials(username, password)
        self.scraper.login()
    
    def get_following_data(self, target_name, tweet_count=None):
        rows = [['username', 'full name', 'biography', 'prive', 'verfied', 'picture']]
        target  = self.scraper.get_account(target_name)
        if not tweet_count:
            tweet_count = target.follows_count
        followers = self.scraper.get_following(target.identifier, tweet_count, 100, delayed=True)
        for item in followers['accounts']:
            rows.append([item.username, item.full_name, item.biography, item.is_private, item.is_verified, item.profile_pic_url])
        return rows
    
    def get_followers_data(self, target_name, tweet_count=None):
        rows = [['username', 'full name', 'biography', 'prive', 'verfied', 'picture']]
        target  = self.scraper.get_account(target_name)
        if not tweet_count:
            tweet_count = target.follows_count
        followers = self.scraper.get_followers(target.identifier, tweet_count, 100, delayed=True)
        for item in followers['accounts']:
            rows.append([item.username, item.full_name, item.biography, item.is_private, item.is_verified, item.profile_pic_url])
        return rows
    
    def substract_folowing_folowers(self, target):
        
        following = self.get_following_data(target, tweet_count=650)
        followers = self.get_followers_data(target, tweet_count=650)
        res = [i for i in following if (i not in followers and not i.is_verified)]
        res.index(following[0],0)
        
        with open('./CSVs/'+ target + '__following.csv', mode='w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(following) 
        
        with open('./CSVs/'+ target + '__followers.csv', mode='w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(followers)    
        
        with open('./CSVs/'+ target + '__substract.csv', mode='w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(res)    
    
    def unfollow_list(self, lst):
        for i in lst:
            try:
                target  = self.scraper.get_account(i)
                self.scraper.unfollow(target.identifier)
                print('unfollowed: '+ i)
            except Exception as e:
                print(e)

