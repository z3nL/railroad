import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
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
    // ... (All your existing state and handler functions remain unchanged)
    const [topics, setTopics] = useState([
        {
            topicId: 't1',
            topicTitle: 'Algebra',
            lessons: [
                {
                    id: 'l1a',
                    lesson_name: 'Understanding y = mx + b',
                    steps: [
                        { text: 'Step 1: Identify the slope "m", which is the number next to x.', image: 'https://picsum.photos/seed/algebra1a/500/300' },
                        { text: 'Step 2: Identify the y-intercept "b", which is the constant number.', image: 'https://picsum.photos/seed/algebra1b/500/300' },
                        { text: 'Step 3: Plot the y-intercept on the vertical y-axis to get your starting point.', image: 'https://picsum.photos/seed/algebra1c/500/300' }
                    ]
                }
            ]
        },
        {
            topicId: 't2',
            topicTitle: 'Geometry',
            lessons: [
                {
                    id: 'l2a',
                    lesson_name: 'The Pythagorean Theorem',
                    steps: [
                        { text: 'Step 1: Identify the two shorter sides of the right triangle, "a" and "b".', image: 'https://picsum.photos/seed/geometry1a/500/300' },
                        { text: 'Step 2: Square both sides, a² and b², and then add them together.', image: 'https://picsum.photos/seed/geometry1b/500/300' }
                    ]
                }
            ]
        }
    ]);
    const [selectedTopic, setSelectedTopic] = useState(null);
    const [selectedLesson, setSelectedLesson] = useState(null);
    const [currentStepIndex, setCurrentStepIndex] = useState(0);

    const handleLessonCreated = (topicTitle, lessonTitle, newSteps) => {
        const updatedTopics = JSON.parse(JSON.stringify(topics));
        const topicIndex = updatedTopics.findIndex(t => t.topicTitle.toLowerCase() === topicTitle.toLowerCase());
        const newLesson = {
            lesson_id: `l${Date.now()}`,
            lesson_name: lessonTitle,
            steps: newSteps
        };
        if (topicIndex !== -1) {
            updatedTopics[topicIndex].lessons.push(newLesson);
        } else {
            const newTopic = {
                topicId: `t${Date.now()}`,
                topicTitle: topicTitle,
                lessons: [newLesson]
            };
            updatedTopics.push(newTopic);
        }
        setTopics(updatedTopics);
    };

    const handleDeleteTopic = (topicId) => {
        if (!window.confirm("Are you sure you want to delete this entire topic and all its lessons?")) return;
        setTopics(topics.filter(topic => topic.topicId !== topicId));
    };

    const handleDeleteLesson = (topicId, lessonId) => {
        if (!window.confirm("Are you sure you want to permanently delete this lesson?")) return;
        const updatedTopics = topics.map(topic => {
            if (topic.topicId === topicId) {
                return { ...topic, lessons: topic.lessons.filter(l => (l.id || l.lesson_id) !== lessonId) };
            }
            return topic;
        });
        setTopics(updatedTopics);
    };

    const handleLogout = () => navigate('/');
    const handleTopicClick = (topicId) => setSelectedTopic(topics.find(t => t.topicId === topicId));
    const handleLessonClick = (lessonId) => {
        setSelectedLesson(selectedTopic.lessons.find(l => (l.id || l.lesson_id) === lessonId));
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
    const handleBackToTopicList = () => {
        setSelectedTopic(null);
        setSelectedLesson(null);
    };

    let content;

    if (selectedTopic && selectedLesson) {
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
                        {currentStep.image && <img className="stepImage" src={currentStep.image} alt={`Visual for ${currentStep.text}`} />}
                        <p className="stepText">{currentStep.text}</p>
                    </div>
                    <button className="nav-arrow next" onClick={handleNextStep} disabled={currentStepIndex === totalSteps - 1}>►</button>
                </div>
                <button className="backButton" onClick={() => setSelectedLesson(null)}>
                    Back to '{selectedTopic.topicTitle}' Lessons
                </button>
            </div>
        );
    } else if (selectedTopic) {
        // ... Lesson List View (no changes needed here)
        content = (
            <>
                <div className="welcome-header">
                    <h3>{selectedTopic.topicTitle}</h3>
                    <div className="header-line"></div>
                </div>
                <div className="lessonList">
                    {selectedTopic.lessons.map((lesson) => (
                        <div key={lesson.id || lesson.lesson_id} className="lessonItem">
                            <div className="lessonItem-main" onClick={() => handleLessonClick(lesson.id || lesson.lesson_id)}>
                                <p>{lesson.lesson_name || lesson.title}</p>
                                <img className="arrowIcon" src={arrowRight} alt="Go" />
                            </div>
                            <button className="delete-button" onClick={(e) => { e.stopPropagation(); handleDeleteLesson(selectedTopic.topicId, lesson.id || lesson.lesson_id); }}>🗑️</button>
                        </div>
                    ))}
                </div>
                <button className="backButton" onClick={handleBackToTopicList}>Back to All Topics</button>
            </>
        );
    } else {
        // ... Topic List and Create Form View (updated for new styles)
        content = (
            <>
                <div className="welcome-header" style={{ marginBottom: '2rem' }}>
                    <h3>Your Lesson Topics</h3>
                    <div className="header-line"></div>
                </div>

                <div className="lessonList">
                    {topics.map((topic) => (
                        <div key={topic.topicId} className="lessonItem">
                            <div className="lessonItem-main" onClick={() => handleTopicClick(topic.topicId)}>
                                <p>{topic.topicTitle}</p>
                                <img className="arrowIcon" src={arrowRight} alt="Go" />
                            </div>
                            <button className="delete-button" onClick={(e) => { e.stopPropagation(); handleDeleteTopic(topic.topicId); }}>🗑️</button>
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
                    <form className="createLessonForm" onSubmit={(e) => handleCreateLessonSubmissionButton(e, () => setIsCreatingLesson(false), handleLessonCreated)}>
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
                                <span>Generate & Create</span>
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
