const handleCreateLessonSubmissionButton = (e, handleCreateLessonModalButton, setPendingLessonName, setIsWaitingOnLessonCreation) => {
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
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert("Lesson created successfully!");
                console.log(data.lesson_id);
            } else {
                alert(`Failed to create lesson: ${data.message}`);
            }
        })
        .catch((err) => {
            console.error("Error during lesson creation:", err);
            alert("An error occurred during lesson creation. Please try again.");
        });
    
    handleCreateLessonModalButton();
    setPendingLessonName(title);
    setIsWaitingOnLessonCreation(true);
}

export default handleCreateLessonSubmissionButton;