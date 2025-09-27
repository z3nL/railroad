import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import arrowRight from './assets/arrow-right.svg';
import './TeacherDashboard.css';
import './App.css';

const TeacherDashboard = () => {
    const navigate = useNavigate();
    const [createButtonText, setCreateButtonText] = useState('Create Lesson');
    const [isCreatingLesson, setIsCreatingLesson] = useState(false);
    const [isWaitingOnLessonCreation, setIsWaitingOnLessonCreation] = useState(false);
    const [pendingLessonName, setPendingLessonName] = useState("default");

    // Mock lessons
    const [lessons, setLessons] = useState([
        { id: 1, title: 'Introduction to Algebra' },
        { id: 2, title: 'Geometry Basics' },
        { id: 3, title: 'Physics: Motion' },
        { id: 4, title: 'World History: Renaissance' },
        { id: 5, title: 'Chemistry: Atoms & Molecules' },
        { id: 6, title: 'Greatness: Lebron James' },
        { id: 7, title: 'Algebra: Solving Linear Equations' },
    ]);

    const handleLogout = () => {
        navigate('/'); // Redirect to login page
    };

    const handleCreateLessonModalButton = () => {
        if (isCreatingLesson) {
            setCreateButtonText('Create Lesson');
        } else {
            setCreateButtonText('Cancel Creation');
        }
        setIsCreatingLesson(!isCreatingLesson);
    };

    const handleCreateLessonSubmissionButton = (e) => {
        e.preventDefault();
        const title = e.target[0].value;
        const topic = e.target[1].value;
        const level = e.target[2].value;
        const description = e.target[3].value;

        fetch(`http://localhost:5000/createLesson`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ title, topic, level, description }),
        });
        /*
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    alert("Lesson created successfully!");
                } else {
                    alert(`Failed to create lesson: ${data.message}`);
                }
            })
            .catch((err) => {
                console.error("Error during lesson creation:", err);
                alert("An error occurred during lesson creation. Please try again.");
            });
        */
        
        handleCreateLessonModalButton();
        setPendingLessonName(title);
        setIsWaitingOnLessonCreation(true);
    }

    const handleLessonClick = (lessonId) => {
        alert(`GK: Clicked ${lessonId}, not implemented yet`);
    };

    useEffect(() => {
        if (isWaitingOnLessonCreation) {
            const timer = setTimeout(() => {
                setIsWaitingOnLessonCreation(false);
                // TODO actually wait on lesson creation
                setLessons([...lessons, { id: lessons.length + 1, title: `New Lesson ${lessons.length + 1}: ${pendingLessonName}` }]);
            }, 3000); // Simulate a 3-second wait time for lesson creation
            return () => clearTimeout(timer);
        }
    }, [isWaitingOnLessonCreation, lessons]);

    return (
        <div className="dashboardContainer">
            <div className="dashboardHeader">
                <h1>Hello, Educator!</h1>
                <button className="logoutButton" onClick={handleLogout}>
                    Log Out
                </button>
            </div>

        {!isCreatingLesson && !isWaitingOnLessonCreation && (
        <>
            <h2>Your Students' Lessons</h2>
            <div className="lessonList">
                {lessons.map((lesson) => (
                    <div
                        key={lesson.id}
                        className="lessonItem"
                        onClick={() => handleLessonClick(lesson.id)}
                    >
                        <p>{lesson.title}</p>
                        <img className="arrowIcon" src={arrowRight} alt="Go" />
                    </div>
                ))}
            </div>
        </>
        )}


            <button className="createButton" onClick={handleCreateLessonModalButton}>
                {createButtonText}
            </button>

            {isCreatingLesson && !isWaitingOnLessonCreation && (
                <form className="createLessonForm" onSubmit={handleCreateLessonSubmissionButton}>
                    <input className='inputField' type="text" placeholder="Lesson Title" required/>
                    <input className='inputField' type="text" placeholder="Lesson Topic" required/>
                    <input className='inputField' type="text" placeholder="Student Learning Level" required/>
                    <textarea className='inputField' placeholder="Lesson Description" required></textarea>
                    <button
                        className="submitLessonButton"
                    >
                        Let's Teach!
                    </button>
                </form>
            )}

            {isWaitingOnLessonCreation && (
                <div className="waitingContainer">
                    <h2>Generating {pendingLessonName}...</h2>
                    <p>awesome train gif</p>
                </div>
            )}
        </div>
    );
};

export default TeacherDashboard;
