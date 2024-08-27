from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from nylas import Client
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob



# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)


nylas = Client(
    os.environ.get('NYLAS_ACCESS_TOKEN'),
    os.environ.get('NYLAS_API_URI')
)
grant_id = os.environ.get("NYLAS_GRANT_ID")

messages = nylas.messages.list(
  grant_id,
  query_params={
    "limit": 5
  }
)
#logging.debug(f"nyls message: {messages}")

# Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()


# Very Negative: Compound score ≤ -0.6
# Negative: -0.6 < Compound score ≤ -0.2
# Neutral: -0.2 < Compound score ≤ 0.2
# Positive: 0.2 < Compound score ≤ 0.6
# Very Positive: Compound score > 0.6

# Very Negative: 😡 (Angry Face) - U+1F621
# Negative: 😞 (Disappointed Face) - U+1F61E
# Neutral: 😑 (Expressionless Face) - U+1F611
# Positive: 🙂 (Slightly Smiling Face) - U+1F642
# Very Positive: 😁 (Beaming Face with Smiling Eyes) - U+1F601


def analyze_email_tone(text):
    # Use VADER to analyze sentiment
    try:
        logging.debug(f"email subject: {text}")
        sentiment_dict = analyzer.polarity_scores(text)
        
        #logging.debug(f"Overall sentiment dictionary is : ", sentiment_dict)
        logging.debug(f"sentence was rated as {sentiment_dict['neg']*100} Negative, {sentiment_dict['neu']*100} Neutral,{sentiment_dict['pos']*100} Positive")

        mood_percentages = {key: value * 100 for key, value in sentiment_dict.items()}

        #sentiment_dict= analyze_sentiment(text)

        if sentiment_dict['compound'] > 0.6 :
            tone = "Very Positive"   
            emoji = "😁"
        elif sentiment_dict['compound'] <= 0.6 and  sentiment_dict['compound'] > 0.2:
            tone = "Positive"
            emoji = "🙂"
        elif sentiment_dict['compound'] <= 0.2 and sentiment_dict['compound'] > -0.2 :
            tone = "Neutral"
            emoji = "😑"
        elif sentiment_dict['compound'] <= - 0.2 and sentiment_dict['compound'] > -0.6 :
            tone = "Negative"
            emoji = "😞"
        elif sentiment_dict['compound'] <= - 0.6:
            tone = "Very Negative"
            emoji = "😡"

        logging.debug(f"compound: {sentiment_dict['compound']}")
        logging.debug(f"emotion: {tone}")

    except Exception as e:
        logging.error(f"Error on analyze email tone: {e}")

    return {
        'tone': tone,
        'mood_percentages': mood_percentages,
        'emoji': emoji
    }

# @app.route('/analyze-email', methods=['POST'])
# def analyze_email():
#     try:
#         logging.info("Start to get email info..")
#         target_email = request.json.get('target_email')
        
#         grant_id = os.environ.get("NYLAS_GRANT_ID")
#         # Fetch the email using Nylas API

#         response = nylas.messages.list(
#         grant_id,
#         query_params={
#             "from": target_email,
#             "limit":5
#         }
#         )
#         logging.debug(f"Response message: {response}")
#         email = response[0][0]

#         # Accessing various fields in the Message object
#         grant_id = email.grant_id
#         from_email = email.from_[0]['email']
#         subject = email.subject
#         snippet = email.snippet
#         body = email.body
#         thread_id = email.thread_id
#         to_email = email.to[0]['email']
#         date = email.date

#         #logging.debug(f"email subject: {email.subject}, email body: {email.body}")
#     except Exception as e:
#         logging.error(f"Error analyzing email: {e}")
#         return jsonify({'error': 'Failed to analyze email'}), 400


#     # Analyze the emotional tone
#     logging.info("Start to analyze enmotion..")
#     emotion_result = analyze_email_tone(email.body)
#     logging.debug(f"emotion_result: {emotion_result}")

#     return jsonify({
#         'subject': subject,
#         'body': body,
#         'tone': emotion_result['tone'],
#         'mood_percentages': emotion_result['mood_percentages'],
#         'emoji': emotion_result['emoji']
#     })


@app.route('/analyze-email', methods=['POST'])
def analyze_email():
    try:
        logging.info("Start to get email info..")
        target_email = request.json.get('target_email')
        
        grant_id = os.environ.get("NYLAS_GRANT_ID")
        # Fetch the emails using Nylas API
        response = nylas.messages.list(
            grant_id,
            query_params={
                "from": target_email,
                "limit": 5
            }
        )
        logging.debug(f"Response message: {response}")

        analyzed_emails = []

        for email in response[0]:
            # Accessing various fields in the Message object
            grant_id = email.grant_id
            from_email = email.from_[0]['email']
            subject = email.subject
            snippet = email.snippet
            body = email.body
            thread_id = email.thread_id
            to_email = email.to[0]['email']
            date = email.date

            # Analyze the emotional tone
            logging.info("Start to analyze emotion..")
            emotion_result = analyze_email_tone(body)
            logging.debug(f"emotion_result: {emotion_result}")

            analyzed_emails.append({
                'subject': subject,
                'body': body,
                'tone': emotion_result['tone'],
                'mood_percentages': emotion_result['mood_percentages'],
                'emoji': emotion_result['emoji']
            })

    except Exception as e:
        logging.error(f"Error analyzing email: {e}")
        return jsonify({'error': 'Failed to analyze email'}), 400

    return jsonify(analyzed_emails)


if __name__ == '__main__':
    logging.info("Starting Flask server...")
    app.run(port=3000)
