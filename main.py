import requests
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def sample_analyze_sentiment(text_content):
    client = language.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    document = {"content": text_content, "type": type_}
    encoding_type = enums.EncodingType.UTF8
    try:
        response = client.analyze_sentiment(document, encoding_type=encoding_type)
        return response
    except:
        return None

def main(request):
    naughty_list = []
    url = "https://aka.ms/holiday-wishes"
    response = requests.get(url, allow_redirects=True)
    wish_list = response.json()	
    for data in wish_list:
        [k, v] = data.items()
        who = k[1]
        message = v[1]
        sentiment = sample_analyze_sentiment(message)
        if sentiment is None:
            status = "Language not supported by GCP yet. Assuming nice for now."
            naughty_list.append({who:status})
        else:
            score = sentiment.document_sentiment.score
            if score > .5:
                status = "nice"
            else:
                status = "naughty"
            naughty_list.append({who:status})
    original = '\n'.join(str(w) for w in wish_list)
    output = '\n'.join(str(k) for k in naughty_list)
    divider = "*" * 40
    combined = f"{original}\n{divider}\n{output}"
    return combined