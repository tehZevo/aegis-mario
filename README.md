# Aegis Super Mario Bros. node
*It's-a me!*

Powered by [gym-super-mario-bros](https://github.com/Kautenja/gym-super-mario-bros)

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
- document req/res; env vars
- document controls (udlrab)
- fix info dict (coerce values in info to json friendly types)
