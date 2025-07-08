Aegis Web Application

Aegis is a user-friendly web application developed as part of a PhD thesis to improve access to seismic hazard and risk information in Greece. Named after the mythological "Aegis" shield of protection, the app is designed to support informed decision-making for earthquake resilience, planning, and preparedness.

✨ Overview

Aegis allows users to interactively explore site-specific seismic hazard data, generate design spectra following Eurocode 8, view basic infrastructure exposure across Greece, and estimate expected seismic damage using well established fragility models. The application consists of two main modules:
1) Seismic Hazard Module: Local site conditions, hazard maps, hazard curves, uniform hazard spectra, and EC8 design spectra.
2) Seismic Risk Module: Exposure models for critical facilities in Greece and a fragility model database covering over 1,200 structural typologies.

📅 Features

▶ Seismic Hazard Module
 - Local site conditions: includes Vs30, slope, and geology data from ESRM20 on a 10×10 km grid, accessible via interactive map clicks.
 - Hazard maps: interactive maps displaying the spatial distribution of 17 ground motion parameters for return periods ranging from 50 to 10,000 years.
 - Hazard Curves: site-specific plots showing the annual probability of exceedance of 17 ground motion parameters across six statistical measures.
 - Uniform Hazard Spectra (UHS): spectral acceleration values at different periods, computed for return periods from 50 to 10,000 years and 6 statistical measures
 - Eurocode 8 Spectra Generator: generates the elastic response spectra of the Eurocode 8 based on the seismic zone and soil type; users can manually modify the soil classification.

▶ Seismic Risk Module
 - Exposure Viewer: interactive map of critical infrastructure (e.g., schools, hospitals, industrial plants, power stations) based on national geospatial data.
 - Fragility Viewer: Viewer for fragility curves from literature covering buildings, tunnels, roads, wastewater systems, and industrial assets like liquid storage tanks (LSTs).

🚀 Quick Start

1) the repo:
git clone https://github.com/SApostolaki/aegis.git
cd aegis
2) Install dependencies: pip install -r requirements.txt
3) Run locally: flask run
Requires Python, Flask, and standard data science packages. Data is loaded from local CSV and GeoJSON files.

📖 Citation

If you use Aegis, please cite:
Apostolaki, S. (2025). Contribution to the revised Eurocode 8 and seismic risk applications for urban environment and critical facilities. PhD Thesis, Aristotle University of Thessaloniki.

⚠️ Disclaimer

The Aegis application is intended solely for informational purposes. The data, analyses, and results provided through the platform are not suitable for, nor should they be used in, the seismic design or structural safety assessment of buildings or infrastructure. Users should consult appropriate codes and standards for structural design.

🔒 License

This project is licensed under the Apache License 2.0. You are free to use, modify, and distribute it under the terms of the license.
