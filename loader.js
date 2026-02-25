// Musica Maze & Terminal Demo

// 1. Maze Background Animation (Canvas)
const canvas = document.createElement('canvas');
canvas.id = 'maze-bg';
canvas.style.position = 'fixed';
canvas.style.top = '0';
canvas.style.left = '0';
canvas.style.width = '100vw';
canvas.style.height = '100vh';
canvas.style.zIndex = '-1';
canvas.style.opacity = '0.05';
canvas.style.pointerEvents = 'none';
document.body.appendChild(canvas);

const ctx = canvas.getContext('2d');
let width, height;

function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}

window.addEventListener('resize', resize);
resize();

const cellSize = 40;

function drawMaze() {
    const cols = Math.ceil(width / cellSize);
    const rows = Math.ceil(height / cellSize);

    ctx.strokeStyle = '#b0fb50';
    ctx.lineWidth = 1;
    ctx.clearRect(0, 0, width, height);

    for (let x = 0; x < cols; x++) {
        for (let y = 0; y < rows; y++) {
            const px = x * cellSize;
            const py = y * cellSize;

            ctx.beginPath();
            if (Math.random() > 0.5) {
                ctx.moveTo(px, py);
                ctx.lineTo(px + cellSize, py + cellSize);
            } else {
                ctx.moveTo(px + cellSize, py);
                ctx.lineTo(px, py + cellSize);
            }
            ctx.stroke();
        }
    }
}

// Redraw maze every 2 seconds for a "regenerating" effect
setInterval(drawMaze, 2000);
drawMaze();


// 2. TUI Interaction Demo
const tracks = [
    "iann dior - is it you",
    "wasted-fast.mp3",
    "juice wrld - lucid dreams",
    "post malone - rockstar",
    "the weeknd - blinding lights"
];

const hints = "[SPACE] Play/Pause  [ENTER] Select  [S] Scan  [Q] Quit";

async function runDemo() {
    const terminalBody = document.querySelector('.terminal-body');
    if (!terminalBody) return;

    await new Promise(r => setTimeout(r, 1000));

    let currentIndex = 0;

    const updateTerminal = () => {
        let html = `<p style="color: #555; margin-bottom: 1rem;">Scanning library... 142 tracks found.</p>`;
        tracks.forEach((track, index) => {
            const isSelected = index === currentIndex;
            const prefix = isSelected ? `<span style="color: #b0fb50">> </span>` : `  `;
            const style = isSelected ? `color: #fff; background: rgba(176, 251, 80, 0.1);` : `color: #777;`;
            html += `<p style="${style} padding: 2px 5px;">${prefix}${track}</p>`;
        });
        html += `<div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #222; color: #b0fb50; font-size: 0.8rem; letter-spacing: 1px;">${hints}</div>`;
        terminalBody.innerHTML = html;
    };

    // Simulate navigation
    for (let i = 0; i < 6; i++) {
        updateTerminal();
        await new Promise(r => setTimeout(r, 1500));
        currentIndex = (currentIndex + 1) % tracks.length;
    }

    // Loop demo
    setTimeout(runDemo, 1000);
}

document.addEventListener('DOMContentLoaded', runDemo);