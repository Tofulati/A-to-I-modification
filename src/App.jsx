import { useState } from 'react'
import GeneTable from './components/GeneTable';
import './App.css'

export default function App() {
  const [gene, setGene] = useState("AZIN1");
  const [submitted, setSubmitted] = useState(null);

  return (
    <div className="app">
      <main>
        <h1>A-to-I Modification Table</h1>
        <div className="input-container">
          <div>
            <label>Gene name:</label>
            <input
              value={gene}
              onChange={e => setGene(e.target.value)}
              placeholder="AZIN1"
            />
          </div>
          <button
            onClick={() => setSubmitted({ gene })}
            disabled={!gene}
          >
            Load Gene Data
          </button>
        </div>
        {submitted && (
          <GeneTable gene={submitted.gene} />
        )}
      </main>
      <footer>
        <p>
          Li Lab + Jiang Lab © 2026 &nbsp; | &nbsp;
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://github.com/Tofulati/A-to-I-modification"
          >
            GitHub Repo
          </a>
        </p>
      </footer>
    </div>
  );
}