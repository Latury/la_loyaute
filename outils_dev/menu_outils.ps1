# ═══════════════════════════════════════════════════════════════
# LA LOYAUTE - SUITE D'OUTILS DE DEVELOPPEMENT
# Version : 4.1.1 - Développé par Latury - 2026 (Corrigé PSScriptAnalyzer)
# ═══════════════════════════════════════════════════════════════

# Configuration encodage
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# ───────────── FONCTION 01 - CentreTexte ─────────────
function CentreTexte {
    param (
        [string]$Texte,
        [int]$Largeur
    )

    if ($Texte.Length -ge $Largeur) {
        return $Texte
    }

    $padding = [Math]::Floor(($Largeur - $Texte.Length) / 2)
    return (" " * $padding) + $Texte
}

# ───────────── FONCTION 02 - Show-SplashScreen ─────────────
function Show-SplashScreen {
    Clear-Host

    # Largeur terminal
    $termWidth = $Host.UI.RawUI.WindowSize.Width

    # ── LOGO ──
    $logo = @(
"╔════════════════════════════════════════════════════════════════════════════════════╗",
"║                                                                                    ║",
"║   ██╗      █████╗     ██╗      ██████╗ ██╗   ██╗ █████╗ ██╗   ██╗████████╗███████╗ ║",
"║   ██║     ██╔══██╗    ██║     ██╔═══██╗╚██╗ ██╔╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝ ║",
"║   ██║     ███████║    ██║     ██║   ██║ ╚████╔╝ ███████║██║   ██║   ██║   █████╗   ║",
"║   ██║     ██╔══██║    ██║     ██║   ██║  ╚██╔╝  ██╔══██║██║   ██║   ██║   ██╔══╝   ║",
"║   ███████╗██║  ██║    ███████╗╚██████╔╝   ██║   ██║  ██║╚██████╔╝   ██║   ███████╗ ║",
"║   ╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝ ║",
"║                                                                                    ║",
"╚════════════════════════════════════════════════════════════════════════════════════╝"
)

    foreach ($line in $logo) {
        Write-Host (CentreTexte $line $termWidth) -ForegroundColor Green
    }

    Write-Host ""

# ── CADRE INFOS RAPIDE ──
$cadreInfos = @(
    "╔══════════════════════════════════════════════════════════════════════╗",
    "║                                                                      ║",
    "║                SUITE D'OUTILS DE DEVELOPPEMENT v4.0.0                ║",
    "║               Développé par Latury - 2026 | LA LOYAUTÉ               ║",
    "║                                                                      ║",
    "╚══════════════════════════════════════════════════════════════════════╝"
)

# Centre le cadre dans le terminal
$termWidth = $Host.UI.RawUI.WindowSize.Width
foreach ($line in $cadreInfos) {
    Write-Host (CentreTexte $line $termWidth) -ForegroundColor DarkGreen
}

Write-Host ""

    # ── CHARGEMENT (machine à écrire, sans lignes vides) ──
    $loadingText = @(
        "INITIALISATION DES SYSTEMES 14%",
        "CHARGEMENT DES MODULES 29%",
        "VERIFICATION DE L'INTEGRITE 43%",
        "CONNEXION AUX BASES DE DONNEES 57%",
        "PREPARATION DE L'INTERFACE 71%",
        "ACTIVATION DES OUTILS 86%",
        "SYSTEME PRET 100%"
    )

    foreach ($line in $loadingText) {
        Write-Host ""
        $centered = CentreTexte $line $termWidth
        foreach ($char in $centered.ToCharArray()) {
            Write-Host -NoNewline $char -ForegroundColor Green
            Start-Sleep -Milliseconds 20
        }
    }

    Write-Host ""
    Write-Host ""
    Write-Host (CentreTexte "✓ CHARGEMENT TERMINE" $termWidth) -ForegroundColor Green
    Write-Host ""
    Write-Host (CentreTexte ">>> Appuyez sur ENTRÉE pour continuer <<<" $termWidth) -ForegroundColor Blue

    Read-Host
}

# ───────────── FONCTION 03 - Afficher-Menu ─────────────
function Show-Menu {
    Clear-Host

    $termWidth = $Host.UI.RawUI.WindowSize.Width

    # ─────────── CADRE PRINCIPAL ───────────
    $cadre = @(
        "┌────────────────────────────────────────────────────────────────┐",
        "│                                                                │",
        "│                LA LOYAUTE - SUITE D'OUTILS v4.0                │",
        "│                Scanner → Diagnostic → Correction               │",
        "│                                                                │",
        "└────────────────────────────────────────────────────────────────┘"
    )

    foreach ($line in $cadre) {
        $padding = ([math]::Floor(($termWidth - $line.Length)/2))
        Write-Host (" " * $padding) + $line -ForegroundColor Blue
    }

    Write-Host ""

    # ─────────── OUTILS DISPONIBLES ───────────
    $outils = @(
        "[1] Scanner les erreurs Pylance",
        "[2] Diagnostiquer les erreurs",
        "[3] Migrer vers emojis centralises",
        "[4] Nettoyer les caches Python",
        "[5] Voir les scans enregistres",
        "[6] Supprimer tous les scans",
        "[0] Quitter"
    )

    $titre = "OUTILS DISPONIBLES :"
    $paddingTitre = ([math]::Floor(($termWidth - $titre.Length)/2))
    Write-Host (" " * $paddingTitre) + $titre -ForegroundColor White
    Write-Host ""

    foreach ($outil in $outils) {
        $padding = ([math]::Floor(($termWidth - $outil.Length)/2))
        $color = "White"
        if ($outil -like "[1]*") { $color = "Green" }
        elseif ($outil -like "[2]*") { $color = "Green" }
        elseif ($outil -like "[3]*") { $color = "Cyan" }
        elseif ($outil -like "[4]*") { $color = "Yellow" }
        elseif ($outil -like "[5]*") { $color = "Yellow" }
        elseif ($outil -like "[6]*") { $color = "Yellow" }
        elseif ($outil -like "[0]*") { $color = "Red" }

        Write-Host (" " * $padding) + $outil -ForegroundColor $color
    }

    Write-Host ""
    $invite = "Votre choix: "
    $paddingInvite = ([math]::Floor(($termWidth - $invite.Length)/2))
    Write-Host (" " * $paddingInvite) -NoNewline
    Write-Host $invite -ForegroundColor Yellow -NoNewline
}

# ───────────── FONCTION 04 - Executer-Commande ─────────────
function Invoke-Command {
    param (
        [string]$Script,
        [string]$Description
    )

    Clear-Host
    Write-Host ""
    Write-Host "Lancement de $Description..." -ForegroundColor Yellow
    Write-Host ""

    $scriptPath = Join-Path $PSScriptRoot $Script

    if (Test-Path $scriptPath) {
        node $scriptPath
    } else {
        Write-Host "Erreur : Le script $Script est introuvable !" -ForegroundColor Red
    }

    Write-Host ""
    Write-Host "Appuyez sur Entrée pour continuer..." -ForegroundColor Gray -NoNewline
    $null = Read-Host
}

# ───────────── FONCTION 05 - Show-Scans ─────────────
function Show-Scans {
    Clear-Host
    Write-Host ""

    $termWidth = $Host.UI.RawUI.WindowSize.Width
    $titre = "SCANS ENREGISTRES"
    $paddingTitre = [math]::Floor(($termWidth - $titre.Length)/2)

    Write-Host (" " * $paddingTitre + "═══════════════════════════════════════════════") -ForegroundColor Blue
    Write-Host (" " * $paddingTitre + $titre) -ForegroundColor White
    Write-Host (" " * $paddingTitre + "═══════════════════════════════════════════════") -ForegroundColor Blue
    Write-Host ""

    $erreursDir = Join-Path $PSScriptRoot "erreurs_pylance"

    if (Test-Path $erreursDir) {
        $scans = Get-ChildItem -Path $erreursDir -Filter "*.json" | Sort-Object LastWriteTime -Descending

        if ($scans.Count -eq 0) {
            Write-Host (" " * $paddingTitre + "Aucun scan trouvé.") -ForegroundColor Yellow
        } else {
            Write-Host (" " * $paddingTitre + "Total : $($scans.Count) fichier(s)") -ForegroundColor Green
            Write-Host ""

            foreach ($scan in $scans) {
                $taille = [math]::Round($scan.Length / 1KB, 2)
                Write-Host (" " * $paddingTitre + "• $($scan.Name) ($taille KB)") -ForegroundColor White
                Write-Host (" " * $paddingTitre + "  Créé le : $($scan.LastWriteTime.ToString('dd/MM/yyyy HH:mm:ss'))") -ForegroundColor DarkGray
            }
        }
    } else {
        Write-Host (" " * $paddingTitre + "Le dossier erreurs_pylance n'existe pas.") -ForegroundColor Red
    }

    Write-Host ""
    Write-Host (" " * $paddingTitre + "Appuyez sur Entrée pour continuer...") -ForegroundColor Gray -NoNewline
    $null = Read-Host
}

# ───────────── FONCTION 06 - Remove-Scans ─────────────
function Remove-Scans {
    Clear-Host
    Write-Host ""

    $termWidth = $Host.UI.RawUI.WindowSize.Width
    $titre = "SUPPRESSION DES SCANS"
    $paddingTitre = [math]::Floor(($termWidth - $titre.Length)/2)

    Write-Host (" " * $paddingTitre + "═══════════════════════════════════════════════") -ForegroundColor Red
    Write-Host (" " * $paddingTitre + $titre) -ForegroundColor White
    Write-Host (" " * $paddingTitre + "═══════════════════════════════════════════════") -ForegroundColor Red
    Write-Host ""

    $erreursDir = Join-Path $PSScriptRoot "erreurs_pylance"

    if (Test-Path $erreursDir) {
        $listeScans = Get-ChildItem -Path $erreursDir -Filter "*.json"

        if ($listeScans.Count -eq 0) {
            Write-Host (" " * $paddingTitre + "Aucun scan à supprimer.") -ForegroundColor Yellow
        } else {
            Write-Host (" " * $paddingTitre + "$($listeScans.Count) fichier(s) à supprimer") -ForegroundColor Yellow
            Write-Host ""
            Write-Host (" " * $paddingTitre + "Êtes-vous sûr ? (O/N) : ") -ForegroundColor Red -NoNewline
            $confirmation = Read-Host

            if ($confirmation -eq "O" -or $confirmation -eq "o") {
                $supprime = 0
                foreach ($fichierScan in $listeScans) {
                    Remove-Item $fichierScan.FullName -Force
                    $supprime++
                }
                Write-Host ""
                Write-Host (" " * $paddingTitre + "✓ $supprime fichier(s) supprimé(s)") -ForegroundColor Green
            } else {
                Write-Host ""
                Write-Host (" " * $paddingTitre + "Opération annulée.") -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host (" " * $paddingTitre + "Le dossier erreurs_pylance n'existe pas.") -ForegroundColor Red
    }

    Write-Host ""
    Write-Host (" " * $paddingTitre + "Appuyez sur Entrée pour continuer...") -ForegroundColor Gray -NoNewline
    $null = Read-Host
}

# ═══════════════════════════════════════════════════════════════
# PROGRAMME PRINCIPAL
# ═══════════════════════════════════════════════════════════════

# Affiche le splash screen
Show-SplashScreen

# Boucle principale du menu
$continuer = $true

while ($continuer) {
    Show-Menu
    $choix = Read-Host

    switch ($choix) {
        "1" {
            Invoke-Command "scanner_erreurs.js" "le scanner"
        }
        "2" {
            Invoke-Command "diagnostiquer_erreurs.js" "le diagnostic"
        }
        "3" {
            Invoke-Command "migrer_emojis.js" "la migration des emojis"
        }
        "4" {
            Invoke-Command "vider_cache.js" "le nettoyeur de cache"
        }
        "5" {
            Show-Scans
        }
        "6" {
            Remove-Scans
        }
        "0" {
            Clear-Host
            Write-Host ""

            $termWidth = $Host.UI.RawUI.WindowSize.Width
            $adieu = @(
                "╔════════════════════════════════════════════════════════════════╗",
                "║                                                                ║",
                "║                Merci d'avoir utilisé LA LOYAUTÉ                ║",
                "║                  Développé par Latury - 2026.                  ║",
                "║                                                                ║",
                "╚════════════════════════════════════════════════════════════════╝"
            )

            foreach ($line in $adieu) {
                Write-Host (CentreTexte $line $termWidth) -ForegroundColor Green
            }

            Write-Host ""
            $continuer = $false
        }
        default {
            Write-Host ""
            Write-Host "Choix invalide ! Veuillez entrer un numéro entre 0 et 6." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
}