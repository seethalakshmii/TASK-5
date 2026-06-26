async function load() {
    const res1 = await fetch("/health");
    const data1 = await res1.json();
    document.getElementById("health").innerText = data1.status;

    const res2 = await fetch("/");
    const data2 = await res2.json();
    document.getElementById("msg").innerText = data2.message;
}

load();

document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        message: document.getElementById("message").value
    };

    const res = await fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    document.getElementById("response").innerText = result.message;
});