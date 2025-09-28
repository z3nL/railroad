import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import arrowRight from './assets/arrow-right.svg';
import handleCreateLessonSubmissionButton from './utils/handleCreateLessonSubmissionButton';
import './TeacherDashboard.css'; // Use the new combined CSS file

// Cloud SVG Component from your App.js for the background
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


const TeacherDashboard = () => {
    const navigate = useNavigate();
    const [isCreatingLesson, setIsCreatingLesson] = useState(false);
    const [isWaitingOnLessonCreation, setIsWaitingOnLessonCreation] = useState(false);
    // ... (All your existing state and handler functions remain unchanged)
    const [lessons, setLessons] = useState(null);
    
    const [selectedLesson, setSelectedLesson] = useState(null);
    const [currentStepIndex, setCurrentStepIndex] = useState(0);

    const handleDeleteLesson = (lessonId) => {
        if (!window.confirm("Are you sure you want to permanently delete this lesson?")) return;
        setLessons(lessons.filter(l => (l.lesson_id) !== lessonId));
    };

    const handleLogout = () => navigate('/');
    const handleLessonClick = (lessonId) => {
        setSelectedLesson(lessons.find(l => (l.lesson_id) === lessonId));
        setCurrentStepIndex(0);
    };
    const handleNextStep = () => {
        if (selectedLesson && currentStepIndex < selectedLesson.steps.length - 1) {
            setCurrentStepIndex(currentStepIndex + 1);
        }
    };
    const handlePreviousStep = () => {
        if (currentStepIndex > 0) {
            setCurrentStepIndex(currentStepIndex - 1);
        }
    };

    useEffect(() => {
        if (lessons !== null) return;
        // Fetch lessons from the backend API
        fetch('http://localhost:5000/getLessons') // Adjust the URL as needed
            .then(response => response.json())
            .then(data => setLessons(data.lessons))
            .catch(error => console.error('Error fetching lessons:', error));
    }, []);

    let content;

    if (selectedLesson) {
        // ... Lesson Detail View (no changes needed here)
        const currentStep = selectedLesson.steps[currentStepIndex];
        const totalSteps = selectedLesson.steps.length;
        content = (
            <div className="lessonDetailContainer">
                <h2>{selectedLesson.lesson_name}</h2>
                <h3 className="step-counter">Step {currentStepIndex + 1} of {totalSteps}</h3>
                <div className="step-navigation">
                    <button className="nav-arrow prev" onClick={handlePreviousStep} disabled={currentStepIndex === 0}>◄</button>
                    <div className="lessonStepItem">
                        {currentStep.image_path && <img className="stepImage" src={currentStep.image_path} alt={`Visual for ${currentStep.step_description}`} />}
                        <p className="stepText">{currentStep.step_description}</p>
                    </div>
                    <button className="nav-arrow next" onClick={handleNextStep} disabled={currentStepIndex === totalSteps - 1}>►</button>
                </div>
                <button className="backButton" onClick={() => setSelectedLesson(null)}>
                    Back to Lessons
                </button>
            </div>
        );
    } else {
        // ... Lesson List View (no changes needed here)
        content = (
            <>
                <div className="welcome-header">
                    <h3>{lessons ? "Your Lessons" : "Loading Lessons..."}</h3>
                    <div className="header-line"></div>
                </div>
                <div className="lessonList">
                    {lessons && lessons.map((lesson) => (
                        <div key={lesson.lesson_id} className="lessonItem">
                            <div className="lessonItem-main" onClick={() => handleLessonClick(lesson.lesson_id)}>
                                <p>{lesson.lesson_name}</p>
                                <img className="arrowIcon" src={arrowRight} alt="Go" />
                            </div>
                            <button className="delete-button" onClick={(e) => { e.stopPropagation(); handleDeleteLesson(lesson.lesson_id); }}>🗑️</button>
                        </div>
                    ))}
                </div>
        
                {!isCreatingLesson && (
                    <div className="createButton-container">
                        <button className="login-button" onClick={() => setIsCreatingLesson(true)}>
                            <span>Create New Lesson</span>
                            <div className="button-shine"></div>
                        </button>
                    </div>
                )}

                {isCreatingLesson && (
                    <form className="createLessonForm" onSubmit={(e) => handleCreateLessonSubmissionButton(e, setLessons, setIsCreatingLesson, setIsWaitingOnLessonCreation)}>
                        <div className="welcome-header">
                            <h3>Create a New Lesson</h3>
                            <div className="header-line"></div>
                        </div>
                        <div className="input-wrapper">
                            <input name="topic" className='inputField' type="text" placeholder="Lesson Topic (e.g., 'Algebra')" required />
                        </div>
                        <div className="input-wrapper">
                            <input name="title" className='inputField' type="text" placeholder="Lesson Title (e.g., 'Solving for X')" required />
                        </div>
                        <div className="input-wrapper">
                            <input name="level" className='inputField' type="text" placeholder="Student Learning Level" required />
                        </div>
                        <div className="input-wrapper">
                            <textarea name="description" className='inputField' placeholder="Brief Lesson Description..." required></textarea>
                        </div>
                        <div className="form-button-group">
                            <button type="button" className="cancelButton" onClick={() => setIsCreatingLesson(false)}>Cancel</button>
                            <button type="submit" className="login-button">
                                <span>{isWaitingOnLessonCreation ? "Creating..." : "Generate & Create"}</span>
                                <div className="button-shine"></div>
                            </button>
                        </div>
                    </form>
                )}
            </>
        );
    }

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
                <div className="dashboardHeader">
                    <h1>Hello, Educator!</h1>
                    <button className="logoutButton" onClick={handleLogout}>
                        <span>Log Out</span>
                        <div className="button-shine"></div>
                    </button>
                </div>
                <div className="dashboard-content-area">
                    {content}
                </div>
            </div>
        </div>
    );
};

export default TeacherDashboard;
