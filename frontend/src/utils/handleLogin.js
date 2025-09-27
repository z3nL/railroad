const handleLogin = (e, navigate) => {
    e.preventDefault();
    const role = e.target[0].checked ? "teacher" : "student";
    const username = e.target[2].value;
    const password = e.target[3].value;

    // TODO Unlock student login when feature is complete
    if (role !== "teacher") {
        navigate('/gk');
        return;
    }

    if (username === "teacher@school.edu" && password === "teacher") {
        navigate('/teacher-dashboard');
    }
    else {
        alert("Invalid credentials. Please try again.");
    }

    return;

    // TODO Legitimate sign-in sequence if desired

    fetch(`http://localhost:3000/${role}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert(`Logged in as ${role}: ${username}`);
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
