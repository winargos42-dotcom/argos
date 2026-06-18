# scripts/test_buffered_store.py
import sys, os, time
sys.path.insert(0, os.path.abspath("src"))

from src.mempalace_bridge import MemPalaceBridge
from src.buffered_thought_store import BufferedThoughtStore

def main():
    print("🧪 Testing BufferedThoughtStore...")
    bridge = MemPalaceBridge()
    buffer = BufferedThoughtStore(bridge)
    
    # Добавляем 5 мыслей (должно сработать 2 флеша: 3+2)
    for i in range(5):
        thought = {
            "id": f"test_t_{i}",
            "content": f"Test thought #{i}",
            "epistemic": "known" if i % 2 == 0 else "known_gap",
            "ts": time.time()
        }
        ok = buffer.add(thought)
        print(f"  Add #{i}: {'✅' if ok else '❌'} | buffer={len(buffer.buffer)}")
        time.sleep(0.1)
    
    # Финальный сброс
    buffer.force_flush()
    
    # Проверка в MemPalace
    from mempalace import MemoryCore
    mp = MemoryCore()
    batches = [n for n in mp.nodes if n.startswith("thought_batch_")]
    print(f"\n📦 Batches stored: {len(batches)}")
    for b in batches:
        node = mp.get_node(b)
        print(f"  → {b}: {node.get('data', {}).get('count', '?')} thoughts")
    
    print("\n🏁 Buffered store test complete.")

if __name__ == "__main__":
    main()
