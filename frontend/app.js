const API = "http://127.0.0.1:5000";

// Fetches all sweets from the backend API
async function fetchSweets() {
  const res = await fetch(`${API}/sweets`);
  const data = await res.json();
  return data;
}

// Renders the list of sweets in the HTML table
async function renderSweets(sweets = null) {
  // If sweets are not provided, fetch all
  if (!sweets) sweets = await fetchSweets();
  const tbody = document.querySelector("#sweetTable tbody");
  tbody.innerHTML = "";
  if (sweets && sweets.length > 0) {
    sweets.forEach((sweet) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${sweet.sweet_id}</td>
        <td>${sweet.name}</td>
        <td>${sweet.category}</td>
        <td>₹${sweet.price}</td>
        <td>${sweet.quantity}</td>
        <td>
          <button onclick="deleteSweet(${sweet.sweet_id})">Delete</button>
          <button onclick="purchaseSweet(${sweet.sweet_id})">Purchase</button>
          <button onclick="restockSweet(${sweet.sweet_id})">Restock</button>
        </td>
      `;
      tbody.appendChild(row);
    });
  } else {
    const row = document.createElement("tr");
    row.innerHTML = `<td colspan="6" style="text-align: center;">No sweets available. Add some!</td>`;
    tbody.appendChild(row);
  }
}

// Search sweets by name, category, price range
async function searchSweets(e) {
  e.preventDefault();
  const name = document.getElementById("searchName").value;
  const category = document.getElementById("searchCategory").value;
  const priceMin = document.getElementById("searchPriceMin").value;
  const priceMax = document.getElementById("searchPriceMax").value;
  let url = `${API}/sweets/search?`;
  if (name) url += `name=${encodeURIComponent(name)}&`;
  if (category) url += `category=${encodeURIComponent(category)}&`;
  if (priceMin) url += `price_min=${encodeURIComponent(priceMin)}&`;
  if (priceMax) url += `price_max=${encodeURIComponent(priceMax)}&`;
  const res = await fetch(url);
  const sweets = await res.json();
  renderSweets(sweets);
}

// Clear search and show all sweets
document.getElementById("clearSearch").addEventListener("click", function() {
  document.getElementById("searchSweetForm").reset();
  renderSweets();
});

// Attach search form event
document.getElementById("searchSweetForm").addEventListener("submit", searchSweets);

// Sort sweets by key and order
function sortSweets(order = "asc") {
  const key = document.getElementById("sortKey").value;
  // Get current sweets in table
  const rows = Array.from(document.querySelectorAll("#sweetTable tbody tr"));
  let sweets = rows.map(row => {
    const cells = row.querySelectorAll("td");
    return {
      sweet_id: cells[0].textContent,
      name: cells[1].textContent,
      category: cells[2].textContent,
      price: parseFloat(cells[3].textContent.replace("₹", "")),
      quantity: parseInt(cells[4].textContent)
    };
  });
  sweets.sort((a, b) => {
    if (key === "price" || key === "quantity") {
      return order === "asc" ? a[key] - b[key] : b[key] - a[key];
    } else {
      return order === "asc"
        ? a[key].localeCompare(b[key])
        : b[key].localeCompare(a[key]);
    }
  });
  renderSweets(sweets);
}

document.getElementById("sortAsc").addEventListener("click", function() {
  sortSweets("asc");
});
document.getElementById("sortDesc").addEventListener("click", function() {
  sortSweets("desc");
});

// Event listener for adding a new sweet
document.getElementById("addSweetForm").addEventListener("submit", async function (e) {
  e.preventDefault(); // Prevent default form submission
  
  // Construct the sweet object with 'sweet_id' as the key
  const sweet = {
    sweet_id: parseInt(document.getElementById("sweetId").value), // <-- CORRECTED: Changed 'id' to 'sweet_id'
    name: document.getElementById("sweetName").value,
    category: document.getElementById("sweetCategory").value,
    price: parseFloat(document.getElementById("sweetPrice").value),
    quantity: parseInt(document.getElementById("sweetQuantity").value)
  };

  const res = await fetch(`${API}/sweets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(sweet) // Send the sweet object as JSON
  });
  
  const data = await res.json(); // Parse the response from the backend
  
  if (res.ok) { // Check if the response status is 2xx (success)
    alert(data.message);
    renderSweets(); // Re-render the table to show the new sweet
    this.reset(); // Clear the form
  } else {
    alert(data.error); // Show error message from the backend
  }
});

// Function to delete a sweet by its ID
async function deleteSweet(sweetId) { // Changed parameter name to sweetId for clarity
  const res = await fetch(`${API}/sweets/${sweetId}`, { method: "DELETE" });
  const data = await res.json();
  
  if (res.ok) {
    alert(data.message);
    renderSweets(); // Re-render the table after deletion
  } else {
    alert(data.error);
  }
}

// Function to purchase a sweet
async function purchaseSweet(sweetId) {
  const qty = prompt("Enter quantity to purchase:");
  if (!qty || isNaN(qty) || qty <= 0) return alert("Enter a valid quantity.");
  const res = await fetch(`${API}/sweets/${sweetId}/purchase`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ quantity: parseInt(qty) })
  });
  const data = await res.json();
  if (res.ok) {
    alert(data.message);
    renderSweets();
  } else {
    alert(data.error);
  }
}

// Function to restock a sweet
async function restockSweet(sweetId) {
  const qty = prompt("Enter quantity to restock:");
  if (!qty || isNaN(qty) || qty <= 0) return alert("Enter a valid quantity.");
  const res = await fetch(`${API}/sweets/${sweetId}/restock`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ quantity: parseInt(qty) })
  });
  const data = await res.json();
  if (res.ok) {
    alert(data.message);
    renderSweets();
  } else {
    alert(data.error);
  }
}

// Initial rendering of sweets when the page loads
renderSweets();