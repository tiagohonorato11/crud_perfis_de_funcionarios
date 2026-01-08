const API_URL = "";

async function def_request(endpoint, method = 'GET', body = null) {

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const config = { method, headers };
    if (body) config.body = JSON.stringify(body);

    const response = await fetch(endpoint, config);
    if (response.status === 401) {
        logout();
        throw new Error("Não autorizado");
    }
    return response;
}

async function login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
    });
    
    if (!response.ok) throw new Error('Falha no login');
    return await response.json();
}

function logout() {
    localStorage.removeItem('token');
    window.location.reload();
}
