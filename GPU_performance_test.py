# GPU_performance_test.py
import torch
import time
from transformers import AutoModel, AutoTokenizer
import psutil
import GPUtil

def test_gpu_performance():
    print("🔧 GPU Performance Test for Enhanced AlephBERT")
    print("=" * 50)
    
    # Check system specs
    print(f"💻 System RAM: {psutil.virtual_memory().total / 1024**3:.1f}GB")
    
    if torch.cuda.is_available():
        gpu = GPUtil.getGPUs()[0]
        print(f"🎮 GPU: {gpu.name}")
        print(f"🎮 GPU Memory: {gpu.memoryTotal}MB total")
        print(f"🎮 GPU Memory Free: {gpu.memoryFree}MB")
        print(f"🎮 CUDA Version: {torch.version.cuda}")
        
        # Test AlephBERT performance
        print("\n🚀 Loading AlephBERT on GPU...")
        start_time = time.time()
        
        device = torch.device("cuda")
        model = AutoModel.from_pretrained("onlplab/alephbert-base").to(device)
        tokenizer = AutoTokenizer.from_pretrained("onlplab/alephbert-base")
        
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.2f} seconds")
        
        # Memory usage after loading
        gpu_after_load = GPUtil.getGPUs()[0]
        memory_used = gpu.memoryTotal - gpu_after_load.memoryFree
        print(f"📊 GPU Memory used by model: {memory_used}MB ({memory_used/1024:.2f}GB)")
        
        # Performance test with Hebrew text
        hebrew_text = "בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ"
        print(f"\n🔬 Testing with Hebrew text: {hebrew_text}")
        
        # Warm-up run
        inputs = tokenizer(hebrew_text, return_tensors="pt").to(device)
        with torch.no_grad():
            _ = model(**inputs)
        
        # Timed performance test
        start_time = time.time()
        with torch.no_grad():
            outputs = model(**inputs)
        
        inference_time = time.time() - start_time
        print(f"⚡ Inference time: {inference_time:.3f} seconds")
        print(f"📈 Tokens processed: {len(inputs['input_ids'][0])}")
        print(f"🎯 Performance: {len(inputs['input_ids'][0])/inference_time:.1f} tokens/second")
        
        # Memory efficiency check
        final_gpu = GPUtil.getGPUs()[0]
        peak_memory = gpu.memoryTotal - final_gpu.memoryFree
        print(f"🔥 Peak GPU memory usage: {peak_memory}MB ({peak_memory/1024:.2f}GB)")
        
        return True
    else:
        print("❌ CUDA not available - GPU acceleration disabled")
        return False

if __name__ == "__main__":
    test_gpu_performance()