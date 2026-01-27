import { useState } from 'react'
import GeneTable from './components/GeneTable';
import './App.css'

export default function App() {
  const [gene, setGene] = useState("AZIN1");
  const [sample, setSample] = useState("MR01-1");
  const [submitted, setSubmitted] = useState(null);

  return (
    <>
      <main>
        <h1>A-to-I Modification Table</h1>

        <div>
          <label>Gene name:</label>
          <input
            value={gene}
            onChange={e => setGene(e.target.value)}
            placeholder='AZIN1'
          />
        </div>

        <div>
          <label>Sample name:</label>
          <select
            value={sample}
            onChange={e => setSample(e.target.value)}
          >
            <option value="MR01-1">MR01-1</option>
            <option value="MR01-2">MR01-2</option>
          </select>
        </div>

        <button
          onClick={() => setSubmitted({gene, sample})}
          disabled={!gene}
        >
          Load
        </button>

        {submitted && (
          <GeneTable
            gene={submitted.gene}
            sample={submitted.sample}
          />
        )}
      </main>
    <footer>
      <p>Li Lab + Jiang Lab &copy; 2026 &nbsp; | &nbsp; <a target="_blank" href="https://github.com/Tofulati/A-to-I-modification">GitHub Repo</a></p>
    </footer>
  </>
  );
}

