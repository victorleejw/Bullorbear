from django.shortcuts import render
from .utils import historical_searches
from .utils import text_analysis_api


def home(request):
    if request.method == 'POST':

        url = request.POST.get('url')

        # Other searches (in both results page and error page)
        other_searches_list = historical_searches.main(url)

        try:
            # Get results from API
            sentiment_analysis, summarization, hashtag_suggestion = text_analysis_api.main(url)
            
            # Bull/bear/neutral
            result = sentiment_analysis['polarity']
            confidence_score = sentiment_analysis['polarity_confidence'] * 100

            # Summaries
            summaries = summarization['sentences']

            # Keywords
            keywords = hashtag_suggestion['hashtags']

            context = {
                'result': result,
                'confidence_score': confidence_score,
                'summaries': summaries,
                'keywords': keywords,
                'other_searches': other_searches_list,
            }

            return render(request, 'bull_bear/results.html', context)

        except Exception as e:
            print(e)
            return render(request, 'bull_bear/error.html', {'other_searches': other_searches_list})

    else:
        return render(request, 'bull_bear/index.html')

