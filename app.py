import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-key"

UPLOAD_FOLDER = "uploads"
SUMMARY_FOLDER = "summaries"
ALLOWED_EXTENSIONS = {"csv"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath)
            shape = df.shape
            dtypes = df.dtypes.astype(str).to_frame("dtype").reset_index().rename(columns={"index": "column"})
            head_html = df.head(10).to_html(classes="table table-striped", index=False, border=0)
            info_html = dtypes.to_html(classes="table table-sm", index=False, border=0)

            numeric_df = df.select_dtypes(include=["number"])
            desc_html, summary_filename = None, None

            if not numeric_df.empty:
                desc = numeric_df.describe().transpose().round(3)
                desc_html = desc.to_html(classes="table table-sm", border=0)

                # Save summary CSV
                summary_filename = f"summary_{filename}"
                summary_path = os.path.join(SUMMARY_FOLDER, summary_filename)
                desc.to_csv(summary_path)

            missing = df.isnull().sum().reset_index()
            missing.columns = ["column", "missing_count"]
            missing["missing_pct"] = (missing["missing_count"] / len(df) * 100).round(2)
            missing_html = missing.to_html(classes="table table-sm", index=False, border=0)

            cat_html = None
            cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
            if cat_cols:
                cat_summary = {}
                for c in cat_cols:
                    cat_summary[c] = df[c].value_counts(dropna=False).head(5).to_dict()
                cat_html = pd.DataFrame({
                    "column": list(cat_summary.keys()),
                    "top_values": [", ".join(f"{k} ({v})" for k, v in vals.items()) for vals in cat_summary.values()]
                }).to_html(classes="table table-sm", index=False, border=0)

            # Charts (optional)
            show_charts = request.form.get("show_charts") == "on"
            chart_divs = []
            if show_charts and not numeric_df.empty:
                for col in numeric_df.columns:
                    fig = px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}")
                    chart_divs.append(pio.to_html(fig, full_html=False, include_plotlyjs='cdn'))
                    fig2 = px.box(df, y=col, title=f"Boxplot of {col}")
                    chart_divs.append(pio.to_html(fig2, full_html=False, include_plotlyjs=False))

                if numeric_df.shape[1] > 1:
                    corr = numeric_df.corr()
                    fig3 = px.imshow(corr, text_auto=True, title="Correlation Matrix")
                    chart_divs.append(pio.to_html(fig3, full_html=False, include_plotlyjs=False))

            os.remove(filepath)
            return render_template(
                "results.html",
                table_head=head_html,
                info_html=info_html,
                desc_html=desc_html,
                missing_html=missing_html,
                cat_html=cat_html,
                charts=chart_divs,
                shape=shape,
                summary_filename=summary_filename
            )

        except Exception as e:
            flash(f"Error processing file: {e}")
            try:
                os.remove(filepath)
            except Exception:
                pass
            return redirect(url_for("index"))

    flash("Invalid file type — please upload a CSV.")
    return redirect(url_for("index"))


@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(SUMMARY_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    flash("File not found.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
