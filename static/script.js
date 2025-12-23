// API Base URL
const API_URL = window.location.origin;

// State
let schools = [];
let cities = [];
let zipcodes = [];
let selectedModelName = 'knn';
let selectedModelPref = 'knn';

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadInitialData();
});

// Load initial data
async function loadInitialData() {
    try {
        // Load schools
        const schoolsResponse = await fetch(`${API_URL}/api/schools`);
        const schoolsData = await schoolsResponse.json();
        schools = schoolsData.schools;

        // Populate datalist
        const datalist = document.getElementById('schools-list');
        schools.forEach(school => {
            const option = document.createElement('option');
            option.value = school;
            datalist.appendChild(option);
        });

        // Update total schools stat
        document.getElementById('total-schools').textContent = schools.length;

        // Load cities
        const citiesResponse = await fetch(`${API_URL}/api/cities`);
        const citiesData = await citiesResponse.json();
        cities = citiesData.cities;

        const citySelect = document.getElementById('city');
        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });

        // Load zipcodes
        const zipcodesResponse = await fetch(`${API_URL}/api/zipcodes`);
        const zipcodesData = await zipcodesResponse.json();
        zipcodes = zipcodesData.zipcodes;

        const zipcodeSelect = document.getElementById('zipcode');
        zipcodes.forEach(zipcode => {
            const option = document.createElement('option');
            option.value = zipcode;
            option.textContent = zipcode;
            zipcodeSelect.appendChild(option);
        });

    } catch (error) {
        console.error('Error loading initial data:', error);
        alert('Error loading data. Please make sure the server is running.');
    }
}

// Switch search mode
function switchMode(mode) {
    // Update buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-mode="${mode}"]`).classList.add('active');

    // Update forms
    document.querySelectorAll('.search-form').forEach(form => {
        form.classList.remove('active');
    });
    document.getElementById(`${mode}-search`).classList.add('active');
}

// Toggle location type
function toggleLocation() {
    const locationType = document.querySelector('input[name="location-type"]:checked').value;

    if (locationType === 'city') {
        document.getElementById('city-group').style.display = 'block';
        document.getElementById('zipcode-group').style.display = 'none';
    } else {
        document.getElementById('city-group').style.display = 'none';
        document.getElementById('zipcode-group').style.display = 'block';
    }
}

// Select model
function selectModel(type, model) {
    if (type === 'name') {
        selectedModelName = model;
        document.getElementById(`${model}-name`).checked = true;
    } else {
        selectedModelPref = model;
        document.getElementById(`${model}-pref`).checked = true;
    }
}

// Update range value display
function updateRangeValue(input) {
    const valueSpan = input.nextElementSibling;
    valueSpan.textContent = input.value;
}

// Scroll to search
function scrollToSearch() {
    document.getElementById('search').scrollIntoView({ behavior: 'smooth' });
}

// Show demo
function showDemo() {
    alert('Demo video coming soon! For now, try searching for a school or describing your preferences.');
}

// Search by school name
async function searchByName() {
    const schoolName = document.getElementById('school-name').value.trim();

    if (!schoolName) {
        alert('Please enter a school name');
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'flex';

    try {
        const response = await fetch(`${API_URL}/api/recommend/by-name`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                school_name: schoolName,
                model: selectedModelName
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to get recommendations');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

// Search by preferences
async function searchByPreferences() {
    const locationType = document.querySelector('input[name="location-type"]:checked').value;

    const preferences = {
        location_type: locationType,
        city: locationType === 'city' ? document.getElementById('city').value : null,
        zipcode: locationType === 'zipcode' ? document.getElementById('zipcode').value : null,
        elementary: document.getElementById('elementary').checked ? 1 : 0,
        intermediate: document.getElementById('intermediate').checked ? 1 : 0,
        middle: document.getElementById('middle').checked ? 1 : 0,
        high: document.getElementById('high').checked ? 1 : 0,
        school_grade: parseInt(document.getElementById('school-grade').value),
        proficiency: parseInt(document.getElementById('proficiency').value),
        graduation_rate: parseInt(document.getElementById('graduation-rate').value),
        model: selectedModelPref,
        // Default values for other fields
        title_i: 0,
        total_students: 1,
        race: 0,
        race_percentage: 1,
        dropout_rate: 0,
        ccri_points: 1,
        promotion_rate: 1,
        ap_courses: 1,
        chronic_absenteeism: 0,
        crime_rate: 0,
        bullying: 0,
        expenditure: 1,
        sel_protection: 1,
        respect_individuals: 1,
        discipline_support: 1,
        appropriate_content: 1,
        no_explicit_content: 1
    };

    // Show loading
    document.getElementById('loading').style.display = 'flex';

    try {
        const response = await fetch(`${API_URL}/api/recommend/by-preferences`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(preferences)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to get recommendations');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

// Display results
function displayResults(data) {
    const resultsContainer = document.getElementById('results-container');
    const resultsSection = document.getElementById('results');

    resultsContainer.innerHTML = '';

    if (!data.recommendations || data.recommendations.length === 0) {
        resultsContainer.innerHTML = '<p>No recommendations found. Please try different criteria.</p>';
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        return;
    }

    data.recommendations.forEach((school, index) => {
        const card = createResultCard(school, index + 1);
        resultsContainer.appendChild(card);
    });

    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Create result card
function createResultCard(school, rank) {
    const card = document.createElement('div');
    card.className = 'result-card';

    // Extract key information
    const schoolName = school.School_name || school['School_name '] || 'Unknown School';
    const city = school.city || school['city '] || 'N/A';
    const zipcode = school.zipcode || 'N/A';
    const totalStudents = school.total_students || 'N/A';
    const schoolGrade = school.School_grade || 'N/A';

    card.innerHTML = `
        <div class="result-header">
            <div class="result-rank">${rank}</div>
            <div class="result-title">
                <h3>${schoolName}</h3>
                <div class="result-location">${city}, ${zipcode}</div>
            </div>
        </div>
        <div class="result-details">
            <div class="detail-item">
                <div class="detail-label">Total Students</div>
                <div class="detail-value">${formatNumber(totalStudents)}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">School Grade</div>
                <div class="detail-value">${schoolGrade}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">City</div>
                <div class="detail-value">${city}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Zipcode</div>
                <div class="detail-value">${zipcode}</div>
            </div>
        </div>
    `;

    return card;
}

// Format number
function formatNumber(num) {
    if (typeof num === 'number') {
        return num.toLocaleString();
    }
    return num;
}
