#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 * LA LOYAUTE - NETTOYEUR DE CACHE ULTRA-PUISSANT
 * Version : 3.0.0
 * Developpeur : Latury
 * Date : 18/01/2026
 * ═══════════════════════════════════════════════════════════════
 */

const fs = require("fs");
const path = require("path");
const { EMOJIS: E } = require("./emojis");

// ═══════════════════════════════════════════════════════════════
// COULEURS
// ═══════════════════════════════════════════════════════════════
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
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════
const CONFIG = {
  rootDir: path.resolve(__dirname, ".."),
  outilsDir: __dirname,
  rapportsDir: path.resolve(__dirname, "rapports"),

  cacheTypes: {
    python: [
      "__pycache__",
      ".pytest_cache",
      ".mypy_cache",
      ".ruff_cache",
      ".coverage",
      "*.pyc",
      "*.pyo",
      "*.pyd",
      ".Python",
    ],
    nodejs: ["node_modules/.cache", ".npm", ".yarn", ".pnp"],
    vscode: [".vscode/.ropeproject", ".vscode-test"],
    discord: [".discordpy_cache", "discord_cache"],
    temp: ["*.tmp", "*.temp", "*.log~", ".DS_Store", "Thumbs.db"],
    build: ["build", "dist", "*.egg-info", ".eggs"],
  },

  ignoredDirs: [".venv", "venv", ".git", "node_modules", ".idea"],
  tempExtensions: [".tmp", ".temp", ".bak", ".old", ".orig", "~"],
};

// ═══════════════════════════════════════════════════════════════
// STATISTIQUES
// ═══════════════════════════════════════════════════════════════
let STATS = {
  totalDeleted: 0,
  totalSize: 0,
  byType: {},
  deletedItems: [],
  errors: [],
  startTime: Date.now(),
};

let LOG_BUFFER = [];

// ═══════════════════════════════════════════════════════════════
// FONCTION 01 - log
// Affiche un message dans la console et le buffer
// ═══════════════════════════════════════════════════════════════
function log(message, toBuffer = true) {
  console.log(message);
  if (toBuffer) {
    LOG_BUFFER.push(message.replace(/\x1b\[[0-9;]*m/g, ""));
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 02 - getTimestamp
// Genere un timestamp pour noms de fichiers et affichage
// ═══════════════════════════════════════════════════════════════
function getTimestamp() {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return {
    filename: `rapport_nettoyage_${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}.txt`,
    display: `${pad(now.getDate())}/${pad(now.getMonth() + 1)}/${now.getFullYear()} a ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`,
  };
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 03 - formatSize
// Convertit une taille en octets vers format lisible
// ═══════════════════════════════════════════════════════════════
function formatSize(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 04 - getDirectorySize
// Calcule la taille totale d'un dossier
// ═══════════════════════════════════════════════════════════════
function getDirectorySize(dirPath) {
  let totalSize = 0;
  try {
    const items = fs.readdirSync(dirPath);
    for (const item of items) {
      const fullPath = path.join(dirPath, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        totalSize += getDirectorySize(fullPath);
      } else {
        totalSize += stat.size;
      }
    }
  } catch (err) {
    // Ignorer les erreurs de permission
  }
  return totalSize;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 05 - getFileSize
// Recupere la taille d'un fichier
// ═══════════════════════════════════════════════════════════════
function getFileSize(filePath) {
  try {
    return fs.statSync(filePath).size;
  } catch {
    return 0;
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 06 - deleteDirectory
// Supprime un dossier et met a jour les statistiques
// ═══════════════════════════════════════════════════════════════
function deleteDirectory(dirPath, cacheType = "unknown") {
  try {
    if (!fs.existsSync(dirPath)) return 0;

    const size = getDirectorySize(dirPath);
    const items = fs.readdirSync(dirPath);

    for (const item of items) {
      const fullPath = path.join(dirPath, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        deleteDirectory(fullPath, cacheType);
      } else {
        fs.unlinkSync(fullPath);
      }
    }

    fs.rmdirSync(dirPath);

    STATS.totalDeleted++;
    STATS.totalSize += size;
    if (!STATS.byType[cacheType])
      STATS.byType[cacheType] = { count: 0, size: 0 };
    STATS.byType[cacheType].count++;
    STATS.byType[cacheType].size += size;

    STATS.deletedItems.push({
      path: path.relative(CONFIG.rootDir, dirPath),
      type: cacheType,
      size: size,
    });

    return size;
  } catch (err) {
    STATS.errors.push({
      path: dirPath,
      error: err.message,
    });
    return 0;
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 07 - deleteFile
// Supprime un fichier et met a jour les statistiques
// ═══════════════════════════════════════════════════════════════
function deleteFile(filePath, cacheType = "temp") {
  try {
    if (!fs.existsSync(filePath)) return 0;

    const size = getFileSize(filePath);
    fs.unlinkSync(filePath);

    STATS.totalDeleted++;
    STATS.totalSize += size;
    if (!STATS.byType[cacheType])
      STATS.byType[cacheType] = { count: 0, size: 0 };
    STATS.byType[cacheType].count++;
    STATS.byType[cacheType].size += size;

    STATS.deletedItems.push({
      path: path.relative(CONFIG.rootDir, filePath),
      type: cacheType,
      size: size,
    });

    return size;
  } catch (err) {
    STATS.errors.push({
      path: filePath,
      error: err.message,
    });
    return 0;
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 08 - matchesPattern
// Verifie si un nom correspond a un pattern
// ═══════════════════════════════════════════════════════════════
function matchesPattern(itemName, pattern) {
  if (pattern.startsWith("*")) {
    return itemName.endsWith(pattern.slice(1));
  }
  if (pattern.endsWith("*")) {
    return itemName.startsWith(pattern.slice(0, -1));
  }
  return itemName === pattern;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 09 - drawProgressBar
// Dessine une barre de progression
// ═══════════════════════════════════════════════════════════════
function drawProgressBar(current, total, width = 40) {
  const percent = Math.round((current / total) * 100);
  const filled = Math.round((percent / 100) * width);
  const empty = width - filled;
  const bar = E.barrePleine.repeat(filled) + E.barreVide.repeat(empty);
  return `[${bar}] ${percent}%`;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 10 - scanAndClean
// Scan recursif et suppression des caches
// ═══════════════════════════════════════════════════════════════
function scanAndClean(dirPath, depth = 0) {
  if (depth > 20) return;

  try {
    const items = fs.readdirSync(dirPath);

    for (const item of items) {
      if (depth === 0 && CONFIG.ignoredDirs.includes(item)) {
        continue;
      }

      const fullPath = path.join(dirPath, item);
      let stat;

      try {
        stat = fs.statSync(fullPath);
      } catch (err) {
        continue;
      }

      if (stat.isDirectory()) {
        let cacheType = null;

        for (const [type, patterns] of Object.entries(CONFIG.cacheTypes)) {
          for (const pattern of patterns) {
            if (!pattern.includes("*") && item === pattern) {
              cacheType = type;
              break;
            }
          }
          if (cacheType) break;
        }

        if (cacheType) {
          deleteDirectory(fullPath, cacheType);
        } else {
          scanAndClean(fullPath, depth + 1);
        }
      } else {
        let isTempFile = false;

        for (const ext of CONFIG.tempExtensions) {
          if (item.endsWith(ext)) {
            isTempFile = true;
            break;
          }
        }

        if (!isTempFile) {
          for (const [type, patterns] of Object.entries(CONFIG.cacheTypes)) {
            for (const pattern of patterns) {
              if (pattern.includes("*") && matchesPattern(item, pattern)) {
                isTempFile = true;
                break;
              }
            }
            if (isTempFile) break;
          }
        }

        if (isTempFile) {
          deleteFile(fullPath, "temp");
        }
      }
    }
  } catch (err) {
    // Ignorer les erreurs de lecture
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 11 - cleanOldReports
// Supprime les anciens rapports pour economiser l'espace
// ═══════════════════════════════════════════════════════════════
function cleanOldReports() {
  if (!fs.existsSync(CONFIG.rapportsDir)) return;

  try {
    const reports = fs
      .readdirSync(CONFIG.rapportsDir)
      .filter((f) => f.startsWith("rapport_nettoyage_"))
      .map((f) => ({
        name: f,
        path: path.join(CONFIG.rapportsDir, f),
        time: fs.statSync(path.join(CONFIG.rapportsDir, f)).mtime,
      }))
      .sort((a, b) => b.time - a.time);

    if (reports.length > 15) {
      reports.slice(15).forEach((report) => {
        fs.unlinkSync(report.path);
      });

      log(
        `  ${C.gris}${reports.length - 15} ancien(s) rapport(s) supprime(s)${C.reset}`,
      );
    }
  } catch (err) {
    // Ignorer les erreurs
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 12 - saveReport
// Sauvegarde le rapport de nettoyage
// ═══════════════════════════════════════════════════════════════
function saveReport() {
  if (!fs.existsSync(CONFIG.rapportsDir)) {
    fs.mkdirSync(CONFIG.rapportsDir, { recursive: true });
  }

  const { filename } = getTimestamp();
  const reportPath = path.join(CONFIG.rapportsDir, filename);

  const duration = ((Date.now() - STATS.startTime) / 1000).toFixed(2);

  LOG_BUFFER.push("");
  LOG_BUFFER.push("═".repeat(80));
  LOG_BUFFER.push("STATISTIQUES PAR TYPE");
  LOG_BUFFER.push("═".repeat(80));

  Object.entries(STATS.byType).forEach(([type, data]) => {
    LOG_BUFFER.push(
      `  ${type.toUpperCase().padEnd(20)} : ${data.count} element(s) | ${formatSize(data.size)}`,
    );
  });

  LOG_BUFFER.push("");
  LOG_BUFFER.push("═".repeat(80));
  LOG_BUFFER.push("ELEMENTS SUPPRIMES (20 premiers)");
  LOG_BUFFER.push("═".repeat(80));

  STATS.deletedItems.slice(0, 20).forEach((item) => {
    LOG_BUFFER.push(`  [${item.type}] ${item.path} (${formatSize(item.size)})`);
  });

  if (STATS.deletedItems.length > 20) {
    LOG_BUFFER.push(`  ... et ${STATS.deletedItems.length - 20} autre(s)`);
  }

  if (STATS.errors.length > 0) {
    LOG_BUFFER.push("");
    LOG_BUFFER.push("═".repeat(80));
    LOG_BUFFER.push("ERREURS RENCONTREES");
    LOG_BUFFER.push("═".repeat(80));

    STATS.errors.slice(0, 10).forEach((err) => {
      LOG_BUFFER.push(`  ${err.path}: ${err.error}`);
    });
  }

  LOG_BUFFER.push("");
  LOG_BUFFER.push(`Duree totale : ${duration}s`);

  fs.writeFileSync(reportPath, LOG_BUFFER.join("\n"), "utf8");

  log("");
  log(
    `${E.succes} ${C.vert}Rapport sauvegarde : ${C.bold}${filename}${C.reset}`,
    false,
  );
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 13 - displayResults
// Affiche les resultats du nettoyage
// ═══════════════════════════════════════════════════════════════
function displayResults() {
  log("");
  log(`${C.bleuIntense}┌${"─".repeat(78)}┐${C.reset}`);
  log(`${C.bleuIntense}│  RESULTATS DU NETTOYAGE${" ".repeat(53)}│${C.reset}`);
  log(`${C.bleuIntense}└${"─".repeat(78)}┘${C.reset}`);
  log("");

  if (STATS.totalDeleted === 0) {
    log(
      `  ${E.validation} ${C.vert}Aucun cache trouve - Projet deja propre${C.reset}`,
    );
  } else {
    log(`  ${C.bold}Elements supprimes${C.reset} : ${STATS.totalDeleted}`);
    log(
      `  ${C.bold}Espace recupere${C.reset}   : ${formatSize(STATS.totalSize)}`,
    );

    log("");
    log(`  ${C.orange}Details par type :${C.reset}`);
    log("");

    const sortedTypes = Object.entries(STATS.byType).sort(
      (a, b) => b[1].size - a[1].size,
    );

    sortedTypes.forEach(([type, data]) => {
      const icon =
        {
          python: E.python,
          nodejs: E.nodejs,
          vscode: E.vscode,
          discord: E.discord,
          temp: E.suppression,
          build: E.build,
        }[type] || E.dossier;

      log(
        `    ${icon} ${type.padEnd(12)} : ${String(data.count).padStart(3)} element(s) | ${formatSize(data.size)}`,
      );
    });

    log("");
    log(`  ${C.jaune}Apercu des suppressions (10 premiers) :${C.reset}`);
    log("");

    STATS.deletedItems.slice(0, 10).forEach((item, index) => {
      const preview =
        item.path.length > 60 ? "..." + item.path.slice(-57) : item.path;
      log(`    ${index + 1}. ${C.gris}${preview}${C.reset}`);
    });

    if (STATS.deletedItems.length > 10) {
      log(
        `    ${C.gris}... et ${STATS.deletedItems.length - 10} autre(s)${C.reset}`,
      );
    }
  }

  if (STATS.errors.length > 0) {
    log("");
    log(
      `  ${E.echec} ${C.rouge}${STATS.errors.length} erreur(s) rencontree(s) (voir rapport)${C.reset}`,
    );
  }

  const duration = ((Date.now() - STATS.startTime) / 1000).toFixed(2);
  log("");
  log(`  ${C.gris}Duree : ${duration}s${C.reset}`);

  log("");
  log(`${C.bleuIntense}${"─".repeat(80)}${C.reset}`);
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 14 - main
// Fonction principale du nettoyeur
// ═══════════════════════════════════════════════════════════════
function main() {
  log("");
  log(`${C.bleuIntense}┌${"─".repeat(78)}┐${C.reset}`);
  log(`${C.bleuIntense}│${" ".repeat(78)}│${C.reset}`);
  log(
    `${C.bleuIntense}│  NETTOYEUR DE CACHE ULTRA-PUISSANT${" ".repeat(42)}│${C.reset}`,
  );
  log(
    `${C.bleuIntense}│  Version 3.0.0 - LA LOYAUTE${" ".repeat(49)}│${C.reset}`,
  );
  log(`${C.bleuIntense}│${" ".repeat(78)}│${C.reset}`);
  log(`${C.bleuIntense}└${"─".repeat(78)}┘${C.reset}`);
  log("");

  log(
    `  ${E.dossier} ${C.orange}Projet :${C.reset} ${C.bold}${CONFIG.rootDir}${C.reset}`,
  );
  log("");

  log(`  ${E.recherche} ${C.orange}Types de caches recherches :${C.reset}`);
  log(`     ${E.python} Python (${CONFIG.cacheTypes.python.length} patterns)`);
  log(`     ${E.nodejs} Node.js (${CONFIG.cacheTypes.nodejs.length} patterns)`);
  log(`     ${E.vscode} VS Code (${CONFIG.cacheTypes.vscode.length} patterns)`);
  log(
    `     ${E.discord} Discord.py (${CONFIG.cacheTypes.discord.length} patterns)`,
  );
  log(
    `     ${E.suppression} Fichiers temporaires (${CONFIG.cacheTypes.temp.length} patterns)`,
  );
  log(
    `     ${E.build} Build artifacts (${CONFIG.cacheTypes.build.length} patterns)`,
  );

  log("");
  log(`  ${E.fusee} ${C.orange}Scan en cours...${C.reset}`);
  log("");

  const totalSteps = 100;
  for (let i = 0; i <= totalSteps; i += 10) {
    process.stdout.write(
      `\r     ${C.orange}Progression : ${drawProgressBar(i, totalSteps)}${C.reset}`,
    );
    if (i === 0 || i === 50) scanAndClean(CONFIG.rootDir);
  }

  log("\n");

  cleanOldReports();
  displayResults();
  saveReport();

  log("");
  if (STATS.totalDeleted > 0) {
    log(
      `  ${E.celebration} ${C.vert}Projet nettoye avec succes ! Espace libere : ${C.bold}${formatSize(STATS.totalSize)}${C.reset}`,
    );
  } else {
    log(`  ${E.propre} ${C.vert}Projet deja propre !${C.reset}`);
  }

  log(
    `  ${E.calendrier} ${C.gris}Nettoye le : ${getTimestamp().display}${C.reset}`,
  );
  log("");
}

if (require.main === module) {
  main();
}

module.exports = { scanAndClean, deleteDirectory, deleteFile };
