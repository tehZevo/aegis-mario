# Aegis Super Mario Bros. node
*It's-a me!*

Powered by [gym-super-mario-bros](https://github.com/Kautenja/gym-super-mario-bros)

## Environment
- `RESIZE` - if non-None, resize the screen images to this size (defaults to None)
- `GRAYSCALE` - if true, convert the screen images to grayscale (defaults to false)
- `ACTIONS` - one of `RIGHT_ONLY`, `SIMPLE_MOVEMENT`, or `COMPLEX_MOVEMENT` (defaults to `SIMPLE_MOVEMENT`; see https://github.com/Kautenja/gym-super-mario-bros/blob/master/gym_super_mario_bros/actions.py)
- `PORT` - the port to listen on (defaults to 80)
- `RENDER` - if true, render the environment

## Usage
POST an [nd-to-json](https://github.com/tehZevo/nd-to-json)-encoded array to `/` to step the environment; returns:
```js
{
  obs: "<base64 encoded image>",
  done: false, //true if environment reset
  reward: 0.1 //reward of current step
  // info: {...} //jk, info is broken currently
}
```
Also, if you POST null to `/`, it will only return:
```js
{
  obs: "<base64 encoded image>"
}
```

## Notes
- the env auto-resets

## TODO
- allow udlrab multibinary space
- fix info dict (coerce values in info to json friendly types)
- add route for reset
- add env var for starting on individual stages/versions (https://github.com/Kautenja/gym-super-mario-bros#individual-stages)
- support saving videos using monitor
