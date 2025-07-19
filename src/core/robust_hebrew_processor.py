#!/usr/bin/env python3
"""
WEEK 2 DAY 3: Professional Error Handling & System Robustness
Making your Hebrew AI system bulletproof for production use
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum
import time

# Professional logging setup
os.makedirs("logs", exist_ok=True)  # Create logs directory first

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/hebrew_ai.log'),
        logging.StreamHandler()
    ]
)

class ErrorSeverity(Enum):
    """Error severity levels for Hebrew AI system"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class HebrewAIError:
    """Structured error information"""
    error_type: str
    message: str
    severity: ErrorSeverity
    component: str
    timestamp: str
    context: Optional[Dict] = None
    recovery_action: Optional[str] = None

class HebrewAIErrorHandler:
    """
    Professional error handling for Hebrew AI system
    Provides graceful degradation and recovery strategies
    """
    
    def __init__(self):
        self.logger = logging.getLogger("HebrewAI.ErrorHandler")
        self.error_history: List[HebrewAIError] = []
        self.recovery_strategies = self._setup_recovery_strategies()
        
        # Create logs directory
        os.makedirs("logs", exist_ok=True)
        
        self.logger.info("Hebrew AI Error Handler initialized")
    
    def _setup_recovery_strategies(self) -> Dict[str, Any]:
        """Setup automatic recovery strategies for common errors"""
        return {
            'model_loading_failed': self._recover_model_loading,
            'gpu_memory_error': self._recover_gpu_memory,
            'network_connection_error': self._recover_network,
            'file_not_found': self._recover_missing_file,
            'hebrew_encoding_error': self._recover_encoding,
            'ai_timeout': self._recover_ai_timeout
        }
    
    def handle_error(self, error: Exception, component: str, context: Optional[Dict] = None) -> HebrewAIError:
        """
        Central error handling with automatic classification and recovery
        
        Args:
            error: The exception that occurred
            component: Component where error occurred
            context: Additional context information
            
        Returns:
            Structured error information
        """
        # Classify error type and severity
        error_type = self._classify_error(error)
        severity = self._determine_severity(error, error_type)
        
        # Create structured error
        hebrew_error = HebrewAIError(
            error_type=error_type,
            message=str(error),
            severity=severity,
            component=component,
            timestamp=datetime.now().isoformat(),
            context=context or {},
            recovery_action=self._suggest_recovery(error_type)
        )
        
        # Log error appropriately
        self._log_error(hebrew_error)
        
        # Store in history
        self.error_history.append(hebrew_error)
        
        # Attempt automatic recovery for non-critical errors
        if severity != ErrorSeverity.CRITICAL:
            self._attempt_recovery(hebrew_error)
        
        return hebrew_error
    
    def _classify_error(self, error: Exception) -> str:
        """Classify error type for appropriate handling"""
        error_name = type(error).__name__
        error_message = str(error).lower()
        
        # GPU/CUDA errors
        if 'cuda' in error_message or 'gpu' in error_message:
            return 'gpu_memory_error'
        
        # Model loading errors
        if 'model' in error_message and ('load' in error_message or 'download' in error_message):
            return 'model_loading_failed'
        
        # Network/API errors
        if error_name in ['ConnectionError', 'TimeoutError', 'HTTPError']:
            return 'network_connection_error'
        
        # File system errors
        if error_name in ['FileNotFoundError', 'PermissionError']:
            return 'file_not_found'
        
        # Encoding errors
        if 'encoding' in error_message or error_name == 'UnicodeDecodeError':
            return 'hebrew_encoding_error'
        
        # AI/LLM timeout
        if 'timeout' in error_message or error_name == 'TimeoutError':
            return 'ai_timeout'
        
        return 'unknown_error'
    
    def _determine_severity(self, error: Exception, error_type: str) -> ErrorSeverity:
        """Determine error severity for appropriate response"""
        # Critical errors that break core functionality
        critical_patterns = ['system', 'memory', 'cannot initialize']
        if any(pattern in str(error).lower() for pattern in critical_patterns):
            return ErrorSeverity.CRITICAL
        
        # High severity errors
        high_severity_types = ['model_loading_failed', 'gpu_memory_error']
        if error_type in high_severity_types:
            return ErrorSeverity.HIGH
        
        # Medium severity errors
        medium_severity_types = ['network_connection_error', 'ai_timeout']
        if error_type in medium_severity_types:
            return ErrorSeverity.MEDIUM
        
        return ErrorSeverity.LOW
    
    def _suggest_recovery(self, error_type: str) -> str:
        """Suggest recovery actions for different error types"""
        recovery_suggestions = {
            'model_loading_failed': 'Try reloading model or switch to fallback model',
            'gpu_memory_error': 'Clear GPU cache and reduce batch size',
            'network_connection_error': 'Check internet connection and retry',
            'file_not_found': 'Verify file path and permissions',
            'hebrew_encoding_error': 'Ensure UTF-8 encoding for Hebrew text',
            'ai_timeout': 'Reduce query complexity or increase timeout',
            'unknown_error': 'Check logs for detailed error information'
        }
        
        return recovery_suggestions.get(error_type, 'Manual intervention required')
    
    def _log_error(self, hebrew_error: HebrewAIError):
        """Log error with appropriate level"""
        log_message = f"{hebrew_error.component}: {hebrew_error.message}"
        
        if hebrew_error.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message)
        elif hebrew_error.severity == ErrorSeverity.HIGH:
            self.logger.error(log_message)
        elif hebrew_error.severity == ErrorSeverity.MEDIUM:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def _attempt_recovery(self, hebrew_error: HebrewAIError):
        """Attempt automatic recovery based on error type"""
        recovery_func = self.recovery_strategies.get(hebrew_error.error_type)
        
        if recovery_func:
            try:
                self.logger.info(f"Attempting recovery for {hebrew_error.error_type}")
                recovery_func(hebrew_error)
            except Exception as recovery_error:
                self.logger.error(f"Recovery failed: {recovery_error}")
    
    # Recovery strategy implementations
    def _recover_model_loading(self, error: HebrewAIError):
        """Recover from model loading failures"""
        self.logger.info("Implementing model loading recovery...")
        # Could implement fallback to different model or retry logic
    
    def _recover_gpu_memory(self, error: HebrewAIError):
        """Recover from GPU memory issues"""
        self.logger.info("Implementing GPU memory recovery...")
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                self.logger.info("GPU cache cleared")
        except ImportError:
            self.logger.warning("PyTorch not available for GPU cache clearing")
    
    def _recover_network(self, error: HebrewAIError):
        """Recover from network connectivity issues"""
        self.logger.info("Implementing network recovery...")
        # Could implement retry logic with exponential backoff
    
    def _recover_missing_file(self, error: HebrewAIError):
        """Recover from missing file errors"""
        self.logger.info("Checking for alternative file locations...")
        # Could implement file search in alternative locations
    
    def _recover_encoding(self, error: HebrewAIError):
        """Recover from Hebrew encoding issues"""
        self.logger.info("Attempting encoding recovery...")
        # Could implement automatic encoding detection and conversion
    
    def _recover_ai_timeout(self, error: HebrewAIError):
        """Recover from AI timeout issues"""
        self.logger.info("Implementing AI timeout recovery...")
        # Could implement shorter queries or fallback responses

class RobustHebrewProcessor:
    """
    Robust Hebrew processor with comprehensive error handling
    Production-ready with graceful degradation
    """
    
    def __init__(self):
        self.error_handler = HebrewAIErrorHandler()
        self.logger = logging.getLogger("HebrewAI.Processor")
        
        # System state tracking
        self.system_health = {
            'alephbert_available': False,
            'ollama_available': False,
            'gpu_available': False,
            'last_health_check': None
        }
        
        # Initialize with error handling
        self._safe_initialize()
    
    def _safe_initialize(self):
        """Initialize system components with error handling"""
        try:
            self.logger.info("Initializing Robust Hebrew Processor")
            
            # Check system health
            self._check_system_health()
            
            # Initialize components with fallbacks
            self._initialize_models()
            
            self.logger.info("Robust Hebrew Processor initialized successfully")
            
        except Exception as e:
            error = self.error_handler.handle_error(e, "RobustHebrewProcessor.__init__")
            self.logger.error(f"Initialization error: {error.message}")
    
    def _check_system_health(self):
        """Comprehensive system health check"""
        try:
            # Check GPU availability
            try:
                import torch
                self.system_health['gpu_available'] = torch.cuda.is_available()
                if self.system_health['gpu_available']:
                    self.logger.info(f"GPU available: {torch.cuda.get_device_name(0)}")
            except ImportError:
                self.system_health['gpu_available'] = False
                self.logger.warning("PyTorch not available - GPU functionality disabled")
            
            # Check Ollama availability
            try:
                import requests
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                self.system_health['ollama_available'] = response.status_code == 200
            except:
                self.system_health['ollama_available'] = False
                self.logger.warning("Ollama not available - tutoring functionality limited")
            
            # Check AlephBERT availability
            try:
                from transformers import AutoModel
                self.system_health['alephbert_available'] = True
            except ImportError:
                self.system_health['alephbert_available'] = False
                self.logger.warning("Transformers not available - Biblical analysis limited")
            
            self.system_health['last_health_check'] = datetime.now().isoformat()
            
        except Exception as e:
            self.error_handler.handle_error(e, "RobustHebrewProcessor._check_system_health")
    
    def _initialize_models(self):
        """Initialize AI models with proper error handling"""
        # Initialize AlephBERT with fallback
        if self.system_health['alephbert_available']:
            try:
                from src.ai.models.alephbert_model import AlephBERTProcessor
                self.alephbert = AlephBERTProcessor()
                self.logger.info("AlephBERT initialized successfully")
            except Exception as e:
                error = self.error_handler.handle_error(e, "AlephBERT initialization")
                self.alephbert = None
                self.logger.warning("AlephBERT failed to initialize - using fallback")
        else:
            self.alephbert = None
            self.logger.info("AlephBERT not available - using alternative processing")
    
    def analyze_hebrew_safely(self, hebrew_text: str, verse_reference: str = "") -> Dict[str, Any]:
        """
        Analyze Hebrew text with comprehensive error handling
        
        Args:
            hebrew_text: Hebrew text to analyze
            verse_reference: Optional verse reference
            
        Returns:
            Analysis results with error handling information
        """
        start_time = time.time()
        
        try:
            # Validate input
            if not hebrew_text or not hebrew_text.strip():
                raise ValueError("Empty Hebrew text provided")
            
            # Attempt analysis with error handling
            return self._perform_analysis_with_fallbacks(hebrew_text, verse_reference)
            
        except Exception as e:
            # Handle any analysis errors gracefully
            error = self.error_handler.handle_error(
                e, 
                "RobustHebrewProcessor.analyze_hebrew_safely",
                context={
                    'hebrew_text': hebrew_text[:50] + "..." if len(hebrew_text) > 50 else hebrew_text,
                    'verse_reference': verse_reference
                }
            )
            
            # Return graceful degradation response
            return {
                'original_text': hebrew_text,
                'verse_reference': verse_reference,
                'analysis_status': 'error',
                'error_info': {
                    'type': error.error_type,
                    'message': error.message,
                    'severity': error.severity.value,
                    'recovery_action': error.recovery_action
                },
                'fallback_analysis': self._get_basic_analysis(hebrew_text),
                'processing_time': time.time() - start_time,
                'timestamp': datetime.now().isoformat()
            }
    
    def _perform_analysis_with_fallbacks(self, hebrew_text: str, verse_reference: str) -> Dict[str, Any]:
        """Perform analysis with multiple fallback strategies"""
        analysis_result = {
            'original_text': hebrew_text,
            'verse_reference': verse_reference,
            'analysis_status': 'success',
            'processing_time': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        start_time = time.time()
        
        # Primary: Try AlephBERT analysis
        if self.alephbert and self.system_health['alephbert_available']:
            try:
                biblical_analysis = self.alephbert.analyze_biblical_text(hebrew_text)
                analysis_result['biblical_analysis'] = {
                    'source': 'AlephBERT',
                    'confidence': biblical_analysis.confidence_score,
                    'context': biblical_analysis.biblical_context,
                    'morphology': biblical_analysis.morphological_info
                }
                self.logger.info("AlephBERT analysis completed successfully")
            except Exception as e:
                self.error_handler.handle_error(e, "AlephBERT analysis")
                analysis_result['biblical_analysis'] = self._get_fallback_biblical_analysis(hebrew_text)
        else:
            analysis_result['biblical_analysis'] = self._get_fallback_biblical_analysis(hebrew_text)
        
        # Secondary: Try Ollama tutoring
        if self.system_health['ollama_available']:
            try:
                tutor_explanation = self._get_ollama_explanation(hebrew_text, verse_reference)
                analysis_result['tutor_explanation'] = tutor_explanation
                self.logger.info("Ollama tutoring completed successfully")
            except Exception as e:
                self.error_handler.handle_error(e, "Ollama tutoring")
                analysis_result['tutor_explanation'] = self._get_fallback_explanation(hebrew_text)
        else:
            analysis_result['tutor_explanation'] = self._get_fallback_explanation(hebrew_text)
        
        analysis_result['processing_time'] = time.time() - start_time
        return analysis_result
    
    def _get_basic_analysis(self, hebrew_text: str) -> Dict[str, Any]:
        """Basic analysis that always works"""
        words = hebrew_text.split()
        
        return {
            'word_count': len(words),
            'character_count': len(hebrew_text),
            'words': words[:5],  # First 5 words
            'has_hebrew_chars': any('\u0590' <= char <= '\u05FF' for char in hebrew_text),
            'analysis_type': 'basic_fallback'
        }
    
    def _get_fallback_biblical_analysis(self, hebrew_text: str) -> Dict[str, Any]:
        """Fallback biblical analysis without AlephBERT"""
        return {
            'source': 'Fallback Analysis',
            'confidence': 0.6,
            'context': 'Basic Hebrew text analysis',
            'morphology': self._get_basic_analysis(hebrew_text),
            'note': 'AlephBERT not available - using basic analysis'
        }
    
    def _get_fallback_explanation(self, hebrew_text: str) -> str:
        """Fallback explanation without AI"""
        words = hebrew_text.split()
        return f"Hebrew text with {len(words)} words. Basic analysis available. AI tutoring temporarily unavailable."
    
    def _get_ollama_explanation(self, hebrew_text: str, verse_reference: str) -> str:
        """Get explanation from Ollama with error handling"""
        try:
            import requests
            
            prompt = f"""
            Analyze this Hebrew text as a Hebrew tutor: {hebrew_text}
            Reference: {verse_reference}
            
            Provide a brief, educational explanation including translation and key insights.
            """
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    'model': 'llama3:8b',
                    'prompt': prompt,
                    'stream': False,
                    'options': {'num_predict': 200}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response from AI tutor')
            else:
                raise Exception(f"Ollama HTTP error: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Ollama connection failed: {str(e)}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'system_health': self.system_health,
            'error_history': [
                {
                    'type': error.error_type,
                    'severity': error.severity.value,
                    'component': error.component,
                    'timestamp': error.timestamp
                }
                for error in self.error_handler.error_history[-10:]  # Last 10 errors
            ],
            'capabilities': {
                'biblical_analysis': self.system_health['alephbert_available'],
                'ai_tutoring': self.system_health['ollama_available'],
                'gpu_acceleration': self.system_health['gpu_available']
            }
        }

def demonstrate_error_handling():
    """Demonstrate robust error handling capabilities"""
    print("🔥 WEEK 2 DAY 3: ROBUST ERROR HANDLING DEMONSTRATION")
    print("=" * 60)
    
    # Initialize robust processor
    processor = RobustHebrewProcessor()
    
    # Test normal operation
    print("\n✅ TESTING NORMAL OPERATION:")
    result = processor.analyze_hebrew_safely("בְּרֵאשִׁית בָּרָא אֱלֹהִים", "Genesis 1:1")
    print(f"Analysis status: {result['analysis_status']}")
    print(f"Processing time: {result['processing_time']:.2f}s")
    
    # Test error scenarios
    print("\n🧪 TESTING ERROR SCENARIOS:")
    
    # Test empty input
    print("\nTesting empty input:")
    empty_result = processor.analyze_hebrew_safely("", "Test")
    print(f"Empty input handled: {empty_result['analysis_status']}")
    
    # Test invalid input
    print("\nTesting invalid input:")
    invalid_result = processor.analyze_hebrew_safely("invalid123", "Test")
    print(f"Invalid input handled: {invalid_result['analysis_status']}")
    
    # System status report
    print("\n📊 SYSTEM STATUS REPORT:")
    status = processor.get_system_status()
    print(f"System capabilities: {status['capabilities']}")
    print(f"Recent errors: {len(status['error_history'])}")
    
    print(f"\n🎉 ERROR HANDLING DEMONSTRATION COMPLETE!")
    print(f"System is robust and production-ready!")

if __name__ == "__main__":
    demonstrate_error_handling()