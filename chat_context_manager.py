"""
Chat Context Manager
Loads and manages conversation history for Luna
Allows Luna to reference everything from our chat when speaking on phone
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class ChatContextManager:
    """
    Manages Luna's knowledge base from chat history
    Injects relevant context into phone calls
    """
    
    def __init__(self, workspace_dir: str = "/Users/luna-openclaw/.openclaw/workspace"):
        self.workspace_dir = workspace_dir
        self.memory_dir = os.path.join(workspace_dir, "memory")
        self.context_cache = {}
        
    def load_memory_files(self) -> str:
        """
        Load all memory files and compile into a context string
        This is what Luna knows about you
        """
        context_parts = []
        
        # Load MEMORY.md (long-term memory)
        memory_file = os.path.join(self.workspace_dir, "MEMORY.md")
        if os.path.exists(memory_file):
            with open(memory_file, 'r') as f:
                context_parts.append(f"=== LONG-TERM MEMORY ===\n{f.read()}\n")
        
        # Load today's memory file
        today_file = os.path.join(self.memory_dir, f"{datetime.now().strftime('%Y-%m-%d')}.md")
        if os.path.exists(today_file):
            with open(today_file, 'r') as f:
                context_parts.append(f"=== TODAY'S NOTES ===\n{f.read()}\n")
        
        # Load USER.md (who is Christopher)
        user_file = os.path.join(self.workspace_dir, "USER.md")
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                context_parts.append(f"=== ABOUT CHRISTOPHER ===\n{f.read()}\n")
        
        return "\n".join(context_parts)
    
    def get_restaurant_context(self) -> str:
        """
        Extract restaurant-related information from memory
        Used when Luna needs to book restaurants
        """
        context = self.load_memory_files()
        
        restaurant_info = []
        
        # Look for restaurant mentions
        if "restaurant" in context.lower():
            restaurant_info.append("Christopher has mentioned specific restaurants")
        
        if "eversports" in context.lower():
            restaurant_info.append("Christopher uses Eversports for bookings")
        
        if "munich" in context.lower() or "münchen" in context.lower():
            restaurant_info.append("Christopher is in Munich (Deutschland)")
        
        return "\n".join(restaurant_info) if restaurant_info else "No specific restaurant preferences found"
    
    def get_appointment_context(self) -> str:
        """Get appointment and scheduling preferences"""
        context = self.load_memory_files()
        
        appointment_info = []
        
        # Parse for appointment-related context
        if "tennis" in context.lower():
            appointment_info.append("Christopher enjoys tennis")
        
        if "appointment" in context.lower():
            appointment_info.append("Christopher has upcoming appointments")
        
        return "\n".join(appointment_info) if appointment_info else "No specific appointments found"
    
    def get_system_prompt(self, call_type: str = "general") -> str:
        """
        Generate a system prompt for Luna with full context
        
        Args:
            call_type: "general", "restaurant", "appointment", etc.
        """
        
        base_prompt = """You are Luna, an AI assistant for Christopher Baumann.

CRITICAL: You have full knowledge of everything we've discussed in our chat.
When on a phone call, reference this knowledge naturally.

PERSONALITY:
- Friendly and professional
- Native German speaker (prefer German, but can do English)
- Direct and efficient
- Problem-solver
- Conversational on phone (concise, natural)

CAPABILITIES:
- Book restaurants
- Schedule appointments  
- Book tennis courts
- Answer questions about Christopher's preferences
- Make and receive calls

INSTRUCTIONS:
1. When answering phone calls, be warm and professional
2. If someone calls, identify yourself as Luna
3. Understand what they need and help
4. If it's a restaurant, try to book with confidence
5. Always be honest about what you can do
6. If unsure, ask clarifying questions

TONE ON PHONE:
- Clear enunciation
- Natural pace (not too fast)
- Friendly but professional
- German: Use formal "Sie" unless told otherwise

---

CHRISTOPHER'S CONTEXT:
"""
        
        # Add context based on call type
        if call_type == "restaurant":
            base_prompt += "\n" + self.get_restaurant_context()
        elif call_type == "appointment":
            base_prompt += "\n" + self.get_appointment_context()
        else:
            # General context
            base_prompt += "\n" + self.load_memory_files()
        
        return base_prompt
    
    def get_call_context(self, to_number: str, purpose: str = "general") -> Dict:
        """
        Get context for a specific outbound call
        
        Returns dict with:
        - system_prompt: What Luna should know
        - context_summary: Short summary for the call
        """
        
        context_summary = f"Call to {to_number}"
        
        if purpose == "restaurant_booking":
            context_summary = f"Restaurant booking call to {to_number}"
        elif purpose == "appointment":
            context_summary = f"Appointment scheduling call to {to_number}"
        
        return {
            "system_prompt": self.get_system_prompt(purpose),
            "context_summary": context_summary,
            "call_purpose": purpose,
            "call_to": to_number,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_call_log(self, call_data: Dict):
        """Save call details for future reference"""
        log_file = os.path.join(self.workspace_dir, "call_logs.json")
        
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(call_data)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)


def main():
    """Test the context manager"""
    manager = ChatContextManager()
    
    print("=== Luna Phone Context ===\n")
    
    # Test general context
    print("General Context:")
    print(manager.get_system_prompt("general")[:500] + "...\n")
    
    # Test restaurant context
    print("Restaurant Context:")
    print(manager.get_restaurant_context() + "\n")
    
    # Test appointment context
    print("Appointment Context:")
    print(manager.get_appointment_context() + "\n")


if __name__ == "__main__":
    main()
