import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
import train from './assets/train.png'; // Your existing train image
import handleLogin from './utils/handleLogin'; // Your existing login function

// Custom Train Component using your actual image
const TrainLogo = () => (
  <div className="train-container">
    <img src={train} className="train-logo" alt="train" />
    <div className="logo-glow"></div>
  </div>
);

// Cloud SVG Component
const CloudIcon = ({ delay = "0s", size = "normal" }) => (
  <div 
    className={`floating-cloud ${size === "small" ? "floating-cloud-small" : ""}`}
    style={{ animationDelay: delay }}
  >
    <svg width="60" height="40" viewBox="0 0 60 40" fill="none">
      <path d="M50 25c0-8.284-6.716-15-15-15-1.341 0-2.646.176-3.891.508C28.715 4.508 22.944 0 16 0 7.163 0 0 7.163 0 16c0 1.105.112 2.185.325 3.227C.112 20.356 0 21.665 0 23c0 6.627 5.373 12 12 12h36c5.523 0 10-4.477 10-10z" fill="rgba(255, 255, 255, 0.9)"/>
    </svg>
  </div>
);

function App() {
  const [role, setRole] = useState("teacher");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    setIsLoading(true);
    
    // Use your existing handleLogin function
    handleLogin(e, navigate);
    
    // Reset loading state after a delay (adjust as needed)
    setTimeout(() => setIsLoading(false), 2000);
  };

  return (
    <div className="app-container">
      <div className="background-elements">
        <CloudIcon delay="0s" />
        <CloudIcon delay="2s" size="small" />
        <CloudIcon delay="4s" />
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      <div className="main-content">
        <div className="logo-section">
          <div className="logo-container">
            <TrainLogo />
          </div>
          <h1 className="main-title">
            <span className="title-rail">Rai</span>
            <span className="title-road">LROAD</span>
          </h1>
          <h3 className="subtitle">
            Transforming learning through interactive pictures and engaging descriptions
          </h3>
        </div>

        <form className="loginContainer" onSubmit={handleSubmit}>
          <div className="welcome-header">
            <h3>Welcome!</h3>
            <div className="header-line"></div>
          </div>

          <div className="input-group">
            <div className="input-wrapper">
              <input 
                className="inputField" 
                type="text" 
                placeholder="Username" 
                required 
              />
              <div className="input-focus-border"></div>
            </div>
          </div>

          <div className="input-group">
            <div className="input-wrapper">
              <input 
                className="inputField" 
                type="password" 
                placeholder="Password" 
                required 
              />
              <div className="input-focus-border"></div>
            </div>
          </div>

          <button 
            type="submit" 
            className={`login-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="loading-spinner"></div>
            ) : (
              <>
                <span>Log In</span>
                <div className="button-shine"></div>
              </>
            )}
          </button>

          <div className="login-footer">
            <p>Ready to embark on your learning journey?</p>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
