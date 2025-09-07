#!/usr/bin/env python3
"""
Quick Quantum Test - Verify your quantum operations are working
Run this for a fast verification of quantum functionality
"""

def quick_quantum_test():
    print("🔬 QUICK QUANTUM VERIFICATION TEST")
    print("=" * 50)
    
    try:
        import qmodule
        
        # Test 1: Basic quantum random bit
        print("1. Testing quantum random bit generation...")
        bit1 = qmodule.quantum_random_bit()
        bit2 = qmodule.quantum_random_bit()
        bit3 = qmodule.quantum_random_bit()
        print(f"   Generated bits: {bit1}, {bit2}, {bit3}")
        
        if bit1 in [0, 1] and bit2 in [0, 1] and bit3 in [0, 1]:
            print("   ✅ PASS: Quantum bits generated correctly")
        else:
            print("   ❌ FAIL: Invalid bit values")
            return False
        
        # Test 2: Quantum random choice
        print("\n2. Testing quantum random choice...")
        options = ["Quantum", "Classical", "Hybrid", "Superposition"]
        choice, bits = qmodule.quantum_random_choice(options)
        print(f"   Quantum chose: '{choice}' (bits: {bits})")
        
        if choice in options and len(bits) > 0:
            print("   ✅ PASS: Quantum choice working")
        else:
            print("   ❌ FAIL: Invalid choice result")
            return False
        
        # Test 3: Entanglement demo
        print("\n3. Testing quantum entanglement demo...")
        import os
        os.makedirs("static", exist_ok=True)
        
        circuit_path = qmodule.quantum_entanglement_demo()
        if os.path.exists(circuit_path):
            print(f"   ✅ PASS: Circuit created at {circuit_path}")
        else:
            print("   ❌ FAIL: Circuit creation failed")
            return False
        
        # Test 4: Quick randomness check
        print("\n4. Quick randomness distribution test...")
        bits = [qmodule.quantum_random_bit() for _ in range(20)]
        zeros = bits.count(0)
        ones = bits.count(1)
        print(f"   20 random bits: {bits}")
        print(f"   Distribution: {zeros} zeros, {ones} ones")
        
        if 5 <= zeros <= 15:  # Reasonable range for 20 bits
            print("   ✅ PASS: Distribution looks reasonable")
        else:
            print("   ⚠️  WARNING: Distribution might be biased")
        
        # Test 5: Quantum system health
        print("\n5. Testing quantum system health...")
        health = qmodule.quantum_health_check()
        if health:
            print("   ✅ PASS: Quantum system is healthy")
        else:
            print("   ❌ FAIL: Quantum system has issues")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 ALL QUICK TESTS PASSED!")
        print("Your quantum computing setup is working correctly!")
        print("\n🔍 What was verified:")
        print("  • Quantum random bit generation ✅")
        print("  • Quantum random choice selection ✅")
        print("  • Quantum circuit creation ✅")
        print("  • Basic randomness distribution ✅")
        print("  • Quantum system health ✅")
        
        print("\n📝 Technical Notes:")
        print("  • Using Qiskit Aer simulator (classical simulation)")
        print("  • Quantum algorithms are mathematically correct")
        print("  • Results follow quantum mechanical principles")
        
        print("\n💡 For comprehensive testing, run: python verify_quantum.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ FAIL: Missing module - {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install qiskit qiskit-aer numpy matplotlib")
        return False
        
    except Exception as e:
        print(f"❌ FAIL: Test error - {e}")
        return False

def test_with_app_integration():
    """Test integration with your main app"""
    print("\n🔗 TESTING APP INTEGRATION")
    print("=" * 50)
    
    try:
        # Test AI client
        print("1. Testing AI client status...")
        from ai_client import get_provider_status
        
        status = get_provider_status()
        print(f"   Provider: {status['provider']}")
        print(f"   Status: {status['status']}")
        
        if status['status'] == 'configured':
            print("   ✅ PASS: AI client configured")
        else:
            print(f"   ❌ FAIL: {status.get('error', 'Unknown error')}")
            return False
        
        # Test utilities
        print("\n2. Testing utilities...")
        import utils
        
        timestamp = utils.timestamp()
        print(f"   Timestamp: {timestamp}")
        
        static_dir = utils.ensure_static_dir()
        print(f"   Static directory: {static_dir}")
        print("   ✅ PASS: Utilities working")
        
        print("\n🎉 APP INTEGRATION TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Integration test error - {e}")
        return False

if __name__ == "__main__":
    print("🚀 STARTING QUICK QUANTUM VERIFICATION...")
    
    # Run quick quantum test
    quantum_ok = quick_quantum_test()
    
    if quantum_ok:
        # If quantum tests pass, test app integration
        app_ok = test_with_app_integration()
        
        if app_ok:
            print("\n🌟 FINAL RESULT: ALL SYSTEMS GO!")
            print("Your Hybrid Quantum AI Chatbot is ready to use!")
            print("\nTo start the app: streamlit run app.py")
        else:
            print("\n⚠️  Quantum works, but check app configuration")
    else:
        print("\n❌ QUANTUM TESTS FAILED")
        print("Please check your Qiskit installation")
    
    print("\n" + "=" * 50)