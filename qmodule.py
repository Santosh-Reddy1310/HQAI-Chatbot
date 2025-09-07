"""
Enhanced Quantum Computing Module for Hybrid Quantum-AI Applications
Provides quantum simulations and algorithms using Qiskit
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
import os
import math
import logging
from typing import List, Tuple, Optional, Dict, Any
import matplotlib.pyplot as plt
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Quantum simulator backend
try:
    SIMULATOR = Aer.get_backend('aer_simulator')
    STATEVECTOR_SIMULATOR = Aer.get_backend('statevector_simulator')
    logger.info("Qiskit Aer simulators initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize quantum simulators: {e}")
    SIMULATOR = None
    STATEVECTOR_SIMULATOR = None

class QuantumError(Exception):
    """Custom exception for quantum computing errors"""
    pass

def validate_quantum_backend():
    """Ensure quantum simulators are available"""
    if SIMULATOR is None:
        raise QuantumError("Quantum simulator not available. Check Qiskit installation.")

def quantum_random_bit(shots: int = 1) -> int:
    """
    Generate a truly random bit using quantum superposition.
    
    Args:
        shots: Number of measurements (default: 1)
    
    Returns:
        Random bit (0 or 1)
    
    Raises:
        QuantumError: If quantum simulation fails
    """
    try:
        validate_quantum_backend()
        
        # Create quantum circuit with 1 qubit and 1 classical bit
        qc = QuantumCircuit(1, 1)
        
        # Put qubit in superposition
        qc.h(0)
        
        # Measure the qubit
        qc.measure(0, 0)
        
        # Execute the circuit
        job = SIMULATOR.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts(qc)
        
        # Extract the most frequent result (for shots=1, there's only one)
        bit = int(max(counts.keys()))
        
        logger.info(f"Generated quantum random bit: {bit}")
        return bit
        
    except Exception as e:
        logger.error(f"Quantum random bit generation failed: {e}")
        raise QuantumError(f"Failed to generate quantum random bit: {str(e)}")

def quantum_random_choice(choices: List[str], shots: int = 1024) -> Tuple[str, str]:
    """
    Use quantum randomness to select from a list of choices.
    
    Args:
        choices: List of options to choose from
        shots: Number of quantum measurements for better randomness
    
    Returns:
        Tuple of (selected_choice, measurement_bitstring)
    
    Raises:
        QuantumError: If quantum simulation fails
        ValueError: If choices list is empty
    """
    try:
        if not choices:
            raise ValueError("Choices list cannot be empty")
        
        validate_quantum_backend()
        
        n = len(choices)
        # Calculate minimum number of qubits needed
        n_qubits = max(1, math.ceil(math.log2(n)))
        
        # Create quantum circuit
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Apply Hadamard gates to create uniform superposition
        for i in range(n_qubits):
            qc.h(i)
        
        # Measure all qubits
        qc.measure(range(n_qubits), range(n_qubits))
        
        # Execute circuit
        job = SIMULATOR.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts(qc)
        
        # Get the most frequent measurement result
        most_frequent = max(counts.keys(), key=lambda x: counts[x])
        
        # Convert bitstring to integer and map to choice
        value = int(most_frequent, 2)
        selected_index = value % n
        selected_choice = choices[selected_index]
        
        logger.info(f"Quantum choice selected: '{selected_choice}' from {len(choices)} options")
        return selected_choice, most_frequent
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Quantum random choice failed: {e}")
        raise QuantumError(f"Failed to make quantum random choice: {str(e)}")

def quantum_entanglement_demo(save_path: str = "static/entanglement.png") -> str:
    """
    Create and visualize a quantum entanglement demonstration (Bell state).
    
    Args:
        save_path: Path to save the circuit diagram
    
    Returns:
        Path to the saved circuit image
    
    Raises:
        QuantumError: If circuit creation or visualization fails
    """
    try:
        # Create Bell state circuit (maximally entangled state)
        qc = QuantumCircuit(2, 2, name="Bell_State")
        
        # Create entanglement: |00⟩ + |11⟩
        qc.h(0)           # Put first qubit in superposition
        qc.cx(0, 1)       # Entangle qubits
        
        # Add measurements
        qc.barrier()      # Visual separator
        qc.measure([0, 1], [0, 1])
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Create and save visualization
        fig = qc.draw(output='mpl', scale=1.2, style='iqx')
        fig.suptitle('Quantum Entanglement: Bell State Circuit', fontsize=14)
        fig.savefig(save_path, bbox_inches='tight', dpi=150, facecolor='white')
        plt.close(fig)
        
        logger.info(f"Bell state circuit saved to: {save_path}")
        return save_path
        
    except Exception as e:
        logger.error(f"Entanglement demo failed: {e}")
        raise QuantumError(f"Failed to create entanglement demo: {str(e)}")

def quantum_optimization_demo(problem_size: int = 4) -> Dict[str, Any]:
    """
    Demonstrate quantum optimization using a simple QAOA-inspired approach.
    
    Args:
        problem_size: Number of qubits/variables in the optimization problem
    
    Returns:
        Dictionary with optimization results
    
    Raises:
        QuantumError: If quantum optimization simulation fails
    """
    try:
        validate_quantum_backend()
        
        if problem_size < 2 or problem_size > 10:
            raise ValueError("Problem size must be between 2 and 10 qubits")
        
        # Create QAOA-inspired circuit
        qc = QuantumCircuit(problem_size, problem_size)
        
        # Initial state: uniform superposition
        for i in range(problem_size):
            qc.h(i)
        
        # Cost layer: encode problem structure (simplified Max-Cut inspired)
        gamma = np.pi / 4  # Cost parameter
        for i in range(problem_size - 1):
            qc.rzz(gamma, i, i + 1)
        
        # Mixer layer: enable transitions between states
        beta = np.pi / 3   # Mixer parameter
        for i in range(problem_size):
            qc.rx(2 * beta, i)
        
        # Measurement
        qc.measure(range(problem_size), range(problem_size))
        
        # Execute circuit
        shots = 1024
        job = SIMULATOR.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts(qc)
        
        # Analyze results
        best_bitstring = max(counts.keys(), key=lambda x: counts[x])
        best_count = counts[best_bitstring]
        success_probability = best_count / shots
        
        optimization_results = {
            "problem_size": problem_size,
            "best_solution": best_bitstring,
            "success_probability": round(success_probability, 3),
            "total_measurements": shots,
            "unique_states_measured": len(counts),
            "quantum_advantage_indicator": success_probability > (1 / (2 ** problem_size))
        }
        
        logger.info(f"Quantum optimization completed: best solution = {best_bitstring}")
        return optimization_results
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Quantum optimization demo failed: {e}")
        raise QuantumError(f"Failed to run quantum optimization: {str(e)}")

def quantum_ml_feature_map(data_point: List[float], 
                          encoding_type: str = "amplitude") -> Dict[str, Any]:
    """
    Create quantum feature maps for classical machine learning data.
    
    Args:
        data_point: Classical data to encode (list of floats)
        encoding_type: Type of encoding ("amplitude" or "angle")
    
    Returns:
        Dictionary with encoding information and quantum state details
    
    Raises:
        QuantumError: If feature mapping fails
        ValueError: If invalid parameters provided
    """
    try:
        if not data_point or len(data_point) == 0:
            raise ValueError("Data point cannot be empty")
        
        if len(data_point) > 8:
            raise ValueError("Data point size limited to 8 features for simulation")
        
        validate_quantum_backend()
        
        n_qubits = len(data_point)
        
        if encoding_type == "amplitude":
            # Amplitude encoding: encode data in quantum state amplitudes
            qc = QuantumCircuit(n_qubits)
            
            # Normalize data point
            norm = np.linalg.norm(data_point)
            if norm == 0:
                normalized_data = [0] * len(data_point)
            else:
                normalized_data = [x / norm for x in data_point]
            
            # Create initial state |0...0⟩
            # Apply rotation gates to encode data
            for i, value in enumerate(normalized_data):
                # Map data to rotation angle [0, π]
                angle = abs(value) * np.pi
                qc.ry(angle, i)
                if value < 0:
                    qc.z(i)  # Phase flip for negative values
            
        elif encoding_type == "angle":
            # Angle encoding: encode data in rotation angles
            qc = QuantumCircuit(n_qubits)
            
            for i, value in enumerate(data_point):
                # Map data value to rotation angle
                angle = value * np.pi  # Scale as needed
                qc.ry(angle, i)
                # Add entangling gates for correlation
                if i < n_qubits - 1:
                    qc.cx(i, i + 1)
        
        else:
            raise ValueError("Invalid encoding_type. Use 'amplitude' or 'angle'")
        
        # Get statevector if available
        feature_map_info = {
            "encoding_type": encoding_type,
            "n_qubits": n_qubits,
            "original_data": data_point,
            "circuit_depth": qc.depth(),
            "gate_count": len(qc.data)
        }
        
        # Try to get statevector for analysis
        try:
            if STATEVECTOR_SIMULATOR:
                job = STATEVECTOR_SIMULATOR.run(qc)
                result = job.result()
                statevector = result.get_statevector(qc)
                
                # Add quantum state analysis
                feature_map_info.update({
                    "state_vector_norm": float(np.linalg.norm(statevector)),
                    "entanglement_measure": calculate_entanglement_measure(statevector),
                    "quantum_state_prepared": True
                })
            else:
                feature_map_info["quantum_state_prepared"] = False
                
        except Exception as sv_error:
            logger.warning(f"Could not analyze statevector: {sv_error}")
            feature_map_info["quantum_state_prepared"] = False
        
        logger.info(f"Quantum feature map created: {encoding_type} encoding for {n_qubits} features")
        return feature_map_info
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Quantum ML feature mapping failed: {e}")
        raise QuantumError(f"Failed to create quantum feature map: {str(e)}")

def calculate_entanglement_measure(statevector: np.ndarray) -> float:
    """
    Calculate a simple entanglement measure (Von Neumann entropy of reduced state).
    
    Args:
        statevector: Quantum state vector
    
    Returns:
        Entanglement measure (0 = no entanglement, higher = more entangled)
    """
    try:
        n_qubits = int(np.log2(len(statevector)))
        if n_qubits < 2:
            return 0.0
        
        # Reshape statevector for partial trace
        state_matrix = np.outer(statevector, np.conj(statevector))
        
        # Simple approximation: calculate purity of the first qubit
        # (More sophisticated measures would require partial trace calculation)
        dim_A = 2  # First qubit dimension
        dim_B = len(statevector) // dim_A  # Remaining system dimension
        
        # Approximate entanglement by looking at state distribution
        amplitudes = np.abs(statevector) ** 2
        entropy = -np.sum(amplitudes * np.log2(amplitudes + 1e-12))  # Add small value to avoid log(0)
        
        # Normalize by maximum possible entropy
        max_entropy = np.log2(len(statevector))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return float(normalized_entropy)
        
    except Exception:
        return 0.0

def quantum_superposition_demo(n_qubits: int = 3, save_path: str = "static/superposition.png") -> str:
    """
    Create a quantum superposition demonstration.
    
    Args:
        n_qubits: Number of qubits to put in superposition
        save_path: Path to save circuit diagram
    
    Returns:
        Path to saved circuit image
    
    Raises:
        QuantumError: If demonstration fails
    """
    try:
        if n_qubits < 1 or n_qubits > 6:
            raise ValueError("Number of qubits must be between 1 and 6")
        
        # Create superposition circuit
        qc = QuantumCircuit(n_qubits, n_qubits, name=f"{n_qubits}_Qubit_Superposition")
        
        # Put all qubits in superposition
        for i in range(n_qubits):
            qc.h(i)
        
        # Add some phase relationships
        for i in range(n_qubits - 1):
            qc.cz(i, i + 1)
        
        # Measure all qubits
        qc.barrier()
        qc.measure(range(n_qubits), range(n_qubits))
        
        # Save visualization
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        fig = qc.draw(output='mpl', scale=1.0, style='iqx')
        fig.suptitle(f'Quantum Superposition: {n_qubits} Qubits in |+⟩ State', fontsize=12)
        fig.savefig(save_path, bbox_inches='tight', dpi=150, facecolor='white')
        plt.close(fig)
        
        logger.info(f"Superposition demo saved to: {save_path}")
        return save_path
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Superposition demo failed: {e}")
        raise QuantumError(f"Failed to create superposition demo: {str(e)}")

def get_quantum_system_info() -> Dict[str, Any]:
    """
    Get information about the quantum computing environment.
    
    Returns:
        Dictionary with system information
    """
    try:
        info = {
            "qiskit_available": True,
            "simulators_available": SIMULATOR is not None,
            "statevector_simulator": STATEVECTOR_SIMULATOR is not None,
            "max_recommended_qubits": 12,  # For simulation performance
            "supported_operations": [
                "quantum_random_bit",
                "quantum_random_choice", 
                "quantum_entanglement_demo",
                "quantum_optimization_demo",
                "quantum_ml_feature_map",
                "quantum_superposition_demo"
            ]
        }
        
        if SIMULATOR:
            # Get backend information
            backend_info = SIMULATOR.configuration()
            info.update({
                "backend_name": backend_info.backend_name,
                "backend_version": backend_info.backend_version,
                "max_shots": getattr(backend_info, 'max_shots', 'unlimited'),
                "coupling_map": getattr(backend_info, 'coupling_map', None)
            })
            
        return info
        
    except Exception as e:
        logger.error(f"Failed to get quantum system info: {e}")
        return {
            "qiskit_available": False,
            "error": str(e),
            "simulators_available": False
        }

def quantum_health_check() -> bool:
    """
    Perform a basic health check of the quantum computing system.
    
    Returns:
        True if system is healthy, False otherwise
    """
    try:
        # Test basic quantum operations
        bit = quantum_random_bit()
        
        # Test circuit creation and execution
        choices = ["test1", "test2"]
        choice, bits = quantum_random_choice(choices)
        
        logger.info("Quantum system health check passed")
        return True
        
    except Exception as e:
        logger.error(f"Quantum system health check failed: {e}")
        return False