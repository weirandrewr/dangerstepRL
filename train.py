import gym
import os
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from dangerstep_env import DangerStepEnv
import torch

env = make_vec_env(DangerStepEnv, n_envs=1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
policy_kwargs = dict(net_arch=[dict(pi=[64, 64], vf=[64, 64])])
model = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs,ent_coef=0.05,verbose=1, learning_rate=0.0003,n_steps=20, n_epochs=10, gamma=.99, gae_lambda=0.95, clip_range=0.2)
print(torch.cuda.current_device())
print(next(model.policy.parameters()).device)

class ScoreLoggerCallback(BaseCallback):
    def __init__(self, save_path, verbose=1):
        super(ScoreLoggerCallback, self).__init__(verbose)
        self.save_path = save_path
        self.scores = []
        os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if all(self.locals['dones']):
            env = self.training_env.envs[0].env
            score = env.score
            self.scores.append(score)
            print(score, "your score is ", score)
            with open(os.path.join(self.save_path, 'scores.txt'), 'a') as file:
                file.write(f"{score}\n")
        return True


def main():
    # Create the environment and wrap it for monitoring
    log_dir = "./logs/"
    os.makedirs(log_dir, exist_ok=True)
    env = make_vec_env(DangerStepEnv, n_envs=1, monitor_dir=log_dir)

    # Checkpoint callback for saving the model
    checkpoint_callback = CheckpointCallback(save_freq=10000, save_path='./trained_models/',
                                             name_prefix='dangerstep_model')

    # Load the model if exists, else create a new one
    model_path = './trained_models/dangerstep_model.zip'
   # if os.path.isfile(model_path):
      #  model = PPO.load(model_path, env=env)
   # else:
       # model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./tensorboard_logs/")

    # Train the agent
    score_logger = ScoreLoggerCallback(save_path=log_dir)
    model.learn(total_timesteps=1000000, callback=[checkpoint_callback, score_logger])

    # Save the agent
    model.save(model_path)

    # Evaluate the agent
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
    print(f"Mean reward: {mean_reward}, std: {std_reward}")

    # Watch the agent play
    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = env.step(action)
        env.render()

if __name__ == "__main__":
    main()