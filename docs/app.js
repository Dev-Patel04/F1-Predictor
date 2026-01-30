// F1 Predictor - App JavaScript

// 2026 Season - Next Race Prediction
const nextRace = {
    round: 1,
    name: "Bahrain Grand Prix",
    date: "March 2, 2026",
    circuit: "Bahrain International Circuit",
    predictions: [
        { pos: 1, driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing", prob: 38.5 },
        { pos: 2, driver: "NOR", fullName: "Lando Norris", team: "McLaren", prob: 22.3 },
        { pos: 3, driver: "LEC", fullName: "Charles Leclerc", team: "Ferrari", prob: 14.8 },
        { pos: 4, driver: "HAM", fullName: "Lewis Hamilton", team: "Ferrari", prob: 9.2 },
        { pos: 5, driver: "PIA", fullName: "Oscar Piastri", team: "McLaren", prob: 6.4 },
        { pos: 6, driver: "SAI", fullName: "Carlos Sainz", team: "Williams", prob: 3.8 },
        { pos: 7, driver: "RUS", fullName: "George Russell", team: "Mercedes", prob: 2.5 },
        { pos: 8, driver: "PER", fullName: "Sergio Perez", team: "Red Bull Racing", prob: 1.4 },
        { pos: 9, driver: "ALO", fullName: "Fernando Alonso", team: "Aston Martin", prob: 0.7 },
        { pos: 10, driver: "STR", fullName: "Lance Stroll", team: "Aston Martin", prob: 0.4 }
    ]
};

// Historical race winners 2022-2025
const historicalWinners = {
    "Bahrain Grand Prix": {
        2022: { driver: "LEC", fullName: "Charles Leclerc", team: "Ferrari" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Saudi Arabian Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "PER", fullName: "Sergio Perez", team: "Red Bull Racing" },
        2024: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Australian Grand Prix": {
        2022: { driver: "LEC", fullName: "Charles Leclerc", team: "Ferrari" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "SAI", fullName: "Carlos Sainz", team: "Ferrari" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Japanese Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Chinese Grand Prix": {
        2022: null,
        2023: null,
        2024: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Miami Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "PER", fullName: "Sergio Perez", team: "Red Bull Racing" },
        2024: { driver: "NOR", fullName: "Lando Norris", team: "McLaren" },
        2025: { driver: "NOR", fullName: "Lando Norris", team: "McLaren" }
    },
    "Emilia Romagna Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2025: null
    },
    "Monaco Grand Prix": {
        2022: { driver: "PER", fullName: "Sergio Perez", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "LEC", fullName: "Charles Leclerc", team: "Ferrari" },
        2025: { driver: "LEC", fullName: "Charles Leclerc", team: "Ferrari" }
    },
    "Spanish Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Canadian Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Austrian Grand Prix": {
        2022: { driver: "LEC", fullName: "Charles Leclerc", team: "Ferrari" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "RUS", fullName: "George Russell", team: "Mercedes" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "British Grand Prix": {
        2022: { driver: "SAI", fullName: "Carlos Sainz", team: "Ferrari" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "HAM", fullName: "Lewis Hamilton", team: "Mercedes" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Hungarian Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "PIA", fullName: "Oscar Piastri", team: "McLaren" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Belgian Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "HAM", fullName: "Lewis Hamilton", team: "Mercedes" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Dutch Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "NOR", fullName: "Lando Norris", team: "McLaren" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Italian Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "LEC", fullName: "Charles Leclerc", team: "Ferrari" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Singapore Grand Prix": {
        2022: { driver: "PER", fullName: "Sergio Perez", team: "Red Bull Racing" },
        2023: { driver: "SAI", fullName: "Carlos Sainz", team: "Ferrari" },
        2024: { driver: "NOR", fullName: "Lando Norris", team: "McLaren" },
        2025: { driver: "NOR", fullName: "Lando Norris", team: "McLaren" }
    },
    "United States Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "LEC", fullName: "Charles Leclerc", team: "Ferrari" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Mexico City Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "SAI", fullName: "Carlos Sainz", team: "Ferrari" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "São Paulo Grand Prix": {
        2022: { driver: "RUS", fullName: "George Russell", team: "Mercedes" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Las Vegas Grand Prix": {
        2022: null,
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "RUS", fullName: "George Russell", team: "Mercedes" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Qatar Grand Prix": {
        2022: null,
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    },
    "Abu Dhabi Grand Prix": {
        2022: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2023: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" },
        2024: { driver: "NOR", fullName: "Lando Norris", team: "McLaren" },
        2025: { driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing" }
    }
};

// Team colors for styling
const teamColors = {
    "Red Bull Racing": "#3671C6",
    "Ferrari": "#E8002D",
    "McLaren": "#FF8000",
    "Mercedes": "#27F4D2",
    "Aston Martin": "#229971",
    "Alpine": "#FF87BC",
    "Williams": "#64C4FF",
    "RB": "#6692FF",
    "Sauber": "#52E252",
    "Haas F1 Team": "#B6BABD"
};

// Initialize
function init() {
    renderPredictions();
    renderHistoricalWinners();
    setupNavigation();
    animateBars();
}

function renderPredictions() {
    const grid = document.querySelector('.predictions-grid');
    if (!grid) return;

    grid.innerHTML = '';

    nextRace.predictions.forEach((pred, index) => {
        const podiumClass = index === 0 ? 'podium gold' :
            index === 1 ? 'podium silver' :
                index === 2 ? 'podium bronze' : '';

        const card = document.createElement('div');
        card.className = `prediction-card ${podiumClass}`;
        card.innerHTML = `
            <div class="position">${pred.pos}</div>
            <div class="driver-info">
                <span class="driver-name">${pred.driver}</span>
                <span class="driver-fullname">${pred.fullName}</span>
                <span class="team">${pred.team}</span>
            </div>
            <div class="probability">
                <span class="prob-value">${pred.prob.toFixed(1)}%</span>
                <div class="prob-bar">
                    <div class="prob-fill" style="width: 0%"></div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderHistoricalWinners() {
    const container = document.querySelector('.history-grid');
    if (!container) return;

    container.innerHTML = '';

    const years = [2022, 2023, 2024, 2025];

    Object.entries(historicalWinners).forEach(([raceName, winners]) => {
        const card = document.createElement('div');
        card.className = 'history-card';

        let winnersHTML = '';
        years.forEach(year => {
            const winner = winners[year];
            if (winner) {
                const teamColor = teamColors[winner.team] || '#ffffff';
                winnersHTML += `
                    <div class="year-winner">
                        <span class="year">${year}</span>
                        <span class="winner-driver" style="border-left: 3px solid ${teamColor}">
                            ${winner.driver}
                        </span>
                    </div>
                `;
            } else {
                winnersHTML += `
                    <div class="year-winner">
                        <span class="year">${year}</span>
                        <span class="winner-driver no-race">—</span>
                    </div>
                `;
            }
        });

        card.innerHTML = `
            <h4 class="race-title">${raceName}</h4>
            <div class="winners-list">
                ${winnersHTML}
            </div>
        `;

        container.appendChild(card);
    });
}

function setupNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });

                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });
}

function animateBars() {
    setTimeout(() => {
        document.querySelectorAll('.prob-fill').forEach(bar => {
            const parent = bar.closest('.probability');
            if (parent) {
                const value = parent.querySelector('.prob-value');
                if (value) {
                    bar.style.width = value.textContent;
                }
            }
        });
    }, 300);
}

document.addEventListener('DOMContentLoaded', init);
