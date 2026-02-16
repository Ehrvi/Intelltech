"""
MOTHER V5 - Reinforcement Learning Agent

Enables MOTHER to learn and improve autonomously through Q-Learning.
Phase 1: Task routing (OpenAI vs browser vs hybrid)
"""

import random
import json
import os
from typing import Dict, Tuple, List, Any
from dataclasses import dataclass, asdict
from enum import Enum


class Action(Enum):
    """Available actions for task routing"""
    USE_OPENAI = "openai"
    USE_BROWSER = "browser"
    USE_HYBRID = "hybrid"


class TaskType(Enum):
    """Types of tasks"""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    GENERATION = "generation"
    AUTOMATION = "automation"


@dataclass
class State:
    """Represents the current state"""
    task_type: TaskType
    complexity: str  # "low", "medium", "high"
    budget: str  # "low", "medium", "high"
    
    def __hash__(self):
        return hash((self.task_type, self.complexity, self.budget))
    
    def to_tuple(self):
        return (self.task_type.value, self.complexity, self.budget)


@dataclass
class Experience:
    """Single experience tuple for learning"""
    state: State
    action: Action
    reward: float
    next_state: State
    quality_score: float
    cost: float


class RLAgent:
    """
    Reinforcement Learning Agent using Q-Learning.
    
    Learns optimal task routing decisions to balance cost and quality.
    """
    
    def __init__(self, 
                 epsilon: float = 0.1,
                 alpha: float = 0.1,
                 gamma: float = 0.9,
                 q_table_path: str = None):
        """
        Initialize RL Agent.
        
        Args:
            epsilon: Exploration rate (probability of random action)
            alpha: Learning rate
            gamma: Discount factor
            q_table_path: Path to save/load Q-table
        """
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table: Dict[Tuple, Dict[Action, float]] = {}
        self.q_table_path = q_table_path or "/home/ubuntu/manus_global_knowledge/mother_v5/domain/models/q_table.json"
        self.actions = list(Action)
        self.experiences: List[Experience] = []
        
        # Load existing Q-table if available
        self.load_q_table()
    
    def select_action(self, state: State) -> Action:
        """
        Select action using ε-greedy policy.
        
        Args:
            state: Current state
            
        Returns:
            Selected action
        """
        # Exploration: random action
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        
        # Exploitation: best known action
        return self.best_action(state)
    
    def best_action(self, state: State) -> Action:
        """
        Get best action for given state based on Q-values.
        
        Args:
            state: Current state
            
        Returns:
            Action with highest Q-value
        """
        state_tuple = state.to_tuple()
        
        # If state not seen before, return default action
        if state_tuple not in self.q_table:
            return self._default_action(state)
        
        # Return action with highest Q-value
        q_values = self.q_table[state_tuple]
        return max(q_values.items(), key=lambda x: x[1])[0]
    
    def _default_action(self, state: State) -> Action:
        """
        Default action for unseen states based on heuristics.
        
        Args:
            state: Current state
            
        Returns:
            Default action
        """
        # Research tasks: hybrid (OpenAI discovery + browser verification)
        if state.task_type == TaskType.RESEARCH:
            return Action.USE_HYBRID
        
        # Low budget: prefer OpenAI (cheaper)
        if state.budget == "low":
            return Action.USE_OPENAI
        
        # High complexity: prefer hybrid (more thorough)
        if state.complexity == "high":
            return Action.USE_HYBRID
        
        # Default: OpenAI (fastest and cheapest)
        return Action.USE_OPENAI
    
    def update(self, state: State, action: Action, reward: float, next_state: State):
        """
        Update Q-table using Q-learning update rule.
        
        Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
        """
        state_tuple = state.to_tuple()
        next_state_tuple = next_state.to_tuple()
        
        # Initialize Q-values if not seen before
        if state_tuple not in self.q_table:
            self.q_table[state_tuple] = {a: 0.0 for a in self.actions}
        if next_state_tuple not in self.q_table:
            self.q_table[next_state_tuple] = {a: 0.0 for a in self.actions}
        
        # Current Q-value
        current_q = self.q_table[state_tuple][action]
        
        # Max Q-value for next state
        max_next_q = max(self.q_table[next_state_tuple].values())
        
        # Q-learning update
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state_tuple][action] = new_q
    
    def record_experience(self, experience: Experience):
        """
        Record experience for later analysis.
        
        Args:
            experience: Experience tuple
        """
        self.experiences.append(experience)
        
        # Calculate reward based on quality and cost
        reward = self._calculate_reward(experience.quality_score, experience.cost)
        
        # Update Q-table
        self.update(experience.state, experience.action, reward, experience.next_state)
        
        # Save Q-table periodically (every 10 experiences)
        if len(self.experiences) % 10 == 0:
            self.save_q_table()
    
    def _calculate_reward(self, quality_score: float, cost: float) -> float:
        """
        Calculate reward from quality and cost.
        
        Reward = quality_score - cost_penalty
        
        Args:
            quality_score: Quality score (0-1)
            cost: Cost in USD
            
        Returns:
            Reward value
        """
        # Normalize cost to 0-1 range (assuming max cost is $20)
        cost_normalized = min(cost / 20.0, 1.0)
        
        # Reward = quality (0-1) - cost penalty (0-1)
        # This encourages high quality at low cost
        reward = quality_score - (0.3 * cost_normalized)
        
        return reward
    
    def save_q_table(self):
        """Save Q-table to disk"""
        # Convert Q-table to JSON-serializable format
        serializable_q_table = {}
        for state_tuple, actions in self.q_table.items():
            state_key = json.dumps(state_tuple)
            serializable_q_table[state_key] = {
                action.value: q_value 
                for action, q_value in actions.items()
            }
        
        # Save to file
        os.makedirs(os.path.dirname(self.q_table_path), exist_ok=True)
        with open(self.q_table_path, 'w') as f:
            json.dump(serializable_q_table, f, indent=2)
    
    def load_q_table(self):
        """Load Q-table from disk"""
        if not os.path.exists(self.q_table_path):
            return
        
        with open(self.q_table_path, 'r') as f:
            serializable_q_table = json.load(f)
        
        # Convert back to internal format
        self.q_table = {}
        for state_key, actions in serializable_q_table.items():
            state_tuple = tuple(json.loads(state_key))
            self.q_table[state_tuple] = {
                Action(action_str): q_value
                for action_str, q_value in actions.items()
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get learning statistics.
        
        Returns:
            Statistics dictionary
        """
        if not self.experiences:
            return {"total_experiences": 0}
        
        # Calculate average reward per action
        action_rewards = {action: [] for action in self.actions}
        for exp in self.experiences:
            reward = self._calculate_reward(exp.quality_score, exp.cost)
            action_rewards[exp.action].append(reward)
        
        avg_rewards = {
            action.value: sum(rewards) / len(rewards) if rewards else 0
            for action, rewards in action_rewards.items()
        }
        
        # Calculate success rate per action (quality >= 0.8)
        action_successes = {action: [] for action in self.actions}
        for exp in self.experiences:
            action_successes[exp.action].append(exp.quality_score >= 0.8)
        
        success_rates = {
            action.value: sum(successes) / len(successes) if successes else 0
            for action, successes in action_successes.items()
        }
        
        return {
            "total_experiences": len(self.experiences),
            "states_explored": len(self.q_table),
            "average_rewards": avg_rewards,
            "success_rates": success_rates,
            "epsilon": self.epsilon,
            "alpha": self.alpha,
            "gamma": self.gamma
        }


# Example usage
if __name__ == "__main__":
    # Create agent
    agent = RLAgent()
    
    # Example state
    state = State(
        task_type=TaskType.RESEARCH,
        complexity="high",
        budget="medium"
    )
    
    # Select action
    action = agent.select_action(state)
    print(f"Selected action: {action.value}")
    
    # Simulate task execution
    quality_score = 0.85
    cost = 2.50
    
    # Record experience
    next_state = State(
        task_type=TaskType.ANALYSIS,
        complexity="medium",
        budget="medium"
    )
    
    experience = Experience(
        state=state,
        action=action,
        reward=0.0,  # Will be calculated
        next_state=next_state,
        quality_score=quality_score,
        cost=cost
    )
    
    agent.record_experience(experience)
    
    # Get statistics
    stats = agent.get_statistics()
    print(f"\nStatistics: {json.dumps(stats, indent=2)}")
