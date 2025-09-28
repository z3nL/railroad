import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App'
import TeacherDashboard from './TeacherDashboard.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        {/* Root route */}
        <Route path="/" element={<App />} />
        {/* Teacher dashboard route */}
        <Route path="/teacher-dashboard" element={<TeacherDashboard />} />
        {/* Gatekeeper route */}
        <Route path="/gk" element={
          <>
          <h1>// Gatekeeper //<br/> Functionality Not Implemented Yet</h1>
          <h3>Do NOT sign in as a student</h3>
          <a href="/">Back to Sign-In</a>

          </>
        } />
        {/* Catch-all route for undefined paths */}
        <Route path="*" element={
          <><h1>404 <br /> Not Found</h1>
          <a href="/">Back to Sign-In</a>
          </>
        } />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
