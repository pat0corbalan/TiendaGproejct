const productList = document.getElementById('productList');

// Sample data (replace with actual data from Flask)
const productos_destacados = [
    {
        nombre: 'Producto 1',
        descripcion: 'Descripción del producto 1',
        precio: 100,
        foto: 'producto1.jpg'
    },
    {
        nombre: 'Producto 2',
        descripcion: 'Descripción del producto 2',
        precio: 200,
        foto: 'producto2.jpg'
    },
    // Add more products as needed
];

// Function to toggle product details
function toggleDetails(index) {
    const details = document.getElementById(`details${index}`);
    if (details.style.display === 'block') {
        details.style.display = 'none';
    } else {
        details.style.display = 'block';
    }
}

// Function to generate product cards
function generateProductCard(product, index) {
    const card = document.createElement('div');
    card.className = 'col-lg-4 col-md-6 mb-4';
    card.innerHTML = `
        <div class="card">
            <img src="static/img/${product.foto}" class="card-img-top" alt="${product.nombre}">
            <div class="card-body">
                <h5 class="card-title">${product.nombre}</h5>
                <p class="card-text">${product.descripcion}</p>
                <p class="card-text">Precio: $${product.precio}</p>
                <button onclick="toggleDetails(${index})" class="btn btn-primary">Ver detalles</button>
                <div id="details${index}" class="details" style="display: none;">
                    Detalles adicionales del producto ${index + 1}
                </div>
            </div>
        </div>
    `;
    return card;
}

// Function to initialize the product list
function initProductList() {
    productos_destacados.forEach((producto, index) => {
        const card = generateProductCard(producto, index);
        productList.appendChild(card);
    });
}

// Initialize the product list
initProductList();
