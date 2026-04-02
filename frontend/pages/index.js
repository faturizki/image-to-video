import { useState, useCallback, useMemo } from 'react';
import { generateVideo } from '../services/api';

export default function Home() {
  const [formData, setFormData] = useState({
    prompt: '',
    mode: 'ads',
    duration: 180,
    referenceImage: null
  });
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = useCallback((field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setError(null); // Clear error on input change
  }, []);

  const handleFileChange = useCallback((e) => {
    const file = e.target.files[0];
    if (file && !file.type.startsWith('image/')) {
      setError('Please select a valid image file');
      return;
    }
    handleInputChange('referenceImage', file);
  }, [handleInputChange]);

  const isFormValid = useMemo(() => {
    return formData.prompt.trim().length > 0 &&
           ['ads', 'cinematic'].includes(formData.mode) &&
           formData.duration >= 120 && formData.duration <= 300;
  }, [formData]);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!isFormValid) return;

    setLoading(true);
    setProgress(0);
    setError(null);
    setResult(null);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90));
      }, 500);

      const data = new FormData();
      data.append('prompt', formData.prompt);
      data.append('mode', formData.mode);
      data.append('duration', formData.duration);
      if (formData.referenceImage) {
        data.append('reference_image', formData.referenceImage);
      }

      const response = await generateVideo(data);
      setResult(response.data);
      setProgress(100);

      clearInterval(progressInterval);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate video. Please try again.');
      setProgress(0);
    } finally {
      setLoading(false);
    }
  }, [formData, isFormValid]);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial', maxWidth: '800px', margin: '0 auto' }}>
      <h1>AI Video Generator</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Prompt:
          </label>
          <textarea
            value={formData.prompt}
            onChange={(e) => handleInputChange('prompt', e.target.value)}
            required
            style={{ width: '100%', minHeight: '100px', padding: '8px' }}
            placeholder="Describe the video you want to create..."
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Mode:
          </label>
          <select
            value={formData.mode}
            onChange={(e) => handleInputChange('mode', e.target.value)}
            style={{ padding: '8px', width: '200px' }}
          >
            <option value="ads">Ads</option>
            <option value="cinematic">Cinematic</option>
          </select>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Duration (seconds):
          </label>
          <input
            type="number"
            value={formData.duration}
            onChange={(e) => handleInputChange('duration', parseInt(e.target.value) || 180)}
            min="120"
            max="300"
            style={{ padding: '8px', width: '200px' }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Reference Image (optional):
          </label>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            style={{ padding: '8px' }}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !isFormValid}
          style={{
            padding: '10px 20px',
            backgroundColor: isFormValid && !loading ? '#007bff' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isFormValid && !loading ? 'pointer' : 'not-allowed'
          }}
        >
          {loading ? 'Generating...' : 'Generate Video'}
        </button>
      </form>

      {loading && (
        <div style={{ marginBottom: '20px' }}>
          <div style={{ marginBottom: '10px' }}>Progress: {progress}%</div>
          <div style={{
            width: '100%',
            height: '20px',
            backgroundColor: '#f0f0f0',
            borderRadius: '10px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: `${progress}%`,
              height: '100%',
              backgroundColor: '#007bff',
              transition: 'width 0.3s ease'
            }} />
          </div>
        </div>
      )}

      {error && (
        <div style={{
          padding: '10px',
          backgroundColor: '#f8d7da',
          color: '#721c24',
          border: '1px solid #f5c6cb',
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          Error: {error}
        </div>
      )}

      {result && (
        <div style={{
          padding: '20px',
          backgroundColor: '#d4edda',
          color: '#155724',
          border: '1px solid #c3e6cb',
          borderRadius: '4px'
        }}>
          <h2>Video Generated Successfully!</h2>
          <p>Status: {result.status}</p>
          <div style={{ marginTop: '15px' }}>
            <video
              controls
              style={{ maxWidth: '100%', height: 'auto' }}
              src={`http://localhost:8000${result.video_url}`}
            />
          </div>
          <div style={{ marginTop: '15px' }}>
            <a
              href={`http://localhost:8000${result.video_url}`}
              download
              style={{
                padding: '8px 16px',
                backgroundColor: '#28a745',
                color: 'white',
                textDecoration: 'none',
                borderRadius: '4px'
              }}
            >
              Download Video
            </a>
          </div>
          {result.scenes && result.scenes.length > 0 && (
            <div style={{ marginTop: '20px' }}>
              <h3>Scenes:</h3>
              <ul>
                {result.scenes.map((scene, index) => (
                  <li key={index}>
                    <strong>Scene {scene.scene}:</strong> {scene.text} ({scene.duration}s)
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}