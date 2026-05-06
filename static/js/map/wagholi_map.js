/**
 * JSPM Wagholi Campus Interactive Map — Leaflet.js
 * Markers loaded dynamically from /api/campus-markers
 * GAT No. 720, JSPM Road, Wagholi, Pune - 412207
 */

const CAMPUS_CENTER = [18.5858, 74.0028];
const ZOOM_LEVEL = 17;

const map = L.map('campusMap').setView(CAMPUS_CENTER, ZOOM_LEVEL);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap | JSPM Wagholi Campus'
}).addTo(map);

// ─── Icons ────────────────────────────────────────────────

function createIcon(color, emoji) {
    return L.divIcon({
        className: 'custom-marker',
        html: `<div style="
            width: 34px; height: 34px;
            background: ${color};
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 16px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
            border: 3px solid white;
        ">${emoji}</div>`,
        iconSize: [34, 34],
        iconAnchor: [17, 17],
        popupAnchor: [0, -20]
    });
}

const icons = {
    academic:  createIcon('#5B7FD6', '&#127979;'),
    hostel:    createIcon('#E8889A', '&#127968;'),
    pg:        createIcon('#D97706', '&#128209;'),
    amenity:   createIcon('#5EBD8A', '&#9749;'),
    sports:    createIcon('#E4C35A', '&#9917;'),
    admin:     createIcon('#E27070', '&#127970;'),
    food:      createIcon('#F59E0B', '&#127836;'),
    transport: createIcon('#8B5CF6', '&#128652;'),
    school:    createIcon('#6B7280', '&#127891;')
};

// ─── Campus Boundary ──────────────────────────────────────

L.polygon([
    [18.5870, 73.9998],
    [18.5870, 74.0045],
    [18.5845, 74.0055],
    [18.5840, 74.0055],
    [18.5840, 74.0010],
    [18.5845, 73.9998]
], {
    color: '#5B7FD6',
    weight: 2,
    fillColor: '#5B7FD6',
    fillOpacity: 0.06,
    dashArray: '8, 8'
}).addTo(map)
  .bindPopup('<h3>JSPM University — Wagholi Campus</h3><p>GAT No. 720, JSPM Road, Wagholi, Pune - 412207</p>');

// ─── Campus Label ─────────────────────────────────────────

L.marker(CAMPUS_CENTER, {
    icon: L.divIcon({
        className: 'campus-label',
        html: '<div style="background:rgba(91,127,214,0.9); color:white; padding:6px 14px; border-radius:8px; font-size:12px; font-weight:700; white-space:nowrap; box-shadow:0 2px 8px rgba(0,0,0,0.2);">JSPM University — Wagholi Campus</div>',
        iconSize: [240, 28],
        iconAnchor: [120, 14]
    })
}).addTo(map);

// ─── Load Markers from API ────────────────────────────────

fetch('/api/campus-markers')
    .then(r => r.json())
    .then(markers => {
        markers.forEach(m => {
            const icon = icons[m.type] || icons.academic;
            L.marker(m.coords, { icon })
                .addTo(map)
                .bindPopup(`<h3>${m.title}</h3><p>${m.desc}</p>`, {
                    maxWidth: 300,
                    className: 'campus-popup'
                });
        });
    })
    .catch(() => console.warn('Could not load campus markers.'));
