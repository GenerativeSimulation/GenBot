
from manipulation.sim import SimpleEnv
import numpy as np
from manipulation.gpt_reward_api import *
from manipulation.gpt_primitive_api import *
import gym

class close_the_window(SimpleEnv):

    def __init__(self, task_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_name = task_name
        self.detected_position = {}

    def _compute_reward(self):
        # This reward encourages the end-effector to stay near the window to grasp it.
        eef_pos = get_eef_pos(self)[0]
        window_pos = get_link_state(self, "Window", "link_0")
        reward_near = -np.linalg.norm(eef_pos - window_pos)
        
        # Get the joint state of the window. The semantics and the articulation tree show that joint_0 connects link_0 and is the joint that controls the rotation of the window.
        joint_angle = get_joint_state(self, "Window", "joint_0") 
        # The reward is the negative distance between the current joint angle and the joint angle when the window is fully closed (lower limit).
        joint_limit_low, joint_limit_high = get_joint_limit(self, "Window", "joint_0")
        diff = np.abs(joint_angle - joint_limit_low)
        reward_joint =  -diff
        
        reward = reward_near + 5 * reward_joint
        
        success = diff < 0.1 * (joint_limit_high - joint_limit_low)
        
        return reward, success

gym.register(
    id='gym-close_the_window-v0',
    entry_point=close_the_window,
)
