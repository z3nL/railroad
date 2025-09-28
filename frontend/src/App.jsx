import { useState } from 'react';
import { useNavigate } from 'react-router-dom'
import './App.css';
import train from './assets/train.png'
import handleLogin from './utils/handleLogin';

function App() {
  const [role, setRole] = useState("teacher");
  const navigate = useNavigate()

  return (
    <>
      <img src={train} className="App-logo" alt="logo" />
      <h1>RaiLROAD</h1>
      <h3>Transforming learning through interactive pictures and engaging descriptions</h3>

      <form className="loginContainer" onSubmit={(e) => handleLogin(e, navigate)}>
        <h3>Welcome Back!</h3>

        {/* Role selector */}
        {/* 
        <div className="roleSelector">
          <label>
            <input
              type="radio"
              value="teacher"
              checked={role === "teacher"}
              onChange={(e) => setRole(e.target.value)}
            />
            Teacher
          </label>
          <label style={{ marginLeft: "1rem" }}>
            <input
              type="radio"
              value="student"
              checked={role === "student"}
              onChange={(e) => setRole(e.target.value)}
            />
            Student
          </label>
        </div>
        */}

        <input className="inputField" type="text" placeholder="Username" required />
        <br />
        <input className="inputField" type="password" placeholder="Password" required />
        <br />

        <br />
        <button type="submit">Log In</button>
      </form>
    </>
  )
}

export default App;
