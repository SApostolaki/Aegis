import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)
app.config["DEBUG"] = True

# === ROUTES ===
@app.route("/")
def home():
    return render_template("v1.0_home.html")

@app.route("/v1.0_seismic_hazard")
def seismic_hazard():
    return render_template("v1.0_seismic_hazard.html")

@app.route("/v1.0_seismic_hazard/v1.0_sites")
def local_site_conditions():
    return render_template("v1.0_sites.html")

@app.route("/v1.0_seismic_hazard/v1.0_hmaps")
def hazard_maps():
    return render_template("v1.0_hmaps.html")

@app.route("/v1.0_seismic_hazard/v1.0_hcurves")
def hazard_curves():
    return render_template("v1.0_hcurves.html")

@app.route("/v1.0_seismic_hazard/v1.0_uhs")
def hazard_uhs():
    return render_template("v1.0_uhs.html")

@app.route("/v1.0_elspec")
def elastic_response_spectra():
    return render_template("v1.0_elspec.html")

@app.route("/v1.0_seismic_risk")
def seismic_risk():
    return render_template("v1.0_seismic_risk.html")

@app.route("/v1.0_seismic_risk/v1.0_fragility")
def fragility():
    return render_template("v1.0_fragility.html")

@app.route("/asset-model-typology-data")
def asset_model_typology_data():
    try:
        asset_file = os.path.join(app.root_path, "static", "asset_category.csv")
        model_file = os.path.join(app.root_path, "static", "fragility_model.csv")
        typology_file = os.path.join(app.root_path, "static", "fragility_typology.csv")

        assets = pd.read_csv(asset_file, encoding="utf-8")
        models = pd.read_csv(model_file, encoding="ISO-8859-1")
        typologies = pd.read_csv(typology_file, encoding="ISO-8859-1")

        assets = assets.where(pd.notnull(assets), None)
        models = models.where(pd.notnull(models), None)
        typologies = typologies.where(pd.notnull(typologies), None)

        asset_data = [{"id": int(row["id"]), "asset_name": row["name"]} for _, row in assets.iterrows()]
        model_data = [{"id": int(row["id"]), "model_name": row["name"], "asset_id": int(row["asset_id"]), "reference": row.get("Reference", "")} for _, row in models.iterrows()]
        typology_data = [{"id": int(row["id"]), "name": row["name"], "model_id": int(row["model_id"]), "imt": row["imt"]} for _, row in typologies.iterrows()]


        return jsonify({
            "assets": asset_data,
            "models": model_data,
            "typologies": typology_data
        })
    except Exception as e:
        print("DATA LOAD ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/get-fragility-curves")
def get_fragility_curves():
    typology_id = request.args.get("typology_id", type=int)
    curves_path = os.path.join(app.root_path, "static", "fragility_curves.csv")
    typology_path = os.path.join(app.root_path, "static", "fragility_typology.csv")

    try:
        curves_df = pd.read_csv(curves_path, encoding="ISO-8859-1")
        typo_df = pd.read_csv(typology_path, encoding="ISO-8859-1")

        curves_df = curves_df[curves_df["typology_id"] == typology_id]
        typology_row = typo_df[typo_df["id"] == typology_id]

        if curves_df.empty or typology_row.empty:
            return jsonify({"error": "No data found for the selected typology."}), 404

        ds_count = int(typology_row.iloc[0]["ds"])
        imt = curves_df["imt"].tolist()
        ds_curves = {
            f"ds{i}": curves_df[f"ds{i}"].where(pd.notnull(curves_df[f"ds{i}"]), None).tolist()
            for i in range(1, ds_count + 1)
        }

        return jsonify({"imt": imt, "ds_curves": ds_curves, "ds_count": ds_count})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/v1.0_seismic_risk/v1.0_exposure")
def exposure():
    return render_template("v1.0_exposure.html")

@app.route("/geofiles/<path:filename>")
def geofiles(filename):
    geofiles_dir = os.path.join(os.getcwd(), "geofiles")
    return send_from_directory(geofiles_dir, filename)

@app.route("/images/<path:filename>")
def images(filename):
    images_dir = os.path.join(os.getcwd(), "images")
    return send_from_directory(images_dir, filename)

@app.route("/css/<path:filename>")
def css(filename):
    css_dir = os.path.join(os.getcwd(), "css")
    return send_from_directory(css_dir, filename)

@app.route("/get_spectrum", methods=["POST"])
def get_spectrum():
    data = request.get_json()
    lon = float(data.get("lon"))
    lat = float(data.get("lat"))
    soil_class = data.get("soil_class")

    file_path = os.path.join(app.root_path, "static", "elspec.csv")
    df = pd.read_csv(file_path)

    df["distance"] = np.sqrt((df["lon"] - lon)**2 + (df["lat"] - lat)**2)
    closest = df.loc[df["distance"].idxmin()]

    soil_params = {
        "A": {"S": 1.00, "TB": 0.15, "TC": 0.40, "TD": 2.00},
        "B": {"S": 1.20, "TB": 0.15, "TC": 0.50, "TD": 2.00},
        "C": {"S": 1.15, "TB": 0.20, "TC": 0.60, "TD": 2.00},
        "D": {"S": 1.35, "TB": 0.20, "TC": 0.80, "TD": 2.00},
        "E": {"S": 1.40, "TB": 0.15, "TC": 0.50, "TD": 2.00},
    }

    PGA = float(closest["PGA_EC8"])
    S = soil_params[soil_class]["S"]
    TB = soil_params[soil_class]["TB"]
    TC = soil_params[soil_class]["TC"]
    TD = soil_params[soil_class]["TD"]
    agS = PGA * S

    T = [round(i * 0.05, 2) for i in range(41)]
    Se = []
    for t in T:
        if t == 0:
            Se.append(agS)
        elif t <= TB:
            Se.append(agS * (1 + t / TB * 1.5))
        elif t <= TC:
            Se.append(agS * 2.5)
        elif t <= TD:
            Se.append(agS * 2.5 * TC / t)
        else:
            Se.append(agS * 2.5 * TC * TD / (t * t))

    return jsonify({
        "zone": int(closest["Zone_EC8"]),
        "pga": round(PGA, 3),
        "default_soil": closest["Soil_EC8"],
        "T": T,
        "Se": Se
    })

if __name__ == "__main__":
    app.run(debug=True)
