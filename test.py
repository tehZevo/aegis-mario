from operator import itemgetter
import time

import cv2
import numpy as np
from protopost import protopost_client as ppcl
from nd_to_json import nd_to_json
from img_to_b64 import b64_to_img

#takes json action, returns b64 image obs, reward, done, info
MARIO = lambda action: ppcl("http://127.0.0.1:8080", action)

#https://github.com/Kautenja/gym-super-mario-bros/blob/master/gym_super_mario_bros/actions.py
NUM_ACTIONS = {
  "RIGHT_ONLY": 5,
  "SIMPLE_MOVEMENT": 7,
  "COMPLEX_MOVEMENT": 12
}

NUM_ACTIONS = NUM_ACTIONS["SIMPLE_MOVEMENT"]

def random_action():
  return np.random.random(size=NUM_ACTIONS)

cv2.namedWindow("img", cv2.WINDOW_NORMAL)

while True:
  action = random_action()
  action = nd_to_json(action)

  result = MARIO(action)
  obs, done, reward, info = itemgetter("obs", "done", "reward", "info")(result)
  obs = b64_to_img(obs)
  obs = cv2.cvtColor(obs, cv2.COLOR_BGR2RGB)
  cv2.imshow("img", obs)
  cv2.waitKey(1)
  print(reward)
