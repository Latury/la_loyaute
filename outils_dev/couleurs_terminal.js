/**
 * ═══════════════════════════════════════════════════════════════
 * LA LOYAUTE - COULEURS TERMINAL
 * Module commun pour les couleurs ANSI dans le terminal
 * Developpe par Latury
 * Version 2.0.0 - 18/01/2026
 * ═══════════════════════════════════════════════════════════════
 */

const { EMOJIS: E } = require("./emojis");

// ═══════════════════════════════════════════════════════════════
// COULEURS ANSI
// ═══════════════════════════════════════════════════════════════

const Couleurs = {
  // ─────────────────────────────────────────────────────────────
  // BLEU INTENSE (pour les cadres)
  // ─────────────────────────────────────────────────────────────
  BLEU_INTENSE: "\x1b[1;34m",

  // ─────────────────────────────────────────────────────────────
  // ORANGE (pour les titres et highlights)
  // ─────────────────────────────────────────────────────────────
  ORANGE: "\x1b[38;5;208m",
  ORANGE_CLAIR: "\x1b[38;5;214m",

  // ─────────────────────────────────────────────────────────────
  // COULEURS STANDARDS
  // ─────────────────────────────────────────────────────────────
  VERT: "\x1b[92m",
  JAUNE: "\x1b[93m",
  ROUGE: "\x1b[91m",
  GRIS: "\x1b[90m",
  BLANC: "\x1b[97m",
  BLEU: "\x1b[94m",

  // ─────────────────────────────────────────────────────────────
  // STYLES DE TEXTE
  // ─────────────────────────────────────────────────────────────
  RESET: "\x1b[0m",
  BOLD: "\x1b[1m",
  DIM: "\x1b[2m",
  ITALIC: "\x1b[3m",
  UNDERLINE: "\x1b[4m",
  BLINK: "\x1b[5m",
  REVERSE: "\x1b[7m",
  HIDDEN: "\x1b[8m",

  // ─────────────────────────────────────────────────────────────
  // BACKGROUNDS
  // ─────────────────────────────────────────────────────────────
  BG_NOIR: "\x1b[40m",
  BG_ROUGE: "\x1b[41m",
  BG_VERT: "\x1b[42m",
  BG_JAUNE: "\x1b[43m",
  BG_BLEU: "\x1b[44m",
  BG_BLANC: "\x1b[47m",
};

// ═══════════════════════════════════════════════════════════════
// FONCTION 01 - coloriser
// Applique une couleur a un texte
// ═══════════════════════════════════════════════════════════════
function coloriser(texte, couleur) {
  return `${couleur}${texte}${Couleurs.RESET}`;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 02 - cadre
// Cree un cadre autour d'un texte
// ═══════════════════════════════════════════════════════════════
function cadre(texte, largeur = 80) {
  const ligneHaut = `${Couleurs.BLEU_INTENSE}┌${"─".repeat(largeur - 2)}┐${Couleurs.RESET}`;
  const ligneBas = `${Couleurs.BLEU_INTENSE}└${"─".repeat(largeur - 2)}┘${Couleurs.RESET}`;
  const lignesTexte = texte.split("\n").map((ligne) => {
    const espaces = largeur - 4 - ligne.length;
    return `${Couleurs.BLEU_INTENSE}│${Couleurs.RESET} ${ligne}${" ".repeat(espaces)} ${Couleurs.BLEU_INTENSE}│${Couleurs.RESET}`;
  });
  return [ligneHaut, ...lignesTexte, ligneBas].join("\n");
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 03 - separateur
// Cree une ligne de separation
// ═══════════════════════════════════════════════════════════════
function separateur(largeur = 80, caractere = "─") {
  return `${Couleurs.BLEU_INTENSE}${caractere.repeat(largeur)}${Couleurs.RESET}`;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 04 - titre
// Affiche un titre encadre avec emoji
// ═══════════════════════════════════════════════════════════════
function titre(texte, emoji = null) {
  const icone = emoji || E.document;
  console.log(`\n${Couleurs.BLEU_INTENSE}${"═".repeat(80)}${Couleurs.RESET}`);
  console.log(
    `${Couleurs.BLEU_INTENSE}│ ${icone} ${texte}${" ".repeat(75 - texte.length)}│${Couleurs.RESET}`,
  );
  console.log(`${Couleurs.BLEU_INTENSE}${"═".repeat(80)}${Couleurs.RESET}\n`);
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 05 - succes
// Affiche un message de succes
// ═══════════════════════════════════════════════════════════════
function succes(message) {
  console.log(`${Couleurs.VERT}${E.succes} ${message}${Couleurs.RESET}`);
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 06 - erreur
// Affiche un message d'erreur
// ═══════════════════════════════════════════════════════════════
function erreur(message) {
  console.log(`${Couleurs.ROUGE}${E.erreur} ${message}${Couleurs.RESET}`);
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 07 - avertissement
// Affiche un message d'avertissement
// ═══════════════════════════════════════════════════════════════
function avertissement(message) {
  console.log(
    `${Couleurs.JAUNE}${E.avertissement} ${message}${Couleurs.RESET}`,
  );
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 08 - info
// Affiche un message d'information
// ═══════════════════════════════════════════════════════════════
function info(message) {
  console.log(`${Couleurs.ORANGE}${E.info} ${message}${Couleurs.RESET}`);
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 09 - chargement
// Affiche un message de chargement
// ═══════════════════════════════════════════════════════════════
function chargement(message) {
  console.log(`${Couleurs.ORANGE}${E.recherche} ${message}${Couleurs.RESET}`);
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  ...Couleurs,
  C: Couleurs,
  E: E, // Export des emojis aussi
  coloriser,
  cadre,
  separateur,
  titre,
  succes,
  erreur,
  avertissement,
  info,
  chargement,
  ok: succes,
  ko: erreur,
  warn: avertissement,
};

// ═══════════════════════════════════════════════════════════════
// EXEMPLE D'UTILISATION
// ═══════════════════════════════════════════════════════════════

if (require.main === module) {
  console.log(`\n${E.menu} Test du module Couleurs Terminal\n`);

  titre("LA LOYAUTE - MODULE COULEURS", E.menu);

  console.log("Couleurs de base :");
  console.log(`  ${coloriser("BLEU INTENSE", Couleurs.BLEU_INTENSE)}`);
  console.log(`  ${coloriser("ORANGE", Couleurs.ORANGE)}`);
  console.log(`  ${coloriser("VERT", Couleurs.VERT)}`);
  console.log(`  ${coloriser("JAUNE", Couleurs.JAUNE)}`);
  console.log(`  ${coloriser("ROUGE", Couleurs.ROUGE)}`);

  console.log("\nMessages d'etat :");
  succes("Operation reussie !");
  erreur("Une erreur est survenue");
  avertissement("Attention, fichier volumineux");
  info("Information : 42 fichiers trouves");
  chargement("Analyse en cours...");

  console.log("\n" + separateur());

  console.log("\nCadre :");
  console.log(
    cadre(
      `${E.menu} LA LOYAUTE\n${E.archive} Version 2.0.0\n${E.fusee} Node.js Edition`,
    ),
  );

  console.log(`\n${E.succes} Test termine !\n`);
}
