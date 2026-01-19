#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 * LA LOYAUTÉ - DIAGNOSTIC INTERACTIF DES ERREURS v4.3
 * Développeur : Latury (Amélioré par Assistant)
 * Date : 19/01/2026
 * ═══════════════════════════════════════════════════════════════
 *
 * NOUVELLES FONCTIONNALITÉS v4.3 :
 * - 📋 Menu immédiat : Copier OU Voir détails
 * - Copie rapide des erreurs sans tout afficher
 * - Navigation améliorée fichier par fichier
 * - Filtrage par sévérité (error/warning/info)
 * ═══════════════════════════════════════════════════════════════
 */

const fs = require("fs");
const path = require("path");
const readline = require("readline");
const { execSync } = require("child_process");
const { EMOJIS: E } = require("./emojis");
const { C, titre, succes, erreur, warn, info } = require("./couleurs_terminal");

const CONFIG = {
  rootDir: path.resolve(__dirname, ".."),
  erreursDir: path.join(__dirname, "erreurs_pylance"),
  contextLines: 2,
};

// ═══════════════════════════════════════════════════════════════
// FONCTION 01 - loadLatestScan
// ═══════════════════════════════════════════════════════════════
function loadLatestScan() {
  if (!fs.existsSync(CONFIG.erreursDir)) {
    return null;
  }

  const files = fs
    .readdirSync(CONFIG.erreursDir)
    .filter((f) => f.endsWith(".json"))
    .map((f) => ({
      path: path.join(CONFIG.erreursDir, f),
      time: fs.statSync(path.join(CONFIG.erreursDir, f)).mtime,
    }))
    .sort((a, b) => b.time - a.time);

  if (files.length === 0) return null;

  try {
    const data = JSON.parse(fs.readFileSync(files[0].path, "utf8"));
    return data;
  } catch (err) {
    return null;
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 02 - normalizePath
// ═══════════════════════════════════════════════════════════════
function normalizePath(filePath) {
  return filePath.replace(/\//g, path.sep).replace(/^\/c:/i, "C:");
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 03 - groupErrorsByFile
// ═══════════════════════════════════════════════════════════════
function groupErrorsByFile(diagnostics, filter = null) {
  const byFile = {};

  diagnostics.forEach((diag) => {
    if (filter && diag.severity !== filter) return;

    const filePath = normalizePath(diag.file || "unknown");
    if (!byFile[filePath]) {
      byFile[filePath] = [];
    }

    byFile[filePath].push(diag);
  });

  return byFile;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 04 - formatErrorsForClipboard
// ═══════════════════════════════════════════════════════════════
function formatErrorsForClipboard(filePath, errors) {
  const fileName = path.basename(filePath);
  let output = [];

  output.push("═".repeat(80));
  output.push(`RAPPORT D'ERREURS - ${fileName}`);
  output.push(`Total: ${errors.length} erreur(s)`);
  output.push(`Fichier: ${filePath}`);
  output.push(`Date: ${new Date().toLocaleString("fr-FR")}`);
  output.push("═".repeat(80));
  output.push("");

  // Lire le contenu du fichier
  let lines = [];
  if (fs.existsSync(filePath)) {
    lines = fs.readFileSync(filePath, "utf8").split("\n");
  }

  // Trier par ligne
  errors.sort((a, b) => {
    const lineA = a.range?.start?.line || a.startLineNumber || 0;
    const lineB = b.range?.start?.line || b.startLineNumber || 0;
    return lineA - lineB;
  });

  errors.forEach((error, idx) => {
    const lineNum =
      (error.range?.start?.line || error.startLineNumber || 1) - 1;
    const column = error.range?.start?.character || error.startColumn || 1;
    const severity = error.severity || "error";
    const category = error.category || "Other";

    output.push("─".repeat(80));
    output.push(`ERREUR #${idx + 1}/${errors.length}`);
    output.push("─".repeat(80));
    output.push(`Ligne: ${lineNum + 1}, Colonne: ${column}`);
    output.push(`Sévérité: ${severity.toUpperCase()}`);
    output.push(`Catégorie: ${category}`);
    output.push(`Message: ${error.message}`);
    output.push("");
    output.push("Code:");

    if (lines.length > 0) {
      // Contexte avant
      for (
        let i = Math.max(0, lineNum - CONFIG.contextLines);
        i < lineNum;
        i++
      ) {
        output.push(`  ${String(i + 1).padStart(4)} │ ${lines[i] || ""}`);
      }

      // Ligne avec erreur
      output.push(
        `> ${String(lineNum + 1).padStart(4)} │ ${lines[lineNum] || ""}`,
      );
      output.push(`       ${" ".repeat(column)}^`);

      // Contexte après
      for (
        let i = lineNum + 1;
        i <= Math.min(lines.length - 1, lineNum + CONFIG.contextLines);
        i++
      ) {
        output.push(`  ${String(i + 1).padStart(4)} │ ${lines[i] || ""}`);
      }
    }

    output.push("");
  });

  output.push("═".repeat(80));
  output.push(`FIN DU RAPPORT - ${errors.length} erreur(s)`);
  output.push("═".repeat(80));

  return output.join("\n");
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 05 - copyToClipboard
// ═══════════════════════════════════════════════════════════════
function copyToClipboard(text) {
  try {
    if (process.platform === "win32") {
      const proc = require("child_process").spawn("clip");
      proc.stdin.write(text);
      proc.stdin.end();
      return true;
    } else if (process.platform === "darwin") {
      execSync("pbcopy", { input: text });
      return true;
    } else {
      try {
        execSync("xclip -selection clipboard", { input: text });
        return true;
      } catch {
        try {
          execSync("xsel --clipboard --input", { input: text });
          return true;
        } catch {
          return false;
        }
      }
    }
  } catch (err) {
    return false;
  }
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 06 - displayErrorContext
// ═══════════════════════════════════════════════════════════════
function displayErrorContext(filePath, error, lines) {
  const lineNum = (error.range?.start?.line || error.startLineNumber || 1) - 1;
  const column = error.range?.start?.character || error.startColumn || 1;

  for (let i = Math.max(0, lineNum - CONFIG.contextLines); i < lineNum; i++) {
    console.log(
      `  ${C.GRIS}${String(i + 1).padStart(4)} │ ${lines[i] || ""}${C.RESET}`,
    );
  }

  console.log(
    `  ${C.ROUGE}${String(lineNum + 1).padStart(4)} │ ${lines[lineNum] || ""}${C.RESET}`,
  );

  const pointer = " ".repeat(7 + column) + "^";
  console.log(`  ${C.ROUGE}${pointer}${C.RESET}`);

  const severity = error.severity || "error";
  const severityColor =
    severity === "error" ? C.ROUGE : severity === "warning" ? C.JAUNE : C.GRIS;

  console.log(
    `  ${severityColor} │ [${severity.toUpperCase()}] ${error.message}${C.RESET}`,
  );

  if (error.category) {
    console.log(`  ${C.GRIS} │ Catégorie : ${error.category}${C.RESET}`);
  }

  for (
    let i = lineNum + 1;
    i <= Math.min(lines.length - 1, lineNum + CONFIG.contextLines);
    i++
  ) {
    console.log(
      `  ${C.GRIS}${String(i + 1).padStart(4)} │ ${lines[i] || ""}${C.RESET}`,
    );
  }

  console.log("");
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 07 - showFileDetails
// ═══════════════════════════════════════════════════════════════
async function showFileDetails(filePath, errors) {
  if (!fs.existsSync(filePath)) {
    erreur(`Fichier introuvable : ${filePath}`);
    return;
  }

  const content = fs.readFileSync(filePath, "utf8");
  const lines = content.split("\n");
  const fileName = path.basename(filePath);

  console.log("");
  console.log(`${C.ORANGE}${"─".repeat(80)}${C.RESET}`);
  console.log(
    `${C.ORANGE}│ ${E.fichier} ${fileName} - Affichage des ${errors.length} erreurs${" ".repeat(80 - 11 - fileName.length - String(errors.length).length - 23)}│${C.RESET}`,
  );
  console.log(`${C.ORANGE}${"─".repeat(80)}${C.RESET}`);
  console.log("");

  errors.sort((a, b) => {
    const lineA = a.range?.start?.line || a.startLineNumber || 0;
    const lineB = b.range?.start?.line || b.startLineNumber || 0;
    return lineA - lineB;
  });

  for (let i = 0; i < errors.length; i++) {
    console.log(`${C.BOLD}[${i + 1}/${errors.length}]${C.RESET}`);
    displayErrorContext(filePath, errors[i], lines);

    if ((i + 1) % 5 === 0 && i < errors.length - 1) {
      await new Promise((resolve) => {
        const rl = readline.createInterface({
          input: process.stdin,
          output: process.stdout,
        });
        rl.question(
          `${E.horloge} ${C.JAUNE}Appuyez sur Entrée pour continuer (${i + 1}/${errors.length})...${C.RESET}`,
          () => {
            rl.close();
            resolve();
          },
        );
      });
    }
  }

  console.log(
    `${C.VERT}✓ Fin de l'affichage des ${errors.length} erreurs${C.RESET}\n`,
  );
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 08 - displayFileList
// ═══════════════════════════════════════════════════════════════
function displayFileList(byFile) {
  const files = Object.keys(byFile).sort(
    (a, b) => byFile[b].length - byFile[a].length,
  );

  console.log("");
  console.log(`${C.BLEU_INTENSE}${"═".repeat(80)}${C.RESET}`);
  console.log(
    `${C.BLEU_INTENSE}║ ${E.document} FICHIERS AVEC ERREURS${" ".repeat(58)}║${C.RESET}`,
  );
  console.log(`${C.BLEU_INTENSE}${"═".repeat(80)}${C.RESET}`);
  console.log("");

  files.forEach((file, index) => {
    const fileName = path.basename(file);
    const count = byFile[file].length;

    const bySeverity = { error: 0, warning: 0, info: 0 };
    byFile[file].forEach((e) => {
      const sev = e.severity || "warning";
      bySeverity[sev] = (bySeverity[sev] || 0) + 1;
    });

    console.log(
      `  ${C.BOLD}[${index + 1}]${C.RESET} ${fileName.padEnd(40)} ` +
        `${C.ROUGE}${bySeverity.error}E${C.RESET} ${C.JAUNE}${bySeverity.warning}W${C.RESET} ${C.GRIS}${bySeverity.info}I${C.RESET}`,
    );
  });

  console.log("");
  return files;
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 09 - showFileMenu
// ═══════════════════════════════════════════════════════════════
async function showFileMenu(filePath, errors) {
  const fileName = path.basename(filePath);

  console.log("");
  console.log(`${C.CYAN}${"─".repeat(80)}${C.RESET}`);
  console.log(
    `${C.CYAN}│ ${E.fichier} ${fileName} - ${errors.length} erreur(s)${" ".repeat(80 - 6 - fileName.length - String(errors.length).length - 11)}│${C.RESET}`,
  );
  console.log(`${C.CYAN}${"─".repeat(80)}${C.RESET}`);
  console.log("");
  console.log(
    `  ${C.VERT}[D]${C.RESET} Voir les détails des erreurs (affichage complet)`,
  );
  console.log(
    `  ${C.VERT}[C]${C.RESET} Copier toutes les erreurs dans le presse-papiers`,
  );
  console.log(`  ${C.JAUNE}[R]${C.RESET} Retour à la liste des fichiers`);
  console.log(`  ${C.GRIS}[Q]${C.RESET} Quitter`);
  console.log("");

  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    rl.question(
      `${E.question} ${C.JAUNE}Votre choix : ${C.RESET}`,
      (answer) => {
        rl.close();
        resolve(answer.trim().toUpperCase());
      },
    );
  });
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 10 - askForFileNumber
// ═══════════════════════════════════════════════════════════════
async function askForFileNumber(maxFiles) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    rl.question(
      `${E.question} ${C.JAUNE}Numéro du fichier (1-${maxFiles}) ou 0 pour quitter : ${C.RESET}`,
      (answer) => {
        rl.close();
        const num = parseInt(answer);
        if (isNaN(num) || num < 0 || num > maxFiles) {
          resolve(null);
        } else {
          resolve(num);
        }
      },
    );
  });
}

// ═══════════════════════════════════════════════════════════════
// FONCTION 11 - main
// ═══════════════════════════════════════════════════════════════
async function main() {
  titre("DIAGNOSTIC INTERACTIF DES ERREURS v4.3", E.scan);

  const scanData = loadLatestScan();
  if (!scanData) {
    erreur("Aucun scan trouvé");
    warn("Lancez d'abord : node scanner_erreurs.js");
    process.exit(1);
  }

  const diagnostics = scanData.diagnostics || [];
  if (diagnostics.length === 0) {
    succes("Aucune erreur détectée !");
    process.exit(0);
  }

  const filter = process.argv.includes("--error")
    ? "error"
    : process.argv.includes("--warning")
      ? "warning"
      : process.argv.includes("--info")
        ? "info"
        : null;

  if (filter) {
    info(`Filtre actif : ${filter.toUpperCase()}`);
  }

  const byFile = groupErrorsByFile(diagnostics, filter);
  const files = displayFileList(byFile);

  let continueLoop = true;

  while (continueLoop) {
    const userChoice = await askForFileNumber(files.length);

    if (userChoice === null || userChoice === 0) {
      console.log(`\n${C.GRIS}Au revoir !${C.RESET}\n`);
      break;
    }

    const fileIndex = userChoice - 1;

    if (fileIndex >= 0 && fileIndex < files.length) {
      const selectedFile = files[fileIndex];
      const fileErrors = byFile[selectedFile];

      let inFileMenu = true;
      while (inFileMenu) {
        const choice = await showFileMenu(selectedFile, fileErrors);

        switch (choice) {
          case "D":
            await showFileDetails(selectedFile, fileErrors);
            break;

          case "C":
            console.log("");
            info("Préparation du rapport...");
            const formattedErrors = formatErrorsForClipboard(
              selectedFile,
              fileErrors,
            );

            if (copyToClipboard(formattedErrors)) {
              succes(
                `✓ ${fileErrors.length} erreur(s) copiée(s) dans le presse-papiers !`,
              );
              console.log(
                `${C.GRIS}  Vous pouvez maintenant coller (Ctrl+V) dans un document${C.RESET}`,
              );
            } else {
              warn("Impossible de copier dans le presse-papiers");
              const outputFile = `erreurs_${path.basename(selectedFile, ".py")}.txt`;
              fs.writeFileSync(outputFile, formattedErrors, "utf8");
              info(`Rapport sauvegardé dans : ${outputFile}`);
            }
            console.log("");
            break;

          case "R":
            inFileMenu = false;
            displayFileList(byFile);
            break;

          case "Q":
            console.log(`\n${C.GRIS}Au revoir !${C.RESET}\n`);
            inFileMenu = false;
            continueLoop = false;
            break;

          default:
            erreur("Choix invalide ! Utilisez D, C, R ou Q");
            break;
        }
      }
    } else {
      erreur("Numéro de fichier invalide");
    }
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  loadLatestScan,
  groupErrorsByFile,
  formatErrorsForClipboard,
};
