let chart = null;

function searchBook() {
    let query = document.getElementById("query").value;

    fetch("/search", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query})
    })
    .then(res => res.json())
    .then(data => {
        renderResults(data);
        renderChart(data);
    });
}

function renderResults(data) {
    let html = `
    <table>
        <tr>
            <th>Site</th>
            <th>Başlık</th>
            <th>Yazar</th>
            <th>Yayınevi</th>
            <th>Fiyat</th>
            <th>Link</th>
            <th>Kaydet</th>
        </tr>
    `;

    data.forEach(b => {
        html += `
        <tr>
            <td>${b.site}</td>
            <td>${b.title}</td>
            <td>${b.author}</td>
            <td>${b.publisher}</td>
            <td>${b.price} TL</td>
            <td><a href="${b.link}" target="_blank">Git</a></td>
            <td><button onclick='addBook(${JSON.stringify(b)})'>Ekle</button></td>
        </tr>
        `;
    });

    html += "</table>";
    document.getElementById("results").innerHTML = html;
}

function renderChart(data) {
    const labels = data.map(d => d.site);
    const prices = data.map(d => d.price);

    if (chart) chart.destroy();

    chart = new Chart(document.getElementById("priceChart"), {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Fiyatlar",
                data: prices,
                backgroundColor: "#d10000",
                borderColor: "#a00000",
                borderWidth: 2
            }]
        }
    });
}

function addBook(book) {
    fetch("/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(book)
    }).then(() => loadBooks());
}

function loadBooks() {
    fetch("/books")
    .then(res => res.json())
    .then(data => {
        let html = "<table><tr><th>ID</th><th>Site</th><th>Başlık</th><th>Fiyat</th><th>Sil</th></tr>";

        data.forEach(row => {
            html += `
            <tr>
                <td>${row[0]}</td>
                <td>${row[1]}</td>
                <td>${row[2]}</td>
                <td>${row[5]}</td>
                <td><button onclick='deleteBook(${row[0]})'>Sil</button></td>
            </tr>`;
        });

        html += "</table>";
        document.getElementById("bookList").innerHTML = html;
    });
}

function deleteBook(id) {
    fetch(`/delete/${id}`, {method: "DELETE"})
    .then(() => loadBooks());
}

// Sayfa açılınca kitapları yükle
loadBooks();
