import os
import time
import json

from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

import cv2
import numpy as np
from protopost import ProtoPost
from nd_to_json import json_to_nd
from img_to_b64 import img_to_b64

PORT = int(os.getenv("PORT", 80))
RENDER = os.getenv("RENDER", "false") == "true"
RESIZE = os.getenv("RESIZE", None)
RESIZE = tuple(json.loads(RESIZE)) if RESIZE is not None else RESIZE #(14, 15)
GRAYSCALE = os.getenv("GRAYSCALE", "false") == "true"

env = gym_super_mario_bros.make('SuperMarioBros-v0')
env = JoypadSpace(env, SIMPLE_MOVEMENT)
obs = env.reset()

def encode_image(img, format=".png"):
  if RESIZE is not None:
    img = cv2.resize(img, RESIZE)
  if GRAYSCALE:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  img = img_to_b64(img, format=format)

  return img

def step(data):
  global obs
  #if no action, just return the current observation
  if data is None:
    return {"obs": encode_image(obs)}

  action = json_to_nd(data)
  # action = controller(action)
  action = np.argmax(action)
  obs, r, done, info = env.step(action)
  done = bool(done)
  r = float(r)
  if done:
    obs = env.reset()
  if RENDER:
    env.render()

  img = obs
  #encode image
  if RESIZE is not None:
    img = cv2.resize(img, RESIZE)
  if GRAYSCALE:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  img = img_to_b64(img, format=".png")

  return {"obs":img, "done":done, "reward":r, "info":{}} #TODO: fix info (need to convert np arrays or use orjson method)

routes = {
  "": step,
  "obs": lambda data: encode_image(obs)
}

ProtoPost(routes).start(PORT, threaded=False)
