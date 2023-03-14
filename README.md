# sentiment-analysis-FUD

The following code contains 5 files (main.ipynb,sentiment.ipynb,complex.ipynb,credentials.py and settings.py).
main.ipynb
This is the main function that extracts streaming data from twitter, pre-processes it and stores in a MYSQL DB.
This function uses Twitter API v2.0(https://developer.twitter.com/en/docs/twitter-api) and Tweepy 4.13(https://docs.tweepy.org/en/stable/).

The function first authenticates twitter API and produces an output "Successfull Authentication" or "Failed Authentication". It then connects to the DB on the
localhost and calls to check for if a table exists inside the DB, if it does not it will create one and use the format from settings.py.
    
Next, functions are defined, there are two main functions: 
    
(1): clean_tweet, which is pre-processing of tweet text data, it removes, \n for new line in tweets,links
mentions and emojis using emoji library(emoji.replace_emoji), it then returns the cleaned tweet that is upto 255 characters long. This is necessary, as with the
new Twitter Blue subscription, users can have tweets with the length of upto 4,000 characters. 255 characters is plenty to determine sentiment.
    
(2): push_results_to_tables, inserts data into DB table using data in the 'Struct' dictionary.
    
Now, the custom 'MyStream' class is inherited from Tweepy's StreamingClient. It is used to override the parent class.
Once MyStream is created and started, it will connect to Twitter Streaming API and display "Connected" once it has established a connection.
Following, the 'on_tweet' method filters and processes incoming tweets, storing only english tweets that do not contain any media attachments or retweets, and
extract attributes from the saved tweets into the MySQL database if once is connected. The 'on_error' is responsible for stopping the data scrapping if rate limit 
is reached and the method returns 'False'.
    
Next, the streaming process is created by creating an instance of 'MyStream' via passing a BEARER TOKEN. The ruleset that is responsible for filtering tweets is 
cleared and new rules per the 'add_rules()' are added to adjust the stream. Finally, 'filter()' starts the stream. 'filter()' has two arguements 'expansions' 
and 'tweet_fields', these are required to be mentioned in order for the stream to display additonal data as they are not root-level fields.
    
    
sentiment.ipynb

This is where initial sentiment and analysis is done. Data will be pulled from MySQL DB to create figures, one will be a time series with the count of sentiment of 
each kind (-1,0,+1) per time-interval and a topic tracking for most frequently used words in the tweets.
    
complex.ipynb

Complex real-time sentiment analysis and more complex analysis.
    
settings.py

settings for table_attributes, table_name.
   
credentials.py

contains all keys and passwords.
    
gitignore

contains credentials.py __pycache__ 
    
    
