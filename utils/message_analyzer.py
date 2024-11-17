from datetime import datetime
import re
from typing import Dict, List, Optional
from openai import OpenAI

class MessageAnalyzer:
    def __init__(self):
        self.client = OpenAI()  # Make sure you have OPENAI_API_KEY in your environment variables
        
    def analyze_message_content(self, message: str, session_messages: List[Dict]) -> Dict[str, bool]:
        """
        Analyze a user message using LLM to detect various information types
        """
        # Construct the analysis prompt
        prompt = self._construct_analysis_prompt(message, session_messages)
        
        # Get LLM response
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": """You are an expert at analyzing messages. 
                Respond only in JSON format with boolean values for these keys:
                has_name, has_contact, has_legal_description, has_yes_no_response, has_documents"""
            }, {
                "role": "user",
                "content": prompt
            }],
            response_format={ "type": "json_object" }
        )
        
        # Parse the JSON response
        try:
            analysis = eval(response.choices[0].message.content)
            return analysis
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                'has_name': False,
                'has_contact': False,
                'has_legal_description': False,
                'has_yes_no_response': False,
                'has_documents': False
            }

    def _construct_analysis_prompt(self, message: str, session_messages: List[Dict]) -> str:
        """
        Construct a prompt for the LLM to analyze the message
        """
        previous_message = session_messages[-2]['content'] if len(session_messages) > 1 else "No previous message"
        
        return f"""Please analyze this message and determine if it contains specific types of information.
        
Current message: "{message}"
Previous message: "{previous_message}"

Analyze for:
1. Name: Does it contain a person's name or name introduction?
2. Contact: Does it contain contact information (email, phone, etc.)?
3. Legal description: Does it describe a legal situation (should be more than 20 words and contain legal context)?
4. Yes/No response: Is this a yes/no response to the previous message?
5. Documents: Does it mention or reference any documents or attachments?

Respond with a JSON object containing boolean values for:
has_name, has_contact, has_legal_description, has_yes_no_response, has_documents"""

def process_user_message(message: str, session) -> Dict[str, bool]:
    """
    Process a new user message and update session information
    """
    # Add message to session history
    session.messages.append({
        'role': 'user',
        'content': message,
        'timestamp': datetime.now()
    })
    
    # Analyze the message
    analyzer = MessageAnalyzer()
    analysis = analyzer.analyze_message_content(message, session.messages)
    
    # Update session tracking
    if analysis['has_name']:
        session.has_provided_name = True
    if analysis['has_contact']:
        session.has_provided_contact = True
    if analysis['has_legal_description']:
        session.has_provided_legal_description = True
    if analysis['has_documents']:
        session.has_provided_documents = True
    
    return analysis