const handleLogin = (e, navigate) => {
    e.preventDefault();
    const username = e.target[0].value;
    const password = e.target[1].value;

    const roles = {
        1: "student",
        2: "teacher"
    };

    const roleNav = {
        "student": "/gk",
        "teacher": "/teacher-dashboard"
    }

    fetch(`http://localhost:5000/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                navigate(roleNav[roles[data.role]]);
            } else {
                alert(`Login failed: ${data.message}`);
            }
        })
        .catch((err) => {
            console.error("Error during login:", err);
            alert("An error occurred during login. Please try again.");
        });
};

export default handleLogin;
