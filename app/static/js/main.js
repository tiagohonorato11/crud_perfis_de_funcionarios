// Estado Global
let currentUser = null;

// Elementos
const loginScreen = document.getElementById('login-screen');
const dashboardScreen = document.getElementById('dashboard-screen');
const loginForm = document.getElementById('login-form');
const logoutBtn = document.getElementById('logout-btn');
const employeesList = document.getElementById('employees-list');
const modal = document.getElementById('modal');
const addBtn = document.getElementById('add-btn');
const closeBtn = document.querySelector('.close-modal');
const employeeForm = document.getElementById('employee-form');
const searchDept = document.getElementById('search-dept');
const searchName = document.getElementById('search-name');

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        showDashboard();
    }
});

// Eventos
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    
    try {
        const data = await login(user, pass);
        localStorage.setItem('token', data.access_token);
        showDashboard();
    } catch (err) {
        document.getElementById('login-error').innerText = "Credenciais inválidas.";
    }
});

logoutBtn.addEventListener('click', logout);

addBtn.addEventListener('click', () => openModal());
closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

employeeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('emp-id').value;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/funcionarios/${id}` : '/funcionarios/';
    
    const payload = {
        nome: document.getElementById('emp-nome').value,
        sobrenome: document.getElementById('emp-sobrenome').value,
        usuario: document.getElementById('emp-usuario').value,
        email: document.getElementById('emp-email').value,
        departamento: document.getElementById('emp-dept').value,
        cargo: document.getElementById('emp-cargo').value,
        celular: document.getElementById('emp-celular').value,
        foto_url: document.getElementById('emp-foto-url').value
    };

    const senha = document.getElementById('emp-senha').value;
    if (senha) payload.senha = senha;
    else if (!id) return alert("Senha é obrigatória para novos usuários");

    try {
        const res = await def_request(url, method, payload);
        if (res.ok) {
            modal.classList.add('hidden');
            loadEmployees();
        } else {
            const err = await res.json();
            alert(err.detail || "Erro ao salvar");
        }
    } catch (e) { console.error(e); }
});

searchDept.addEventListener('input', () => loadEmployees());
searchName.addEventListener('input', () => loadEmployees());

// Máscara Celular
const celularInput = document.getElementById('emp-celular');
celularInput.addEventListener('input', (e) => {
    let x = e.target.value.replace(/\D/g, '').match(/(\d{0,2})(\d{0,1})(\d{0,4})(\d{0,4})/);
    e.target.value = !x[2] ? x[1] : '(' + x[1] + ')' + x[2] + (x[3] ? '.' + x[3] : '') + (x[4] ? '-' + x[4] : '');
});

// Upload de Foto
const photoInput = document.getElementById('emp-foto-input');
photoInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        if(response.ok) {
            const data = await response.json();
            document.getElementById('emp-foto-url').value = data.url;
            document.getElementById('emp-foto-preview').src = data.url;
        } else {
            alert("Erro ao fazer upload da imagem");
        }
    } catch(err) {
        console.error("Erro upload", err);
    }
});

// Zoom Foto Logic
const zoomModal = document.getElementById('zoom-modal');
const zoomImg = document.getElementById('zoom-img');
const closeZoom = document.querySelector('.close-zoom');
const viewPhotoBtn = document.getElementById('view-photo-btn');
const imgPreview = document.getElementById('emp-foto-preview');

viewPhotoBtn.addEventListener('click', (e) => {
    e.preventDefault();
    if (imgPreview.src) {
        zoomImg.src = imgPreview.src;
        zoomModal.classList.remove('hidden');
    }
});

closeZoom.addEventListener('click', () => {
    zoomModal.classList.add('hidden');
});

// Fecha modal de zoom se clicar fora da imagem
zoomModal.addEventListener('click', (e) => {
    if (e.target === zoomModal) {
        zoomModal.classList.add('hidden');
    }
});


// Funções UI
async function showDashboard() {
    loginScreen.classList.add('hidden');
    dashboardScreen.classList.remove('hidden');
    
    // Obter dados do usuário logado via JWT decode (simplificado)
    const token = localStorage.getItem('token');
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        document.getElementById('user-display').innerText = `${payload.sub} (${payload.cargo})`;
        
        // Recupera aba ativa ou "home"
        const lastTab = localStorage.getItem('activeTab') || 'home';
        switchTab(lastTab);
    } catch(e) { logout(); }
}

async function loadEmployees() {
    const deptFilter = searchDept ? searchDept.value : '';
    const nameFilter = searchName ? searchName.value : '';
    
    let url = '/funcionarios/';
    const params = new URLSearchParams();
    if (deptFilter) params.append('departamento', deptFilter);
    if (nameFilter) params.append('nome', nameFilter);
    
    const queryString = params.toString();
    if (queryString) url += `?${queryString}`;
    
    try {
        const res = await def_request(url);
        if (!res.ok) throw new Error();
        const users = await res.json();
        renderTable(users);
    } catch (e) {
        console.log("Erro ao carregar lista ou acesso negado");
    }
}

function renderTable(users) {
    employeesList.innerHTML = users.map(u => `
        <tr>
            <td>
                <img src="${u.foto_url || '/static/img/default-user.png'}" class="user-avatar-table" alt="Foto">
            </td>
            <td>${u.id}</td>
            <td>${u.nome} ${u.sobrenome}</td>
            <td>${u.usuario}</td>
            <td>${u.celular || '-'}</td>
            <td>${u.email}</td>
            <td>${u.departamento}</td>
            <td><span class="badge ${u.cargo}">${u.cargo}</span></td>
            <td>
                <button class="btn-secondary" onclick="editUser(${u.id})">Editar</button>
                <button class="btn-danger" onclick="deleteUser(${u.id})">Exc</button>
            </td>
        </tr>
    `).join('');
}

// Helpers Globais para onclick no HTML
window.editUser = async (id) => {
    const res = await def_request(`/funcionarios/${id}`);
    const u = await res.json();
    openModal(u);
};

window.deleteUser = async (id) => {
    if(!confirm("Tem certeza?")) return;
    await def_request(`/funcionarios/${id}`, 'DELETE');
    loadEmployees();
};

// Navegação
window.switchTab = (tab) => {
    // Esconde todas as tabs
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));

    // Mostra a selecionada
    document.getElementById(`tab-${tab}`).classList.remove('hidden');
    document.getElementById(`link-${tab}`).classList.add('active');
    
    // Salva no cache
    localStorage.setItem('activeTab', tab);

    if (tab === 'users') {
        loadEmployees();
    }
};

function openModal(user = null) {

    modal.classList.remove('hidden');
    document.getElementById('modal-title').innerText = user ? "Editar Funcionário" : "Novo Funcionário";
    document.getElementById('emp-id').value = user ? user.id : '';
    document.getElementById('emp-nome').value = user ? user.nome : '';
    document.getElementById('emp-sobrenome').value = user ? user.sobrenome : '';
    document.getElementById('emp-usuario').value = user ? user.usuario : '';
    document.getElementById('emp-email').value = user ? user.email : '';
    document.getElementById('emp-dept').value = user ? user.departamento : '';
    document.getElementById('emp-cargo').value = user ? user.cargo : 'funcionario';
    
    // Novos campos
    document.getElementById('emp-celular').value = user ? (user.celular || '') : '';
    document.getElementById('emp-foto-url').value = user ? (user.foto_url || '') : '';
    document.getElementById('emp-foto-preview').src = user && user.foto_url ? user.foto_url : '/static/img/default-user.png';
    document.getElementById('emp-foto-input').value = '';

    document.getElementById('emp-senha').value = '';
}
