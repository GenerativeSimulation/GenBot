
from manipulation.sim import SimpleEnv
import numpy as np
from manipulation.gpt_reward_api import *
from manipulation.gpt_primitive_api import *
import gym

class turn_the_hot_water_switch(SimpleEnv):

    def __init__(self, task_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_name = task_name
        self.detected_position = {}

    def _compute_reward(self):
        # This reward encourages the end-effector to stay near the switch to grasp it.
        eef_pos = get_eef_pos(self)[0]
        switch_pos = get_link_state(self, "Faucet", "link_1")
        reward_near = -np.linalg.norm(eef_pos - switch_pos)
        
        # Get the joint state of the switch. The semantics and the articulation tree show that joint_1 connects link_1 and is the joint that controls the rotation of the switch.
        joint_angle = get_joint_state(self, "Faucet", "joint_1") 
        # The reward is the negative distance between the current joint angle and the joint angle when the switch is fully turned on (upper limit).
        joint_limit_low, joint_limit_high = get_joint_limit(self, "Faucet", "joint_1")
        diff = np.abs(joint_angle - joint_limit_high)
        reward_joint =  -diff
        
        reward = reward_near + 5 * reward_joint
        success = diff < 0.1 * (joint_limit_high - joint_limit_low)
        
        return reward, success

gym.register(
    id='gym-turn_the_hot_water_switch-v0',
    entry_point=turn_the_hot_water_switch,
)
