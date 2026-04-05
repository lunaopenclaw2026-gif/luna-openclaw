#!/usr/bin/env python3
"""
Luna Phone System - Complete Integration
Orchestrates Twilio + ElevenLabs Conversational AI for phone calls

Usage:
    python3 luna_phone_system.py start       # Start the server
    python3 luna_phone_system.py test        # Make test call
    python3 luna_phone_system.py call <num>  # Call a number
"""

import os
import sys
import json
import logging
from typing import Optional
from datetime import datetime
from twilio.rest import Client
from elevenlabs.client import ElevenLabs

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+14159034051")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
CHRISTOPHER_PHONE = os.getenv("CHRISTOPHER_PHONE", "+4915770368632")

HEROKU_APP_URL = os.getenv("HEROKU_APP_URL")  # e.g., https://luna-phone-system.herokuapp.com

# Initialize clients
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


class LunaPhoneSystem:
    """
    Main orchestrator for Luna's phone system
    """
    
    def __init__(self):
        self.call_history = []
        self.active_calls = {}
        
    def validate_config(self) -> bool:
        """Validate all required environment variables"""
        required = [
            "TWILIO_ACCOUNT_SID",
            "TWILIO_AUTH_TOKEN",
            "ELEVENLABS_API_KEY",
            "HEROKU_APP_URL"
        ]
        
        missing = [var for var in required if not os.getenv(var)]
        
        if missing:
            logger.error(f"Missing environment variables: {', '.join(missing)}")
            return False
        
        logger.info("✓ All required environment variables configured")
        return True
    
    def setup_twilio_webhook(self) -> bool:
        """
        Configure Twilio webhook to point to Heroku app
        This tells Twilio where to send incoming calls
        """
        try:
            phone_number = twilio_client.incoming_phone_numbers.list(
                phone_number=TWILIO_PHONE_NUMBER
            )[0]
            
            webhook_url = f"{HEROKU_APP_URL}/incoming-call"
            
            logger.info(f"Setting up Twilio webhook: {webhook_url}")
            
            phone_number.update(
                voice_url=webhook_url,
                voice_method="POST",
            )
            
            logger.info("✓ Twilio webhook configured")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Twilio webhook: {e}")
            return False
    
    def initiate_call(
        self,
        to_number: str,
        purpose: str = "general",
        context: str = ""
    ) -> Optional[str]:
        """
        Initiate outbound call from Luna to a phone number
        
        Args:
            to_number: Phone number to call (e.g., +49...)
            purpose: Purpose of call (restaurant_booking, appointment, etc.)
            context: Additional context for the call
            
        Returns:
            Call SID if successful, None otherwise
        """
        try:
            logger.info(f"Initiating call to {to_number} (purpose: {purpose})")
            
            call = twilio_client.calls.create(
                to=to_number,
                from_=TWILIO_PHONE_NUMBER,
                url=f"{HEROKU_APP_URL}/outbound-call-handler",
                method="POST",
                record=True,
            )
            
            self.call_history.append({
                "timestamp": datetime.now().isoformat(),
                "call_sid": call.sid,
                "to": to_number,
                "from": TWILIO_PHONE_NUMBER,
                "purpose": purpose,
                "context": context,
                "status": call.status
            })
            
            logger.info(f"✓ Call initiated: {call.sid}")
            return call.sid
            
        except Exception as e:
            logger.error(f"Failed to initiate call: {e}")
            return None
    
    def get_call_status(self, call_sid: str) -> Optional[str]:
        """Get status of a call"""
        try:
            call = twilio_client.calls(call_sid).fetch()
            return call.status
        except Exception as e:
            logger.error(f"Failed to get call status: {e}")
            return None
    
    def verify_elevenlabs_connection(self) -> bool:
        """Verify ElevenLabs API connection"""
        try:
            # Try to list agents
            agents = elevenlabs_client.conversational_ai.agents.list()
            logger.info(f"✓ ElevenLabs connected ({len(agents.agents)} agents found)")
            return True
        except Exception as e:
            logger.error(f"ElevenLabs connection failed: {e}")
            return False
    
    def print_status(self):
        """Print system status"""
        print("\n" + "="*60)
        print("LUNA PHONE SYSTEM STATUS")
        print("="*60)
        
        print("\n📱 Twilio Configuration:")
        print(f"  Phone Number: {TWILIO_PHONE_NUMBER}")
        print(f"  Account: {TWILIO_ACCOUNT_SID[:8]}...")
        
        print("\n🔊 ElevenLabs Configuration:")
        print(f"  API Key: {ELEVENLABS_API_KEY[:10]}...")
        
        print("\n🌐 Heroku Deployment:")
        print(f"  URL: {HEROKU_APP_URL}")
        
        print("\n📞 Call History:")
        if self.call_history:
            for call in self.call_history[-5:]:  # Last 5 calls
                print(f"  - {call['timestamp']}: {call['to']} ({call['purpose']})")
        else:
            print("  (No calls yet)")
        
        print("\n" + "="*60 + "\n")


def main():
    """Main CLI interface"""
    
    system = LunaPhoneSystem()
    
    if len(sys.argv) < 2:
        print("Usage: python3 luna_phone_system.py [command]")
        print("\nCommands:")
        print("  start          - Start the Flask server")
        print("  status         - Show system status")
        print("  test           - Make a test call to Christopher")
        print("  call <number>  - Call a phone number")
        print("  validate       - Validate configuration")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "status":
        system.print_status()
        
    elif command == "validate":
        print("Validating configuration...\n")
        if system.validate_config():
            if system.verify_elevenlabs_connection():
                print("✓ All checks passed!")
            else:
                print("✗ ElevenLabs connection failed")
                sys.exit(1)
        else:
            sys.exit(1)
    
    elif command == "test":
        logger.info(f"Initiating test call to {CHRISTOPHER_PHONE}...")
        call_sid = system.initiate_call(
            CHRISTOPHER_PHONE,
            purpose="test",
            context="This is a test call to verify the system is working"
        )
        if call_sid:
            logger.info(f"Test call initiated: {call_sid}")
        else:
            logger.error("Failed to initiate test call")
            sys.exit(1)
    
    elif command == "call" and len(sys.argv) > 2:
        to_number = sys.argv[2]
        purpose = sys.argv[3] if len(sys.argv) > 3 else "general"
        
        logger.info(f"Calling {to_number}...")
        call_sid = system.initiate_call(to_number, purpose=purpose)
        if call_sid:
            logger.info(f"Call initiated: {call_sid}")
        else:
            logger.error("Failed to initiate call")
            sys.exit(1)
    
    elif command == "start":
        logger.info("Starting Luna Phone System...")
        
        if not system.validate_config():
            sys.exit(1)
        
        if not system.verify_elevenlabs_connection():
            sys.exit(1)
        
        if not system.setup_twilio_webhook():
            logger.warning("Warning: Twilio webhook setup failed, but continuing...")
        
        system.print_status()
        
        logger.info("Starting Flask server...")
        # Import and run Flask app
        from twilio_elevenlabs_integration import app
        
        port = int(os.getenv("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=False)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
