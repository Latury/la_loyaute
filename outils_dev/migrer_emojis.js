#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 * LA LOYAUTE - MIGRATION AUTOMATIQUE VERS EMOJIS CENTRALISES
 * Version : 2.0.0
 * Developpeur : Latury
 * Date : 18/01/2026
 * ═══════════════════════════════════════════════════════════════
 */

const fs = require("fs");
const path = require("path");
const { EMOJIS: E } = require("./emojis");

const C = {
  bleuIntense: "\x1b[1;34m",
  orange: "\x1b[38;5;208m",
  vert: "\x1b[92m",
  jaune: "\x1b[93m",
  rouge: "\x1b[91m",
  gris: "\x1b[90m",
  reset: "\x1b[0m",
  bold: "\x1b[1m",
};

// ═══════════════════════════════════════════════════════════════
// MAPPING EMOJIS VERS VARIABLES
// ═══════════════════════════════════════════════════════════════
const EMOJI_MAP = {
  "✅": "E.succes",
  "❌": "E.erreur",
  "⚠️": "E.avertissement",
  "ℹ️": "E.info",
  "❓": "E.question",
  "⚡": "E.attention",
  "✓": "E.validation",
  "✗": "E.echec",
  "📄": "E.fichier",
  "📁": "E.dossier",
  "📋": "E.document",
  "📊": "E.rapport",
  "💾": "E.sauvegarde",
  "📦": "E.archive",
  "🔍": "E.recherche",
  "🔎": "E.scan",
  "🧹": "E.nettoyage",
  "🗑️": "E.suppression",
  "🔧": "E.correction",
  "✨": "E.creation",
  "📝": "E.modification",
  "⏳": "E.chargement",
  "⏱️": "E.horloge",
  "📅": "E.calendrier",
  "🚀": "E.fusee",
  "🔥": "E.feu",
  "⭐": "E.etoile",
  "🎉": "E.celebration",
  "🐍": "E.python",
  "💻": "E.vscode",
  "🤖": "E.discord",
  "🔨": "E.build",
  "💡": "E.bulleIdee",
  "💬": "E.message",
  "🔔": "E.notification",
  "🚨": "E.alerte",
  "📢": "E.megaphone",
  "🎮": "E.menu",
  "⚙️": "E.configuration",
  "🛠️": "E.outils",
  "📈": "E.tableau",
  "🔒": "E.verrouille",
  "🔓": "E.deverrouille",
  "■": "E.barrePleine",
  "□": "E.barreVide",
  "▶": "E.fleche",
  "●": "E.puce",
  "🧪": "E.test",
  "🐛": "E.debug",
  "🔐": "E.securite",
  "🌐": "E.reseau",
};

// ═══════════════════════════════════════════════════════════════
// FONCTION 01 - migrerFichier
// Migre un fichier vers le systeme d'emojis centralise
// ═══════════════════════════════════════════════════════════════
function migrerFichier(filePath) {
  let content = fs.readFileSync(filePath, "utf8");
  let modified = false;

  // Verifier si le fichier importe deja emojis.js
  if (!content.includes('require("./emojis")')) {
    // Ajouter l'import apres les autres requires
    const requireRegex = /(const .+ = require\(.+\);)\n/g;
    const matches = content.match(requireRegex);
    if (matches) {
      const lastRequire = matches[matches.length - 1];
      content = content.replace(
        lastRequire,
        lastRequire + 'const { EMOJIS: E } = require("./emojis");\n',
      );
      modified = true;
    }
  }

  // Remplacer les emojis litteraux par les variables
  for (const [emoji, variable] of Object.entries(EMOJI_MAP)) {
    const regex = new RegExp(
      `"${emoji.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}"`,
      "g",
    );
    if (content.match(regex)) {
      content = content.replace(regex, variable);
      modified = true;
    }
  }

  if (modified) {
    fs.writeFileSync(filePath, content, "utf8");
    return true;
  }

  return false;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 02 - main
// Fonction principale de migration
// ═══════════════════════════════════════════════════════════════
function main() {
  console.log("");
  console.log(`${C.bleuIntense}┌${"─".repeat(78)}┐${C.reset}`);
  console.log(`${C.bleuIntense}│${" ".repeat(78)}│${C.reset}`);
  console.log(
    `${C.bleuIntense}│  MIGRATION VERS EMOJIS CENTRALISES${" ".repeat(42)}│${C.reset}`,
  );
  console.log(`${C.bleuIntense}│  Version 2.0.0${" ".repeat(63)}│${C.reset}`);
  console.log(`${C.bleuIntense}│${" ".repeat(78)}│${C.reset}`);
  console.log(`${C.bleuIntense}└${"─".repeat(78)}┘${C.reset}`);
  console.log("");

  const fichiers = [
    "scanner_erreurs.js",
    "correcteur_intelligent.js",
    "diagnostiquer_erreurs.js",
    "vider_cache.js",
    "couleurs_terminal.js",
    "analyser_projet.js",
    "corriger_erreurs_auto.js",
    "detecter_doublons.js",
    "tester_projet.js",
  ];

  let count = 0;
  let errors = 0;

  fichiers.forEach((fichier) => {
    const filePath = path.join(__dirname, fichier);
    if (fs.existsSync(filePath)) {
      try {
        if (migrerFichier(filePath)) {
          console.log(`  ${E.succes} ${C.vert}${fichier} migre${C.reset}`);
          count++;
        } else {
          console.log(`  ${E.info} ${C.gris}${fichier} deja a jour${C.reset}`);
        }
      } catch (err) {
        console.log(
          `  ${E.erreur} ${C.rouge}${fichier} : ${err.message}${C.reset}`,
        );
        errors++;
      }
    } else {
      console.log(
        `  ${E.avertissement} ${C.jaune}${fichier} introuvable${C.reset}`,
      );
    }
  });

  console.log("");
  console.log(`${C.bleuIntense}${"─".repeat(80)}${C.reset}`);
  console.log(
    `  ${E.celebration} ${C.vert}${count} fichier(s) migre(s)${C.reset}`,
  );
  if (errors > 0) {
    console.log(`  ${E.erreur} ${C.rouge}${errors} erreur(s)${C.reset}`);
  }
  console.log("");
}

if (require.main === module) {
  main();
}

module.exports = { migrerFichier, EMOJI_MAP };
