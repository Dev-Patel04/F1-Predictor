// F1 Predictor - App JavaScript

// 2026 Season - Next Race Prediction
const nextRace = {
    round: 1,
    name: "Australian Grand Prix",
    date: "March 8, 2026",
    circuit: "Albert Park Circuit, Melbourne",
    predictions: [
        {
            pos: 1, driver: "VER", fullName: "Max Verstappen", team: "Red Bull Racing", prob: 35.2,
            reasoning: {
                summary: "Dominant recent form and exceptional track record",
                factors: [
                    { label: "Recent Win Rate", value: "68%", impact: "high" },
                    { label: "Australian GP Wins", value: "2 (2023, 2025)", impact: "high" },
                    { label: "Qualifying Avg", value: "P1.3", impact: "high" },
                    { label: "2025 Championship", value: "1st", impact: "medium" }
                ]
            }
        },
        {
            pos: 2, driver: "NOR", fullName: "Lando Norris", team: "McLaren", prob: 24.8,
            reasoning: {
                summary: "Strong 2024-2025 form with competitive McLaren",
                factors: [
                    { label: "Recent Win Rate", value: "28%", impact: "high" },
                    { label: "2025 Championship", value: "2nd", impact: "high" },
                    { label: "Qualifying Avg", value: "P2.4", impact: "medium" },
                    { label: "Podium Rate", value: "72%", impact: "medium" }
                ]
            }
        },
        {
            pos: 3, driver: "LEC", fullName: "Charles Leclerc", team: "Ferrari", prob: 15.3,
            reasoning: {
                summary: "Ferrari pace improvement and Australian GP experience",
                factors: [
                    { label: "Australian GP Win", value: "2022", impact: "medium" },
                    { label: "Qualifying Avg", value: "P2.8", impact: "medium" },
                    { label: "Ferrari 2025 Form", value: "Strong", impact: "medium" },
                    { label: "Podium Rate", value: "58%", impact: "medium" }
                ]
            }
        },
        {
            pos: 4, driver: "HAM", fullName: "Lewis Hamilton", team: "Ferrari", prob: 10.1,
            reasoning: {
                summary: "7x champion adapting to Ferrari machinery",
                factors: [
                    { label: "Career Wins", value: "104", impact: "high" },
                    { label: "Australian GP Wins", value: "3", impact: "medium" },
                    { label: "New Team", value: "Ferrari (2025)", impact: "low" },
                    { label: "Experience Factor", value: "Elite", impact: "medium" }
                ]
            }
        },
        {
            pos: 5, driver: "PIA", fullName: "Oscar Piastri", team: "McLaren", prob: 7.2,
            reasoning: {
                summary: "Home race advantage and rising star momentum",
                factors: [
                    { label: "Home Race", value: "Australia 🇦🇺", impact: "high" },
                    { label: "2024 Wins", value: "2", impact: "medium" },
                    { label: "Team Support", value: "McLaren", impact: "medium" },
                    { label: "Podium Rate", value: "45%", impact: "medium" }
                ]
            }
        },
        {
            pos: 6, driver: "RUS", fullName: "George Russell", team: "Mercedes", prob: 3.5,
            reasoning: {
                summary: "Consistent performer seeking Mercedes resurgence",
                factors: [
                    { label: "2025 Wins", value: "1", impact: "medium" },
                    { label: "Qualifying Avg", value: "P4.2", impact: "medium" },
                    { label: "Consistency", value: "High", impact: "medium" },
                    { label: "Mercedes Form", value: "Improving", impact: "low" }
                ]
            }
        },
        {
            pos: 7, driver: "SAI", fullName: "Carlos Sainz", team: "Williams", prob: 1.8,
            reasoning: {
                summary: "2024 Australian GP winner but new team adjustment",
                factors: [
                    { label: "2024 Aus GP Win", value: "Winner", impact: "high" },
                    { label: "New Team", value: "Williams (2025)", impact: "low" },
                    { label: "Experience", value: "High", impact: "medium" },
                    { label: "Team Competitiveness", value: "Midfield", impact: "low" }
                ]
            }
        },
        {
            pos: 8, driver: "ALO", fullName: "Fernando Alonso", team: "Aston Martin", prob: 1.2,
            reasoning: {
                summary: "Veteran experience but Aston Martin pace limited",
                factors: [
                    { label: "Career Wins", value: "32", impact: "medium" },
                    { label: "Experience", value: "Elite", impact: "medium" },
                    { label: "Team Form", value: "Midfield", impact: "low" },
                    { label: "Qualifying Avg", value: "P6.5", impact: "low" }
                ]
            }
        },
        {
            pos: 9, driver: "ANT", fullName: "Kimi Antonelli", team: "Mercedes", prob: 0.5,
            reasoning: {
                summary: "Talented rookie with potential but limited experience",
                factors: [
                    { label: "Rookie Season", value: "2025", impact: "low" },
                    { label: "F2 Champion", value: "2024", impact: "medium" },
                    { label: "Mercedes Seat", value: "Factory", impact: "medium" },
                    { label: "Race Experience", value: "Limited", impact: "low" }
                ]
            }
        },
        {
            pos: 10, driver: "LAW", fullName: "Liam Lawson", team: "Red Bull Racing", prob: 0.4,
            reasoning: {
                summary: "Promoted to top team but proving phase",
                factors: [
                    { label: "Red Bull Seat", value: "2025", impact: "medium" },
                    { label: "2024 Performances", value: "Promising", impact: "medium" },
                    { label: "Experience", value: "Limited", impact: "low" },
                    { label: "Team Support", value: "Red Bull", impact: "medium" }
                ]
            }
        }
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

        const teamColor = teamColors[pred.team] || '#ffffff';

        // Build factors HTML
        let factorsHTML = '';
        if (pred.reasoning && pred.reasoning.factors) {
            pred.reasoning.factors.forEach(factor => {
                const impactClass = `impact-${factor.impact}`;
                factorsHTML += `
                    <div class="factor-item ${impactClass}">
                        <span class="factor-label">${factor.label}</span>
                        <span class="factor-value">${factor.value}</span>
                    </div>
                `;
            });
        }

        const card = document.createElement('div');
        card.className = `prediction-card ${podiumClass}`;
        card.innerHTML = `
            <div class="card-main" style="border-left: 4px solid ${teamColor}">
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
                <div class="expand-icon">▼</div>
            </div>
            <div class="reasoning-panel" style="display: none;">
                <div class="reasoning-header">
                    <span class="reasoning-title">Why this prediction?</span>
                </div>
                <p class="reasoning-summary">${pred.reasoning ? pred.reasoning.summary : 'Based on historical performance data'}</p>
                <div class="factors-grid">
                    ${factorsHTML}
                </div>
            </div>
        `;

        // Add click handler
        const cardMain = card.querySelector('.card-main');
        const reasoningPanel = card.querySelector('.reasoning-panel');
        const expandIcon = card.querySelector('.expand-icon');

        cardMain.addEventListener('click', () => {
            const isExpanded = reasoningPanel.style.display !== 'none';

            // Close all other panels first
            document.querySelectorAll('.reasoning-panel').forEach(panel => {
                panel.style.display = 'none';
            });
            document.querySelectorAll('.expand-icon').forEach(icon => {
                icon.textContent = '▼';
                icon.classList.remove('expanded');
            });
            document.querySelectorAll('.prediction-card').forEach(c => {
                c.classList.remove('expanded');
            });

            // Toggle current panel
            if (!isExpanded) {
                reasoningPanel.style.display = 'block';
                expandIcon.textContent = '▲';
                expandIcon.classList.add('expanded');
                card.classList.add('expanded');
            }
        });

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
