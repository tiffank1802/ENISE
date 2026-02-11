\LoadClass[a4paper,12pt]{article} % Classe du document

% ==================== CONFIGURATION DE BASE ====================
\usepackage[utf8]{inputenc}  
\usepackage[T1]{fontenc}     
\usepackage[french]{babel}   
\usepackage{lmodern}         
\usepackage{geometry}        
\usepackage{hyperref}
\usepackage[french]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{mathtools}
\usepackage{siunitx}
\usepackage{float}
\usepackage[justification=centering]{caption}
\usepackage{subcaption}
\usepackage{wallpaper}
\usepackage{nomencl}
\usepackage{url}
\usepackage[hidelinks]{hyperref}

% ==================== PAQUETS MATHÉMATIQUES ====================
\usepackage{amsmath, amssymb} 
\usepackage{mathtools}
\usepackage{siunitx}

% ==================== PAQUETS GRAPHIQUES ====================
\usepackage{graphicx}        
\usepackage{xcolor}          
\usepackage[most]{tcolorbox}
\usepackage{background}
\usepackage{wallpaper}

% ==================== PAQUETS MISE EN PAGE ====================
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{listings}

% ==================== CONFIGURATION GÉOMÉTRIE ====================
\geometry{
    top=2cm,
    bottom=2cm,
    left=2cm,
    right=2cm
}

% ==================== CONFIGURATION COULEURS ====================
\definecolor{cyan}{RGB}{0, 255, 255}
\definecolor{jade}{RGB}{0, 168, 107}
\definecolor{magenta}{RGB}{255, 0, 255}
\definecolor{midnightblue}{RGB}{25, 25, 112}

% ==================== CONFIGURATION HYPERREF ====================
\hypersetup{
    colorlinks=true, 
    urlcolor=green, 
    linkcolor=blue, 
    citecolor=red
}

% ==================== CONFIGURATION INTERLIGNE ====================
\renewcommand{\baselinestretch}{1.5}
\renewcommand{\labelitemi}{\textbullet}

% ==================== CONFIGURATION EN-TÊTE/PIED DE PAGE ====================
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}
\backgroundsetup{contents={}}

% ==================== CONFIGURATION TITRES ====================
\titleformat{\section}{\color{midnightblue}\normalfont\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\color{midnightblue}\normalfont\large\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\color{midnightblue}\normalfont\large\bfseries}{\thesubsubsection}{1em}{}

% ==================== CONFIGURATION LISTINGS (CODE) ====================
\lstset{
    language=Matlab,
    basicstyle=\ttfamily\small,
    keywordstyle=\color{blue},
    commentstyle=\color{gray},
    stringstyle=\color{red},
    numbers=left,
    numberstyle=\tiny,
    stepnumber=1,
    numbersep=5pt,
    frame=single,
    breaklines=true,
    backgroundcolor=\color{white}
}

% ==================== COMMANDES PERSONNALISÉES ====================

% Commandes pour les informations du rapport
\newcommand{\UE}[1]{\renewcommand{\UE}{#1}}
\newcommand{\sujet}[1]{\renewcommand{\sujet}{#1}}
\newcommand{\titre}[1]{\renewcommand{\titre}{#1}}
\newcommand{\enseignant}[1]{\renewcommand{\enseignant}{#1}}
\newcommand{\eleves}[1]{\renewcommand{\eleves}{#1}}
\newcommand{\UEU}[1]{\renewcommand{\UEU}{#1}}

% Configuration des marges et en-têtes
\newcommand{\fairemarges}{
    \makenomenclature
    \pagestyle{fancy}
    \fancyheadoffset{1cm}
    \setlength{\headheight}{2cm}
    \lhead{\includegraphics[scale=0.3]{logos/logo_ECL.jpg}}
    \rhead{\nouppercase{\leftmark}}
    \rfoot{\thepage}
    \cfoot{Rapport - \textbf{\titre}}
    % \lfoot{\UEU}
}

% Page de garde
\newcommand{\fairepagedegarde}{
    \begin{titlepage}
        \newcommand{\insertimage}[2]{
            \begin{center}
                \includegraphics[width=#1]{#2}
            \end{center}
        }
        
        \ThisLRCornerWallPaper{0.6}{logos/SteinECL.jpg}
        \centering
        \includegraphics[width=0.5\textwidth]{logos/logo.png}\par\vspace{0.6cm}
        {\scshape\LARGE École Centrale Lyon ENISE \par}
        \vspace{0.7cm}
        {\scshape\Large \UE \\ \sujet \\ Rapport\par}
        \vspace{0.7cm}
        \rule{\linewidth}{0.2 mm} \\[0.4 cm]
        {\huge\bfseries \titre \par}
        \rule{\linewidth}{0.2 mm} \\[1.5 cm]
        \vspace{1cm}
        
        \begin{minipage}{0.5\textwidth}
            \begin{flushleft} \large
                \emph{\textbf{Élèves :}}\\
                \eleves\\
            \end{flushleft}
        \end{minipage}
        ~
        \begin{minipage}{0.4\textwidth}
            \begin{flushright} \large
                \emph{\textbf{Enseignant :}} \\
                \enseignant \\
            \end{flushright}
        \end{minipage}\\[2cm]
        
        \vfill
        {\large \today\par}
    \end{titlepage}
}

% Table des matières
\newcommand{\tabledematieres}{
    \tableofcontents
    \newpage
}

% Commande pour insérer des figures
\newcommand{\insererfigure}[4]{
    \begin{figure}[ht]
        \centering
        \includegraphics[height=#2]{#1}
        \caption{#3}
        \label{fig: #4}
    \end{figure}
}