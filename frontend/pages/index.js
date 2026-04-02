import { useState } from 'react';
import { generateVideo } from '../services/api';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [mode, setMode] = useState('ads');
  const [duration, setDuration] = useState(180);
  const [referenceImage, setReferenceImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append('prompt', prompt);
    formData.append('mode', mode);
    formData.append('duration', duration);
    if (referenceImage) {
      formData.append('reference_image', referenceImage);
    }

    try {
      const response = await generateVideo({
        prompt,
        mode,
        duration,
        reference_image: referenceImage
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert('Error generating video');
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>AI Video Generator</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Prompt:</label>
          <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} required />
        </div>
        <div>
          <label>Mode:</label>
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="ads">Ads</option>
            <option value="cinematic">Cinematic</option>
          </select>
        </div>
        <div>
          <label>Duration (seconds):</label>
          <input type="number" value={duration} onChange={(e) => setDuration(e.target.value)} min="120" max="300" />
        </div>
        <div>
          <label>Reference Image:</label>
          <input type="file" onChange={(e) => setReferenceImage(e.target.files[0])} />
        </div>
        <button type="submit" disabled={loading}>Generate</button>
      </form>
      {loading && <p>Loading...</p>}
      {result && (
        <div>
          <h2>Result</h2>
          <p>Status: {result.status}</p>
          <video controls src={`http://localhost:8000${result.video_url}`} />
          <a href={`http://localhost:8000${result.video_url}`} download>Download</a>
        </div>
      )}
    </div>
  );
}