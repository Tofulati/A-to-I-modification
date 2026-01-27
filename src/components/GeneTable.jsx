import { useState, useEffect } from "react";
import "../App.css"; 

export default function GeneTable({ gene, sample }) {
  const [rows, setRows] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setRows(null);
    setError(null);

    fetch(`/api/gene_table?gene_name=${gene}&sample=${sample}`)
      .then((res) => {
        if (!res.ok) throw new Error("Gene not found");
        return res.json();
      })
      .then(setRows)
      .catch((err) => setError(err.message));
  }, [gene, sample]);

  if (error) return <p className="error">{error}</p>;
  if (!rows) return <p className="loading">Loading...</p>;

  const cols = Object.keys(rows[0]);

  return (
    <div className="gene-table-container">
      <h2 className="table-title">
        {gene} - {sample}
      </h2>

      <div className="table-wrapper">
        <table className="gene-table">
          <thead>
            <tr>
              {cols.map((c) => (
                <th key={c}>{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                {cols.map((c) => (
                  <td key={c}>{String(r[c])}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
