#!/bin/bash
# Script de compilation du rapport de Tribologie

echo "Compilation du rapport LaTeX..."

# Vérification des prérequis
if ! command -v pdflatex &> /dev/null; then
    echo "Erreur: pdflatex n'est pas installé."
    exit 1
fi

# Compilation
echo "Compilation de tribologie.tex..."
pdflatex -interaction=nonstopmode -output-directory=. tribologie.tex

if [ $? -eq 0 ]; then
    echo "Compilation réussie!"
    echo "Le fichier PDF est disponible: tribologie.pdf"
else
    echo "Erreur lors de la compilation."
    exit 1
fi
