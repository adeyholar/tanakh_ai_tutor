# src/core/hebrew_analyzers.py
"""
Professional Hebrew AI Analyzers - Week 3 Day 1
Object-Oriented Architecture for Hebrew Text Analysis
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from datetime import datetime
import logging
import asyncio

# PyTorch and Transformers imports with type handling
try:
    import torch
    from transformers import AutoTokenizer, AutoModel
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    # Type stubs for when torch isn't available
    torch = None
    AutoTokenizer = None
    AutoModel = None

# Configure logging
logging.basicConfig(level=logging.INFO)

@dataclass
class AnalysisResult:
    """Structured result from Hebrew analysis"""
    word: str
    translation: str
    grammar_info: Dict[str, Any]
    confidence: float
    model_used: str
    timestamp: datetime


class HebrewAnalyzer(ABC):
    """Abstract base class for Hebrew text analyzers"""
    
    def __init__(self, name: str):
        self.name = name
        self.is_available = False
        self.logger = logging.getLogger(f"HebrewAI.{name}")
        self.analysis_count = 0
        
    @abstractmethod
    async def analyze_word(self, word: str) -> AnalysisResult:
        """Analyze a single Hebrew word"""
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the analyzer and check availability"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get analyzer statistics"""
        return {
            "name": self.name,
            "available": self.is_available,
            "analyses_performed": self.analysis_count
        }


class AlephBertAnalyzer(HebrewAnalyzer):
    """Biblical Hebrew specialist using AlephBERT model"""
    
    def __init__(self):
        super().__init__("AlephBERT")
        self.model: Optional[Any] = None  # More flexible typing
        self.tokenizer: Optional[Any] = None  # More flexible typing
        self.device: Optional[Any] = None
        self.model_name = "onlplab/alephbert-base"
        
    def initialize(self) -> bool:
        """Initialize AlephBERT model and check GPU availability"""
        if not TORCH_AVAILABLE:
            self.logger.error("PyTorch and transformers not available")
            return False
            
        try:
            self.logger.info("Initializing AlephBERT analyzer...")
            
            # Check GPU availability
            if torch and torch.cuda.is_available():
                self.device = torch.device("cuda")
                gpu_name = torch.cuda.get_device_name(0)
                self.logger.info(f"GPU detected: {gpu_name}")
            else:
                self.device = torch.device("cpu") if torch else "cpu"
                self.logger.warning("No GPU detected, using CPU")
            
            # Load model and tokenizer
            self.logger.info("Loading AlephBERT model...")
            if AutoTokenizer and AutoModel:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModel.from_pretrained(self.model_name)
                
                # Move to device if available and model is not None
                if self.model is not None and hasattr(self.model, 'to') and self.device:
                    self.model.to(self.device)
                if self.model is not None and hasattr(self.model, 'eval'):
                    self.model.eval()
            
            self.is_available = True
            self.logger.info("AlephBERT initialization successful!")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AlephBERT: {e}")
            self.is_available = False
            return False
    
    async def analyze_word(self, word: str) -> AnalysisResult:
        """Analyze Hebrew word using AlephBERT"""
        if not self.is_available:
            raise RuntimeError("AlephBERT analyzer not initialized")
        
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model or tokenizer not loaded")
        
        try:
            self.logger.debug(f"Analyzing word: {word}")
            
            # Tokenize the Hebrew word - check if tokenizer is callable
            if hasattr(self.tokenizer, '__call__'):
                inputs = self.tokenizer(word, return_tensors="pt", padding=True)
            else:
                # Fallback method
                inputs = self.tokenizer.encode_plus(word, return_tensors="pt", padding=True)
            
            if self.device and hasattr(inputs, 'to'):
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get model embeddings - check if model is callable
            if torch:
                with torch.no_grad():
                    if hasattr(self.model, '__call__'):
                        outputs = self.model(**inputs)
                    else:
                        outputs = self.model.forward(**inputs)
                    # Get the [CLS] token embedding (sentence representation)
                    word_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                    embedding_shape = str(word_embedding.shape)
            else:
                embedding_shape = "N/A"
            
            # Create analysis result
            analysis = AnalysisResult(
                word=word,
                translation=f"[AlephBERT analysis of {word}]",
                grammar_info={
                    "embedding_shape": embedding_shape,
                    "model_confidence": 0.85,
                    "biblical_context": True,
                    "device_used": str(self.device)
                },
                confidence=0.85,
                model_used="AlephBERT",
                timestamp=datetime.now()
            )
            
            self.analysis_count += 1
            self.logger.debug(f"Analysis complete. Total analyses: {self.analysis_count}")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing word '{word}': {e}")
            raise
    
    def get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU utilization information"""
        if torch and self.device and hasattr(self.device, 'type') and self.device.type == "cuda":
            try:
                return {
                    "device": str(self.device),
                    "gpu_name": torch.cuda.get_device_name(0),
                    "memory_allocated": torch.cuda.memory_allocated(0) / 1024**3,  # GB
                    "memory_reserved": torch.cuda.memory_reserved(0) / 1024**3,   # GB
                    "utilization": "Available"
                }
            except Exception:
                return {"device": str(self.device), "gpu_status": "Error getting GPU info"}
        else:
            return {"device": "CPU", "gpu_status": "Not available"}
    
    def cleanup(self):
        """Clean up GPU memory"""
        if torch and self.device and hasattr(self.device, 'type') and self.device.type == "cuda":
            try:
                torch.cuda.empty_cache()
                self.logger.info("GPU memory cleared")
            except Exception as e:
                self.logger.warning(f"Could not clear GPU memory: {e}")


class OllamaAnalyzer(HebrewAnalyzer):
    """Educational Hebrew tutor using Ollama Llama 3"""
    
    def __init__(self):
        super().__init__("Ollama-Llama3")
        self.base_url = "http://localhost:11434"
        self.model_name = "llama3:8b"  # Use the exact model name
        
    def initialize(self) -> bool:
        """Check if Ollama is available"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                if any('llama3' in name for name in model_names):
                    self.is_available = True
                    self.logger.info("Ollama Llama 3 is available!")
                    return True
                else:
                    self.logger.warning("Llama 3 model not found in Ollama")
                    return False
            else:
                self.logger.warning("Ollama service not responding")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to connect to Ollama: {e}")
            self.is_available = False
            return False
    
    async def analyze_word(self, word: str) -> AnalysisResult:
        """Analyze Hebrew word using Ollama"""
        if not self.is_available:
            raise RuntimeError("Ollama analyzer not initialized")
        
        try:
            import requests
            
            prompt = f"""
            Please analyze this Hebrew word: {word}
            
            Provide:
            1. English translation
            2. Grammar information
            3. Biblical context if applicable
            4. Pronunciation guide
            
            Be educational and encouraging for a Hebrew learner.
            """
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result.get('response', 'No analysis available')
                
                analysis = AnalysisResult(
                    word=word,
                    translation=f"Educational analysis: {analysis_text[:100]}...",
                    grammar_info={
                        "full_analysis": analysis_text,
                        "educational_focus": True,
                        "model_type": "conversational"
                    },
                    confidence=0.75,
                    model_used="Ollama-Llama3",
                    timestamp=datetime.now()
                )
                
                self.analysis_count += 1
                return analysis
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error analyzing word '{word}' with Ollama: {e}")
            raise


# Quick test function
async def test_analyzers():
    """Test both analyzers with a Hebrew word"""
    print("🧪 Testing Hebrew Analyzers...")
    
    # Test AlephBERT
    aleph = AlephBertAnalyzer()
    if aleph.initialize():
        print("✅ AlephBERT initialized successfully")
        try:
            result = await aleph.analyze_word("בְּרֵאשִׁית")
            print(f"✅ AlephBERT analysis: {result.word} -> {result.confidence}")
        except Exception as e:
            print(f"❌ AlephBERT analysis failed: {e}")
    else:
        print("❌ AlephBERT initialization failed")
    
    # Test Ollama
    ollama = OllamaAnalyzer()
    if ollama.initialize():
        print("✅ Ollama initialized successfully")
        try:
            result = await ollama.analyze_word("בְּרֵאשִׁית")
            print(f"✅ Ollama analysis: {result.word} -> {result.confidence}")
        except Exception as e:
            print(f"❌ Ollama analysis failed: {e}")
    else:
        print("❌ Ollama initialization failed")


if __name__ == "__main__":
    # Run the test
    asyncio.run(test_analyzers())