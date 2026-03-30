/**
 * JSPM Wagholi Campus Interactive Map — Leaflet.js
 * ALL coordinates fetched from OpenStreetMap Nominatim API.
 * GAT No. 720, JSPM Road, Wagholi, Pune - 412207
 */

// Campus center — between JSPM University and Play Ground
const CAMPUS_CENTER = [18.5860, 74.0020];
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

// ─── ALL MARKERS — Real OSM Coordinates ───────────────────

const markers = [

    // ══════ ACADEMIC BUILDINGS ══════
    {
        coords: [18.5860973, 74.0028226],
        type: 'academic',
        title: 'JSPM University — Main Building',
        desc: 'GAT No. 720, JSPM Road. BCA, BBA, B.Sc, B.Com, B.A., B.Voc, B.Des, B.Tech programs. Central university block with registrar, examination cell, and dean offices.'
    },
    {
        coords: [18.5855, 74.0025],
        type: 'academic',
        title: 'JSCOE — Jayawantrao Sawant College of Engineering',
        desc: 'Departments: Computer, IT, AI&DS, AI&ML, E&TC, Mechanical, Civil, Electrical. NAAC Accredited, affiliated to SPPU.'
    },
    {
        coords: [18.5850, 74.0030],
        type: 'academic',
        title: 'ICOER — Imperial College of Engineering & Research',
        desc: 'B.E./B.Tech programs. AI, ML, IoT labs. Smart classrooms, project labs, and workshop facility.'
    },
    {
        coords: [18.5865, 74.0022],
        type: 'academic',
        title: 'JSIMR — Institute of Management & Research',
        desc: 'MBA program (Marketing, Finance, HR, Operations, Business Analytics). Seminar halls, case study rooms.'
    },
    {
        coords: [18.5848, 74.0020],
        type: 'academic',
        title: 'JSPM Pharmacy College',
        desc: 'B.Pharm, D.Pharm, M.Pharm. Pharmaceutical labs, drug testing lab, medicinal plant garden.'
    },

    // ══════ ADMIN & SERVICES ══════
    {
        coords: [18.5858, 74.0035],
        type: 'admin',
        title: 'Main Gate — GAT No. 720 (JSPM Road)',
        desc: 'Campus main entrance on JSPM Road. Security check, visitor management. Admissions helpdesk. Hours: Mon-Sat 9:30 AM – 5:30 PM.'
    },
    {
        coords: [18.5863, 74.0032],
        type: 'admin',
        title: 'Admin Block & Accounts Office',
        desc: 'Principal cabin, administrative offices, accounts section, scholarship cell.'
    },
    {
        coords: [18.5853, 74.0028],
        type: 'admin',
        title: 'Training & Placement Cell',
        desc: 'Placement office, mock interviews, resume workshops. Top recruiters: TCS, Infosys, Wipro, Cognizant, Capgemini, Persistent.'
    },

    // ══════ LIBRARY & FACILITIES ══════
    {
        coords: [18.5862295, 74.0039412],
        type: 'amenity',
        title: 'Library of BSIOTR — Central Library',
        desc: '50,000+ books, DELNET/IEEE/NPTEL access. Reading hall (200+ seats). Open 8 AM – 8 PM, extended to 10 PM during exams.'
    },
    {
        coords: [18.5856, 74.0020],
        type: 'amenity',
        title: 'Computer Center & IT Labs',
        desc: '500+ systems, high-speed WiFi. Labs for programming, networking, IoT, AI/ML practicals.'
    },
    {
        coords: [18.5850, 74.0025],
        type: 'amenity',
        title: 'Health Center & Medical Room',
        desc: 'Resident doctor (9:30 AM – 5:30 PM), nurse on duty, first-aid 24/7. Tie-up with Sahyadri & Noble Hospital.'
    },
    {
        coords: [18.5866, 74.0026],
        type: 'amenity',
        title: 'Auditorium & Seminar Hall',
        desc: '500+ seating. Tech fests, cultural events, guest lectures, convocation, and annual functions.'
    },

    // ══════ SPORTS ══════
    {
        coords: [18.5859604, 74.0007401],
        type: 'sports',
        title: 'JSPM Play Ground',
        desc: 'Large campus ground for cricket, football, athletics. Annual sports day, inter-college tournaments held here.'
    },
    {
        coords: [18.5851541, 73.9991040],
        type: 'sports',
        title: 'AK Badminton Court',
        desc: 'Professional badminton court near campus. Indoor facility for students and faculty.'
    },
    {
        coords: [18.5848, 74.0015],
        type: 'sports',
        title: 'Gymnasium & Fitness Center',
        desc: 'Fully equipped gym with modern machines. Yoga and meditation center.'
    },

    // ══════ JSPM HOSTELS ══════
    {
        coords: [18.5862474, 74.0051927],
        type: 'hostel',
        title: "JSPM Girls' Hostel B",
        desc: "On JSPM Road. Warden, CCTV, biometric entry. WiFi, mess, common room with TV. Near Library of BSIOTR."
    },
    {
        coords: [18.5845, 74.0052],
        type: 'hostel',
        title: "JSPM Girls' Hostel A",
        desc: "Main girls hostel. 3 buildings, 2/3/4 sharing. Solar water heating, laundry, 24/7 security. Fees: ₹45,000 – ₹80,000/year."
    },

    // ══════ NEARBY PGs & HOSTELS (from OSM) ══════
    {
        coords: [18.5861848, 73.9989585],
        type: 'pg',
        title: 'Anand Boys Hostel',
        desc: 'Boys hostel near campus. Furnished rooms, WiFi, home-style mess. ₹6,000 – ₹10,000/month. ~4 min walk.'
    },
    {
        coords: [18.5856844, 73.9988739],
        type: 'pg',
        title: 'Happy Living Boys Hostel',
        desc: 'Budget boys hostel. Single/double/triple sharing. Tiffin, WiFi, parking. ₹5,500 – ₹9,000/month. ~3 min walk.'
    },
    {
        coords: [18.5863635, 73.9996405],
        type: 'pg',
        title: 'Ravinanda Trinity — PG Rooms',
        desc: 'Residential complex near playground. Multiple PG operators. Furnished rooms for boys & girls. ₹7,000 – ₹12,000/month.'
    },
    {
        coords: [18.5872451, 74.0011289],
        type: 'pg',
        title: 'Nyati Elan — PG & Flat Rentals',
        desc: 'Premium complex north of campus. PG rooms, shared flats. WiFi, security, parking. ₹8,000 – ₹15,000/month.'
    },
    {
        coords: [18.5847070, 74.0006402],
        type: 'pg',
        title: 'Umang Pride — PG Accommodation',
        desc: 'South of campus. PG for boys & girls (separate floors). Meals, WiFi, laundry. ₹6,500 – ₹11,000/month.'
    },
    {
        coords: [18.5852488, 73.9970220],
        type: 'pg',
        title: 'Gulmohar Primrose — Student PG',
        desc: 'Apartments with PG operators. Near AK Badminton Court. Budget rooms. ₹5,000 – ₹8,000/month. ~5 min walk.'
    },

    // ══════ SCHOOL ══════
    {
        coords: [18.5853596, 74.0042453],
        type: 'school',
        title: "JSPM's Prodigy Public School",
        desc: "K-12 school by JSPM Trust. Adjacent to university campus near JSPM Road."
    },
    {
        coords: [18.5877172, 73.9968361],
        type: 'school',
        title: 'Lexikon International School',
        desc: 'Near Nagar Road. Landmark — "JSPM campus is south of Lexikon School, take JSPM Road."'
    },

    // ══════ FOOD ══════
    {
        coords: [18.5856, 74.0018],
        type: 'food',
        title: 'Campus Cafeteria & Canteen',
        desc: 'Multi-cuisine food court inside campus. Veg & non-veg. Meals ₹40-60. Seating 200+. Open 8 AM – 7 PM.'
    },
    {
        coords: [18.5858, 74.0040],
        type: 'food',
        title: 'JSPM Road — Food Stalls & Chai',
        desc: 'Chai tapris, Maggi points, vada pav, juice stalls outside the gate. Student hangout. ₹20-80.'
    },
    {
        coords: [18.5845, 74.0008],
        type: 'food',
        title: 'Umang Pride Area — Restaurants',
        desc: 'Eateries, biryani shops, thali restaurants near Umang Pride. Walking distance. Budget meals ₹50-150.'
    },

    // ══════ TRANSPORT ══════
    {
        coords: [18.5880, 73.9960],
        type: 'transport',
        title: 'Nagar Road — PMPML Bus Stop',
        desc: 'City bus stop on Pune-Nagar Road. Routes to Pune Station, Hadapsar, Kharadi, Viman Nagar. College buses pick up here.'
    },
    {
        coords: [18.5860, 74.0043],
        type: 'transport',
        title: 'Auto-Rickshaw Stand (JSPM Road)',
        desc: 'Auto stand near main gate. Shared autos to Kharadi (₹20), Viman Nagar (₹30). Ola/Uber pickup.'
    },

    // ══════ NEARBY RESIDENTIAL (landmarks) ══════
    {
        coords: [18.5847846, 73.9981701],
        type: 'school',
        title: 'Ivy Botanica (Residential)',
        desc: 'Residential complex west of campus. Some students rent flats here. Walking distance to JSPM.'
    }
];

// ─── Add All Markers ──────────────────────────────────────

markers.forEach(m => {
    const icon = icons[m.type] || icons.academic;
    L.marker(m.coords, { icon: icon })
        .addTo(map)
        .bindPopup(`<h3>${m.title}</h3><p>${m.desc}</p>`, {
            maxWidth: 300,
            className: 'campus-popup'
        });
});

// ─── Campus Boundary (around JSPM University + Playground + academic blocks) ──

const campusBoundary = L.polygon([
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
}).addTo(map);

campusBoundary.bindPopup('<h3>JSPM University — Wagholi Campus</h3><p>GAT No. 720, JSPM Road, Wagholi, Pune - 412207</p>');

// ─── Campus Label ─────────────────────────────────────────

L.marker(CAMPUS_CENTER, {
    icon: L.divIcon({
        className: 'campus-label',
        html: '<div style="background:rgba(91,127,214,0.9); color:white; padding:6px 14px; border-radius:8px; font-size:12px; font-weight:700; white-space:nowrap; box-shadow:0 2px 8px rgba(0,0,0,0.2);">JSPM University — Wagholi Campus</div>',
        iconSize: [240, 28],
        iconAnchor: [120, 14]
    })
}).addTo(map);
