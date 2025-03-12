import { useState } from "react";
import axios from "axios";

function App() {
  const [fx, setFx] = useState("16/x + 2*x**2");
  const [a, setA] = useState();
  const [b, setB] = useState();
  const [tol, setTol] = useState();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      // Sends a POST request to backend endpoint
      const res = await axios.post("http://127.0.0.1:8000/minimize", {
        fx,
        a: parseFloat(a),
        b: parseFloat(b),
        tol: parseFloat(tol),
      });

      setResult(res.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(
        "An error occurred while processing. Please check your inputs and try again."
      );
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-green-600 flex flex-col items-center p-6">
      {/* Header */}
      <h1 className="text-4xl font-bold text-white bg-green-900 px-6 py-4 rounded-lg shadow-lg">
        Secant Minimization
      </h1>

      {/* Form */}
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 mt-6 rounded-lg shadow-lg flex flex-col gap-4 w-full max-w-lg"
      >
        <label className="text-lg font-semibold">Function (f(x)):</label>
        <input
          className="border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          value={fx}
          onChange={(e) => setFx(e.target.value)}
          placeholder="Enter function"
        />

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-lg font-semibold">Lower Bound (a):</label>
            <input
              type="number"
              className="border p-2 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-green-500"
              value={a}
              onChange={(e) => setA(e.target.value)}
              placeholder="Enter lower bound"
            />
          </div>
          <div>
            <label className="text-lg font-semibold">Upper Bound (b):</label>
            <input
              type="number"
              className="border p-2 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-green-500"
              value={b}
              onChange={(e) => setB(e.target.value)}
              placeholder="Enter upper bound"
            />
          </div>
        </div>

        <label className="text-lg font-semibold">Tolerance (ε):</label>
        <input
          type="number"
          className="border p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          value={tol}
          onChange={(e) => setTol(e.target.value)}
          placeholder="Enter termination tolerance"
        />

        <button
          type="submit"
          className="bg-green-700 text-white p-3 rounded-md hover:bg-green-600 transition shadow-md"
        >
          {loading ? "Processing..." : "Minimize"}
        </button>
      </form>

      {/* Error Display */}
      {error && (
        <div className="mt-6 w-full max-w-2xl bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded">
          <p>{error}</p>
        </div>
      )}

      {/* Result Summary */}
      {result && (
        <div className="mt-6 w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-semibold text-green-800 text-center">
            Minimization Result
          </h2>
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <p className="text-lg font-medium text-green-800">Minimum x:</p>
              <p className="text-2xl font-bold">{result.x_min.toFixed(6)}</p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <p className="text-lg font-medium text-green-800">
                Minimum f(x):
              </p>
              <p className="text-2xl font-bold">{result.f_min.toFixed(6)}</p>
            </div>
          </div>
        </div>
      )}

      {/* Iterations Display */}
      {result && result.iterations && result.iterations.length > 0 && (
        <div className="mt-6 w-full max-w-2xl">
          <h2 className="text-2xl font-semibold text-white text-center">
            Iterations
          </h2>
          <div className="bg-white p-4 rounded-lg shadow-md mt-4 overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="bg-green-100 text-green-800">
                  <th className="px-4 py-2 text-left">Iteration</th>
                  <th className="px-4 py-2 text-left">L</th>
                  <th className="px-4 py-2 text-left">R</th>
                  <th className="px-4 py-2 text-left">z</th>
                  <th className="px-4 py-2 text-left">f'(L)</th>
                  <th className="px-4 py-2 text-left">f'(R)</th>
                  <th className="px-4 py-2 text-left">f'(z)</th>
                </tr>
              </thead>
              <tbody>
                {result.iterations.map((iter, index) => (
                  <tr
                    key={index}
                    className={index % 2 === 0 ? "bg-gray-50" : ""}
                  >
                    <td className="px-4 py-2">{iter.iteration}</td>
                    <td className="px-4 py-2">{iter.L.toFixed(6)}</td>
                    <td className="px-4 py-2">{iter.R.toFixed(6)}</td>
                    <td className="px-4 py-2">{iter.z.toFixed(6)}</td>
                    <td className="px-4 py-2">{iter["f'(L)"].toFixed(6)}</td>
                    <td className="px-4 py-2">{iter["f'(R)"].toFixed(6)}</td>
                    <td className="px-4 py-2">{iter["f'(z)"].toFixed(6)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Graph Display */}
      {result && result.graphs && result.graphs.length > 0 && (
        <div className="mt-6 w-full max-w-3xl">
          <h2 className="text-2xl font-semibold text-white text-center">
            Iteration Graphs
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
            {result.graphs.map((img, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md p-2">
                <img
                  src={img}
                  alt={`Iteration ${index + 1}`}
                  className="w-full rounded-md"
                />
                <p className="text-center text-sm font-medium text-gray-700 mt-1">
                  Iteration {index + 1}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Final Graph Display */}
      {result && result.final_graph && (
        <div className="mt-6 w-full max-w-3xl">
          <h2 className="text-2xl font-semibold text-white text-center">
            Final Result
          </h2>
          <div className="bg-white rounded-lg shadow-md p-4 mt-4">
            <img
              src={result.final_graph}
              alt="Final optimization result"
              className="w-full rounded-md"
            />
            <p className="text-center font-medium text-gray-700 mt-2">
              Function and Derivative at Minimum
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
