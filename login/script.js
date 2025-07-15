const brandSelect = document.getElementById('brand');
const modelSelect = document.getElementById('model');
const registerForm = document.getElementById('registerForm');

// Load brands on page load
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('http://127.0.0.1:5002/api/brands');
    const brands = await res.json();

    brandSelect.innerHTML = '<option value="" disabled selected>Select Brand</option>';
    brands.forEach(brand => {
      const option = document.createElement('option');
      option.value = brand;
      option.textContent = brand;
      brandSelect.appendChild(option);
    });

    brandSelect.disabled = false;
  } catch (err) {
    console.error('Error loading brands:', err);
  }
});

// Load models when brand changes
brandSelect.addEventListener('change', async () => {
  const selectedBrand = brandSelect.value;

  try {
    const res = await fetch(`http://127.0.0.1:5002/api/models/${encodeURIComponent(selectedBrand)}`);
    const models = await res.json();

    modelSelect.innerHTML = '<option value="" disabled selected>Select Model</option>';
    models.forEach(model => {
      const option = document.createElement('option');
      option.value = model;
      option.textContent = model;
      modelSelect.appendChild(option);
    });

    modelSelect.disabled = false;
  } catch (err) {
    console.error('Error loading models:', err);
  }
});

// Form submission handler
registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const phone = document.getElementById('phone').value;
  const brand = document.getElementById('brand').value;
  const model = document.getElementById('model').value;
  const password = document.getElementById('password').value;
  // const lastService = document.getElementById('lastService').value;

  const userData = {
    name,
    email,
    phone,
    brand,
    model,
    password,
    // last_service_date: lastService
  };

  try {
    const res = await fetch('http://127.0.0.1:5002/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    });

    const result = await res.json();
    if (res.ok) {
      alert(result.message);
      registerForm.reset();
    } else {
      alert('Error: ' + result.error);
    }
  } catch (error) {
    console.error('Registration failed:', error);
    alert('Registration failed. Try again.');
  }
});