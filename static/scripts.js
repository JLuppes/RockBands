// ----------------------------
// CLIENT-SIDE FORM VALIDATION
// ----------------------------

// Arrow function here because:
// ✅ short and used once
// ✅ keeps code concise for event listeners
const validateBandForm = (event) => {
    const bandName = document.querySelector("input[name='bandname']").value.trim();
    const formedYear = document.querySelector("input[name='formedyear']").value.trim();

    if (!bandName) {
        alert("Band name is required!");
        event.preventDefault(); // Stops form submission
        return false;
    }

    if (formedYear && (formedYear < 1900 || formedYear > new Date().getFullYear())) {
        alert("Please enter a valid Formed Year.");
        event.preventDefault();
        return false;
    }
};

const validateAlbumForm = (event) => {
    const albumTitle = document.querySelector("input[name='albumtitle']").value.trim();
    const releaseYear = document.querySelector("input[name='releaseyear']").value.trim();

    if (!albumTitle) {
        alert("Please identify the album released!");
        event.preventDefault();
        return false;
    }

    if (releaseYear && (releaseYear < 100 || releaseYear > new Date().getFullYear())) {
        alert("Put a Valid year in.");
        event.preventDefault();
        return false;
    }
}

// Anonymous function example:
// ✅ We don't reuse this logic
// ✅ Good example of inline validation
const validateMemberForm = function(event) {
    const memberName = document.querySelector("input[name='membername']").value.trim();
    if (!memberName) {
        alert("Member name is required!");
        event.preventDefault();
        return false;
    }
};

// DOMContentLoaded waits until HTML is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    
    console.log("JavaScript loaded — validation active!");

    // Attach validation only if forms exist on the current page
    const bandForm = document.getElementById("bandForm");
    if (bandForm) {
        bandForm.addEventListener("submit", validateBandForm);
    }

    const memberForm = document.getElementById("memberForm");
    if (memberForm) {
        memberForm.addEventListener("submit", validateMemberForm);
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const checkboxContainer = document.getElementById('checkboxContainer');

    if (!checkboxContainer) return;
    

    fetch('/api/bands')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(bands => {

            checkboxContainer.innerHTML = '';
            

            if (bands.length === 0) {
                checkboxContainer.innerHTML = '<p style="color: #999;">No bands available.</p>';
                return;
            }

            bands.forEach((band) => {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `band_${band.id}`;
                checkbox.name = 'bandid';
                checkbox.value = band.id;
                // checkbox.checked 

                const label = document.createElement('label');
                label.setAttribute('for', `band_${band.id}`);
                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(` ${band.name}`));
                console.log("working")
                
                checkboxContainer.appendChild(label);
                checkboxContainer.appendChild(document.createElement('br'));
            });
        })
        .catch(error => {
            console.error('Error fetching bands:', error);
            checkboxContainer.innerHTML = '<p style="color: #d32f2f;">Error loading bands. Please refresh the page.</p>';
        });
});


