// const view_all_btn = document.getElementById("btn-display");
const display = document.getElementById("display");
// const display_single = document.getElementById("display-single");
const singlePID = document.getElementById("display-single");
const singleDel = document.getElementById("single-del");
const display_form = document.getElementById("createpatient");
// const display_update_form = document.getElementById("editpatient");
const display_update_form = document.getElementById("editpatient");

function hideAll() {
    singlePID.style.display = "none";
    singleDel.style.display = "none";
    display.style.display = "none";
    display_form.style.display = "none";
    display_update_form.style.display = "none";
}

function displayTable(data) {
    let title = '';
    let tableHTML = '';
    
    if ('name' in data) {
        // Single patient
        title = '<h2>Patient Details</h2>';
        tableHTML = `
            <table border="1" style="margin: 0 auto; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th>Field</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>ID</td><td>${document.getElementById("single-pid").value}</td></tr>
                    <tr><td>Name</td><td>${data.name}</td></tr>
                    <tr><td>City</td><td>${data.city}</td></tr>
                    <tr><td>Age</td><td>${data.age}</td></tr>
                    <tr><td>Gender</td><td>${data.gender}</td></tr>
                    <tr><td>Height</td><td>${data.height}</td></tr>
                    <tr><td>Weight</td><td>${data.weight}</td></tr>
                    <tr><td>BMI</td><td>${data.bmi}</td></tr>
                    <tr><td>Verdict</td><td>${data.verdict}</td></tr>
                </tbody>
            </table>
        `;
    } else {
        // All patients
        title = '<h2>All Patients</h2>';
        tableHTML = `
            <table border="1" style="margin: 0 auto; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>City</th>
                        <th>Age</th>
                        <th>Gender</th>
                        <th>Height</th>
                        <th>Weight</th>
                        <th>BMI</th>
                        <th>Verdict</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        for (const [id, patient] of Object.entries(data)) {
            tableHTML += `
                <tr>
                    <td>${id}</td>
                    <td>${patient.name}</td>
                    <td>${patient.city}</td>
                    <td>${patient.age}</td>
                    <td>${patient.gender}</td>
                    <td>${patient.height}</td>
                    <td>${patient.weight}</td>
                    <td>${patient.bmi}</td>
                    <td>${patient.verdict}</td>
                </tr>
            `;
        }
        
        tableHTML += `
                </tbody>
            </table>
        `;
    }
    
    display.innerHTML = title + tableHTML;
}

document.getElementById("btn-display").onclick = async () => {
    hideAll();
    display.style.display = "block";
    const res = await fetch("http://127.0.0.1:8000/view-all");
    const data = await res.json();
    displayTable(data);
};

document.getElementById("btn-single").onclick = () => {
    hideAll();
    singlePID.style.display = "block";
};

document.getElementById("sdis-btn").onclick = async (event) => {
    event.preventDefault();
    display.innerHTML = "";
    display.style.display = "block";
    const pid = document.getElementById("single-pid").value;
    const res = await fetch(`http://127.0.0.1:8000/view/${pid}`);
    const data = await res.json();
    displayTable(data);
};

document.getElementById("btn-create").onclick = () => {
    hideAll();
    display_form.style.display = "block";
};

document
  .getElementById("createpatient")
  .addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent form submission

    const payload = {
      id: document.getElementById("pid").value,
      name: document.getElementById("pname").value,
      gender: document.getElementById("pgen").value,
      city: document.getElementById("pcity").value,
      age: document.getElementById("page").value,
      weight: document.getElementById("pweight").value,
      height: document.getElementById("pheight").value
    };

    const res = await fetch("http://127.0.0.1:8000/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok) {
        window.alert("Patient created successfully");
        display.innerHTML = "<b>Successfully created a new patient</b>";
        hideAll();
        display.style.display = "block";
    } else {
        window.alert(`Error: ${data.detail[0].msg}`);
    }
  });

document.getElementById("btn-edit").onclick = () => {
    hideAll();
    display_update_form.style.display = "block";
};

document
  .getElementById("editpatient")
  .addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent form submission

    const payload = {};

    const name = document.getElementById("epname").value;
    const gender = document.getElementById("epgen").value;
    const city = document.getElementById("epcity").value;
    const age = document.getElementById("epage").value;
    const weight = document.getElementById("epweight").value;
    const height = document.getElementById("epheight").value;

    // Only send fields that are filled (partial update)
    if (name) payload.name = name;
    if (gender) payload.gender = gender;
    if (city) payload.city = city;
    if (age) payload.age = Number(age);
    if (weight) payload.weight = Number(weight);
    if (height) payload.height = Number(height);

    const id = document.getElementById("epid").value;

    const res = await fetch(`http://127.0.0.1:8000/update/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok) {
        window.alert("Patient updated successfully");
        display.innerHTML = "<b>Successfully updated patient</b>";
        hideAll();
        display.style.display = "block";
    } else {
        window.alert(`Error: ${data.detail || data.message || 'Unknown error'}`);
    }
  });

document.getElementById("btn-delete").onclick = () => {
    hideAll();
    singleDel.style.display = "block";
};

document.getElementById("sdel-btn").onclick = async(e) => {
    e.preventDefault();
    const id = document.getElementById("del-pid").value;
    const res = await fetch(`http://127.0.0.1:8000/delete/${id}`, {
        method: "DELETE", 
        headers: {
            "Content-Type" : "application/json"
        }
    });
    const data = await res.json();
    if (res.ok) {
        window.alert(`Patient ${id} deleted successfully`);
        display.innerHTML = "<b>Successfully deleted the patient</b>";
        hideAll();
        display.style.display = "block";
    } else {
        window.alert(`Error: ${data.detail || data.message || 'Unknown error'}`);
    }
}