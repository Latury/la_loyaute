#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 * LA LOYAUTÉ - SCANNER AVANCÉ D'ERREURS PYLANCE/PYRIGHT v4.0
 * Développeur : Latury (Amélioré par Assistant)
 * Date : 19/01/2026
 * ═══════════════════════════════════════════════════════════════
 *
 * NOUVEAUTÉS v4.0 :
 * - Détection des types d'erreurs (error/warning/info)
 * - Catégorisation par type de problème
 * - Statistiques par sévérité
 * - Buffer augmenté (100MB pour gros projets)
 * - Mode verbose/silencieux
 * ═══════════════════════════════════════════════════════════════
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const { EMOJIS: E } = require("./emojis");
const { C, titre, succes, erreur, info, warn } = require("./couleurs_terminal");

// ═══════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════
const CONFIG = {
  rootDir: path.resolve(__dirname, ".."),
  utilsDir: __dirname,
  erreursDir: path.join(__dirname, "erreurs_pylance"),
  maxScans: 10, // Nombre de scans à conserver
  maxBuffer: 100 * 1024 * 1024, // 100MB buffer
  verboseMode:
    process.argv.includes("--verbose") || process.argv.includes("-v"),
};

// ═══════════════════════════════════════════════════════════════
// CATÉGORIES D'ERREURS
// ═══════════════════════════════════════════════════════════════
const ERROR_CATEGORIES = {
  "is not defined": {
    category: "Undefined",
    emoji: E.erreur,
    severity: "error",
  },
  "Cannot access member": {
    category: "Type",
    emoji: E.avertissement,
    severity: "warning",
  },
  "has no attribute": {
    category: "Attribute",
    emoji: E.question,
    severity: "error",
  },
  Import: { category: "Import", emoji: E.archive, severity: "error" },
  "Argument missing": {
    category: "Arguments",
    emoji: E.info,
    severity: "error",
  },
  "Too many arguments": {
    category: "Arguments",
    emoji: E.info,
    severity: "error",
  },
  Expected: { category: "Syntax", emoji: E.correction, severity: "error" },
  Indentation: {
    category: "Indentation",
    emoji: E.modification,
    severity: "error",
  },
  "not used": { category: "Unused", emoji: E.gris, severity: "info" },
  reportUnusedImport: { category: "Unused", emoji: E.gris, severity: "info" },
};

// ═══════════════════════════════════════════════════════════════
// FONCTION 01 - ensureDirs
// Crée les dossiers nécessaires
// ═══════════════════════════════════════════════════════════════
function ensureDirs() {
  if (!fs.existsSync(CONFIG.erreursDir)) {
    fs.mkdirSync(CONFIG.erreursDir, { recursive: true });
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 02 - checkPyright
// Vérifie si Pyright est installé
// ═══════════════════════════════════════════════════════════════
function checkPyright() {
  try {
    execSync("pyright --version", { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 03 - installPyright
// Installe Pyright via npm
// ═══════════════════════════════════════════════════════════════
function installPyright() {
  warn("Installation de Pyright en cours...");
  try {
    execSync("npm install -g pyright", { stdio: "inherit" });
    succes("Pyright installé avec succès");
    return true;
  } catch {
    erreur("Échec de l'installation");
    return false;
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 04 - getTimestamp
// Génère un timestamp pour noms de fichiers
// ═══════════════════════════════════════════════════════════════
function getTimestamp() {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return {
    filename: `erreurs_pylance_${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}_${pad(now.getHours())}h${pad(now.getMinutes())}m${pad(now.getSeconds())}s.json`,
    display: `${pad(now.getDate())}/${pad(now.getMonth() + 1)}/${now.getFullYear()} à ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`,
  };
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 05 - categorizeError
// Catégorise une erreur selon son message
// ═══════════════════════════════════════════════════════════════
function categorizeError(message) {
  for (const [keyword, meta] of Object.entries(ERROR_CATEGORIES)) {
    if (message.includes(keyword)) {
      return meta;
    }
  }
  return { category: "Other", emoji: E.info, severity: "warning" };
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 06 - scanWithPyright
// Lance Pyright et analyse les erreurs
// ═══════════════════════════════════════════════════════════════
function scanWithPyright() {
  const { filename, display } = getTimestamp();
  const outputPath = path.join(CONFIG.erreursDir, filename);

  try {
    info("Lancement de Pyright...");

    let result;
    try {
      result = execSync("pyright --outputjson", {
        cwd: CONFIG.rootDir,
        encoding: "utf8",
        maxBuffer: CONFIG.maxBuffer,
      });
    } catch (err) {
      // Pyright retourne un code d'erreur si des erreurs sont trouvées
      result = err.stdout || "{}";
    }

    // Parser le JSON
    let data;
    try {
      data = JSON.parse(result);
    } catch {
      warn("Réponse JSON invalide, utilisation des valeurs par défaut");
      data = { generalDiagnostics: [], summary: { errorCount: 0 } };
    }

    // Enrichir les diagnostics avec catégories
    const diagnostics = (data.generalDiagnostics || []).map((diag) => {
      const category = categorizeError(diag.message || "");
      return {
        ...diag,
        category: category.category,
        categoryEmoji: category.emoji,
        severity: diag.severity || category.severity,
      };
    });

    // Créer l'objet de sortie enrichi
    const output = {
      timestamp: display,
      projectRoot: CONFIG.rootDir,
      totalErrors: diagnostics.length,
      diagnostics: diagnostics,
      summary: data.summary || {},
      statistics: generateStatistics(diagnostics),
    };

    // Sauvegarder
    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), "utf8");

    return { outputPath, output };
  } catch (err) {
    erreur(`Erreur lors du scan : ${err.message}`);
    return null;
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 07 - generateStatistics
// Génère des statistiques détaillées sur les erreurs
// ═══════════════════════════════════════════════════════════════
function generateStatistics(diagnostics) {
  const stats = {
    bySeverity: { error: 0, warning: 0, info: 0 },
    byCategory: {},
    byFile: {},
    topFiles: [],
  };

  diagnostics.forEach((diag) => {
    // Par sévérité
    const severity = diag.severity || "warning";
    stats.bySeverity[severity] = (stats.bySeverity[severity] || 0) + 1;

    // Par catégorie
    const category = diag.category || "Other";
    stats.byCategory[category] = (stats.byCategory[category] || 0) + 1;

    // Par fichier
    const file = diag.file || "unknown";
    stats.byFile[file] = (stats.byFile[file] || 0) + 1;
  });

  // TOP 10 fichiers
  stats.topFiles = Object.entries(stats.byFile)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([file, count]) => ({
      file: path.basename(file),
      fullPath: file,
      count,
    }));

  return stats;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 08 - displayResults
// Affiche les résultats du scan
// ═══════════════════════════════════════════════════════════════
function displayResults(output) {
  const { totalErrors, statistics } = output;

  console.log("");
  console.log(`${C.BLEU_INTENSE}${"─".repeat(80)}${C.RESET}`);
  console.log(
    `${C.BLEU_INTENSE}│ ${E.rapport} RÉSULTATS DU SCAN${" ".repeat(61)}│${C.RESET}`,
  );
  console.log(`${C.BLEU_INTENSE}${"─".repeat(80)}${C.RESET}`);
  console.log("");

  // Total
  console.log(
    `  ${E.document} ${C.BOLD}Total :${C.RESET} ${totalErrors} erreur(s) détectée(s)`,
  );
  console.log("");

  // Par sévérité
  console.log(`  ${E.graphique} ${C.BOLD}Par sévérité :${C.RESET}`);
  console.log(
    `     ${C.ROUGE}${E.erreur} Erreurs       : ${statistics.bySeverity.error}${C.RESET}`,
  );
  console.log(
    `     ${C.JAUNE}${E.avertissement} Avertissements : ${statistics.bySeverity.warning}${C.RESET}`,
  );
  console.log(
    `     ${C.GRIS}${E.info} Informations   : ${statistics.bySeverity.info}${C.RESET}`,
  );
  console.log("");

  // Par catégorie (top 5)
  if (Object.keys(statistics.byCategory).length > 0) {
    console.log(`  ${E.tableau} ${C.BOLD}Top 5 catégories :${C.RESET}`);
    Object.entries(statistics.byCategory)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .forEach(([cat, count], idx) => {
        const category =
          Object.values(ERROR_CATEGORIES).find((c) => c.category === cat) || {};
        const emoji = category.emoji || E.info;
        console.log(`     ${idx + 1}. ${emoji} ${cat.padEnd(15)} : ${count}`);
      });
    console.log("");
  }

  // Top fichiers
  if (statistics.topFiles.length > 0) {
    console.log(
      `  ${E.fichier} ${C.BOLD}Top ${Math.min(5, statistics.topFiles.length)} fichiers :${C.RESET}`,
    );
    statistics.topFiles.slice(0, 5).forEach((f, idx) => {
      console.log(
        `     ${idx + 1}. ${f.file.padEnd(40)} ${C.ROUGE}${f.count} erreurs${C.RESET}`,
      );
    });
    console.log("");
  }

  console.log(`${C.BLEU_INTENSE}${"─".repeat(80)}${C.RESET}`);
  console.log("");

  // Suggestions
  if (totalErrors > 0) {
    console.log(`${E.bulleIdee} ${C.JAUNE}Prochaines étapes :${C.RESET}`);
    console.log(
      `   ${C.GRIS}1. Analyser les erreurs :${C.RESET} node diagnostiquer_erreurs.js`,
    );
    console.log(`   ${C.GRIS}2. Corriger manuellement dans VS Code${C.RESET}`);
    console.log(`   ${C.GRIS}3. Relancer le scan pour vérifier${C.RESET}`);
    console.log("");
  } else {
    console.log(
      `${E.celebration} ${C.VERT}Aucune erreur détectée ! Projet propre !${C.RESET}`,
    );
    console.log("");
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 09 - cleanOldScans
// Supprime les anciens scans (garde les 10 derniers)
// ═══════════════════════════════════════════════════════════════
function cleanOldScans() {
  if (!fs.existsSync(CONFIG.erreursDir)) return;

  const files = fs
    .readdirSync(CONFIG.erreursDir)
    .filter((f) => f.endsWith(".json"))
    .map((f) => ({
      name: f,
      path: path.join(CONFIG.erreursDir, f),
      time: fs.statSync(path.join(CONFIG.erreursDir, f)).mtime,
    }))
    .sort((a, b) => b.time - a.time);

  if (files.length > CONFIG.maxScans) {
    const toDelete = files.slice(CONFIG.maxScans);
    toDelete.forEach((file) => {
      fs.unlinkSync(file.path);
      if (CONFIG.verboseMode) {
        console.log(
          `${E.suppression} ${C.GRIS}Supprimé : ${file.name}${C.RESET}`,
        );
      }
    });
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 10 - main
// Fonction principale
// ═══════════════════════════════════════════════════════════════
function main() {
  titre("SCANNER D'ERREURS PYLANCE v4.0", E.recherche);

  ensureDirs();

  // Vérifier Pyright
  if (!checkPyright()) {
    warn("Pyright non installé");
    if (!installPyright()) {
      erreur("Impossible de continuer sans Pyright");
      process.exit(1);
    }
  }

  // Lancer le scan
  const result = scanWithPyright();
  if (!result) {
    process.exit(1);
  }

  const { outputPath, output } = result;

  // Afficher les résultats
  displayResults(output);

  // Nettoyer les anciens scans
  cleanOldScans();

  // Chemin du rapport
  console.log(`${E.sauvegarde} ${C.ORANGE}Rapport sauvegardé :${C.RESET}`);
  console.log(`${C.GRIS}   ${outputPath}${C.RESET}`);
  console.log("");
}

if (require.main === module) {
  main();
}

module.exports = { scanWithPyright, categorizeError, generateStatistics };
