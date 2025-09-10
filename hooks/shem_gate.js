// Runtime: summon a Shem angel + paired shadow daemon; modulate by Tarot.
export function openShemGate(index, currentArcana){
  const angel = `Shem_${String(index).padStart(2,"0")}`;
  const daemon = `Shadow_${String(index).padStart(2,"0")}`;
  const mode = (currentArcana.includes("The Tower")) ? "trial" :
               (currentArcana.includes("Temperance")) ? "reconcile" :
               (currentArcana.includes("The Star")) ? "heal" : "learn";
  return { angel, daemon, mode };
}
