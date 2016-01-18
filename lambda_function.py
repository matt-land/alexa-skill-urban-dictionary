import pycurl, json, urllib

from io import BytesIO

def lambda_handler(event, context):
    #event['session']
    #event['user']
    #event['request']
    type = event['request']['type']
    if type == 'LaunchRequest':
        return get_welcome_response()

    word = str(event['request']['intent']['slots']['Word']['value'])
    if str.startswith(word, 'a '):
        word = word[2:]
    c = pycurl.Curl()
    data = BytesIO()
    c.setopt(c.WRITEFUNCTION, data.write)
    url = str('http://api.urbandictionary.com/v0/define?term='+urllib.quote(word))
    print url
    c.setopt(c.URL, url)
    c.perform()
    c.close()
    dictionary = json.loads(data.getvalue())
    title = 'Urban: '+word

    if dictionary['result_type'] == 'no_results':
        output = "Well, that isn't a thing, but I see where you were going."
    else:
        definition = dictionary['list'][0]['definition']
        #output =  "A %s is defined as,  %s" % (word, definition)
        output = definition

    speechlet = build_speechlet_response(title,output, 'test', True)
    return build_response({}, speechlet)

def get_welcome_response():
    session_attributes = {}
    card_title = "Urban Dictionary"
    speech_output = "Urban Dictionary:, A place formerly used to find out about slang. " \
                    "Say, Tell me about term?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please say, Tell me about term. "

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

