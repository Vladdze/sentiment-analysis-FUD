# sentiment-analysis-FUD

Data and Methodology
The updated research is to develop and validate a sentiment analysis approach that leverages social media data to effectively decipher market climate and associated risks within the volatile cryptocurrency market. Aiming to provide an easily readable tool that displays the state and sentiment around a cryptocurrency. Empowering investors to make more informed and strategic investment decisions in the cryptocurrency market.
The currently minimally viable product contributes to past research and work in the field by providing real-time insights into the sentiment and emotional state of the online community surrounding cryptocurrencies, in this case – Ethereum. This offers several advanced and practical applications for academics, retail investors and crypto hobbyists:

1.	Real-time monitoring: 
Traditional sentiment analysis methods often use historical data, which does not capture the rapidly changing modern world, and even more so especially the volatile cryptocurrency space. Streaming and analyzing social media data in real time, provides up-to-date insights into the market, ecosystem and anything related in the Web3.0 space.
2.	Emotional Analysis:
Expands upon previous research of sentiment analysis by incorporation emotional analysis into the sentiment analysis framework. Allowing for a deeper understanding of online communities. This deeper level of understanding has limitless applications and utility for further understanding of sociological phenomena such as FOMO and FUD and its triggers.
3.	Data Visualization:
User-friendly approach for making complex data accessible and understandable.

The current product builds upon the theoretical in sentiment analysis and social media analytics and applies it to the real world via a user-friendly format, making insights more accessible and actionable.
In-depth Methodology
The web app works by collecting, processing, and visualizing real-time Twitter data related to Ethereum, or any cryptocurrency of interest. Focusing specifically on the sentiment of tweets and topics/trends of tweets.

The primary data that is analyzed is the “class tweepy. Tweet”. Tweets are the basic building blocks of all things Twitter. The Tweet object has the basic ‘root-level’ fields: id – unique identified of the requested (int) Tweet, text – actual text of the tweet (str) , created at – creation time of the Tweet (datetime.datetime). Since tweets contains lots of unnecessary information that can interfere with determining the sentiment surrounding the topic at hand, the tweets must be cleaned - this is done through pre-processing. There are several regular expressions that clean tweets, these expressions remove newlines, links, mentions, IDs, emojis, Ethereum wallet addresses and convert Latin characters to ASCII equivalents and then remove them. The cleaned tweets are then limited to 255 characters in length.
Next, the custom implementation of the Tweepy’s “.StreamingClient” class is adjusted to connect to Twitters 2.0API. The custom implementation includes an “on_connect” method to display if connection is successful, when the stream is connected. The “on_tweet” method is adjusted to extract specific attributes from incoming tweets as described above and cleans the tweets using the “clean_tweet” function explained above as well. The cleaned tweets are analyzed for sentiment using the TextBlob Library and then stored in the MySQL database. The new “clean_tweet” function is improved from the previous iteration by pre-compiling the regular expressions before they are used, leading to an improvement in terms of time-complexity. Having the regex pre-processed into an internal already set format, allowing for faster execution when they are called multiple times, instead of having to recompile the regex every time the “clean_tweet” function is called. The new function also combines several regular expressions into one regex, reducing the number of operations needed to process the tweets. In addition, to better performance, the new function has more detailed error handling, using try-except code block to handle errors and notifies the user with a printed message. The new improved function is more robust and versatile.

The updated filtered stream query handles Twitter 2.0 API rate limits by waiting when the limit is reached. The filtered stream excludes retweets, quotes, replies and multiple unwanted keywords and phrases to eliminate spam tweets and advertisements. The data scrapping continuously runs and inserts the obtained cleaned data into an SQL database. 
Data Visualization is done using Plotly to create real-time visualizations, showing sentiment on Ethereum over time categorized by sentiment polarity - positive, neutral, negative, and frequency of most common words used. Three new functions were created in order to clean up the code and improve execution: 
(1) “clean_content”  - Takes text as input and performs cleaning operations to prepare the text for processing. Using regex to remove, URLs, replace “&” with “and”, remove any non-alphanumeric characters and converts text to lowercase.

(2) “create_filtered_sen” – Takes cleaned content and tokenizes it using ‘word_tokenize” from ‘NLTK’ library. Removes any stop words from the tokenized words using ‘stopwords’ module from ‘NLTK’. ‘stopwords’ contains common English stop words.
(3)”create_frequency_df”. – Takes the filtered words and uses ‘FreqDist’ from ‘NLTK’ library to compute frequency distribution of words and creates a Pandas DataFrame with the 20 most used words and their frequency count.

These functions are used to preprocess the data, tokenize it, remove stop words, and compute word frequency.
“TextBlob.sentiment” uses a machine learning algorithm to analyze words in the “tweet.text” data field and assigns a polarity and subjectivity score to each word, It then calculated the average of these scores to determine the overall sentiment polarity and subjectivity of the text. This algorithm is based on the Naïve Bayes Classifier. This is the main algorithm used for sentiment analysis in this application.
Tools and Libraries

Tweepy == 4.13.0	Python library for accessing the Twitter API. Used to retrieve Twitter API data (Tweets)
MySQL-Connector == 2.2.9	Python library for connect to MySQL databases. Used to connect to a MySQL database on the localhost
Pandas == 1.5.3	Python library for data manipulation and analysis.
Used for data structures (DataFrame)
Numpy == 1.24.2	Python library for numerical computing.
NLTK == 3.8.1	Python library from Natural Language Processing. Used to analyze “hot words” (most frequently used words around a topic) for analysis.
TextBlob == 0.17.1	Python library for processing textual data. Used for sentiment analysis 
Emoji == 2.2.0	Python library for working with emojis. Tweets can contain lots of emojis, used for pre-processing functions to remove emojis from Tweet.Text for better storage in database
Regex == 2022.10.31	Python library for working with regular expressions. Used for different pre-processing functions.
Plotly == 5.13.1
Plotly-express == 0.4.1	Python library for creating interactive data visualization. Used for data visualization
Seaborn == 0.12.2	Python library for data visualization. Used for data visualization
Matplotlib == 3.7.1	Python library for data visualization. Used for data visualization
SQLAlchemy ==2.0.7	Python library for interacting with MySQL.
Dash == 2.9.2	Python library for developing analytical web application.
NOT IN CURRENT ITTERATION
Transformers == 4.27.4
(Hugging Face)	Python library developed by Hugging Face library for Nature Language Processing and Machine Learning. Not currently implemented into the web app (discussed in shortcomings).
Torch == 2.0	Python library for Machine Learning.


    
Framework
Current Framework
The current framework directly interacts with the Twitter 2.0API streaming the data directly into a MySQL Database which then gets pulled in real time for Sentiment Analysis and Modeling. The analyzed data gets visualized in real time in 60s intervals which is the streamed to a Web App Analytical Dashboard.

Optimized Framework
Optimized Framework using parallelizing streaming of Twitter data using Kafka. Current iteration is not capable of processing large volumes of data in real-time with limited scalability. Kafka streaming allows for processing of extremely large volumes of data in real-time with built-in fault-tolerance (replication of data to multiple nodes inside Kafka cluster, allowing for data recovery).  Current model is limited to the amount of data it can process making advanced sentiment analysis methods such as neural networking-based sentiment analysis impossible. The proposed optimized framework allows for more accurate sentiment analysis using deep learning/neural networks.

Frameworks are shown Framework.JPG file.



Shortcomings and Concluding Remarks 
This is an MVP – Minimally Viable Product, showing proof of concept for a real-time analytical web dashboard for monitoring the cryptocurrency ecosystem. Shortcoming and next steps for continuity are discussed below.
Shortcomings and Continuity
1.	Machine Learning, Data Storage and Parallel Streaming: 
Current implementation is not capable of processing large volumes of data in real-time. Implementing Kafka streaming allowing for processing of extremely large volumes of data in real-time with built-in fault-tolerance (replication of data to multiple nodes inside Kafka cluster, allowing for data recovery) makes the application more robust and sustainable. In addition, current model is limited by the amount of data it can process and analyze, computing power also becomes a limiting factor. Making advanced sentiment analysis methods such as neural networking-based sentiment analysis and emotion analysis impossible. Using models like BERT,GPT or RoBERTa for sentiment analysis would greatly improve sentiment accuracy. I have included an emotional analysis code block in the current iteration, using Hugging Face’s “transformers” library, using the RoBERTa model for emotion analysis (can be seen in complex.ipynb). However, due to a lack of computing power, it was not possible to generate the model and visualize the data. This could be fixed by utilizing cloud computing to run the web app through a collection of AWS services such as, EC2 for the web app, Amazon RDS for data warehousing, S3 for data storage, Sagemaker for training and deploying machine learning models, such as advanced sentiment analysis and emotional analysis, Lambda for running the code, and MSK for management of Apache Kafka. 
2.	Error Handling
Current iteration has minimal error handling, especially around the interactions between the database and streaming client. Implementing robust error handling and adding logging would make it easier to maintain and debug the code. The addition of logging would allow for quick identification of issues.
3.	Visualization Update: 
Current visualization is set to update every minute. Ideally, asynchronous visualization would be used.
4.	Filtering:
Current filtering parameters can be further enhanced to eliminate junk and spam information more efficiently. Allowing for better and cleaner data to work with.
Concluding remarks 
As this is a minimally viable product demonstrating a proof of concept for a web3.0 ecosystem monitoring system, in this case – Ethereum. Integrating the product with other data sources, not just Twitter API2.0 would allow for much more comprehensive analysis and develop more insights becoming an aggregated monitoring system for all things cryptocurrency, web3.0 related throughout all social media platforms.

