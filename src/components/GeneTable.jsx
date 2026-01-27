import { useState, useEffect } from "react";
import "../App.css"; 

export default function GeneTable({ gene }) {
  const [rows, setRows] = useState(null);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    setRows(null);
    setError(null);
    
    fetch(`/api/gene_table?gene_name=${gene}`)
      .then((res) => {
        if (!res.ok) throw new Error("Gene not found");
        return res.json();
      })
      .then((data) => {
        setRows(data);
      })
      .catch((err) => setError(err.message));
  }, [gene]);
  
  if (error) return <p className="error">{error}</p>;
  if (!rows || rows.length === 0) return <p className="loading">Loading...</p>;
  
  // Define column order and display names
  const columnConfig = [
    { key: "Feature", label: "Feature" },
    { key: "Modification", label: "Modification" },
    { key: "MR01_1", label: "MR01-1 (Raw)" },
    { key: "MR01_1_mean", label: "MR01-1 (Mean %)" },
    { key: "MR01_2", label: "MR01-2 (Raw)" },
    { key: "MR01_2_mean", label: "MR01-2 (Mean %)" }
  ];
  
  // Helper function to format values
  const formatValue = (value) => {
    if (value === null || value === undefined) return "N/A";
    if (typeof value === "number") return value.toFixed(2);
    return String(value);
  };
  
  return (
    <div className="gene-table-container">
      <h2 className="table-title">
        {gene} - Modification Summary
      </h2>
      <div className="table-wrapper">
        <table className="gene-table">
          <thead>
            <tr>
              {columnConfig.map((col) => (
                <th key={col.key}>{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                {columnConfig.map((col) => (
                  <td key={col.key}>{formatValue(r[col.key])}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}