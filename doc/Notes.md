
| nom colonne             | type de donées | description |
|--------------------------|----------|----------|
| Iramat_ID               | STRING   | Identifiant laboratoire, suggestion: IRAMAT-XXXX (sur *n*-digit), auto-incrémenation |
| Analysis_ID             | STRING   | Identifiant analyse |
| Sample_ID               | STRING   | Identifiant échantillon |
| Analysis_Type           | STRING   | MEB-EDS, Gamma Spectroscopy, Raman, etc. |
| Element/Isotope         | STRING   | Élément (pour MEB-EDS) ou isotope (pour spectroscopie gamma) analysé |
| Concentration/Activity  | FLOAT    | Valeur mesurée (par exemple, concentration élémentaire ou activité radioactive) |
| Unit                    | STRING   | Unité de mesure (par exemple, %, ppm, Bq, keV) |
| Wavelength (cm⁻¹)       | FLOAT    | Uniquement pour l'analyse Raman, la position du pic dans le décalage Raman |
| Intensity               | FLOAT    | Intensité du pic Raman ou autres caractéristiques spectrales |
| Uncertainty             | FLOAT    | Incertitude de mesure |
| Date_Analyzed           | DATE     | Date à laquelle l'analyse a été réalisée |
| Comments                | STRING   | Observations ou métadonnées supplémentaires |
| ...                | ...   | ... |