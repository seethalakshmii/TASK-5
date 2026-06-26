async function load() {
    const res1 = await fetch("/api/health");
    const data1 = await res1.json();
    document.getElementById("health").innerText = data1.status;

    const res2 = await fetch("/api/");
    const data2 = await res2.json();
    document.getElementById("msg").innerText = data2.message;
}

load();


// -------------------------
// FORM SUBMIT → RDS
// -------------------------
document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        message: document.getElementById("message").value
    };

    const res = await fetch("/api/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    document.getElementById("response").innerText = result.message || result.error;
});


// -------------------------
// S3 FILE UPLOAD
// -------------------------
async function uploadFile() {
    const fileInput = document.getElementById("fileInput");

    if (!fileInput.files.length) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const res = await fetch("/api/upload", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("uploadStatus").innerText =
        data.message || data.error;
}