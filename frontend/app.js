const apiBase = "http://127.0.0.1:8000";

function renderResults(items) {
  const root = document.getElementById("results");
  root.innerHTML = "";
  (items || []).forEach((r) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${apiBase}/${r.path}" alt="result" onerror="this.style.display='none'"/>
      <div class="meta">
        <div class="desc">${r.desc}</div>
        <div class="score">score: ${r.score.toFixed(3)}</div>
        <div class="path">${r.path}</div>
      </div>`;
    root.appendChild(card);
  });
}

// Upload image to index
const btnUpload = document.getElementById("btnUpload");
btnUpload.onclick = async () => {
  const file = document.getElementById("uploadFile").files[0];
  if (!file) {
    return alert("Choose an image first");
  }
  const form = new FormData();
  form.append("file", file);
  try {
    const res = await fetch(`${apiBase}/upload-image/`, { method: "POST", body: form });
    const data = await res.json();
    document.getElementById("uploadResult").textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    console.error("Upload failed:", error);
    alert("Upload failed. Check console for details.");
  }
};

// Search by text
const btnSearchText = document.getElementById("btnSearchText");
btnSearchText.onclick = async () => {
  const q = document.getElementById("textQuery").value;
  if (!q) {
    return;
  }
  const form = new FormData();
  form.append("query", q);
  try {
    const res = await fetch(`${apiBase}/search-text/`, { method: "POST", body: form });
    const data = await res.json();
    renderResults(data.results);
  } catch (error) {
    console.error("Text search failed:", error);
    alert("Text search failed. Check console for details.");
  }
};

// Search by image
const btnSearchImage = document.getElementById("btnSearchImage");
btnSearchImage.onclick = async () => {
  const file = document.getElementById("imageQuery").files[0];
  if (!file) {
    return alert("Choose an image first");
  }
  const form = new FormData();
  form.append("file", file);
  try {
    const res = await fetch(`${apiBase}/search-image/`, { method: "POST", body: form });
    const data = await res.json();
    renderResults(data.results);
  } catch (error) {
      console.error("Image search failed:", error);
      alert("Image search failed. Check console for details.");
  }
};