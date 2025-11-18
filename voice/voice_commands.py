"""
Voice Command Processing for Autonomous UI Engine
Phase 6: Innovation - Voice Interface

Processes and executes voice commands.
"""

import logging
from typing import Dict, Any, Optional, Callable
from pathlib import Path
import asyncio

from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech

logger = logging.getLogger(__name__)


class VoiceCommandProcessor:
    """
    Processes voice commands and executes corresponding actions.
    """
    
    def __init__(self):
        """Initialize voice command processor."""
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self._commands: Dict[str, Callable] = {}
        self._register_default_commands()
        
    def _register_default_commands(self) -> None:
        """Register default voice commands."""
        self.register_command("generate ui", self._generate_ui)
        self.register_command("create component", self._create_component)
        self.register_command("modify theme", self._modify_theme)
        self.register_command("show status", self._show_status)
        self.register_command("help", self._show_help)
    
    def register_command(self, command: str, handler: Callable) -> None:
        """
        Register a voice command handler.
        
        Args:
            command: Command phrase
            handler: Async function to handle command
        """
        self._commands[command.lower()] = handler
        logger.debug(f"Registered voice command: {command}")
    
    async def process_audio(self, audio_file: Path) -> Dict[str, Any]:
        """
        Process audio file and execute command.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Dictionary with execution result
        """
        try:
            # Transcribe audio
            transcription = await self.stt.transcribe(audio_file)
            text = transcription.get("text", "").lower()
            
            logger.info(f"Transcribed: {text}")
            
            # Match command
            command = self._match_command(text)
            
            if command:
                # Execute command
                result = await self._commands[command](text)
                
                # Respond with voice
                await self.tts.speak(result.get("response", "Command executed."))
                
                return {
                    "success": True,
                    "command": command,
                    "transcription": text,
                    "result": result
                }
            else:
                response = "Sorry, I didn't understand that command."
                await self.tts.speak(response)
                
                return {
                    "success": False,
                    "transcription": text,
                    "error": "Command not recognized"
                }
                
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            await self.tts.speak("An error occurred while processing your command.")
            
            return {
                "success": False,
                "error": str(e)
            }
    
    async def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process text command directly.
        
        Args:
            text: Command text
            
        Returns:
            Dictionary with execution result
        """
        command = self._match_command(text.lower())
        
        if command:
            result = await self._commands[command](text)
            await self.tts.speak(result.get("response", "Command executed."))
            
            return {
                "success": True,
                "command": command,
                "result": result
            }
        
        return {
            "success": False,
            "error": "Command not recognized"
        }
    
    def _match_command(self, text: str) -> Optional[str]:
        """
        Match transcribed text to registered command.
        
        Args:
            text: Transcribed text
            
        Returns:
            Matched command or None
        """
        for command in self._commands.keys():
            if command in text:
                return command
        return None
    
    # Default command handlers
    
    async def _generate_ui(self, text: str) -> Dict[str, Any]:
        """Handle UI generation command."""
        logger.info("Executing: Generate UI")
        return {
            "action": "generate_ui",
            "response": "Generating your UI now. This will take a moment."
        }
    
    async def _create_component(self, text: str) -> Dict[str, Any]:
        """Handle component creation command."""
        logger.info("Executing: Create Component")
        return {
            "action": "create_component",
            "response": "Creating component for you."
        }
    
    async def _modify_theme(self, text: str) -> Dict[str, Any]:
        """Handle theme modification command."""
        logger.info("Executing: Modify Theme")
        return {
            "action": "modify_theme",
            "response": "Modifying the theme as requested."
        }
    
    async def _show_status(self, text: str) -> Dict[str, Any]:
        """Handle status display command."""
        logger.info("Executing: Show Status")
        return {
            "action": "show_status",
            "response": "All systems operational. Everything is running smoothly."
        }
    
    async def _show_help(self, text: str) -> Dict[str, Any]:
        """Handle help command."""
        logger.info("Executing: Show Help")
        commands = ", ".join(list(self._commands.keys())[:3])
        return {
            "action": "show_help",
            "response": f"Available commands include: {commands}, and more."
        }
    
    def list_commands(self) -> list:
        """Get list of available commands."""
        return list(self._commands.keys())


# Interactive voice interface
class VoiceInterface:
    """Interactive voice interface for the UI Engine."""
    
    def __init__(self):
        """Initialize voice interface."""
        self.processor = VoiceCommandProcessor()
        self.active = False
        
    async def start(self) -> None:
        """Start voice interface."""
        self.active = True
        await self.processor.tts.speak("Voice interface activated. How can I help you?")
        logger.info("Voice interface started")
    
    async def stop(self) -> None:
        """Stop voice interface."""
        self.active = False
        await self.processor.tts.speak("Voice interface deactivated. Goodbye!")
        logger.info("Voice interface stopped")
    
    async def listen_and_respond(self, audio_file: Path) -> Dict[str, Any]:
        """
        Listen to audio and respond.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Processing result
        """
        if not self.active:
            return {"error": "Voice interface not active"}
        
        return await self.processor.process_audio(audio_file)


# Example usage
async def example_usage():
    """Example of using voice commands."""
    processor = VoiceCommandProcessor()
    
    # List available commands
    print("Available commands:")
    for cmd in processor.list_commands():
        print(f"  - {cmd}")
    
    # Process text command
    result = await processor.process_text("generate ui for dashboard")
    print(f"\nResult: {result}")
    
    # Interactive interface
    interface = VoiceInterface()
    await interface.start()
    # In production: await interface.listen_and_respond(Path("audio.wav"))
    await interface.stop()
    
    print("\nVoice command processing ready")


if __name__ == "__main__":
    asyncio.run(example_usage())
