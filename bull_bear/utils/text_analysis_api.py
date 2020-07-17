import requests


def main(link):

    headers = {
        'x-rapidapi-host': "aylien-text.p.rapidapi.com",
        'x-rapidapi-key': "ce903b676emsh07edcca0c209af3p1092ffjsn0ae07bcedaf0"
    }


    def request_api(url, querystring):
        response = requests.request("GET", url, headers=headers, params=querystring)
        return eval(response.text)


    # Article extraction
    extract_url = "https://aylien-text.p.rapidapi.com/extract"
    extract_querystring = {"url":link}
    article_extraction = request_api(extract_url, extract_querystring)
    article = article_extraction['article']
    title = article_extraction['title']

    # Sentiment analysis
    sentiment_url = "https://aylien-text.p.rapidapi.com/sentiment"
    sentiment_querystring = {"text":article, "url":link, "mode":"document"}
    sentiment_analysis = request_api(sentiment_url, sentiment_querystring)
    
    # Summarization
    summarize_url = "https://aylien-text.p.rapidapi.com/summarize"
    summarize_querystring = {"title":title,"text":article}
    summarization = request_api(summarize_url, summarize_querystring)

    # Hashtag suggestion
    hashtags_url = "https://aylien-text.p.rapidapi.com/hashtags"
    hashtags_querystring = {"url":link,"text":article,"language":"en"}
    hashtag_suggestion = request_api(hashtags_url, hashtags_querystring)

    return sentiment_analysis, summarization, hashtag_suggestion
