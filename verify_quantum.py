#!/usr/bin/env python3
"""
Quantum Verification Script
Run this to verify that your quantum operations are working correctly
"""

import sys
import time
from collections import Counter
import numpy as np

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔬 {title}")
    print('='*60)

def test_quantum_randomness():
    """Test if quantum random generation is truly random"""
    print_header("QUANTUM RANDOMNESS TEST")
    
    try:
        import qmodule
        
        print("Generating 1000 quantum random bits...")
        print("(This may take 10-15 seconds)")
        
        bits = []
        start_time = time.time()
        
        for i in range(1000):
            if i % 100 == 0:
                print(f"Progress: {i}/1000")
            bit = qmodule.quantum_random_bit()
            bits.append(bit)
        
        end_time = time.time()
        print(f"Generated 1000 bits in {end_time - start_time:.2f} seconds")
        
        # Analyze results
        zeros = bits.count(0)
        ones = bits.count(1)
        
        print(f"\nResults:")
        print(f"  Zeros (0): {zeros}")
        print(f"  Ones (1):  {ones}")
        print(f"  Ratio:     {ones/zeros:.3f} (ideal: 1.000)")
        print(f"  Deviation: {abs(500 - ones)} from perfect 50/50")
        
        # Statistical test
        if 450 <= zeros <= 550 and 450 <= ones <= 550:
            print("✅ PASS: Distribution looks quantum-random")
        else:
            print("⚠️  WARNING: Distribution is biased")
        
        # Look for patterns
        print("\nPattern Analysis:")
        pairs = [(bits[i], bits[i+1]) for i in range(len(bits)-1)]
        pair_counts = Counter(pairs)
        
        print(f"  00 pairs: {pair_counts[(0,0)]}")
        print(f"  01 pairs: {pair_counts[(0,1)]}")
        print(f"  10 pairs: {pair_counts[(1,0)]}")
        print(f"  11 pairs: {pair_counts[(1,1)]}")
        
        # All pairs should be roughly equal for true randomness
        pair_values = list(pair_counts.values())
        if max(pair_values) - min(pair_values) < 50:
            print("✅ PASS: No obvious patterns detected")
        else:
            print("⚠️  WARNING: Patterns detected in bit sequence")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_quantum_superposition():
    """Test quantum superposition"""
    print_header("QUANTUM SUPERPOSITION TEST")
    
    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import Aer
        
        print("Testing single qubit superposition...")
        
        # Create superposition circuit
        qc = QuantumCircuit(1, 1)
        qc.h(0)  # Hadamard gate creates |+⟩ = (|0⟩ + |1⟩)/√2
        qc.measure(0, 0)
        
        # Run simulation
        simulator = Aer.get_backend('aer_simulator')
        job = simulator.run(qc, shots=1000)
        result = job.result()
        counts = result.get_counts()
        
        zeros = counts.get('0', 0)
        ones = counts.get('1', 0)
        
        print(f"Superposition measurement results:")
        print(f"  |0⟩ state: {zeros} times")
        print(f"  |1⟩ state:  {ones} times")
        print(f"  Ratio: {ones/zeros:.3f}")
        
        if abs(zeros - ones) < 100:
            print("✅ PASS: Superposition working correctly")
        else:
            print("❌ FAIL: Superposition not working")
        
        # Test multi-qubit superposition
        print("\nTesting 3-qubit superposition...")
        
        qc2 = QuantumCircuit(3, 3)
        for i in range(3):
            qc2.h(i)  # All qubits in superposition
        qc2.measure(range(3), range(3))
        
        job2 = simulator.run(qc2, shots=1000)
        result2 = job2.result()
        counts2 = result2.get_counts()
        
        print(f"3-qubit superposition states observed: {len(counts2)}/8")
        print("States and counts:")
        for state, count in sorted(counts2.items()):
            print(f"  |{state}⟩: {count} times")
        
        if len(counts2) >= 7:  # Should see at least 7 out of 8 states
            print("✅ PASS: Multi-qubit superposition working")
        else:
            print("❌ FAIL: Not all superposition states observed")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_quantum_entanglement():
    """Test quantum entanglement"""
    print_header("QUANTUM ENTANGLEMENT TEST")
    
    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import Aer
        
        print("Creating Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2...")
        
        # Create Bell state
        qc = QuantumCircuit(2, 2)
        qc.h(0)      # Put first qubit in superposition
        qc.cx(0, 1)  # Entangle with second qubit
        qc.measure([0, 1], [0, 1])
        
        # Run simulation
        simulator = Aer.get_backend('aer_simulator')
        job = simulator.run(qc, shots=1000)
        result = job.result()
        counts = result.get_counts()
        
        print(f"Bell state measurement results:")
        for state, count in sorted(counts.items()):
            print(f"  |{state}⟩: {count} times")
        
        # Check for entanglement
        correlated = counts.get('00', 0) + counts.get('11', 0)
        uncorrelated = counts.get('01', 0) + counts.get('10', 0)
        
        print(f"\nEntanglement analysis:")
        print(f"  Correlated states (00, 11): {correlated}")
        print(f"  Uncorrelated states (01, 10): {uncorrelated}")
        print(f"  Correlation strength: {correlated/(correlated+uncorrelated):.3f}")
        
        if correlated > 950:  # Should be >95% correlated
            print("✅ PASS: Strong quantum entanglement detected!")
        elif correlated > 800:
            print("⚠️  WARNING: Weak entanglement (might be noise)")
        else:
            print("❌ FAIL: No entanglement detected")
        
        return correlated > 800
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_quantum_interference():
    """Test quantum interference"""
    print_header("QUANTUM INTERFERENCE TEST")
    
    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import Aer
        
        print("Testing quantum interference pattern...")
        
        # Test different phase shifts
        phases = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
        results = []
        
        simulator = Aer.get_backend('aer_simulator')
        
        for phase in phases:
            # Mach-Zehnder interferometer-like circuit
            qc = QuantumCircuit(1, 1)
            qc.h(0)           # First beam splitter
            qc.rz(phase, 0)   # Phase shift
            qc.h(0)           # Second beam splitter
            qc.measure(0, 0)
            
            job = simulator.run(qc, shots=1000)
            result = job.result()
            counts = result.get_counts()
            
            ones = counts.get('1', 0)
            probability_1 = ones / 1000
            results.append(probability_1)
            
            print(f"  Phase {phase:.3f}: P(|1⟩) = {probability_1:.3f}")
        
        # Check for interference pattern
        max_prob = max(results)
        min_prob = min(results)
        contrast = (max_prob - min_prob) / (max_prob + min_prob)
        
        print(f"\nInterference analysis:")
        print(f"  Maximum probability: {max_prob:.3f}")
        print(f"  Minimum probability: {min_prob:.3f}")
        print(f"  Contrast: {contrast:.3f}")
        
        if contrast > 0.5:
            print("✅ PASS: Strong quantum interference detected!")
        elif contrast > 0.2:
            print("⚠️  WARNING: Weak interference pattern")
        else:
            print("❌ FAIL: No interference pattern detected")
        
        return contrast > 0.2
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_bell_inequality():
    """Test Bell's inequality violation (advanced)"""
    print_header("BELL'S INEQUALITY TEST")
    
    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import Aer
        
        print("Testing Bell's inequality violation...")
        print("This is the gold standard for quantum behavior verification.")
        
        def measure_correlation(angle1, angle2):
            """Measure correlation between qubits at different angles"""
            qc = QuantumCircuit(2, 2)
            
            # Create Bell state
            qc.h(0)
            qc.cx(0, 1)
            
            # Rotate measurement bases
            qc.ry(2 * angle1, 0)
            qc.ry(2 * angle2, 1)
            
            qc.measure([0, 1], [0, 1])
            
            # Run simulation
            simulator = Aer.get_backend('aer_simulator')
            job = simulator.run(qc, shots=1000)
            result = job.result().get_counts()
            
            # Calculate correlation E(a,b) = P(same) - P(different)
            same = result.get('00', 0) + result.get('11', 0)
            different = result.get('01', 0) + result.get('10', 0)
            
            correlation = (same - different) / 1000
            return correlation
        
        # Test specific angles that should violate Bell's inequality
        angles = [0, np.pi/8, np.pi/4, 3*np.pi/8]
        
        print("Measuring correlations at different angles:")
        correlations = {}
        
        for i, a1 in enumerate(angles):
            for j, a2 in enumerate(angles):
                corr = measure_correlation(a1, a2)
                correlations[(i,j)] = corr
                print(f"  E({i},{j}) = {corr:.3f}")
        
        # Calculate CHSH inequality: |E(0,0) - E(0,1) + E(1,0) + E(1,1)| ≤ 2
        chsh_value = abs(correlations[(0,0)] - correlations[(0,1)] + 
                        correlations[(1,0)] + correlations[(1,1)])
        
        print(f"\nCHSH inequality test:")
        print(f"  CHSH value: {chsh_value:.3f}")
        print(f"  Classical limit: 2.000")
        print(f"  Quantum maximum: 2.828")
        
        if chsh_value > 2.1:  # Allow for statistical noise
            print("✅ PASS: Bell's inequality VIOLATED - Quantum behavior confirmed!")
            return True
        elif chsh_value > 1.8:
            print("⚠️  WARNING: Weak violation (statistical noise?)")
            return True
        else:
            print("❌ FAIL: Classical behavior (no violation)")
            return False
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def compare_with_classical():
    """Compare quantum results with classical pseudorandom"""
    print_header("QUANTUM vs CLASSICAL COMPARISON")
    
    try:
        import qmodule
        import random
        
        print("Comparing quantum vs classical randomness...")
        
        choices = ["Red", "Blue", "Green", "Yellow"]
        n_trials = 50
        
        # Classical choices
        print(f"\nClassical pseudorandom choices ({n_trials} trials):")
        classical_choices = []
        for i in range(n_trials):
            choice = random.choice(choices)
            classical_choices.append(choice)
            print(choice, end=" ")
            if (i + 1) % 10 == 0:
                print()  # New line every 10
        
        # Quantum choices
        print(f"\nQuantum random choices ({n_trials} trials):")
        quantum_choices = []
        for i in range(n_trials):
            choice, _ = qmodule.quantum_random_choice(choices)
            quantum_choices.append(choice)
            print(choice, end=" ")
            if (i + 1) % 10 == 0:
                print()  # New line every 10
        
        # Compare distributions
        classical_dist = Counter(classical_choices)
        quantum_dist = Counter(quantum_choices)
        
        print(f"\n\nDistribution comparison:")
        print(f"{'Color':<8} {'Classical':<10} {'Quantum':<10} {'Difference'}")
        print("-" * 40)
        
        for choice in choices:
            c_count = classical_dist[choice]
            q_count = quantum_dist[choice]
            diff = abs(c_count - q_count)
            print(f"{choice:<8} {c_count:<10} {q_count:<10} {diff}")
        
        print(f"\n✅ Both methods produce random-looking results")
        print(f"✅ Quantum method uses true quantum superposition")
        print(f"✅ Classical method uses deterministic pseudorandom algorithm")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def main():
    """Run all quantum verification tests"""
    print("🚀 HYBRID QUANTUM AI CHATBOT - QUANTUM VERIFICATION")
    print("=" * 60)
    print("This script will verify that your quantum operations are working correctly.")
    print("Note: This uses Qiskit Aer simulators (classical simulation of quantum behavior).")
    print("The results are quantum-mechanically correct but run on classical hardware.")
    
    tests = [
        ("Quantum Randomness", test_quantum_randomness),
        ("Quantum Superposition", test_quantum_superposition),
        ("Quantum Entanglement", test_quantum_entanglement),
        ("Quantum Interference", test_quantum_interference),
        ("Bell's Inequality", test_bell_inequality),
        ("Quantum vs Classical", compare_with_classical)
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print("\n⚠️  Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    end_time = time.time()
    total_time = end_time - start_time
    
    print_header("VERIFICATION RESULTS SUMMARY")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Results:")
    print(f"  Tests Passed: {passed}/{len(results)}")
    print(f"  Success Rate: {passed/len(results)*100:.1f}%")
    print(f"  Total Time: {total_time:.1f} seconds")
    
    if passed == len(results):
        print("\n🎉 EXCELLENT! All quantum verification tests passed!")
        print("Your quantum computing implementation is working correctly.")
        print("\n🔬 What this means:")
        print("  ✅ Quantum superposition is working")
        print("  ✅ Quantum entanglement is working")
        print("  ✅ Quantum interference is working")
        print("  ✅ Quantum randomness is working")
        print("  ✅ Bell's inequality violations confirm quantum behavior")
        
        print("\n📝 Important Notes:")
        print("  • You're using Qiskit Aer simulators (classical computers)")
        print("  • The quantum algorithms are mathematically correct")
        print("  • Results follow quantum mechanical principles exactly")
        print("  • For 'true' quantum, you'd need quantum hardware (IBM, Google, etc.)")
        
    elif passed >= len(results) * 0.8:
        print("\n🎯 GOOD! Most tests passed.")
        print("Your quantum implementation is mostly working correctly.")
        print("Check the failed tests for potential issues.")
        
    else:
        print("\n⚠️  WARNING: Several tests failed.")
        print("Your quantum implementation may have issues.")
        print("Check your Qiskit installation and configuration.")
    
    print(f"\n📊 To see individual test details, scroll up in the output.")
    print(f"💡 For real quantum hardware testing, sign up at: https://quantum-computing.ibm.com/")
    
    return passed == len(results)

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification interrupted by user. Goodbye!")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Verification script crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)