import os
import time
import json

from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import RIGHT_ONLY, SIMPLE_MOVEMENT, COMPLEX_MOVEMENT
import gym

import cv2
import numpy as np
from scipy.special import softmax
from protopost import ProtoPost
from nd_to_json import json_to_nd
from img_to_b64 import img_to_b64

PORT = int(os.getenv("PORT", 80))
RENDER = os.getenv("RENDER", "false") == "true"
RESIZE = os.getenv("RESIZE", None)
RESIZE = tuple(json.loads(RESIZE)) if RESIZE is not None else RESIZE #(14, 15)
ACTION_REPEAT = int(os.getenv("ACTION_REPEAT", 1))
GRAYSCALE = os.getenv("GRAYSCALE", "false") == "true"
ACTIONS = os.getenv("ACTIONS", "SIMPLE_MOVEMENT")
ACTION_CHOICE = os.getenv("ACTION_CHOICE", "argmax")

#https://github.com/Kautenja/gym-super-mario-bros/blob/master/gym_super_mario_bros/actions.py
action_spaces = {
  "RIGHT_ONLY": RIGHT_ONLY,             #N=5
  "SIMPLE_MOVEMENT": SIMPLE_MOVEMENT,   #N=7
  "COMPLEX_MOVEMENT": COMPLEX_MOVEMENT  #N=12
}

env = gym.make("SuperMarioBros-v0", apply_api_compatibility=True)
env = JoypadSpace(env, action_spaces[ACTIONS])
obs, _ = env.reset()

def encode_image(img, format=".png"):
  if RESIZE is not None:
    img = cv2.resize(img, RESIZE)
  if GRAYSCALE:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  img = img_to_b64(img, format=format)

  return img

def choose_action(x, method):
  if method == "softmax":
    return np.random.choice(len(x), p=softmax(x))

  return np.argmax(x)

def step(data):
  global obs
  #if no action, just return the current observation
  if data is None:
    return {"obs": encode_image(obs)}

  action = json_to_nd(data)
  action = choose_action(action, ACTION_CHOICE)
  reward = 0
  for _ in range(ACTION_REPEAT):
    obs, r, done, terminated, info = env.step(action)
    reward += r
    if done or terminated:
      break
  reward = float(reward)
  done = bool(done)
  terminated = bool(terminated)
  if done:
    obs, _ = env.reset()
  if RENDER:
    env.render()

  #encode observation
  img = encode_image(obs)

  #TODO: fix info (need to convert np arrays or use orjson method)
  return {"obs":img, "done":done, "terminated":terminated, "reward":reward, "info":{}}

routes = {
  "": step,
  "obs": lambda data: encode_image(obs)
}

ProtoPost(routes).start(PORT, threaded=False)
