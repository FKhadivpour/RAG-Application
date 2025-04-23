import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          top_k: 5
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
      console.error('Error querying API:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>RAG Knowledge Assistant</h1>
        <p>Ask questions about scientific papers from ArXiv</p>
      </header>

      <main className="App-main">
        <form onSubmit={handleSubmit} className="query-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your question..."
            className="query-input"
          />
          <button type="submit" className="query-button" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}

        {result && (
          <div className="result-container">
            <div className="answer-container">
              <h2>Answer</h2>
              <p>{result.answer}</p>
            </div>

            <div className="context-container">
              <h2>Sources</h2>
              {result.context_chunks.map((chunk, index) => (
                <div key={index} className="context-chunk">
                  <h3>{chunk.metadata.title || 'Untitled'}</h3>
                  <p className="source-info">Source: {chunk.metadata.source || 'Unknown'}</p>
                  <p className="chunk-text">{chunk.text}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>RAG Knowledge Assistant &copy; 2025</p>
      </footer>
    </div>
  );
}

export default App;
