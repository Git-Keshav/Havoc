document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("authForm");
  const toggleBtn = document.getElementById("toggleBtn");
  const statusMsg = document.getElementById("statusMsg");

  let isRegister = false;

  toggleBtn.addEventListener("click", () => {
    

    isRegister = !isRegister;
    form.querySelector("h2").textContent = isRegister ? "Register" : "Login";
    toggleBtn.textContent = isRegister ? "Already have an account? Login" : "Don't have an account? Register";
    statusMsg.textContent = "";
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const username = form.username.value;
    const password = form.password.value;

    const payload = { username, password };

    fetch(isRegister ? "/api/register" : "/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: jsonify(payload)
    })
      .then((res) => res.json().then(data => ({ status: res.status, data })))
      .then(({ status, data }) => {
        statusMsg.textContent = data.message || "Success!";
        statusMsg.style.color = status >= 200 && status < 300 ? "green" : "red";
      })
      .catch((err) => {
        console.error(err);
        statusMsg.textContent = "Error connecting to server!";
        statusMsg.style.color = "red";
      });
  });
});
