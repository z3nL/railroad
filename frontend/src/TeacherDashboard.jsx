import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import arrowRight from './assets/arrow-right.svg';
import './TeacherDashboard.css';
import './App.css';

const TeacherDashboard = () => {
    const navigate = useNavigate();
    const [createButtonText, setCreateButtonText] = useState('Create Lesson');
    const [isCreatingLesson, setIsCreatingLesson] = useState(false);

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
            setCreateButtonText('Cancel');
        }
        setIsCreatingLesson(!isCreatingLesson);
    };

    const handleCreateLessonSubmissionButton = (e) => {
        e.preventDefault();
        title = e.target[0].value;
        topic = e.target[1].value;
        level = e.target[2].value;
        description = e.target[3].value;
    }

    const handleLessonClick = (lessonId) => {
        alert(`GK: Clicked ${lessonId}, not implemented yet`);
    };

    return (
        <div className="dashboardContainer">
            <div className="dashboardHeader">
                <h1>Hello, Educator!</h1>
                <button className="logoutButton" onClick={handleLogout}>
                    Log Out
                </button>
            </div>

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


            <button className="createButton" onClick={handleCreateLessonModalButton}>
                {createButtonText}
            </button>

            {isCreatingLesson && (
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
        </div>
    );
};

export default TeacherDashboard;
