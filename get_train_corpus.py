

 
max_tweets = 3200





def get_tweets(screen_name, max_tweets=None):
    show = api.request("users/show", {"screen_name": screen_name}).json()
    tweet_length = show.get('statuses_count')
    if(tweet_length > 3200):
    	tweet_length = 3200

    params = {'screen_name':screen_name,'max_id':None,'count':200}
    save_tweets = []
    while True:
   		request = api.request("statuses/user_timeline",params)
   		tweets = request.json()
   		if(tweets[-1]['id']==last_seen):
   			break
   		last_seen = tweets[-1]['id']
   		params['max_id'] = last_seen
   		save_tweets.extend(tweets)
   		if(len(save_tweets) >= max_tweets):
   			break

    final_tweets = []
   	ids = []
   	for t in final_tweets:
   		if t['id'] not in ids:
   			final_tweets.append(t)
   			ids.append(t['id'])
   	return final_tweets



def get_question_and_answers(tweets):
	answer_tweets = []
	questions = []
	answers = []
	for tweet in tweets:
		if(tweet.get('in_reply_to_status_id'))
			answer_tweets.append(tweet)

	tweet_dict = {tweet['in_reply_to_status_id']: tweet for tweet in answer_tweets}

	tweet_len = len(answer_tweets)
	while len(answer_tweets) > 0:

		query_tweets = answer_tweets[:100]
		id_query = ','.join([str(q['id']) for q in query_tweets])
		origin_tweets = api.request("statuses/lookup", {"id": id_query}).json()
		for o in origin_tweets:
			if(o['id'] in tweet_dict)
				questions.append(o['text'])
				answers.append(tweet_dict[o['id']]['text'])

		answer_tweets = answer_tweets[100:]
		

	return answers,questions

def normalize_tweet(x):
    x = " ".join(x.split())
    x = x.lower()
    x = re.sub("http[^ ]+", "LINK", x)
    x = re.sub("#[^ ]+", "TAG", x)
    x = re.sub("(@[^ ]+ )*@[^ ]+", "MENTION", x)
    for punc in [".", ",", "?", "!"]:
        x = re.sub("[{}]+".format(punc), " " + punc, x)
    x = x.replace("n't", " not")
    x = " ".join(x.split())
    x = x.lstrip("MENTION ")
    return x.strip()


def get_qa_tweets(screen_name,max_tweets):
	tweets = get_tweets(screen_name,max_tweets)
	questions,answers = get_question_and_answers(tweets)
	questions = [normalize_tweet(q) for q in questions]
	answers = [normalize_tweet(a) for a in answers]
	return questions,answers







   	
