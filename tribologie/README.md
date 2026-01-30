# Rapport de Tribologie - Contact Hertzien Sphère-Plan

Ce projet contient le rapport au format LaTeX pour l'analyse du contact élastique entre une sphère et un plan selon la théorie de Hertz.

## Structure du projet

```
tribologie/
├── rapportECL.cls              # Classe LaTeX pour le rapport ECL
├── tribologie.tex              # Document principal LaTeX
├── tribologie_dm2.py           # Script Python d'analyse
├── generate_figures.py         # Script de génération des figures
├── compile.sh                  # Script de compilation
├── README.md                   # Ce fichier
└── figures/
    ├── ECL_logo.png            # Logo ECL
    ├── hertz_pressure_profile.png
    ├── force_displacement_curve.png
    ├── stress_evolution.png
    ├── sigma_z_depth.png
    └── shear_stress.png
```

## Compilation du rapport

### Méthode 1 : Script de compilation

```bash
chmod +x compile.sh
./compile.sh
```

### Méthode 2 : Compilation directe

```bash
pdflatex -interaction=nonstopmode -output-directory=. tribologie.tex
```

## Prérequis

- LaTeX (pdflatex)
- Python 3 avec numpy et matplotlib (pour regenerate les figures)
- ImageMagick (optionnel, pour le logo)

## Figures générées

Le script `generate_figures.py` génère automatiquement les figures suivantes :
- Profil de pression hertzien
- Courbes force-déplacement et contrainte-déformation
- Évolution des contraintes dans le cercle de contact
- Variation de σz avec la profondeur
- Distribution de la contrainte de cisaillement

## Données du problème

- Sphère en acier : d = 6 mm, E₁ = 210 GPa, ν₁ = 0.3
- Effort maximal : Fmax = 0.5 N
- Enfoncement : δ = 50 μm
- Plan métallique : ν₂ = 0.3 (supposé)

## Auteurs

- \textcolor{red}{À compléter avec les noms des étudiants}
- Encadrants : Éric Feulvarch, Françoise Fauvin
