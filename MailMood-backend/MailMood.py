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

# MongoDB setup
client = MongoClient(os.getenv('MONGO_URI'),server_api=ServerApi('1'),tls=True,tlsAllowInvalidCertificates=True)
db = client['knowledge_base']
collection = db['emails']

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
            emoji = "U+1F601"
        elif sentiment_dict['compound'] <= 0.6 and  sentiment_dict['compound'] > 0.2:
            tone = "Positive"
            emoji = "U+1F642"
        elif sentiment_dict['compound'] <= 0.2 and sentiment_dict['compound'] > -0.2 :
            tone = "Neutral"
            emoji = "U+1F611"
        elif sentiment_dict['compound'] <= - 0.2 and sentiment_dict['compound'] > -0.6 :
            tone = "Negative"
            emoji = "U+1F61E"
        elif sentiment_dict['compound'] <= - 0.6:
            tone = "Very Negative"
            emoji = "U+1F621"

        logging.debug(f"compound: {sentiment_dict['compound']}")
        logging.debug(f"emotion: {tone}")

    except Exception as e:
        logging.error(f"Error on analyze email tone: {e}")

    return {
        'tone': tone,
        'mood_percentages': mood_percentages,
        'emoji': emoji
    }

@app.route('/analyze-email', methods=['POST'])
def analyze_email():
    try:
        logging.info("Start to get email info..")
        target_email = request.json.get('target_email')
        
        grant_id = os.environ.get("NYLAS_GRANT_ID")
        # Fetch the email using Nylas API

        response = nylas.messages.list(
        grant_id,
        query_params={
            "from": target_email,
            "limit":5
        }
        )
        logging.debug(f"Response message: {response}")
        email = response[0][0]

        # Accessing various fields in the Message object
        grant_id = email.grant_id
        from_email = email.from_[0]['email']
        subject = email.subject
        snippet = email.snippet
        body = email.body
        thread_id = email.thread_id
        to_email = email.to[0]['email']
        date = email.date

        #logging.debug(f"email subject: {email.subject}, email body: {email.body}")
    except Exception as e:
        logging.error(f"Error analyzing email: {e}")
        return jsonify({'error': 'Failed to analyze email'}), 400


    # Analyze the emotional tone
    logging.info("Start to analyze enmotion..")
    emotion_result = analyze_email_tone(email.body)
    logging.debug(f"emotion_result: {emotion_result}")


    return jsonify({
        'subject': subject,
        'body': body,
        'tone': emotion_result['tone'],
        'mood_percentages': emotion_result['mood_percentages'],
        'emoji': emotion_result['emoji']
    })


def categorize_email(subject):
    if 'project' in subject.lower():
        return 'Project Updates'
    if 'invoice' in subject.lower():
        return 'Finance'
    return 'General'

@app.route('/add-email', methods=['POST'])
def add_email():
    logging.debug("Received request to add email.")
    
    try:
        data = request.json
        logging.debug(f"Data received: {data}")
        
        collection.insert_one(data)
        logging.info("Email added successfully.")
        return jsonify({'message': 'Email added successfully'}), 201

    except Exception as e:
        logging.error(f"Error adding email: {e}")
        return jsonify({'error': 'Failed to add email'}), 500

# @app.route('/parse-email', methods=['POST'])
# def parse_email():
#     email_id = request.json.get('emailId')
#     logging.debug(f"Email Id received: {email_id}")
#     headers = {'Authorization': f'Bearer {os.getenv("NYLAS_ACCESS_TOKEN")}'}
    
#     response = requests.get(f'https://api.nylas.com/messages/{email_id}', headers=headers)
#     if response.status_code != 200:
#         logging.error(f"Error adding email: {e}")
#         return jsonify({'error': 'Failed to retrieve email'}), 500
    
#     logging.info("Email added successfully.")

#     email = response.json()
#     category = categorize_email(email['subject'])

#     email_data = {
#         'subject': email['subject'],
#         'body': email['snippet'],
#         'category': category,
#         'dateReceived': email['date_received']
#     }
    
#     collection.insert_one(email_data)
    
#     return jsonify({'message': 'Email parsed and stored successfully', 'emailData': email_data})



@app.route('/get-emails', methods=['GET'])
def get_emails():
    logging.debug("Received request to get emails.")
    
    try:
        emails = list(collection.find())
        logging.debug(f"Emails retrieved: {emails}")
        
        return jsonify(emails), 200

    except Exception as e:
        logging.error(f"Error retrieving emails: {e}")
        return jsonify({'error': 'Failed to retrieve emails'}), 500

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = collection.find({
        '$text': {'$search': query}
    })
    return jsonify(list(results))

if __name__ == '__main__':
    logging.info("Starting Flask server...")
    app.run(port=3000)
