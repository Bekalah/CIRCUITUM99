// ND-safe: adjusts companion logic without animation or network.
export function onArcanaSwitch(state, companions) {
  if (state.arcana === 'OCTA-FORTUNE') {
    companions.mode = 'seer_guardian';
    state.pathworking = {
      style: 'gentle mirror riddles',
      hygiene: 'psychic checks before deep dives'
    };
  }
}
