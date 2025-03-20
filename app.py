from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    try:
        data = request.get_json()
        coluna = data.get("coluna")
        matriz_vals = data.get("matriz")  

       
        matriz_np = np.array(matriz_vals, dtype=float)

        
        n = coluna
        matriz_triangular = matriz_np.copy().astype(float)
        for k in range(n-1):
            for i in range(k+1, n):
                m = matriz_triangular[i, k] / matriz_triangular[k, k]
                matriz_triangular[i, k] = 0
                for j in range(k+1, n):
                    matriz_triangular[i, j] -= m * matriz_triangular[k, j]

        diagonal = np.diagonal(matriz_triangular)

        determinante = np.prod(diagonal)

        if determinante != 0:
            matriz_inversa = np.around(np.linalg.inv(matriz_np), 2).tolist()
        else:
            matriz_inversa = "A matriz não é invertível pois seu determinante é 0."

        resultado = {
            "matriz_original": matriz_np.tolist(),
            "triangularizada": matriz_triangular.tolist(),
            "diagonal": diagonal.tolist(),
            "determinante": determinante,
            "inversa": matriz_inversa
        }
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
