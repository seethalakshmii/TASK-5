async function load() {

    const health = await fetch("/api/health");
    const healthData = await health.json();

    document.getElementById("health").innerText =
        healthData.status;

    const home = await fetch("/api/");
    const homeData = await home.json();

    document.getElementById("msg").innerText =
        homeData.message;
}

load();


document.getElementById("form").addEventListener("submit", async (e) => {

    e.preventDefault();

    const body = {

        name: document.getElementById("name").value,

        email: document.getElementById("email").value,

        message: document.getElementById("message").value
    };

    const res = await fetch("/api/submit", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(body)
    });

    const result = await res.json();

    document.getElementById("response").innerText =
        result.message || result.error;
});


async function uploadFile() {

    const file =
        document.getElementById("fileInput").files[0];

    if (!file) {

        alert("Select a file");

        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    const res = await fetch("/api/upload", {

        method: "POST",

        body: formData
    });

    const result = await res.json();

    document.getElementById("uploadStatus").innerText =
        result.message || result.error;
}