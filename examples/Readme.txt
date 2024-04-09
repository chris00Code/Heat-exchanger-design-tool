To export pdf with images:
cd to directory
jupyter nbconvert --to latex TOCONVERT.ipynb


    \usepackage{caption}
    %\DeclareCaptionFormat{nocaption}{}
    %\captionsetup{format=nocaption,aboveskip=0pt,belowskip=0pt}
    \usepackage[autostyle=true,german=quotes]{csquotes}
    \usepackage[main=ngerman,english]{babel}
    \usepackage[%
    	backend=biber,
    	style=numeric-comp, % authoryear
    	bibstyle=numeric, % authoryear
    	citestyle=numeric, % authoryear
    	% maxcitenames=2,
    	sorting=none, %nty
    	backref=true,
    	backrefstyle=none
    ]{biblatex}
    \addbibresource{literature.bib}
    
\begin{document}
    \title{
        Standard Wärmeübertrager \\ 
        \large standard\_heatexchangers.ipynb
    }
    \date{März 2024}
    
\begin{figure}[H]
    \includegraphics{images/simpleHeatexchanger.PNG}
    \caption{Prinzipskizzen des Wärmübertragers 
    \newline (oben) Längsschnitt: nur Rohrmittellinien dargestellt 
    \newline (unten) Querschnitt: Rohrdurchströmung im Gegen-/Gleichstrom durch helle und dunkle Rohrquerschnitte angedeutet
    \newline (entnommen aus Michael Krieger, Skriptum zur kombinierten LV Technische Thermofluiddynamik. 2023, Seite 164)}
\end{figure}

convert latex

To change pdf title:
Open raw text of .ipynb
Change Metadata (last lines)