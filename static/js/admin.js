/**
 * Admin panel — FAQ CRUD operations and dataset upload.
 */

// ─── Load FAQs ────────────────────────────────────────────

async function loadFaqs() {
    try {
        const res = await fetch('/api/admin/faqs');
        const data = await res.json();
        const tbody = document.getElementById('faqTableBody');

        if (!data.faqs || data.faqs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No FAQs found. Add one!</td></tr>';
            return;
        }

        tbody.innerHTML = data.faqs.map(faq => `
            <tr>
                <td>${faq.id}</td>
                <td><span class="badge badge-primary">${faq.category}</span></td>
                <td>${truncate(faq.question_en, 60)}</td>
                <td>${truncate(faq.answer_en, 80)}</td>
                <td><span class="badge ${faq.is_active ? 'badge-success' : 'badge-warning'}">${faq.is_active ? 'Active' : 'Inactive'}</span></td>
                <td class="actions">
                    <button class="btn btn-secondary" style="padding:6px 12px; font-size:12px;" onclick='editFaq(${JSON.stringify(faq)})'>Edit</button>
                    <button class="btn btn-danger" style="padding:6px 12px; font-size:12px;" onclick="deleteFaq(${faq.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        console.error('Failed to load FAQs:', err);
    }
}

function truncate(str, len) {
    if (!str) return '';
    return str.length > len ? str.substring(0, len) + '...' : str;
}

// ─── Modal Operations ─────────────────────────────────────

function openAddModal() {
    document.getElementById('modalTitle').textContent = 'Add New FAQ';
    document.getElementById('editFaqId').value = '';
    document.getElementById('faqCategory').value = 'general';
    document.getElementById('faqQuestionEn').value = '';
    document.getElementById('faqQuestionHi').value = '';
    document.getElementById('faqQuestionMr').value = '';
    document.getElementById('faqAnswerEn').value = '';
    document.getElementById('faqAnswerHi').value = '';
    document.getElementById('faqAnswerMr').value = '';
    document.getElementById('faqModal').classList.add('active');
}

function editFaq(faq) {
    document.getElementById('modalTitle').textContent = 'Edit FAQ';
    document.getElementById('editFaqId').value = faq.id;
    document.getElementById('faqCategory').value = faq.category || 'general';
    document.getElementById('faqQuestionEn').value = faq.question_en || '';
    document.getElementById('faqQuestionHi').value = faq.question_hi || '';
    document.getElementById('faqQuestionMr').value = faq.question_mr || '';
    document.getElementById('faqAnswerEn').value = faq.answer_en || '';
    document.getElementById('faqAnswerHi').value = faq.answer_hi || '';
    document.getElementById('faqAnswerMr').value = faq.answer_mr || '';
    document.getElementById('faqModal').classList.add('active');
}

function closeModal() {
    document.getElementById('faqModal').classList.remove('active');
}

// ─── Save FAQ (Add or Update) ─────────────────────────────

async function saveFaq() {
    const faqId = document.getElementById('editFaqId').value;
    const payload = {
        category: document.getElementById('faqCategory').value,
        question_en: document.getElementById('faqQuestionEn').value,
        question_hi: document.getElementById('faqQuestionHi').value,
        question_mr: document.getElementById('faqQuestionMr').value,
        answer_en: document.getElementById('faqAnswerEn').value,
        answer_hi: document.getElementById('faqAnswerHi').value,
        answer_mr: document.getElementById('faqAnswerMr').value
    };

    if (!payload.question_en || !payload.answer_en) {
        alert('English question and answer are required.');
        return;
    }

    try {
        const url = faqId ? `/api/admin/faqs/${faqId}` : '/api/admin/faqs';
        const method = faqId ? 'PUT' : 'POST';

        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.success) {
            closeModal();
            loadFaqs();
        } else {
            alert('Failed to save FAQ.');
        }
    } catch (err) {
        console.error('Save FAQ error:', err);
        alert('Error saving FAQ.');
    }
}

// ─── Delete FAQ ───────────────────────────────────────────

async function deleteFaq(id) {
    if (!confirm('Are you sure you want to delete this FAQ?')) return;

    try {
        const res = await fetch(`/api/admin/faqs/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) loadFaqs();
    } catch (err) {
        console.error('Delete error:', err);
    }
}

// ─── Upload Dataset ───────────────────────────────────────

async function uploadDataset(input) {
    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch('/api/admin/upload-dataset', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (data.success) {
            alert('Dataset uploaded successfully!');
            loadFaqs();
        } else {
            alert('Upload failed: ' + (data.error || 'Unknown error'));
        }
    } catch (err) {
        alert('Upload error.');
        console.error(err);
    }

    input.value = '';
}

// ─── Initial Load ─────────────────────────────────────────
loadFaqs();
